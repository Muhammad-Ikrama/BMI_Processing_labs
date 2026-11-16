"""
Experiment 09 - Task 9.3: Order of Operations Analysis (Open-then-Close vs. Close-then-Open)
Proves mathematically and visually why applying Closing first causes irreversible salt fusion.
"""
import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import ndimage

def run_task_9_3():
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

    _, gt_raw = cv2.threshold(mri, 175, 255, cv2.THRESH_BINARY)
    se5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    gt_mask = cv2.morphologyEx(cv2.morphologyEx(gt_raw, cv2.MORPH_CLOSE, se5), cv2.MORPH_OPEN, se5)

    # High background salt density to trigger fusion
    np.random.seed(209)
    noisy_high = gt_mask.copy()
    se3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    salt_high = cv2.dilate(((np.random.rand(512, 512) < 0.0075) & (gt_mask == 0)).astype(np.uint8) * 255, se3)
    pepper_high = cv2.dilate(((np.random.rand(512, 512) < 0.0080) & (gt_mask > 0)).astype(np.uint8) * 255, se3)
    noisy_high = cv2.bitwise_or(noisy_high, salt_high)
    noisy_high[pepper_high > 0] = 0

    # Pipeline A: Open first, then Close ((M o B) . B)
    stepA1_open = cv2.morphologyEx(noisy_high, cv2.MORPH_OPEN, se5)
    pipeA_open_close = cv2.morphologyEx(stepA1_open, cv2.MORPH_CLOSE, se5)

    # Pipeline B: Close first, then Open ((M . B) o B)
    stepB1_close = cv2.morphologyEx(noisy_high, cv2.MORPH_CLOSE, se5)
    pipeB_close_open = cv2.morphologyEx(stepB1_close, cv2.MORPH_OPEN, se5)

    def eval_mask(gt, m):
        g, p = (gt > 0), (m > 0)
        inter = np.logical_and(g, p).sum()
        dsc = (2.0 * inter) / (g.sum() + p.sum())
        iou = inter / np.logical_or(g, p).sum()
        cc = cv2.connectedComponents(p.astype(np.uint8))[0] - 1
        holes = int(np.sum(ndimage.binary_fill_holes(p) & (~p)))
        return dsc, iou, cc, holes, int(p.sum())

    pipelines = [
        ("Noisy Input (High Salt)", noisy_high, "Input"),
        ("Pipeline A: Open-then-Close", pipeA_open_close, "PipeA"),
        ("Pipeline B: Close-then-Open", pipeB_close_open, "PipeB")
    ]

    records = []
    print("=" * 80)
    print("TASK 9.3: ORDER OF OPERATIONS BENCHMARK (OPEN-CLOSE VS. CLOSE-OPEN)")
    print("=" * 80)
    print(f"{'Pipeline Strategy':<28} | {'Dice (DSC)':<10} | {'Jaccard IoU':<11} | {'CC Count':<8} | {'Hole Px':<7} | {'Area Px'}")
    print("-" * 80)

    for name, mask, tag in pipelines:
        dsc, iou, cc, holes, area = eval_mask(gt_mask, mask)
        records.append({
            "Pipeline_Strategy": name,
            "Tag": tag,
            "Dice_DSC": round(dsc, 4),
            "Jaccard_IoU": round(iou, 4),
            "CC_Count": cc,
            "Hole_Pixels": holes,
            "Area_Pixels": area
        })
        print(f"{name:<28} | {dsc:<10.4f} | {iou:<11.4f} | {cc:<8d} | {holes:<7d} | {area}")

    df = pd.DataFrame(records)
    csv_path = os.path.join(tab_dir, "exp09_task_9_3_order_of_ops.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[SAVED] Task 9.3 metrics to: {csv_path}")

    # Plot Visual Figures demonstrating Salt Fusion Mechanism
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    fig.patch.set_facecolor("#FFFFFF")

    # High noise ROI zoom: [50:180, 50:180] (in pure background air)
    r_z = slice(50, 180)
    c_z = slice(50, 180)

    # Row 1: Full Masks
    axes[0, 0].imshow(noisy_high, cmap="gray")
    axes[0, 0].set_title(f"Input Noisy Mask (High Salt)\nCC={records[0]['CC_Count']}, DSC={records[0]['Dice_DSC']:.4f}", fontsize=10, fontweight="bold", pad=5)
    axes[0, 0].axis("off")

    axes[0, 1].imshow(pipeA_open_close, cmap="gray")
    axes[0, 1].set_title(f"Pipeline A: Open-then-Close\nDSC={records[1]['Dice_DSC']:.4f} | CC={records[1]['CC_Count']} (Optimal)", fontsize=10, fontweight="bold", color="#16A34A", pad=5)
    axes[0, 1].axis("off")

    axes[0, 2].imshow(pipeB_close_open, cmap="gray")
    axes[0, 2].set_title(f"Pipeline B: Close-then-Open\nDSC={records[2]['Dice_DSC']:.4f} | CC={records[2]['CC_Count']} (Salt Fused!)", fontsize=10, fontweight="bold", color="#DC2626", pad=5)
    axes[0, 2].axis("off")

    # Row 2: Background Air Zooms showing Salt Fusion
    axes[1, 0].imshow(noisy_high[r_z, c_z], cmap="gray")
    axes[1, 0].set_title("Input Salt Dots in Air (Crop)\nDense Speckle Field", fontsize=9.5, fontweight="bold", pad=5)
    axes[1, 0].axis("off")

    axes[1, 1].imshow(pipeA_open_close[r_z, c_z], cmap="gray")
    axes[1, 1].set_title("Pipeline A: Pure Black Air\nErosion in Open erased all dots first!", fontsize=9.5, fontweight="bold", color="#16A34A", pad=5)
    axes[1, 1].axis("off")

    axes[1, 2].imshow(pipeB_close_open[r_z, c_z], cmap="gray")
    axes[1, 2].set_title("Pipeline B: Giant Fused Blobs!\nClosing dilated dots into touching islands", fontsize=9.5, fontweight="bold", color="#DC2626", pad=5)
    axes[1, 2].axis("off")

    plt.suptitle("Task 9.3: Order of Operations Analysis — Proving Irreversible Salt Fusion in Close-then-Open", fontsize=12.5, fontweight="bold", y=0.99)
    plt.tight_layout()
    fig_path = os.path.join(out_dir, "exp09_task_9_3_order_of_ops.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Task 9.3 figure to: {fig_path}")

    return df

if __name__ == "__main__":
    run_task_9_3()
