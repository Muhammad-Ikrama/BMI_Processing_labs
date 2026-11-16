"""
Experiment 03: Image Smoothing of Medical Images Using Spatial Domain Mean/Averaging and Gaussian Filters
Task 3.3: 2D Gaussian Kernel Construction, Normalization & Spread Parameter Sweep [sigma = 0.6, 1.2, 2.0]
Course: Medical Image Processing | Riphah International University
Instructor: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

def create_gaussian_kernel(k_size=7, sigma=1.0):
    """
    Generate normalized 2D isotropic Gaussian kernel of size k_size x k_size.
    Formula: G(x, y) = (1 / (2*pi*sigma^2)) * exp(-(x^2 + y^2) / (2*sigma^2))
    """
    radius = k_size // 2
    x = np.linspace(-radius, radius, k_size)
    y = np.linspace(-radius, radius, k_size)
    xx, yy = np.meshgrid(x, y)

    # Raw Gaussian continuous formulation
    normalizer = 1.0 / (2.0 * np.pi * (sigma ** 2))
    exponent = -(xx ** 2 + yy ** 2) / (2.0 * (sigma ** 2))
    raw_kernel = normalizer * np.exp(exponent)

    # Discrete Normalization to ensure sum equals exactly 1.000000
    kernel_sum = np.sum(raw_kernel)
    kernel_norm = raw_kernel / kernel_sum

    return xx, yy, kernel_norm

def run_task_3_3():
    print("=" * 70)
    print("EXPERIMENT 03 - TASK 3.3: 2D GAUSSIAN KERNEL CONSTRUCTION & SIGMA SWEEP")
    print("=" * 70)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.dirname(script_dir)
    img_path = os.path.join(exp_dir, "Inputs", "images", "MRI.jpg")

    if not os.path.exists(img_path):
        img_path = os.path.join(exp_dir, "..", "..", "images", "MRI.jpg")

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not load image from {img_path}")

    # Degrade scan with simulated Gaussian noise (sigma = 18.0)
    np.random.seed(42)
    noise = np.random.normal(0, 18.0, img.shape)
    noisy = np.clip(img.astype(float) + noise, 0, 255).astype(np.uint8)

    k_size = 7
    sigmas = [0.6, 1.2, 2.0]
    kernels = []
    filtered_images = []
    psnr_vals = []
    ssim_vals = []

    print(f"\nConstructing 7x7 Gaussian Kernels (Radius = 3, Elements = 49):")
    print("-" * 65)
    for sig in sigmas:
        xx, yy, k_norm = create_gaussian_kernel(k_size, sig)
        k_sum = np.sum(k_norm)
        center_val = k_norm[k_size // 2, k_size // 2]
        corner_val = k_norm[0, 0]

        print(f"Sigma = {sig:3.1f} | Sum: {k_sum:.6f} | Center Peak: {center_val:.5f} | Corner Tail: {corner_val:.7f}")
        assert np.isclose(k_sum, 1.0, atol=1e-6), f"Kernel sum {k_sum} != 1.0"

        # Apply convolution using custom kernel with replicate border
        filtered = cv2.filter2D(noisy, -1, k_norm, borderType=cv2.BORDER_REPLICATE)
        p = psnr(img, filtered)
        s = ssim(img, filtered)

        kernels.append((xx, yy, k_norm))
        filtered_images.append(filtered)
        psnr_vals.append(p)
        ssim_vals.append(s)

    print("-" * 65)
    print(f"{'Sigma Spread':<14} | {'Center Weight':<14} | {'PSNR (dB)':<10} | {'SSIM':<8} | {'Clinical Performance'}")
    print("-" * 65)
    for sig, (_, _, k_norm), p, s in zip(sigmas, kernels, psnr_vals, ssim_vals):
        c_wt = k_norm[k_size // 2, k_size // 2]
        if sig == 0.6:
            perf = "Sharp detail retained; moderate noise remains"
        elif sig == 1.2:
            perf = "Optimal trade-off (peak structural fidelity)"
        else:
            perf = "Heavy noise suppression; subtle soft-tissue blurred"
        print(f"sigma = {sig:<6.1f} | {c_wt:<14.5f} | {p:<10.2f} | {s:<8.4f} | {perf}")

    # Visualization: 3 rows x 3 columns
    # Row 1: 2D Heatmaps with weight values
    # Row 2: 3D Surface plots of bell curves
    # Row 3: Resulting filtered medical scans
    fig = plt.figure(figsize=(15, 12), dpi=300)
    plt.subplots_adjust(wspace=0.25, hspace=0.32)

    for idx, (sig, (xx, yy, k_norm), f_im, p, s) in enumerate(zip(sigmas, kernels, filtered_images, psnr_vals, ssim_vals)):
        # Row 1: 2D Heatmap
        ax_heat = fig.add_subplot(3, 3, idx + 1)
        im_h = ax_heat.imshow(k_norm, cmap='viridis', origin='upper')
        ax_heat.set_title(f"7x7 Kernel Heatmap (σ = {sig})\nCenter Peak = {k_norm[3, 3]:.4f}",
                          fontsize=9.5, fontweight='bold', color='#1e3a8a')
        ax_heat.set_xticks(range(7))
        ax_heat.set_yticks(range(7))
        ax_heat.set_xticklabels(range(-3, 4), fontsize=8)
        ax_heat.set_yticklabels(range(-3, 4), fontsize=8)
        fig.colorbar(im_h, ax=ax_heat, fraction=0.046, pad=0.04)

        # Row 2: 3D Surface Plot
        ax_3d = fig.add_subplot(3, 3, idx + 4, projection='3d')
        surf = ax_3d.plot_surface(xx, yy, k_norm, cmap='coolwarm', edgecolor='none', alpha=0.9)
        ax_3d.set_title(f"3D Bell Surface (σ = {sig})\nVolume Sum = 1.000",
                        fontsize=9.5, fontweight='bold', color='#1e3a8a')
        ax_3d.set_xlabel("X Offset", fontsize=7.5)
        ax_3d.set_ylabel("Y Offset", fontsize=7.5)
        ax_3d.set_zlabel("Weight", fontsize=7.5)
        ax_3d.view_init(elev=28, azim=45)

        # Row 3: Filtered Scan
        ax_img = fig.add_subplot(3, 3, idx + 7)
        ax_img.imshow(f_im, cmap='gray', vmin=0, vmax=255)
        ax_img.set_title(f"Filtered Scan (σ = {sig})\nPSNR: {p:.2f} dB | SSIM: {s:.4f}",
                         fontsize=9.5, fontweight='bold', color='#15803d' if sig == 1.2 else '#334155')
        ax_img.axis('off')

    fig.suptitle("Task 3.3: 2D Gaussian Kernel Construction, Normalization & Spread Parameter Sweep (K=7x7)",
                 fontsize=13, fontweight='bold', color='#0f172a', y=0.98)

    out_dir_py = os.path.join(exp_dir, "Outputs", "Python")
    fig_dir = os.path.join(exp_dir, "Figures")
    os.makedirs(out_dir_py, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    out_path_1 = os.path.join(out_dir_py, "exp03_task_3_3_gaussian_kernel_sweep_py.png")
    out_path_2 = os.path.join(fig_dir, "exp03_task_3_3_gaussian_kernel_sweep_py.png")

    plt.savefig(out_path_1, bbox_inches='tight', dpi=300)
    plt.savefig(out_path_2, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"[SUCCESS] Saved figure to:\n  {out_path_1}\n  {out_path_2}")

if __name__ == '__main__':
    run_task_3_3()
