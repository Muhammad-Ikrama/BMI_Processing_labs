"""
Experiment 02 - Example 1: Medical Image Histogram & CDF Computation
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("=" * 70)
    print("EXAMPLE 1: MEDICAL IMAGE HISTOGRAM & CDF COMPUTATION")
    print("=" * 70)

    # 1. Locate and load image
    possible_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'Inputs', 'images', 'Xray.jpg'),
        os.path.join(os.path.dirname(__file__), '..', '..', '..', 'images', 'Xray.jpg'),
        'images/Xray.jpg'
    ]
    img_path = next((p for p in possible_paths if os.path.exists(p)), None)
    if not img_path:
        raise FileNotFoundError("Could not locate Xray.jpg")

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    H, W = img.shape
    total_pixels = H * W

    # 2. Discrete Histogram h(r_k) and Normalized PDF p(r_k)
    hist, bins = np.histogram(img.flatten(), 256, [0, 256])
    pdf = hist / float(total_pixels)

    # 3. Cumulative Distribution Function CDF(r_k)
    cdf = pdf.cumsum()

    # 4. Shannon Information Entropy
    p_nz = pdf[pdf > 0]
    entropy = -np.sum(p_nz * np.log2(p_nz))

    print(f"Image Resolution   : {W} x {H} ({total_pixels:,} pixels)")
    print(f"Dynamic Range      : Min = {img.min()} | Max = {img.max()}")
    print(f"Mean Brightness    : {img.mean():.2f} | Std Dev = {img.std():.2f}")
    print(f"Shannon Entropy    : {entropy:.4f} bits/pixel (Max = 8.0)")
    print(f"CDF Final Sum      : {cdf[-1]:.6f} (Must reach 1.000000)")

    # 5. Visualization
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'Outputs', 'Python')
    fig_dir = os.path.join(os.path.dirname(__file__), '..', 'Figures')
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5), facecolor='#0f172a')
    
    # Panel 1: Image
    axes[0].imshow(img, cmap='gray')
    axes[0].set_title(f"Clinical Chest Radiograph\n{W}x{H} ({total_pixels:,} px)", color='white', fontweight='bold', fontsize=11)
    axes[0].axis('off')

    # Panel 2: Histogram
    axes[1].bar(range(256), hist, color='#38bdf8', width=1.0, edgecolor='none')
    axes[1].set_facecolor('#1e293b')
    axes[1].set_title("Discrete Histogram h(r_k)", color='white', fontweight='bold', fontsize=11)
    axes[1].set_xlabel("Gray Level Intensity r_k", color='#94a3b8')
    axes[1].set_ylabel("Pixel Frequency n_k", color='#94a3b8')
    axes[1].tick_params(colors='#94a3b8')
    axes[1].set_xlim([0, 255])

    # Panel 3: CDF Curve
    axes[2].plot(range(256), cdf, color='#4ade80', linewidth=2.5)
    axes[2].set_facecolor('#1e293b')
    axes[2].set_title("Cumulative Distribution Function (CDF)", color='white', fontweight='bold', fontsize=11)
    axes[2].set_xlabel("Gray Level Intensity r_k", color='#94a3b8')
    axes[2].set_ylabel("Cumulative Probability P(r_k)", color='#94a3b8')
    axes[2].tick_params(colors='#94a3b8')
    axes[2].set_xlim([0, 255])
    axes[2].set_ylim([0, 1.05])
    axes[2].grid(True, color='#334155', linestyle='--', alpha=0.7)

    plt.suptitle("Example 1: Radiograph Intensity Distribution and Cumulative Response", color='#38bdf8', fontsize=13, fontweight='bold')
    plt.tight_layout()

    out_file1 = os.path.join(out_dir, 'example_01_histogram_cdf_python.png')
    out_file2 = os.path.join(fig_dir, 'example_01_histogram_cdf_python.png')
    plt.savefig(out_file1, dpi=200, facecolor=fig.get_facecolor())
    plt.savefig(out_file2, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"[SAVED] Saved plot to {out_file1} and {out_file2}")

if __name__ == '__main__':
    main()
