"""
Experiment 05 - Task 5.2: Prewitt vs. Sobel Noise Sensitivity Benchmarking
Quantifying Spurious Edge Breakthrough in Homogeneous Background Air ROI
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Riphah International University
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve


def run_task_5_2():
    print("=" * 70)
    print("EXPERIMENT 05 - TASK 5.2: PREWITT VS SOBEL NOISE SENSITIVITY BENCHMARK")
    print("=" * 70)

    # Path handling
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.dirname(script_dir)
    img_path = os.path.join(exp_dir, "Inputs", "images", "CT.jpg")
    if not os.path.exists(img_path):
        img_path = os.path.join(exp_dir, "..", "..", "images", "CT.jpg")
    
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not load image at {img_path}")

    H, W = img.shape

    # 1. Add simulated Gaussian electronic noise (sigma = 15.0)
    np.random.seed(42)
    noise_sigma = 15.0
    gaussian_noise = np.random.normal(0, noise_sigma, (H, W))
    noisy_img = np.clip(img.astype(float) + gaussian_noise, 0, 255).astype(np.uint8)

    # 2. Define homogeneous background air Region of Interest (ROI)
    # Background air at top-left corner
    r_start, r_end = 20, 80
    c_start, c_end = 20, 80
    roi_area = float((r_end - r_start) * (c_end - c_start))
    print(f"[INFO] Background Air ROI: [{r_start}:{r_end}, {c_start}:{c_end}] (Area: {int(roi_area)} pixels)")

    # 3. Prewitt Operator on Noisy Image
    px = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
    py = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)
    noisy_f = noisy_img.astype(float)
    prew_mag = np.hypot(convolve(noisy_f, px), convolve(noisy_f, py))

    # 4. Sobel Operator on Noisy Image
    sob_x = cv2.Sobel(noisy_img, cv2.CV_64F, 1, 0, ksize=3)
    sob_y = cv2.Sobel(noisy_img, cv2.CV_64F, 0, 1, ksize=3)
    sob_mag = np.hypot(sob_x, sob_y)

    # 5. Calibrated Thresholding Analysis:
    # Sobel kernel has gain = 4 in orthogonal direction ([1, 2, 1]), while Prewitt has gain = 3 ([1, 1, 1]).
    # Equivalent step-edge response requires Sobel threshold = (4/3) * Prewitt threshold.
    eval_thresholds = [
        ("Level 1 (Low)", 35.0, 46.7),
        ("Level 2 (Standard)", 45.0, 60.0),
        ("Level 3 (High)", 55.0, 73.3),
        ("Level 4 (Strict)", 65.0, 86.7)
    ]

    prew_roi_counts = []
    sob_roi_counts = []
    prew_roi_rates = []
    sob_roi_rates = []

    print("\n" + "-" * 85)
    print(f"{'Sensitivity Level':<20} | {'Prewitt Th':<11} | {'Sobel Th':<10} | {'Prewitt False':<14} | {'Sobel False':<14}")
    print("-" * 85)

    for lvl_name, p_th, s_th in eval_thresholds:
        p_bin = (prew_mag > p_th).astype(np.uint8)
        s_bin = (sob_mag > s_th).astype(np.uint8)

        p_roi_cnt = int(np.count_nonzero(p_bin[r_start:r_end, c_start:c_end]))
        s_roi_cnt = int(np.count_nonzero(s_bin[r_start:r_end, c_start:c_end]))

        p_roi_rate = (p_roi_cnt / roi_area) * 100.0
        s_roi_rate = (s_roi_cnt / roi_area) * 100.0

        prew_roi_counts.append(p_roi_cnt)
        sob_roi_counts.append(s_roi_cnt)
        prew_roi_rates.append(p_roi_rate)
        sob_roi_rates.append(s_roi_rate)

        print(f"{lvl_name:<20} | {p_th:<11.1f} | {s_th:<10.1f} | {p_roi_cnt:<5} ({p_roi_rate:5.1f}%) | {s_roi_cnt:<5} ({s_roi_rate:5.1f}%)")
    print("-" * 85)

    # Standard benchmark edge maps at Level 2 (45 vs 60)
    prew_edge_std = (prew_mag > 45.0).astype(np.uint8) * 255
    sob_edge_std = (sob_mag > 60.0).astype(np.uint8) * 255

    # Save outputs
    out_dir = os.path.join(exp_dir, "Outputs", "Python")
    os.makedirs(out_dir, exist_ok=True)
    cv2.imwrite(os.path.join(out_dir, "exp05_task_5_2_noisy_input.png"), noisy_img)
    cv2.imwrite(os.path.join(out_dir, "exp05_task_5_2_prewitt_noisy.png"), prew_edge_std)
    cv2.imwrite(os.path.join(out_dir, "exp05_task_5_2_sobel_noisy.png"), sob_edge_std)

    # Visualization
    fig, axes = plt.subplots(2, 2, figsize=(13, 11), dpi=300)

    # 1. Noisy image with ROI box
    roi_disp = cv2.cvtColor(noisy_img, cv2.COLOR_GRAY2RGB)
    cv2.rectangle(roi_disp, (c_start, r_start), (c_end, r_end), (255, 0, 0), 2)
    axes[0, 0].imshow(roi_disp)
    axes[0, 0].set_title(f"Noisy Clinical CT Scan (Gaussian sigma = {int(noise_sigma)})\n[Red Box: Evaluated Homogeneous Background Air ROI]",
                         fontsize=11, fontweight="bold", pad=8)
    axes[0, 0].axis("off")

    # 2. Prewitt at Th=45
    p_roi_disp = cv2.cvtColor(prew_edge_std, cv2.COLOR_GRAY2RGB)
    cv2.rectangle(p_roi_disp, (c_start, r_start), (c_end, r_end), (255, 50, 50), 2)
    axes[0, 1].imshow(p_roi_disp)
    p_cnt_std = prew_roi_counts[1]
    p_rate_std = prew_roi_rates[1]
    axes[0, 1].set_title(f"Prewitt Operator (Calibrated Th = 45.0)\nAir ROI False Edges: {p_cnt_std:,} ({p_rate_std:.1f}%) [Box Averaging Clutter]",
                         fontsize=11, fontweight="bold", pad=8)
    axes[0, 1].axis("off")

    # 3. Sobel at Th=60
    s_roi_disp = cv2.cvtColor(sob_edge_std, cv2.COLOR_GRAY2RGB)
    cv2.rectangle(s_roi_disp, (c_start, r_start), (c_end, r_end), (50, 255, 50), 2)
    axes[1, 0].imshow(s_roi_disp)
    s_cnt_std = sob_roi_counts[1]
    s_rate_std = sob_roi_rates[1]
    axes[1, 0].set_title(f"Sobel Operator (Calibrated Th = 60.0)\nAir ROI False Edges: {s_cnt_std:,} ({s_rate_std:.1f}%) [Binomial Kernel Smoothing]",
                         fontsize=11, fontweight="bold", pad=8)
    axes[1, 0].axis("off")

    # 4. Quantitative Bar Chart Comparison
    x = np.arange(len(eval_thresholds))
    width = 0.35
    ax_bar = axes[1, 1]
    rects1 = ax_bar.bar(x - width/2, prew_roi_rates, width, label="Prewitt (Unweighted [1,1,1]^T)", color="#d9534f", edgecolor="black")
    rects2 = ax_bar.bar(x + width/2, sob_roi_rates, width, label="Sobel (Binomial [1,2,1]^T)", color="#5cb85c", edgecolor="black")
    ax_bar.set_ylabel("False Spurious Edge Rate (%) in Air ROI", fontsize=10, fontweight="bold")
    ax_bar.set_xlabel("Sensitivity Level (Calibrated Step-Response Thresholds)", fontsize=10, fontweight="bold")
    ax_bar.set_title("Spurious Edge Breakthrough across Calibrated Thresholds\nPrewitt vs. Sobel Kernel Frequency Selectivity", fontsize=11, fontweight="bold", pad=8)
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels([f"L{i+1}\n(P:{int(p)}/S:{int(s)})" for i, (_, p, s) in enumerate(eval_thresholds)], fontweight="bold", fontsize=9)
    ax_bar.legend(fontsize=9, loc="upper right")
    ax_bar.grid(axis="y", linestyle="--", alpha=0.5)

    # Bar value labels
    for rect in rects1:
        h = rect.get_height()
        ax_bar.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width()/2, h),
                        xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8, fontweight="bold")
    for rect in rects2:
        h = rect.get_height()
        ax_bar.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width()/2, h),
                        xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8, fontweight="bold")

    plt.suptitle("Task 5.2: Noise Sensitivity Benchmarking: Prewitt vs. Sobel Kernels\nBinomial Orthogonal Smoothing [1,2,1]^T vs. Unweighted Moving Average [1,1,1]^T",
                 fontsize=13, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    fig_dir = os.path.join(exp_dir, "Figures")
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, "exp05_task_5_2_noise_sensitivity_py.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SUCCESS] Figure saved to {fig_path}")

    return {
        "eval_thresholds": eval_thresholds,
        "prewitt_roi_rates": prew_roi_rates,
        "sobel_roi_rates": sob_roi_rates
    }


if __name__ == "__main__":
    run_task_5_2()
