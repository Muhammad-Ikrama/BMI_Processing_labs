"""
Experiment 04: Noise Modeling and Removal in Medical Images Using Median and Adaptive Filtering Techniques
Task 4.4: Custom Two-Stage Adaptive Median Filter (AMF) Implementation & High-Density Stress Test [10%, 25%, 40%, 50%]
Course: Medical Image Processing | Riphah International University
Instructor: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

def adaptive_median_filter(im, s_min=3, s_max=9):
    """
    Two-Stage Adaptive Median Filter (AMF) as formulated by Gonzalez & Woods.
    Dynamically expands window from s_min to s_max.
    Stage A: Verify if zmed is clean (zmin < zmed < zmax). If not, increase window size.
    Stage B: Verify if zxy is clean (zmin < zxy < zmax). If clean, keep zxy. If not, output zmed.
    """
    out = im.copy()
    h_im, w_im = im.shape
    pad = s_max // 2
    padded = np.pad(im, pad, mode='reflect')

    for r in range(h_im):
        for c in range(w_im):
            pr, pc = r + pad, c + pad
            k = s_min
            while k <= s_max:
                rad = k // 2
                sub = padded[pr - rad : pr + rad + 1, pc - rad : pc + rad + 1]
                zmin = int(np.min(sub))
                zmax = int(np.max(sub))
                zmed = int(np.median(sub))
                zxy  = int(padded[pr, pc])

                # Stage A: Is the median itself an impulse?
                if zmin < zmed < zmax:
                    # Stage B: Is the center pixel an impulse?
                    if zmin < zxy < zmax:
                        out[r, c] = zxy  # Uncorrupted pixel preserved with 100% fidelity!
                    else:
                        out[r, c] = zmed # Corrupted pixel replaced by median
                    break
                else:
                    k += 2  # Expand filter window

                if k > s_max:
                    out[r, c] = zmed
                    break
    return out

def run_task_4_4():
    print("=" * 70)
    print("EXPERIMENT 04 - TASK 4.4: ADAPTIVE MEDIAN (AMF) HIGH-DENSITY STRESS TEST")
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
    densities = [0.10, 0.25, 0.40, 0.50]
    med3_psnr = []
    med3_ssim = []
    amf_psnr = []
    amf_ssim = []
    amf_images = []
    med3_images = []
    noisy_images = []

    print(f"{'Density':<10} | {'Med 3x3 PSNR':<14} | {'Med 3x3 SSIM':<14} | {'AMF PSNR':<12} | {'AMF SSIM':<10} | {'AMF Advantage'}")
    print("-" * 80)

    for d in densities:
        np.random.seed(42)
        noisy = ref.copy()
        num_corrupt = int(d * ref.size)
        num_salt = num_corrupt // 2
        num_pepper = num_corrupt // 2

        r_idx = np.random.randint(0, H, num_corrupt)
        c_idx = np.random.randint(0, W, num_corrupt)
        noisy[r_idx[:num_salt], c_idx[:num_salt]] = 255
        noisy[r_idx[num_salt:], c_idx[num_salt:]] = 0

        # Standard Median 3x3
        f_med3 = cv2.medianBlur(noisy, 3)
        p_m3 = psnr(ref, f_med3)
        s_m3 = ssim(ref, f_med3)

        # Adaptive Median AMF (3 to 9)
        f_amf = adaptive_median_filter(noisy, s_min=3, s_max=9)
        p_amf = psnr(ref, f_amf)
        s_amf = ssim(ref, f_amf)

        med3_psnr.append(p_m3)
        med3_ssim.append(s_m3)
        amf_psnr.append(p_amf)
        amf_ssim.append(s_amf)
        noisy_images.append(noisy)
        med3_images.append(f_med3)
        amf_images.append(f_amf)

        gain_psnr = p_amf - p_m3
        print(f"{int(d*100)}% noise   | {p_m3:<14.2f} | {s_m3:<14.4f} | {p_amf:<12.2f} | {s_amf:<10.4f} | +{gain_psnr:.2f} dB gain")

    print("-" * 80)
    print("Conclusion: At high noise densities (40%-50%), standard 3x3 median fails completely")
    print("because impulses form dense clusters that dominate the 3x3 window. AMF dynamically")
    print("expands up to 9x9, successfully identifying clean medians and restoring diagnostic anatomy.")

    # Visualization: 2 Rows x 4 Columns
    # Row 1: Standard Median 3x3 outputs across [10%, 25%, 40%, 50%]
    # Row 2: Adaptive Median Filter (AMF) outputs across [10%, 25%, 40%, 50%]
    fig, axes = plt.subplots(2, 4, figsize=(16, 8.5), dpi=300)
    plt.subplots_adjust(wspace=0.12, hspace=0.22)

    for col_idx, d in enumerate(densities):
        # Row 1: Standard Median 3x3
        ax_top = axes[0, col_idx]
        ax_top.imshow(med3_images[col_idx], cmap='gray', vmin=0, vmax=255)
        ax_top.set_title(f"Standard Med 3x3 ({int(d*100)}% Noise)\nPSNR: {med3_psnr[col_idx]:.2f} dB | SSIM: {med3_ssim[col_idx]:.4f}",
                         fontsize=9, fontweight='bold', color='#dc2626' if d >= 0.40 else '#334155')
        ax_top.axis('off')

        # Row 2: Adaptive Median AMF
        ax_bot = axes[1, col_idx]
        ax_bot.imshow(amf_images[col_idx], cmap='gray', vmin=0, vmax=255)
        ax_bot.set_title(f"Adaptive AMF ({int(d*100)}% Noise)\nPSNR: {amf_psnr[col_idx]:.2f} dB | SSIM: {amf_ssim[col_idx]:.4f}",
                         fontsize=9, fontweight='bold', color='#15803d')
        ax_bot.axis('off')

    fig.suptitle("Task 4.4: Custom Two-Stage Adaptive Median Filter (AMF) High-Density Stress Test (10% to 50%)",
                 fontsize=13.5, fontweight='bold', color='#0f172a', y=0.98)

    out_dir_py = os.path.join(exp_dir, "Outputs", "Python")
    fig_dir = os.path.join(exp_dir, "Figures")
    os.makedirs(out_dir_py, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    out_path_1 = os.path.join(out_dir_py, "exp04_task_4_4_adaptive_median_stress_py.png")
    out_path_2 = os.path.join(fig_dir, "exp04_task_4_4_adaptive_median_stress_py.png")

    plt.savefig(out_path_1, bbox_inches='tight', dpi=300)
    plt.savefig(out_path_2, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"[SUCCESS] Saved figure to:\n  {out_path_1}\n  {out_path_2}")

if __name__ == '__main__':
    run_task_4_4()
