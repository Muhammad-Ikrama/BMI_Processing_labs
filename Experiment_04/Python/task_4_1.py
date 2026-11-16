"""
Experiment 04: Noise Modeling and Removal in Medical Images Using Median and Adaptive Filtering Techniques
Task 4.1: Synthetic Noise Modeling & Statistical Probability Density (PDF) Analysis
Course: Medical Image Processing | Riphah International University
Instructor: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def add_gaussian_noise(image, mean=0.0, sigma=20.0):
    """Additive thermal Gaussian noise: g = f + eta, eta ~ N(mu, sigma^2)"""
    noise = np.random.normal(mean, sigma, image.shape)
    noisy = np.clip(image.astype(float) + noise, 0, 255).astype(np.uint8)
    residual = noisy.astype(float) - image.astype(float)
    return noisy, residual, noise

def add_salt_pepper_noise(image, density=0.15):
    """Impulse noise: Pa at 0 (pepper), Pb at 255 (salt)"""
    noisy = image.copy()
    num_corrupt = int(density * image.size)
    num_salt = num_corrupt // 2
    num_pepper = num_corrupt // 2

    # Random pixel coordinates
    r_coords = np.random.randint(0, image.shape[0], num_corrupt)
    c_coords = np.random.randint(0, image.shape[1], num_corrupt)

    noisy[r_coords[:num_salt], c_coords[:num_salt]] = 255
    noisy[r_coords[num_salt:], c_coords[num_salt:]] = 0

    residual = noisy.astype(float) - image.astype(float)
    return noisy, residual

def add_speckle_noise(image, variance=0.25):
    """Multiplicative speckle noise: g = f + f * eta, eta ~ N(0, var)"""
    std = np.sqrt(variance)
    noise = np.random.normal(0, std, image.shape)
    noisy = np.clip(image.astype(float) + image.astype(float) * noise, 0, 255).astype(np.uint8)
    residual = noisy.astype(float) - image.astype(float)
    return noisy, residual

def run_task_4_1():
    print("=" * 70)
    print("EXPERIMENT 04 - TASK 4.1: SYNTHETIC NOISE MODELING & PDF ANALYSIS")
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
    np.random.seed(42)

    # 1. Generate Noise Models
    print("[INFO] Simulating Additive Gaussian Noise (sigma = 20.0)...")
    noisy_gauss, res_gauss, _ = add_gaussian_noise(ref, mean=0.0, sigma=20.0)

    print("[INFO] Simulating Salt-and-Pepper Impulse Noise (density = 15%)...")
    noisy_sp, res_sp = add_salt_pepper_noise(ref, density=0.15)

    print("[INFO] Simulating Multiplicative Speckle Noise (variance = 0.25)...")
    noisy_speckle, res_speckle = add_speckle_noise(ref, variance=0.25)

    # 2. Statistical Analysis of Residuals
    mean_g, std_g = np.mean(res_gauss), np.std(res_gauss)
    mean_sp, std_sp = np.mean(res_sp), np.std(res_sp)
    mean_spk, std_spk = np.mean(res_speckle), np.std(res_speckle)

    # Count impulse spikes in S&P residual
    pos_spikes = np.sum(res_sp > 100)
    neg_spikes = np.sum(res_sp < -100)

    print("\n" + "-" * 75)
    print("STATISTICAL MOMENTS OF RESIDUAL PERTURBATIONS (Noisy - Clean):")
    print(f"  * Gaussian Residual:  Mean = {mean_g:+.2f} (Expected: ~0.0), StdDev = {std_g:.2f} (Expected: ~20.0)")
    print(f"  * S&P Residual:       Positive Spikes = {pos_spikes}, Negative Spikes = {neg_spikes}")
    print(f"  * Speckle Residual:   Mean = {mean_spk:+.2f}, StdDev = {std_spk:.2f} (Signal-Dependent)")
    print("-" * 75)

    # 3. Visualization: 2 Rows x 3 Columns
    # Row 1: Corrupted Clinical Scans
    # Row 2: Empirical Histograms and Theoretical PDF Fits
    fig, axes = plt.subplots(2, 3, figsize=(15, 9.5), dpi=300)
    plt.subplots_adjust(wspace=0.22, hspace=0.28)

    # Top-Row: Images
    axes[0, 0].imshow(noisy_gauss, cmap='gray', vmin=0, vmax=255)
    axes[0, 0].set_title(f"A: Additive Thermal Gaussian\n(μ = 0, σ = 20.0) [MRI RF Coils]",
                          fontsize=10, fontweight='bold', color='#1e3a8a')
    axes[0, 0].axis('off')

    axes[0, 1].imshow(noisy_sp, cmap='gray', vmin=0, vmax=255)
    axes[0, 1].set_title(f"B: Salt-and-Pepper Impulse\n(Density = 15%) [Detector Failures]",
                          fontsize=10, fontweight='bold', color='#b91c1c')
    axes[0, 1].axis('off')

    axes[0, 2].imshow(noisy_speckle, cmap='gray', vmin=0, vmax=255)
    axes[0, 2].set_title(f"C: Multiplicative Speckle\n(Variance = 0.25) [Ultrasound / OCT]",
                          fontsize=10, fontweight='bold', color='#c2410c')
    axes[0, 2].axis('off')

    # Bottom-Row: Residual Histograms and PDFs
    # Plot 1: Gaussian Residual
    bins_g = np.linspace(-70, 70, 71)
    axes[1, 0].hist(res_gauss.ravel(), bins=bins_g, density=True, color='#3b82f6', alpha=0.65, edgecolor='#1d4ed8', label='Empirical Residual')
    x_g = np.linspace(-70, 70, 200)
    pdf_g = norm.pdf(x_g, mean_g, std_g)
    axes[1, 0].plot(x_g, pdf_g, color='#1e3a8a', linewidth=2.2, label=f'Gaussian Fit\n(μ={mean_g:.1f}, σ={std_g:.1f})')
    axes[1, 0].set_title("Gaussian Residual Distribution (Zero-Mean)", fontsize=10, fontweight='bold', color='#1e3a8a')
    axes[1, 0].set_xlabel("Residual Intensity Error (g - f)", fontsize=9, fontweight='bold')
    axes[1, 0].set_ylabel("Probability Density", fontsize=9, fontweight='bold')
    axes[1, 0].legend(fontsize=8, loc='upper right')
    axes[1, 0].grid(True, linestyle='--', alpha=0.5)

    # Plot 2: Salt & Pepper Residual
    bins_sp = np.linspace(-255, 255, 100)
    axes[1, 1].hist(res_sp.ravel(), bins=bins_sp, density=True, color='#ef4444', alpha=0.75, edgecolor='#991b1b', label='Bipolar Residual')
    axes[1, 1].set_title("Salt & Pepper Residual (Bipolar Spikes)", fontsize=10, fontweight='bold', color='#b91c1c')
    axes[1, 1].set_xlabel("Residual Intensity Error (g - f)", fontsize=9, fontweight='bold')
    axes[1, 1].set_ylabel("Probability Density", fontsize=9, fontweight='bold')
    axes[1, 1].set_yscale('log')
    axes[1, 1].grid(True, linestyle='--', alpha=0.5)
    axes[1, 1].text(-240, 1e-2, "Pepper Spikes\n(Drop to 0)", color='#991b1b', fontsize=8.5, fontweight='bold')
    axes[1, 1].text(140, 1e-2, "Salt Spikes\n(Burst to 255)", color='#991b1b', fontsize=8.5, fontweight='bold')

    # Plot 3: Speckle Residual
    bins_spk = np.linspace(-120, 120, 81)
    axes[1, 2].hist(res_speckle.ravel(), bins=bins_spk, density=True, color='#f97316', alpha=0.65, edgecolor='#c2410c', label='Speckle Residual')
    axes[1, 2].set_title("Multiplicative Speckle Distribution", fontsize=10, fontweight='bold', color='#c2410c')
    axes[1, 2].set_xlabel("Residual Intensity Error (g - f)", fontsize=9, fontweight='bold')
    axes[1, 2].set_ylabel("Probability Density", fontsize=9, fontweight='bold')
    axes[1, 2].grid(True, linestyle='--', alpha=0.5)

    fig.suptitle("Task 4.1: Synthetic Noise Modeling & Statistical Probability Density (PDF) Analysis",
                 fontsize=13.5, fontweight='bold', color='#0f172a', y=0.98)

    out_dir_py = os.path.join(exp_dir, "Outputs", "Python")
    fig_dir = os.path.join(exp_dir, "Figures")
    os.makedirs(out_dir_py, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    out_path_1 = os.path.join(out_dir_py, "exp04_task_4_1_noise_models_pdf_py.png")
    out_path_2 = os.path.join(fig_dir, "exp04_task_4_1_noise_models_pdf_py.png")

    plt.savefig(out_path_1, bbox_inches='tight', dpi=300)
    plt.savefig(out_path_2, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"[SUCCESS] Saved figure to:\n  {out_path_1}\n  {out_path_2}")

if __name__ == '__main__':
    run_task_4_1()
