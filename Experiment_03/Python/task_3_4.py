"""
Experiment 03: Image Smoothing of Medical Images Using Spatial Domain Mean/Averaging and Gaussian Filters
Task 3.4: Quantitative Image Quality Benchmarking (PSNR, SSIM, CNR) & 'Good to Go' Verification
Course: Medical Image Processing | Riphah International University
Instructor: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

def run_task_3_4():
    print("=" * 70)
    print("EXPERIMENT 03 - TASK 3.4: QUANTITATIVE BENCHMARKING (PSNR, SSIM, CNR)")
    print("=" * 70)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.dirname(script_dir)
    img_path = os.path.join(exp_dir, "Inputs", "images", "MRI.jpg")

    if not os.path.exists(img_path):
        img_path = os.path.join(exp_dir, "..", "..", "images", "MRI.jpg")

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not load image from {img_path}")

    H, W = img.shape

    # 1. Simulate Gaussian thermal acquisition noise (sigma = 18.0)
    np.random.seed(42)
    noise = np.random.normal(0, 18.0, img.shape)
    noisy = np.clip(img.astype(float) + noise, 0, 255).astype(np.uint8)

    # 2. Filter images: Mean 5x5 vs Gaussian 5x5 (sigma = 1.2)
    mean_5 = cv2.blur(noisy, (5, 5), borderType=cv2.BORDER_REPLICATE)
    gauss_5 = cv2.GaussianBlur(noisy, (5, 5), sigmaX=1.2, borderType=cv2.BORDER_REPLICATE)

    # 3. Define Clinical Regions of Interest (ROIs)
    # ROI 1: Signal (Cerebral Cortex / Deep Parenchyma)
    # Center 40x40 patch: rows [H//2-20, H//2+20], cols [W//2-20, W//2+20]
    r_sig_y1, r_sig_y2 = H // 2 - 20, H // 2 + 20
    r_sig_x1, r_sig_x2 = W // 2 - 20, W // 2 + 20
    sig_slice = (slice(r_sig_y1, r_sig_y2), slice(r_sig_x1, r_sig_x2))

    # ROI 2: Background Air
    # Top-left corner 40x40 patch: rows [10, 50], cols [10, 50]
    r_bg_y1, r_bg_y2 = 10, 50
    r_bg_x1, r_bg_x2 = 10, 50
    bg_slice = (slice(r_bg_y1, r_bg_y2), slice(r_bg_x1, r_bg_x2))

    def compute_metrics(im, ref_im):
        p = psnr(ref_im, im)
        s = ssim(ref_im, im)

        s_patch = im[sig_slice].astype(float)
        b_patch = im[bg_slice].astype(float)

        mu_s = s_patch.mean()
        mu_b = b_patch.mean()
        var_s = s_patch.var()
        var_b = b_patch.var()

        cnr = abs(mu_s - mu_b) / np.sqrt(var_s + var_b)
        sigma_bg = np.sqrt(var_b)

        return p, s, cnr, mu_s, mu_b, sigma_bg

    cases = [
        ("Noisy Baseline", noisy),
        ("Mean Filter 5x5", mean_5),
        ("Gaussian Filter 5x5 (sig=1.2)", gauss_5)
    ]

    records = []
    print(f"{'Condition':<28} | {'PSNR (dB)':<10} | {'SSIM':<8} | {'CNR':<6} | {'Noise std_bg':<12} | {'Status'}")
    print("-" * 80)

    for name, im in cases:
        p, s, cnr, mu_s, mu_b, s_bg = compute_metrics(im, img)
        # Good to go check: PSNR >= 27.5 dB, SSIM >= 0.50, CNR >= 1.0
        g2g = (p >= 27.5 and s >= 0.50 and cnr >= 1.0)
        status = "Good to Go" if g2g else "Needs Clinical Review"
        print(f"{name:<28} | {p:<10.2f} | {s:<8.4f} | {cnr:<6.2f} | {s_bg:<10.2f} | {status}")
        records.append({
            "Method": name,
            "PSNR_dB": round(p, 2),
            "SSIM": round(s, 4),
            "CNR": round(cnr, 2),
            "Signal_Mean": round(mu_s, 2),
            "Background_Mean": round(mu_b, 2),
            "Air_Noise_StdDev": round(s_bg, 2),
            "Status": status
        })

    # Export to CSV
    df = pd.DataFrame(records)
    table_dir = os.path.join(exp_dir, "Tables")
    os.makedirs(table_dir, exist_ok=True)
    csv_path = os.path.join(table_dir, "task_3_4_smoothing_benchmark_summary.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[INFO] Benchmark metrics exported to CSV:\n  {csv_path}")

    # 4. Visualization: Dual-Panel Figure
    # Left: MRI scan with overlaid ROI bounding boxes
    # Right: Grouped bar chart comparing PSNR, SSIM (*50 for scale), and CNR
    fig, (ax_img, ax_bar) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    plt.subplots_adjust(wspace=0.25)

    # Left: ROI Overlay on Clean MRI
    ax_img.imshow(img, cmap='gray', vmin=0, vmax=255)
    # ROI 1: Signal (Cyan)
    rect_sig = plt.Rectangle((r_sig_x1, r_sig_y1), 40, 40, fill=False, edgecolor='#06b6d4', linewidth=2.5, label="ROI 1: Cortex (Signal)")
    ax_img.add_patch(rect_sig)
    ax_img.text(r_sig_x1, r_sig_y1 - 6, "ROI 1: Cortex", color='#06b6d4', fontsize=9.5, fontweight='bold')

    # ROI 2: Background (Red)
    rect_bg = plt.Rectangle((r_bg_x1, r_bg_y1), 40, 40, fill=False, edgecolor='#ef4444', linewidth=2.5, label="ROI 2: Air (Noise)")
    ax_img.add_patch(rect_bg)
    ax_img.text(r_bg_x1, r_bg_y2 + 16, "ROI 2: Background Air", color='#ef4444', fontsize=9.5, fontweight='bold')

    ax_img.set_title("Clinical Brain MRI ROI Definitions\n[ROI 1: Tissue Signal | ROI 2: Background Air Noise]",
                     fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax_img.axis('off')
    ax_img.legend(loc='lower right', fontsize=8.5)

    # Right: Grouped Bar Chart
    methods = [r["Method"] for r in records]
    psnr_vals = [r["PSNR_dB"] for r in records]
    ssim_vals = [r["SSIM"] for r in records]
    cnr_vals = [r["CNR"] for r in records]

    x = np.arange(len(methods))
    width = 0.25

    rects1 = ax_bar.bar(x - width, psnr_vals, width, label='PSNR (dB)', color='#3b82f6')
    rects2 = ax_bar.bar(x, [s * 30 for s in ssim_vals], width, label='SSIM (x30 scale)', color='#10b981')
    rects3 = ax_bar.bar(x + width, [c * 15 for c in cnr_vals], width, label='CNR (x15 scale)', color='#f59e0b')

    # Add threshold line for PSNR = 28 dB
    ax_bar.axhline(28.0, color='#3b82f6', linestyle='--', linewidth=1.5, alpha=0.7, label="'Good to Go' PSNR Threshold (28 dB)")

    ax_bar.set_ylabel('Metric Value (with visual scaling)', fontsize=10, fontweight='bold', color='#1e293b')
    ax_bar.set_title("Quantitative Quality Benchmark Comparison", fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(["Noisy\nBaseline", "Mean\n5x5", "Gaussian\n5x5 (sig=1.2)"], fontsize=9.5)
    ax_bar.grid(axis='y', linestyle='--', alpha=0.5)
    ax_bar.legend(loc='upper left', fontsize=8.5)

    # Bar value labels
    for rect, orig_val in zip(rects1, psnr_vals):
        height = rect.get_height()
        ax_bar.annotate(f'{orig_val:.1f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')
    for rect, orig_val in zip(rects2, ssim_vals):
        height = rect.get_height()
        ax_bar.annotate(f'{orig_val:.3f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')
    for rect, orig_val in zip(rects3, cnr_vals):
        height = rect.get_height()
        ax_bar.annotate(f'{orig_val:.2f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

    fig.suptitle("Task 3.4: Quantitative Image Quality Benchmarking (PSNR, SSIM, and CNR)",
                 fontsize=13, fontweight='bold', color='#0f172a', y=0.98)

    out_dir_py = os.path.join(exp_dir, "Outputs", "Python")
    fig_dir = os.path.join(exp_dir, "Figures")
    os.makedirs(out_dir_py, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    out_path_1 = os.path.join(out_dir_py, "exp03_task_3_4_quality_benchmarking_py.png")
    out_path_2 = os.path.join(fig_dir, "exp03_task_3_4_quality_benchmarking_py.png")

    plt.savefig(out_path_1, bbox_inches='tight', dpi=300)
    plt.savefig(out_path_2, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"[SUCCESS] Saved figure to:\n  {out_path_1}\n  {out_path_2}")

if __name__ == '__main__':
    run_task_3_4()
