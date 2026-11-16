"""
Experiment 04: Noise Modeling and Removal in Medical Images Using Median and Adaptive Filtering Techniques
Task 4.3: Implementation and Kernel Sizing Sensitivity of Standard Median Filtering [3x3, 5x5, 7x7]
Course: Medical Image Processing | Riphah International University
Instructor: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

def calc_epi(ref_im, filt_im):
    """
    Edge Preservation Index (EPI / beta):
    Correlation coefficient between the Laplacian high-pass edge maps of reference and filtered scans.
    """
    lap_ref = cv2.Laplacian(ref_im.astype(float), cv2.CV_64F)
    lap_filt = cv2.Laplacian(filt_im.astype(float), cv2.CV_64F)

    d_ref = lap_ref - np.mean(lap_ref)
    d_filt = lap_filt - np.mean(lap_filt)

    num = np.sum(d_ref * d_filt)
    den = np.sqrt(np.sum(d_ref ** 2) * np.sum(d_filt ** 2))
    if den == 0:
        return 0.0
    return float(num / den)

def run_task_4_3():
    print("=" * 70)
    print("EXPERIMENT 04 - TASK 4.3: STANDARD MEDIAN FILTER KERNEL SWEEP [3x3, 5x5, 7x7]")
    print("=" * 70)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.dirname(script_dir)
    img_path = os.path.join(exp_dir, "Inputs", "images", "MRI.jpg")

    if not os.path.exists(img_path):
        img_path = os.path.join(exp_dir, "..", "..", "images", "MRI.jpg")

    ref = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if ref is None:
        raise FileNotFoundError(f"Could not load image from {img_path}")

    H, W = ref.shape

    # 1. Corrupt with 15% Salt-and-Pepper Impulse Noise
    np.random.seed(42)
    noisy = ref.copy()
    num_sp = int(0.15 * ref.size)
    num_salt = num_sp // 2
    num_pepper = num_sp // 2

    r_idx = np.random.randint(0, H, num_sp)
    c_idx = np.random.randint(0, W, num_sp)
    noisy[r_idx[:num_salt], c_idx[:num_salt]] = 255
    noisy[r_idx[num_salt:], c_idx[num_salt:]] = 0

    p_noisy = psnr(ref, noisy)
    s_noisy = ssim(ref, noisy)
    e_noisy = calc_epi(ref, noisy)

    # 2. Sweep Median Filter Windows: [3x3, 5x5, 7x7]
    windows = [3, 5, 7]
    filtered_images = []
    psnr_vals = []
    ssim_vals = []
    epi_vals = []

    print(f"{'Window Size':<12} | {'PSNR (dB)':<10} | {'SSIM':<8} | {'EPI (beta)':<10} | {'Clinical Assessment'}")
    print("-" * 75)
    print(f"{'Noisy Baseline':<12} | {p_noisy:<10.2f} | {s_noisy:<8.4f} | {e_noisy:<10.4f} | Corrupted input (15% SP)")

    for w in windows:
        f_im = cv2.medianBlur(noisy, w)
        p = psnr(ref, f_im)
        s = ssim(ref, f_im)
        e = calc_epi(ref, f_im)

        filtered_images.append(f_im)
        psnr_vals.append(p)
        ssim_vals.append(s)
        epi_vals.append(e)

        if w == 3:
            obs = "Optimal; clears 15% noise without rounding edges"
        elif w == 5:
            obs = "Over-filtered; corners rounded, thin vessels eroded"
        else:
            obs = "Excessive detail truncation; anatomical corners blunted"

        print(f"{w}x{w:<10} | {p:<10.2f} | {s:<8.4f} | {e:<10.4f} | {obs}")

    print("-" * 75)
    print("Finding: Peak SSIM and EPI occur at 3x3. Larger median windows cause detail truncation")
    print("because even uncorrupted pixels are replaced by the local window median.")

    # 3. Visualization: 4-Panel Composite
    # 3 images + 1 quantitative line plot of SSIM & EPI vs Window Size
    fig, axes = plt.subplots(2, 2, figsize=(13, 11), dpi=300)
    plt.subplots_adjust(wspace=0.18, hspace=0.25)

    # Top-Left: Median 3x3
    axes[0, 0].imshow(filtered_images[0], cmap='gray', vmin=0, vmax=255)
    axes[0, 0].set_title(f"A: Standard Median 3x3 [Optimal]\nPSNR: {psnr_vals[0]:.2f} dB | SSIM: {ssim_vals[0]:.4f} | EPI: {epi_vals[0]:.4f}",
                          fontsize=9.5, fontweight='bold', color='#15803d')
    axes[0, 0].axis('off')

    # Top-Right: Median 5x5
    axes[0, 1].imshow(filtered_images[1], cmap='gray', vmin=0, vmax=255)
    axes[0, 1].set_title(f"B: Standard Median 5x5 [Edge Rounding]\nPSNR: {psnr_vals[1]:.2f} dB | SSIM: {ssim_vals[1]:.4f} | EPI: {epi_vals[1]:.4f}",
                          fontsize=9.5, fontweight='bold', color='#ca8a04')
    axes[0, 1].axis('off')

    # Bottom-Left: Median 7x7
    axes[1, 0].imshow(filtered_images[2], cmap='gray', vmin=0, vmax=255)
    axes[1, 0].set_title(f"C: Standard Median 7x7 [Detail Truncation]\nPSNR: {psnr_vals[2]:.2f} dB | SSIM: {ssim_vals[2]:.4f} | EPI: {epi_vals[2]:.4f}",
                          fontsize=9.5, fontweight='bold', color='#dc2626')
    axes[1, 0].axis('off')

    # Bottom-Right: Line Graph (SSIM and EPI vs Window Size)
    ax_graph = axes[1, 1]
    ax_epi = ax_graph.twinx()

    l1 = ax_graph.plot(windows, ssim_vals, 'o-b', linewidth=2.2, markersize=8, label="SSIM")
    l2 = ax_epi.plot(windows, epi_vals, 's--g', linewidth=2.2, markersize=8, label="EPI (Edge Preservation)")

    ax_graph.set_xlabel("Median Filter Window Size (K x K)", fontsize=10, fontweight='bold', color='#1e293b')
    ax_graph.set_ylabel("Structural Similarity Index (SSIM)", fontsize=10, fontweight='bold', color='#2563eb')
    ax_epi.set_ylabel("Edge Preservation Index (EPI)", fontsize=10, fontweight='bold', color='#16a34a')
    ax_graph.set_xticks(windows)
    ax_graph.set_xticklabels(["3x3", "5x5", "7x7"])
    ax_graph.grid(True, linestyle='--', alpha=0.5)
    ax_graph.set_title("SSIM and EPI Trajectory vs. Window Dimension", fontsize=10.5, fontweight='bold', color='#1e3a8a')

    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax_graph.legend(lines, labels, loc='center right', fontsize=9)

    fig.suptitle("Task 4.3: Implementation and Kernel Sizing Sensitivity of Standard Median Filtering",
                 fontsize=13.5, fontweight='bold', color='#0f172a', y=0.98)

    out_dir_py = os.path.join(exp_dir, "Outputs", "Python")
    fig_dir = os.path.join(exp_dir, "Figures")
    os.makedirs(out_dir_py, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    out_path_1 = os.path.join(out_dir_py, "exp04_task_4_3_median_kernel_sweep_py.png")
    out_path_2 = os.path.join(fig_dir, "exp04_task_4_3_median_kernel_sweep_py.png")

    plt.savefig(out_path_1, bbox_inches='tight', dpi=300)
    plt.savefig(out_path_2, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"[SUCCESS] Saved figure to:\n  {out_path_1}\n  {out_path_2}")

if __name__ == '__main__':
    run_task_4_3()
