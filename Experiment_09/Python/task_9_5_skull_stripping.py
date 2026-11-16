"""
Experiment 09 - Task 9.5: Automated Cortical Skull Stripping (Brain Extraction Pipeline)
Integrates Otsu thresholding, morphological bridge snapping, connected-component analysis,
and binary hole filling on Head CT to strip the hyperdense skull and extract intracranial parenchyma.
"""
import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import ndimage

def run_task_9_5():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(base_dir, "Inputs", "images", "Head_CT.png")
    out_dir = os.path.join(base_dir, "Outputs", "Python")
    tab_dir = os.path.join(base_dir, "Tables")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(tab_dir, exist_ok=True)

    ct = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if ct is None:
        raise FileNotFoundError(f"Head CT not found at {img_path}")
    if ct.shape != (512, 512):
        ct = cv2.resize(ct, (512, 512))

    # Step 1: Global Otsu thresholding to segment head from background air
    t_head, head_mask = cv2.threshold(ct, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Step 2: Separate high-density bone from brain tissue
    # In Head CT, bone has high HU (> 140) while brain parenchyma is [30, 90]
    t_bone, bone_mask = cv2.threshold(ct, 130, 255, cv2.THRESH_BINARY)

    # Step 3: Morphological Opening on bone mask to ensure a clean calvarial ring
    se_disk5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    bone_clean = cv2.morphologyEx(bone_mask, cv2.MORPH_OPEN, se_disk5)

    # Step 4: Hole Filling on the skull ring to create the full intracranial cavity volume
    # Fill holes inside the skull
    skull_filled = ndimage.binary_fill_holes(bone_clean > 0).astype(np.uint8) * 255

    # Step 5: Intracranial Brain Mask = Skull Filled MINUS the bone ring itself
    intracranial_raw = cv2.subtract(skull_filled, bone_clean)

    # Step 6: Morphological Opening to strip remaining dural remnants and break boundary touches
    se_brain = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    brain_opened = cv2.morphologyEx(intracranial_raw, cv2.MORPH_OPEN, se_brain)

    # Step 7: Largest Connected Component Isolation (retaining true brain parenchyma)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(brain_opened, connectivity=8)
    # Background is label 0; find largest foreground component
    if num_labels > 1:
        largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        brain_mask = (labels == largest_label).astype(np.uint8) * 255
    else:
        brain_mask = brain_opened

    # Step 8: Fill internal ventricles / CSF voids for a solid parenchymal volume
    brain_solid = ndimage.binary_fill_holes(brain_mask > 0).astype(np.uint8) * 255

    # Step 9: Mask original CT scan
    ct_stripped = cv2.bitwise_and(ct, ct, mask=brain_solid)

    # Calculate quantitative areas
    n_total = float(ct.size)
    head_px = int((head_mask > 0).sum())
    bone_px = int((bone_clean > 0).sum())
    brain_px = int((brain_solid > 0).sum())

    head_pct = (head_px / n_total) * 100.0
    bone_pct = (bone_px / n_total) * 100.0
    brain_pct = (brain_px / n_total) * 100.0
    brain_to_head_ratio = (brain_px / float(head_px)) * 100.0 if head_px > 0 else 0.0

    print("=" * 80)
    print("TASK 9.5: AUTOMATED CORTICAL SKULL STRIPPING (BRAIN EXTRACTION PIPELINE)")
    print("=" * 80)
    print(f"Total CT Image Geometry               : 512 x 512 ({int(n_total)} pixels)")
    print(f"Total Head Volume Area                : {head_px} px ({head_pct:.2f}% of scan)")
    print(f"Calvarial Bone Volume Area            : {bone_px} px ({bone_pct:.2f}% of scan)")
    print(f"Extracted Intracranial Brain Area     : {brain_px} px ({brain_pct:.2f}% of scan)")
    print(f"Brain-to-Head Parenchymal Ratio       : {brain_to_head_ratio:.2f}%")
    print("Status: Hyperdense skull ring successfully stripped from neuroimaging volume.")

    records = [{
        "Modality": "Head CT",
        "Image_Size": "512x512",
        "Total_Pixels": int(n_total),
        "Total_Head_Area_Px": head_px,
        "Bone_Ring_Area_Px": bone_px,
        "Extracted_Brain_Area_Px": brain_px,
        "Brain_Scan_Volume_Pct": round(brain_pct, 2),
        "Brain_to_Head_Ratio_Pct": round(brain_to_head_ratio, 2)
    }]
    df = pd.DataFrame(records)
    csv_path = os.path.join(tab_dir, "exp09_task_9_5_skull_stripping.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[SAVED] Task 9.5 metrics to: {csv_path}")

    # Plot Multi-Panel Pipeline Progression
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    fig.patch.set_facecolor("#FFFFFF")

    panels = [
        ("1. Input Head CT (512x512)", ct, "gray"),
        (f"2. Calvarial Bone Mask (T=130)\nArea = {bone_px} px ({bone_pct:.1f}%)", bone_clean, "gray"),
        ("3. Intracranial Space\n(Skull Ring Subtracted)", intracranial_raw, "gray"),
        ("4. Morphological Opening (7x7 Disk)\n(Dural Touches Stripped)", brain_opened, "gray"),
        (f"5. Final Brain Mask (Holes Filled)\nArea = {brain_px} px ({brain_pct:.1f}%)", brain_solid, "gray"),
        ("6. Skull-Stripped Intracranial CT\n(Clean Brain Parenchyma)", ct_stripped, "gray")
    ]

    for ax, (title, img, cmap) in zip(axes.flatten(), panels):
        ax.imshow(img, cmap=cmap)
        ax.set_title(title, fontsize=10, fontweight="bold", pad=6)
        ax.axis("off")

    plt.suptitle("Task 9.5: Automated Morphological Skull-Stripping Pipeline on Head CT", fontsize=13, fontweight="bold", y=0.99)
    plt.tight_layout()
    fig_path = os.path.join(out_dir, "exp09_task_9_5_skull_stripping.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Task 9.5 figure to: {fig_path}")

    return df

if __name__ == "__main__":
    run_task_9_5()
