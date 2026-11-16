"""
Experiment 08 - Task 8.4: Adaptive Window Size (W) & Offset (C) Sensitivity Sweep
Evaluates 16 parameter combinations on bias-corrupted Brain MRI, demonstrating why
undersized windows (e.g., 7x7) cause hollow interiors in solid anatomical structures.
"""
import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_task_8_4():
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

    # Bias field simulation (as in benchmark)
    Y, X = np.ogrid[:512, :512]
    bias_field = 0.45 + 0.95 * ((X / 512.0) * 0.7 + (Y / 512.0) * 0.3)
    mri_biased = np.clip(mri.astype(float) * bias_field, 0, 255).astype(np.uint8)

    # Clean ground truth
    m_clean = cv2.GaussianBlur(mri.astype(float), (35, 35), 6.0)
    gt_mask = ((mri > (m_clean + 4)) & (mri > 25)).astype(np.uint8) * 255

    W_list = [7, 15, 35, 75]
    C_list = [-10, -5, 0, 5]

    records = []
    masks_dict = {}

    print("=" * 80)
    print("TASK 8.4: ADAPTIVE GAUSSIAN PARAMETER SWEEP (W x C GRID)")
    print("=" * 80)
    print(f"{'Window W':<10} | {'Offset C':<10} | {'Dice (DSC)':<11} | {'Jaccard IoU':<12} | {'FG Area %':<10}")
    print("-" * 80)

    for W in W_list:
        for C in C_list:
            # OpenCV subtracts C: th = f > (mean - C)
            th_mask = cv2.adaptiveThreshold(
                mri_biased, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, W, -C
            )
            masks_dict[(W, C)] = th_mask

            g = (gt_mask > 0)
            p = (th_mask > 0)
            inter = np.logical_and(g, p).sum()
            denom = g.sum() + p.sum()
            dsc = (2.0 * inter / denom) if denom > 0 else 0.0
            union = np.logical_or(g, p).sum()
            iou = (inter / union) if union > 0 else 0.0
            fg_pct = (p.sum() / p.size) * 100.0

            records.append({
                "Window_W": W,
                "Offset_C": C,
                "Dice_DSC": round(dsc, 4),
                "Jaccard_IoU": round(iou, 4),
                "FG_Area_Pct": round(fg_pct, 2)
            })

            print(f"{W:<10} | {C:<10} | {dsc:<11.4f} | {iou:<12.4f} | {fg_pct:<8.2f}%")

    df = pd.DataFrame(records)
    csv_path = os.path.join(tab_dir, "exp08_task_8_4_adaptive_sweep.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[SAVED] Task 8.4 metrics to: {csv_path}")

    # Best parameter set
    best_row = df.loc[df["Dice_DSC"].idxmax()]
    print(f"\nOptimal Parameter Set: W = {int(best_row['Window_W'])}, C = {int(best_row['Offset_C'])} (DSC = {best_row['Dice_DSC']:.4f})")

    # Multi-panel visualization
    fig, axes = plt.subplots(4, 4, figsize=(14, 14))
    fig.patch.set_facecolor("#FFFFFF")

    for i, W in enumerate(W_list):
        for j, C in enumerate(C_list):
            ax = axes[i, j]
            mask = masks_dict[(W, C)]
            row = df[(df["Window_W"] == W) & (df["Offset_C"] == C)].iloc[0]
            dsc = row["Dice_DSC"]
            
            ax.imshow(mask, cmap="gray")
            color = "#16A34A" if dsc >= 0.85 else ("#D97706" if dsc >= 0.70 else "#DC2626")
            ax.set_title(f"W={W}x{W}, C={C}\nDSC={dsc:.4f}", fontsize=8.5, fontweight="bold", color=color, pad=3)
            ax.axis("off")

    plt.suptitle("Task 8.4: Adaptive Gaussian Parameter Sweep ($W \in [7, 15, 35, 75]$ vs. $C \in [-10, -5, 0, +5]$)", fontsize=13, fontweight="bold", y=0.99)
    plt.tight_layout()
    fig_path = os.path.join(out_dir, "exp08_task_8_4_adaptive_sweep.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Task 8.4 sweep grid figure to: {fig_path}")

    # Anatomy Zoom-in comparison (W=7 vs W=35 vs W=75) showing hollow core artifact
    fig_zoom, axes_z = plt.subplots(1, 4, figsize=(16, 4.5))
    fig_zoom.patch.set_facecolor("#FFFFFF")
    
    # ROI: Central cortical parenchyma [180:320, 180:320]
    r_slice = slice(180, 320)
    c_slice = slice(180, 320)

    panels_z = [
        ("Input Biased ROI (140x140)", mri_biased[r_slice, c_slice]),
        (f"W=7x7 (C=-5)\nHollow Core Artifact (DSC={df[(df['Window_W']==7)&(df['Offset_C']==-5)]['Dice_DSC'].iloc[0]:.3f})", masks_dict[(7, -5)][r_slice, c_slice]),
        (f"W=35x35 (C=-5)\nOptimal Solid Fill (DSC={df[(df['Window_W']==35)&(df['Offset_C']==-5)]['Dice_DSC'].iloc[0]:.3f})", masks_dict[(35, -5)][r_slice, c_slice]),
        (f"W=75x75 (C=-5)\nOver-Merged (DSC={df[(df['Window_W']==75)&(df['Offset_C']==-5)]['Dice_DSC'].iloc[0]:.3f})", masks_dict[(75, -5)][r_slice, c_slice])
    ]

    for ax, (title, img_crop) in zip(axes_z, panels_z):
        ax.imshow(img_crop, cmap="gray")
        ax.set_title(title, fontsize=10, fontweight="bold", pad=6)
        ax.axis("off")

    plt.suptitle("Clinical Explanation: Why W=7x7 Hollows Out Solid Anatomical Structures", fontsize=12, fontweight="bold", y=1.02)
    plt.tight_layout()
    zoom_fig_path = os.path.join(out_dir, "exp08_task_8_4_hollow_core_zoom.png")
    plt.savefig(zoom_fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Task 8.4 zoom figure to: {zoom_fig_path}")

    return df

if __name__ == "__main__":
    run_task_8_4()
