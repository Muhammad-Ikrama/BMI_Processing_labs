"""
Experiment 04: Noise Modeling and Removal in Medical Images Using Median and Adaptive Filtering Techniques
Task 4.2: Failure Analysis of Linear Averaging & Gaussian Smoothing on Impulse Noise
Course: Medical Image Processing | Riphah International University
Instructor: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

def run_task_4_2():
    print("=" * 70)
    print("EXPERIMENT 04 - TASK 4.2: LINEAR FILTER FAILURE ANALYSIS ON IMPULSE NOISE")
    print("=" * 70)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.dirname(script_dir)
    img_path = os.path.join(exp_dir, "Inputs", "images", "CT.jpg")

    if not os.path.exists(img_path):
        img_path = os.path.join(exp_dir, "Inputs", "images", "MRI.jpg")

    ref = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if ref is None:
        raise FileNotFoundError(f"Could not load image from {img_path}")

    H, W = ref.shape

    # 1. Corrupt with 10% Salt & Pepper noise
    np.random.seed(42)
    noisy = ref.copy()
    num_sp = int(0.10 * ref.size)
    num_salt = num_sp // 2
    num_pepper = num_sp // 2

    r_idx = np.random.randint(0, H, num_sp)
    c_idx = np.random.randint(0, W, num_sp)
    noisy[r_idx[:num_salt], c_idx[:num_salt]] = 255
    noisy[r_idx[num_salt:], c_idx[num_salt:]] = 0

    # 2. Apply Linear Filters
    print("[INFO] Computing 5x5 Mean Box Filter...")
    mean_5 = cv2.blur(noisy, (5, 5))

    print("[INFO] Computing 5x5 Gaussian Filter (sigma = 1.2)...")
    gauss_5 = cv2.GaussianBlur(noisy, (5, 5), sigmaX=1.2)

    # 3. Apply Median Filter for comparison
    med_5 = cv2.medianBlur(noisy, 5)

    # Metrics
    p_noisy = psnr(ref, noisy)
    p_mean = psnr(ref, mean_5)
    p_gauss = psnr(ref, gauss_5)
    p_med = psnr(ref, med_5)

    s_noisy = ssim(ref, noisy)
    s_mean = ssim(ref, mean_5)
    s_gauss = ssim(ref, gauss_5)
    s_med = ssim(ref, med_5)

    # Mathematical Smear Quantification
    # An impulse of 255 in a 5x5 window contributes: 255 / 25 = 10.2 intensity levels to all 24 neighbors!
    # A pepper of 0 depresses true anatomical values (e.g. 120) by: (120 - 0) / 25 = 4.8 intensity levels.
    print("\n" + "-" * 75)
    print("MATHEMATICAL SMEAR MECHANISM ANALYSIS:")
    print("  * Single Salt Impulse (255) in 5x5 Mean Window -> Adds +10.20 intensity levels to 24 neighbors.")
    print("  * Single Pepper Impulse (0) in 5x5 Mean Window -> Subtracts -4.80 levels (for tissue=120).")
    print(f"  * Linear Mean 5x5 PSNR:     {p_mean:.2f} dB (Residual smear errors destroy contrast)")
    print(f"  * Linear Gaussian 5x5 PSNR: {p_gauss:.2f} dB (Gaussian weights amplify central blotch)")
    print(f"  * Non-Linear Median 5x5:   {p_med:.2f} dB (Order-statistics completely eliminates outliers)")
    print("-" * 75)

    # Magnified Uniform ROI (Center 60x60 patch)
    r1, r2 = H // 2 - 30, H // 2 + 30
    c1, c2 = W // 2 - 30, W // 2 + 30
    roi_noisy = noisy[r1:r2, c1:c2]
    roi_mean = mean_5[r1:r2, c1:c2]
    roi_gauss = gauss_5[r1:r2, c1:c2]
    roi_med = med_5[r1:r2, c1:c2]

    # Visualization: 4-Panel Figure
    fig, axes = plt.subplots(2, 2, figsize=(13, 11), dpi=300)
    plt.subplots_adjust(wspace=0.18, hspace=0.25)

    # Top-Left: Full Noisy Scan with ROI bounding box
    axes[0, 0].imshow(noisy, cmap='gray', vmin=0, vmax=255)
    axes[0, 0].set_title(f"A: 10% Impulse-Corrupted CT Scan\nPSNR: {p_noisy:.2f} dB | SSIM: {s_noisy:.4f}",
                          fontsize=10, fontweight='bold', color='#dc2626')
    axes[0, 0].axis('off')
    rect = plt.Rectangle((c1, r1), 60, 60, fill=False, edgecolor='#ef4444', linewidth=2.5, linestyle='--')
    axes[0, 0].add_patch(rect)

    # Top-Right: Full Mean 5x5 Scan
    axes[0, 1].imshow(mean_5, cmap='gray', vmin=0, vmax=255)
    axes[0, 1].set_title(f"B: Linear Mean 5x5 Filter Output\nPSNR: {p_mean:.2f} dB | SSIM: {s_mean:.4f} [Severe Smudge]",
                          fontsize=10, fontweight='bold', color='#ea580c')
    axes[0, 1].axis('off')

    # Bottom-Left: Magnified Uniform Region (Mean 5x5 Smear)
    axes[1, 0].imshow(roi_mean, cmap='gray', vmin=0, vmax=255)
    axes[1, 0].set_title("C: Magnified ROI - Linear Mean 5x5 Failure\n[Discrete Impulses Converted to Broad Gray Smudges]",
                          fontsize=10, fontweight='bold', color='#b91c1c')
    axes[1, 0].axis('off')

    # Bottom-Right: Magnified Uniform Region (Median 5x5 Success)
    axes[1, 1].imshow(roi_med, cmap='gray', vmin=0, vmax=255)
    axes[1, 1].set_title(f"D: Magnified ROI - Non-Linear Median 5x5 Success\nPSNR: {p_med:.2f} dB [Outliers Cleanly Excluded by Sorting]",
                          fontsize=10, fontweight='bold', color='#15803d')
    axes[1, 1].axis('off')

    fig.suptitle("Task 4.2: Failure Analysis of Linear Smoothing on Impulse Noise (CT Scan)",
                 fontsize=13.5, fontweight='bold', color='#0f172a', y=0.98)

    out_dir_py = os.path.join(exp_dir, "Outputs", "Python")
    fig_dir = os.path.join(exp_dir, "Figures")
    os.makedirs(out_dir_py, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    out_path_1 = os.path.join(out_dir_py, "exp04_task_4_2_linear_failure_smear_py.png")
    out_path_2 = os.path.join(fig_dir, "exp04_task_4_2_linear_failure_smear_py.png")

    plt.savefig(out_path_1, bbox_inches='tight', dpi=300)
    plt.savefig(out_path_2, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"[SUCCESS] Saved figure to:\n  {out_path_1}\n  {out_path_2}")

if __name__ == '__main__':
    run_task_4_2()
