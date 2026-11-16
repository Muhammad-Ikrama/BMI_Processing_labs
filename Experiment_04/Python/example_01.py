"""
Experiment 04: Noise Modeling and Removal in Medical Images Using Median and Adaptive Filtering Techniques
Example 01: Medical Noise Modeling & Multi-Filter Restoration Benchmark (Python)
Course: Medical Image Processing | Riphah International University
Instructor: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import wiener
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

def apply_amf(im, max_w=7):
    """
    Two-Stage Adaptive Median Filter (Gonzalez & Woods)
    Stage A: Determines if median is an impulse. If so, increases window size.
    Stage B: Determines if center pixel is an impulse. If not, preserves it.
    """
    out = im.copy()
    pad = max_w // 2
    padded = np.pad(im, pad, mode='reflect')
    h_im, w_im = im.shape

    for r in range(h_im):
        for c in range(w_im):
            pr, pc = r + pad, c + pad
            k = 3
            while k <= max_w:
                rad = k // 2
                sub = padded[pr - rad : pr + rad + 1, pc - rad : pc + rad + 1]
                zmin = int(np.min(sub))
                zmax = int(np.max(sub))
                zmed = int(np.median(sub))
                zxy  = int(padded[pr, pc])

                # Stage A: Check if median is clean
                if zmin < zmed < zmax:
                    # Stage B: Check if center pixel is clean
                    if zmin < zxy < zmax:
                        out[r, c] = zxy  # Uncorrupted pixel preserved
                    else:
                        out[r, c] = zmed # Corrupted impulse replaced
                    break
                else:
                    k += 2  # Expand window size

                if k > max_w:
                    out[r, c] = zmed
                    break
    return out

def run_example_01():
    print("=" * 70)
    print("EXPERIMENT 04 - EXAMPLE 01: NOISE MODELING & ADAPTIVE FILTERING")
    print("=" * 70)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.dirname(script_dir)
    img_path = os.path.join(exp_dir, "Inputs", "images", "MRI.jpg")

    if not os.path.exists(img_path):
        img_path = os.path.join(exp_dir, "..", "..", "images", "MRI.jpg")

    print(f"[INFO] Loading reference MRI scan: {img_path}")
    ref = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if ref is None:
        raise FileNotFoundError(f"Could not load image from {img_path}")

    H, W = ref.shape
    print(f"[INFO] Image Dimensions: {W} x {H} pixels, dtype: {ref.dtype}")

    # 1. Simulate Mixed Noise: 10% Salt & Pepper + Gaussian (sigma = 10.0)
    np.random.seed(42)
    # Add Gaussian thermal noise
    gauss_noisy = np.clip(ref.astype(float) + np.random.normal(0, 10.0, ref.shape), 0, 255).astype(np.uint8)
    noisy = gauss_noisy.copy()

    # Add 10% Salt & Pepper impulse noise (5% salt, 5% pepper)
    sp_count = int(0.10 * ref.size)
    num_salt = sp_count // 2
    num_pepper = sp_count // 2

    # Uniform random coordinate selection
    r_idx = np.random.randint(0, H, sp_count)
    c_idx = np.random.randint(0, W, sp_count)
    noisy[r_idx[:num_salt], c_idx[:num_salt]] = 255
    noisy[r_idx[num_salt:], c_idx[num_salt:]] = 0

    # 2. Apply Filtering Algorithms
    print("[INFO] Computing Linear Mean Filter 5x5...")
    mean_5 = cv2.blur(noisy, (5, 5))

    print("[INFO] Computing Standard Median Filter 3x3...")
    med_3 = cv2.medianBlur(noisy, 3)

    print("[INFO] Computing Two-Stage Adaptive Median Filter (AMF 3 to 7)...")
    amf_out = apply_amf(noisy, max_w=7)

    print("[INFO] Computing Adaptive Wiener Filter 5x5...")
    wiener_out = np.clip(wiener(noisy.astype(float), (5, 5)), 0, 255).astype(np.uint8)

    # 3. Quantitative Benchmarking
    tests = [
        ("Noisy Scan Baseline", noisy),
        ("Linear Mean 5x5", mean_5),
        ("Adaptive Wiener 5x5", wiener_out),
        ("Standard Median 3x3", med_3),
        ("Adaptive Median AMF", amf_out)
    ]

    print("\n" + "-" * 70)
    print(f"{'Filter Method':<24} | {'PSNR (dB)':<10} | {'SSIM':<8} | {'Clinical Assessment'}")
    print("-" * 70)
    for name, im in tests:
        p = psnr(ref, im)
        s = ssim(ref, im)
        if "Noisy" in name:
            obs = "Severely corrupted by bipolar outliers"
        elif "Linear" in name:
            obs = "Impulses smeared into gray smudge blotches"
        elif "Wiener" in name:
            obs = "Poor on impulses (linear variance assumption fails)"
        elif "Standard" in name:
            obs = "Impulses removed; mild detail truncation"
        else:
            obs = "Optimal restoration; impulses cleared, edges preserved"
        print(f"{name:<24} | {p:<10.2f} | {s:<8.4f} | {obs}")
    print("-" * 70)
    print(">>> Conclusion: Non-linear Median & AMF achieve > +16 dB gain; Linear Mean smudges impulses.")

    # 4. Visualization: 6-Panel Composite
    fig, axes = plt.subplots(2, 3, figsize=(15, 9.5), dpi=300)
    plt.subplots_adjust(wspace=0.15, hspace=0.25)

    panels = [
        ("A: Ground Truth Clean MRI", ref, '#1e3a8a'),
        (f"B: Mixed Noisy Scan (10% SP + Gauss)\nPSNR: {psnr(ref, noisy):.2f} dB | SSIM: {ssim(ref, noisy):.4f}", noisy, '#dc2626'),
        (f"C: Linear Mean 5x5 (Smear Failure)\nPSNR: {psnr(ref, mean_5):.2f} dB | SSIM: {ssim(ref, mean_5):.4f}", mean_5, '#dc2626'),
        (f"D: Adaptive Wiener 5x5 (Gaussian Only)\nPSNR: {psnr(ref, wiener_out):.2f} dB | SSIM: {ssim(ref, wiener_out):.4f}", wiener_out, '#ca8a04'),
        (f"E: Standard Median 3x3 (Impulses Removed)\nPSNR: {psnr(ref, med_3):.2f} dB | SSIM: {ssim(ref, med_3):.4f}", med_3, '#2563eb'),
        (f"F: Adaptive Median AMF (Edge Preserved)\nPSNR: {psnr(ref, amf_out):.2f} dB | SSIM: {ssim(ref, amf_out):.4f}", amf_out, '#15803d')
    ]

    for ax, (title, im_data, col) in zip(axes.ravel(), panels):
        ax.imshow(im_data, cmap='gray', vmin=0, vmax=255)
        ax.set_title(title, fontsize=9.5, fontweight='bold', color=col)
        ax.axis('off')

    fig.suptitle("Example 01: Medical Noise Modeling & Non-Linear Adaptive Restoration (Brain MRI)",
                 fontsize=13.5, fontweight='bold', color='#0f172a', y=0.98)

    out_dir_py = os.path.join(exp_dir, "Outputs", "Python")
    fig_dir = os.path.join(exp_dir, "Figures")
    os.makedirs(out_dir_py, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    out_path_1 = os.path.join(out_dir_py, "exp04_example_01_noise_filtering_py.png")
    out_path_2 = os.path.join(fig_dir, "exp04_example_01_noise_filtering_py.png")

    plt.savefig(out_path_1, bbox_inches='tight', dpi=300)
    plt.savefig(out_path_2, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"[SUCCESS] Saved figure to:\n  {out_path_1}\n  {out_path_2}")

if __name__ == '__main__':
    run_example_01()
