"""
Experiment 09 - Task 9.4: Morphological Boundary Extraction & Gradient Thickness Control
Extracts Internal, External, and Symmetrical Morphological Gradients on Brain MRI tumor mask,
overlaying contours on original anatomical grayscale imaging.
"""
import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_task_9_4():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(base_dir, "Inputs", "images", "Brain_MRI.png")
    out_dir = os.path.join(base_dir, "Outputs", "Python")
    tab_dir = os.path.join(base_dir, "Tables")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(tab_dir, exist_ok=True)

    mri = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if mri is None:
        raise FileNotFoundError(f"Brain MRI not found at {img_path}")
    if mri.shape != (512, 512):
        mri = cv2.resize(mri, (512, 512))

    # Clean tumor mask
    _, raw = cv2.threshold(mri, 175, 255, cv2.THRESH_BINARY)
    se3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    clean_tumor = cv2.morphologyEx(cv2.morphologyEx(raw, cv2.MORPH_CLOSE, se3), cv2.MORPH_OPEN, se3)

    # 1. Three Morphological Boundary Formulations
    # (a) Internal Boundary: A - (A (-) B)
    m_eroded = cv2.erode(clean_tumor, se3, iterations=1)
    b_internal = cv2.subtract(clean_tumor, m_eroded)

    # (b) External Boundary: (A (+) B) - A
    m_dilated = cv2.dilate(clean_tumor, se3, iterations=1)
    b_external = cv2.subtract(m_dilated, clean_tumor)

    # (c) Symmetrical Morphological Gradient: (A (+) B) - (A (-) B)
    b_gradient = cv2.morphologyEx(clean_tumor, cv2.MORPH_GRADIENT, se3)

    # Quantitative metrics
    p_int = int((b_internal > 0).sum())
    p_ext = int((b_external > 0).sum())
    p_grad = int((b_gradient > 0).sum())

    print("=" * 80)
    print("TASK 9.4: MORPHOLOGICAL BOUNDARY EXTRACTION BENCHMARK")
    print("=" * 80)
    print(f"{'Boundary Formulation':<32} | {'Perimeter (Pixels)':<20} | {'Theoretical Thickness'}")
    print("-" * 80)
    print(f"{'Internal Boundary: A - (A ⊖ B)':<32} | {p_int:<20d} | 1 Pixel Wide (Inside)")
    print(f"{'External Boundary: (A ⊕ B) - A':<32} | {p_ext:<20d} | 1 Pixel Wide (Outside)")
    print(f"{'Symmetrical Gradient: (A ⊕ B) - (A ⊖ B)':<32} | {p_grad:<20d} | 2 Pixels Wide (Centered)")

    records = [
        {"Formulation": "Internal Boundary: A - (A ⊖ B)", "Perimeter_Pixels": p_int, "Thickness_Pixels": 1, "Location": "Inside true boundary"},
        {"Formulation": "External Boundary: (A ⊕ B) - A", "Perimeter_Pixels": p_ext, "Thickness_Pixels": 1, "Location": "Outside true boundary"},
        {"Formulation": "Symmetrical Gradient: (A ⊕ B) - (A ⊖ B)", "Perimeter_Pixels": p_grad, "Thickness_Pixels": 2, "Location": "Straddles true boundary"}
    ]
    df = pd.DataFrame(records)
    csv_path = os.path.join(tab_dir, "exp09_task_9_4_boundary_metrics.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[SAVED] Task 9.4 metrics to: {csv_path}")

    # Color overlay on original MRI
    # Convert grayscale MRI to RGB
    mri_rgb = cv2.cvtColor(mri, cv2.COLOR_GRAY2RGB)
    overlay_all = mri_rgb.copy()

    # Overlay colors:
    # Internal: Cyan [0, 255, 255]
    # External: Magenta [255, 0, 255]
    # Symmetrical: Yellow [255, 255, 0]
    overlay_all[b_internal > 0] = [0, 240, 255]   # Cyan
    overlay_all[b_external > 0] = [255, 50, 150]  # Magenta/Coral

    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    fig.patch.set_facecolor("#FFFFFF")

    axes[0, 0].imshow(clean_tumor, cmap="gray")
    axes[0, 0].set_title("Input Solid Tumor Mask A", fontsize=11, fontweight="bold", pad=6)
    axes[0, 0].axis("off")

    axes[0, 1].imshow(b_gradient, cmap="hot")
    axes[0, 1].set_title(f"Symmetrical Morphological Gradient\n(Thickness = 2 px, Area = {p_grad} px)", fontsize=11, fontweight="bold", pad=6)
    axes[0, 1].axis("off")

    # Zoomed ROI: [150:350, 150:350]
    r_z = slice(150, 350)
    c_z = slice(150, 350)

    axes[1, 0].imshow(overlay_all)
    axes[1, 0].set_title("Clinical Overlay: Internal (Cyan) vs External (Magenta)", fontsize=11, fontweight="bold", pad=6)
    axes[1, 0].axis("off")

    axes[1, 1].imshow(overlay_all[r_z, c_z])
    axes[1, 1].set_title("High-Magnification Anatomical Zoom (200x200 Crop)\nShows 1-Pixel Inward vs Outward Separation", fontsize=11, fontweight="bold", pad=6)
    axes[1, 1].axis("off")

    plt.suptitle("Task 9.4: Morphological Boundary Extraction & Anatomical Contour Delineation", fontsize=13, fontweight="bold", y=0.98)
    plt.tight_layout()
    fig_path = os.path.join(out_dir, "exp09_task_9_4_boundary_extraction.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Task 9.4 figure to: {fig_path}")

    return df

if __name__ == "__main__":
    run_task_9_4()
