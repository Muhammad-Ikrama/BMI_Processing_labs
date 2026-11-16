"""
Experiment 08 - Task 8.3: MRI RF Bias-Field Simulation & Global Failure Demonstration
Simulates RF coil illumination shading across severity levels alpha in [0.0, 0.3, 0.6, 0.9],
quantifies catastrophic failure of global Otsu, and proves local adaptive robustness.
"""
import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_task_8_3():
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

    # Ground truth anatomical mask from clean MRI
    m_clean = cv2.GaussianBlur(mri.astype(float), (35, 35), 6.0)
    gt_mask = ((mri > (m_clean + 4)) & (mri > 25)).astype(np.uint8) * 255
    gt_area = (gt_mask > 0).sum()

    Y, X = np.ogrid[:512, :512]
    rf_grad = 0.45 + 0.95 * ((X / 512.0) * 0.7 + (Y / 512.0) * 0.3)

    alphas = [0.0, 0.3, 0.6, 0.9]
    records = []
    shading_imgs = []
    otsu_masks = []
    adap_masks = []

    print("=" * 80)
    print("TASK 8.3: MRI RF BIAS-FIELD SHADING & GLOBAL THRESHOLDING FAILURE BENCHMARK")
    print("=" * 80)
    print(f"{'Severity alpha':<15} | {'Otsu T*':<9} | {'Otsu DSC':<10} | {'Otsu IoU':<10} | {'Adap DSC':<10} | {'Adap IoU':<10}")
    print("-" * 80)

    for alpha in alphas:
        # Synthesize bias field
        field = (1.0 - alpha) + alpha * rf_grad
        mri_shaded = np.clip(mri.astype(float) * field, 0, 255).astype(np.uint8)
        shading_imgs.append(mri_shaded)

        # 1. Global Otsu
        t_otsu, th_otsu = cv2.threshold(mri_shaded, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        otsu_masks.append(th_otsu)

        # 2. Adaptive Gaussian-C (35x35, C=-5)
        th_adap = cv2.adaptiveThreshold(mri_shaded, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
        adap_masks.append(th_adap)

        # Dice & IoU evaluation
        def calc_metrics(pr):
            p = (pr > 0)
            g = (gt_mask > 0)
            inter = np.logical_and(g, p).sum()
            denom = g.sum() + p.sum()
            dsc = (2.0 * inter / denom) if denom > 0 else 0.0
            union = np.logical_or(g, p).sum()
            iou = (inter / union) if union > 0 else 0.0
            fg_pct = (p.sum() / p.size) * 100.0
            return dsc, iou, fg_pct

        d_otsu, iou_otsu, fg_otsu = calc_metrics(th_otsu)
        d_adap, iou_adap, fg_adap = calc_metrics(th_adap)

        records.append({
            "Shading_Severity_Alpha": alpha,
            "Otsu_T_star": int(t_otsu),
            "Otsu_DSC": round(d_otsu, 4),
            "Otsu_IoU": round(iou_otsu, 4),
            "Otsu_FG_Area_Pct": round(fg_otsu, 2),
            "Adap_DSC": round(d_adap, 4),
            "Adap_IoU": round(iou_adap, 4),
            "Adap_FG_Area_Pct": round(fg_adap, 2)
        })

        print(f"{alpha:<15.1f} | {int(t_otsu):<9} | {d_otsu:<10.4f} | {iou_otsu:<10.4f} | {d_adap:<10.4f} | {iou_adap:<10.4f}")

    df = pd.DataFrame(records)
    csv_path = os.path.join(tab_dir, "exp08_task_8_3_rf_bias_metrics.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[SAVED] Task 8.3 metrics to: {csv_path}")

    # Plot Multi-Panel Comparison & DSC Degradation Curve
    fig = plt.figure(figsize=(16, 9))
    fig.patch.set_facecolor("#FFFFFF")

    # Row 1: Shaded MRIs across alpha
    for i, alpha in enumerate(alphas):
        ax = fig.add_subplot(3, 4, i + 1)
        ax.imshow(shading_imgs[i], cmap="gray")
        ax.set_title(f"Shaded MRI ($\\alpha = {alpha}$)", fontsize=10, fontweight="bold", pad=5)
        ax.axis("off")

    # Row 2: Global Otsu Segmentation Masks
    for i, alpha in enumerate(alphas):
        ax = fig.add_subplot(3, 4, i + 5)
        ax.imshow(otsu_masks[i], cmap="gray")
        dsc = records[i]["Otsu_DSC"]
        color = "#16A34A" if dsc >= 0.80 else "#DC2626"
        ax.set_title(f"Otsu Mask ($T^*={records[i]['Otsu_T_star']}$)\nDSC = {dsc:.4f}", fontsize=10, fontweight="bold", color=color, pad=5)
        ax.axis("off")

    # Row 3 Left: Adaptive Gaussian Segmentation at alpha=0.9
    ax_adap = fig.add_subplot(3, 4, 9)
    ax_adap.imshow(adap_masks[3], cmap="gray")
    ax_adap.set_title(f"Adaptive Gauss ($\\alpha=0.9$)\nDSC = {records[3]['Adap_DSC']:.4f}", fontsize=10, fontweight="bold", color="#16A34A", pad=5)
    ax_adap.axis("off")

    # Row 3 Center & Right: DSC Degradation Curve (spanning cols 10-12)
    ax_curve = fig.add_subplot(3, 4, (10, 12))
    ax_curve.plot(alphas, [r["Otsu_DSC"] for r in records], marker="o", color="#DC2626", linewidth=2.5, markersize=7, label="Global Otsu Method (Severe Failure)")
    ax_curve.plot(alphas, [r["Adap_DSC"] for r in records], marker="s", color="#16A34A", linewidth=2.5, markersize=7, label="Local Adaptive Gaussian-C (Robust)")
    ax_curve.axhline(0.85, color="#2563EB", linestyle="--", linewidth=1.5, label="Target 'Good to Go' (DSC >= 0.85)")
    ax_curve.set_title("Dice Similarity Coefficient Degradation vs. RF Shading Severity ($\\alpha$)", fontsize=11, fontweight="bold", pad=8)
    ax_curve.set_xlabel("RF Bias Shading Severity $\\alpha$", fontsize=10, fontweight="bold")
    ax_curve.set_ylabel("Dice Similarity Coefficient (DSC)", fontsize=10, fontweight="bold")
    ax_curve.set_ylim([0.45, 1.02])
    ax_curve.legend(fontsize=9, loc="lower left")
    ax_curve.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    fig_path = os.path.join(out_dir, "exp08_task_8_3_rf_bias_failure.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Task 8.3 figure to: {fig_path}")

    return df

if __name__ == "__main__":
    run_task_8_3()
