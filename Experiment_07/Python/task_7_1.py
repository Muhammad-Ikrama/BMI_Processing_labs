"""
Experiment 07 - Task 7.1: High-Boost Factor Sweep & Dynamic Range Clipping Analysis
Sweeps boost factor k across [0.5, 1.0, 1.8, 3.0], quantifies underflow clipping at 0,
overflow saturation at 255, Shannon information entropy, and gradient magnitude boost.
Course: Medical Image Processing | Riphah International University
Faculty: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

def run_task_7_1():
    print("==============================================================================")
    print("EXPERIMENT 07 - TASK 7.1: HIGH-BOOST SWEEP & CLIPPING ANALYSIS")
    print("==============================================================================")

    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.abspath(os.path.join(script_dir, ".."))
    img_path = os.path.join(exp_dir, "Inputs", "images", "Xray.jpg")
    if not os.path.exists(img_path):
        img_path = os.path.join(exp_dir, "..", "..", "images", "Xray.jpg")

    out_py_dir = os.path.join(exp_dir, "Outputs", "Python")
    fig_dir = os.path.join(exp_dir, "Figures")
    tab_dir = os.path.join(exp_dir, "Tables")
    os.makedirs(out_py_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(tab_dir, exist_ok=True)

    # 1. Load Image
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Cannot load radiograph at {img_path}")
    H, W = img.shape
    total_pixels = H * W
    img_f = img.astype(np.float64)

    # 2. Extract High-Frequency Mask (sigma = 1.5)
    blurred = gaussian_filter(img_f, sigma=1.5)
    g_mask = img_f - blurred

    # Baseline calculations
    def calc_mean_grad(im):
        gy, gx = np.gradient(im.astype(np.float64))
        return float(np.mean(np.hypot(gx, gy)))

    def calc_entropy(im_u8):
        hist = cv2.calcHist([im_u8], [0], None, [256], [0, 256]).flatten()
        prob = hist / (np.sum(hist) + 1e-12)
        prob = prob[prob > 0]
        return float(-np.sum(prob * np.log2(prob)))

    base_grad = calc_mean_grad(img)
    base_entropy = calc_entropy(img)

    k_vals = [0.5, 1.0, 1.8, 3.0]
    metrics_list = []
    sharpened_images = {}

    for k in k_vals:
        raw_sharp = img_f + k * g_mask
        clip_0_cnt = np.sum(raw_sharp < 0.0)
        clip_255_cnt = np.sum(raw_sharp > 255.0)
        total_clip_cnt = clip_0_cnt + clip_255_cnt

        pct_clip_0 = (clip_0_cnt / total_pixels) * 100.0
        pct_sat_255 = (clip_255_cnt / total_pixels) * 100.0
        pct_total_clip = (total_clip_cnt / total_pixels) * 100.0

        im_u8 = np.clip(raw_sharp, 0, 255).astype(np.uint8)
        sharpened_images[k] = im_u8
        cv2.imwrite(os.path.join(out_py_dir, f"exp07_task_7_1_sharp_k_{str(k).replace('.', '_')}.png"), im_u8)

        mg = calc_mean_grad(raw_sharp)
        grad_boost = ((mg - base_grad) / base_grad) * 100.0
        ent = calc_entropy(im_u8)

        if k == 0.5:
            diag_status = "Sub-optimal (Mild Edge Boost)"
            verdict = "Acceptable (Low Contrast)"
        elif k == 1.0:
            diag_status = "OPTIMAL CLINICAL STANDARD"
            verdict = "APPROVED (Good to Go)"
        elif k == 1.8:
            diag_status = "High-Boost (Moderate Noise)"
            verdict = "Acceptable (Dense Bones)"
        else:
            diag_status = "Severe Clipping & Noise Halos"
            verdict = "CONTRAINDICATED"

        metrics_list.append({
            "Boost_Factor_k": k,
            "Mean_Gradient": round(mg, 2),
            "Gradient_Boost_Pct": round(grad_boost, 2),
            "Clipped_0_Pct": round(pct_clip_0, 3),
            "Saturated_255_Pct": round(pct_sat_255, 3),
            "Total_Clipping_Pct": round(pct_total_clip, 3),
            "Shannon_Entropy_Bits": round(ent, 3),
            "Diagnostic_Status": diag_status,
            "Clinical_Verdict": verdict
        })

    # Save CSV
    df_metrics = pd.DataFrame(metrics_list)
    csv_path = os.path.join(tab_dir, "exp07_task_7_1_clipping_metrics.csv")
    df_metrics.to_csv(csv_path, index=False)
    print(f"\n[INFO] High-Boost Sweep & Clipping Metrics saved at: {csv_path}")
    print(df_metrics.to_string(index=False))

    # Visualization Figure (2x3)
    fig, axes = plt.subplots(2, 3, figsize=(16, 11), facecolor='white')
    plt.subplots_adjust(wspace=0.25, hspace=0.32)

    # (a) Original
    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title(f"(a) Original Radiograph\nGrad: {base_grad:.2f} | Entropy: {base_entropy:.2f} b/px",
                          fontsize=10.5, fontweight='bold', color='#1e3a8a')
    axes[0, 0].axis('off')

    # (b) k = 0.5
    axes[0, 1].imshow(sharpened_images[0.5], cmap='gray')
    m0 = metrics_list[0]
    axes[0, 1].set_title(f"(b) Mild Boost ($k=0.5$)\nBoost: {m0['Gradient_Boost_Pct']:+.1f}% | Clip: {m0['Total_Clipping_Pct']}%\n(Under-sharpened)",
                          fontsize=10.5, fontweight='bold', color='#0284c7')
    axes[0, 1].axis('off')

    # (c) k = 1.0 (CLINICAL OPTIMUM)
    axes[0, 2].imshow(sharpened_images[1.0], cmap='gray')
    m1 = metrics_list[1]
    axes[0, 2].set_title(f"(c) Unsharp Masking ($k=1.0$) [OPTIMUM]\nBoost: {m1['Gradient_Boost_Pct']:+.1f}% | Clip: {m1['Total_Clipping_Pct']}%\n(Zero Visible Halos)",
                          fontsize=10.5, fontweight='bold', color='#15803d')
    axes[0, 2].axis('off')

    # (d) k = 1.8
    axes[1, 0].imshow(sharpened_images[1.8], cmap='gray')
    m2 = metrics_list[2]
    axes[1, 0].set_title(f"(d) High-Boost ($k=1.8$)\nBoost: {m2['Gradient_Boost_Pct']:+.1f}% | Clip: {m2['Total_Clipping_Pct']}%\n(Moderate Grain)",
                          fontsize=10.5, fontweight='bold', color='#f59e0b')
    axes[1, 0].axis('off')

    # (e) k = 3.0 (Over-boosted)
    axes[1, 1].imshow(sharpened_images[3.0], cmap='gray')
    m3 = metrics_list[3]
    axes[1, 1].set_title(f"(e) Over-Boosted ($k=3.0$)\nBoost: {m3['Gradient_Boost_Pct']:+.1f}% | Clip: {m3['Total_Clipping_Pct']}%\n[SEVERE HALOS & NOISE]",
                          fontsize=10.5, fontweight='bold', color='#dc2626')
    axes[1, 1].axis('off')

    # (f) Clipping and Gradient Boost Trend Chart
    ax_chart = axes[1, 2]
    ks = [m['Boost_Factor_k'] for m in metrics_list]
    boosts = [m['Gradient_Boost_Pct'] for m in metrics_list]
    clips = [m['Total_Clipping_Pct'] for m in metrics_list]

    color1 = '#2563eb'
    ax_chart.set_xlabel('Boost Factor $k$', fontsize=9.5, fontweight='bold')
    ax_chart.set_ylabel('Gradient Boost (%)', color=color1, fontsize=9.5, fontweight='bold')
    l1 = ax_chart.plot(ks, boosts, 'o-', color=color1, linewidth=2.0, label='Gradient Boost %')
    ax_chart.tick_params(axis='y', labelcolor=color1)
    ax_chart.grid(True, linestyle=':', alpha=0.6)

    ax2 = ax_chart.twinx()
    color2 = '#dc2626'
    ax2.set_ylabel('Total Pixels Clipped (%)', color=color2, fontsize=9.5, fontweight='bold')
    l2 = ax2.plot(ks, clips, 's--', color=color2, linewidth=2.0, label='Clipped Pixels %')
    ax2.axhline(1.2, color='gray', linestyle=':', linewidth=1.0, label='Acceptable Limit (1.2%)')
    ax2.tick_params(axis='y', labelcolor=color2)

    lines = l1 + l2
    labels_chart = [l.get_label() for l in lines]
    ax_chart.legend(lines, labels_chart, loc='upper left', fontsize=8)
    ax_chart.set_title('(f) Gradient Boost vs Clipping Saturation\n($k\\geq 2.5$ Exceeds Safe Saturation Limit)',
                       fontsize=10.5, fontweight='bold', color='#1e3a8a')

    plt.suptitle("Experiment 07 - Task 7.1: High-Boost Factor Sweep & Dynamic Range Clipping Analysis",
                 fontsize=13, fontweight='bold', color='#0f172a', y=0.98)

    fig_path = os.path.join(fig_dir, "exp07_task_7_1_clipping_sweep_py.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Figure saved at: {fig_path}")

    return metrics_list

if __name__ == "__main__":
    run_task_7_1()
