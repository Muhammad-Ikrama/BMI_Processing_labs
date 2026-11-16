"""
Experiment 01 - Example 7.2: RGB Color Decomposition and Perceptual Luminance Conversion
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("=" * 70)
    print("EXAMPLE 7.2: RGB DECOMPOSITION & PERCEPTUAL LUMINANCE CONVERSION")
    print("=" * 70)

    # 1. Load color image
    image_path = 'images/PET.jpg'
    if not os.path.exists(image_path):
        image_path = os.path.join('..', 'images', 'PET.jpg')
    
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        raise FileNotFoundError(f"Could not load image from {image_path}")
    
    # Convert BGR (OpenCV default) to RGB
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    height, width, channels = img_rgb.shape
    print(f"Loaded Color Image Shape: ({height}, {width}, {channels}) [Height, Width, Channels]")

    # 2. Decompose into individual R, G, B planes as float64
    R = img_rgb[:, :, 0].astype(np.float64)
    G = img_rgb[:, :, 1].astype(np.float64)
    B = img_rgb[:, :, 2].astype(np.float64)

    print(f"Red Channel (R)   : Mean = {R.mean():.2f}, Dynamic Range = [{R.min():.0f}, {R.max():.0f}]")
    print(f"Green Channel (G) : Mean = {G.mean():.2f}, Dynamic Range = [{G.min():.0f}, {G.max():.0f}]")
    print(f"Blue Channel (B)  : Mean = {B.mean():.2f}, Dynamic Range = [{B.min():.0f}, {B.max():.0f}]")

    # 3. Human Perceptual Luminance (ITU-R BT.601 standard)
    gray_perceptual = np.clip(0.299 * R + 0.587 * G + 0.114 * B, 0, 255).astype(np.uint8)

    # 4. Simple unweighted arithmetic average
    gray_unweighted = np.clip((R + G + B) / 3.0, 0, 255).astype(np.uint8)

    # 5. Difference metrics
    diff_matrix = np.abs(gray_perceptual.astype(np.float64) - gray_unweighted.astype(np.float64))
    max_diff = diff_matrix.max()
    mean_diff = diff_matrix.mean()

    print(f"\nPerceptual Grayscale Shape: {gray_perceptual.shape} [1-Channel 2D Matrix]")
    print(f"Max Intensity Discrepancy (Perceptual vs Unweighted): {max_diff:.2f} intensity levels")
    print(f"Mean Absolute Difference: {mean_diff:.2f} levels (Confirms perceptual contrast preservation)")

    # 6. Visualization
    os.makedirs('outputs', exist_ok=True)
    fig, axes = plt.subplots(2, 3, figsize=(14, 8), facecolor='#0f172a')
    
    # [Row 1] Original RGB and Individual Planes
    axes[0, 0].imshow(img_rgb)
    axes[0, 0].set_title("Original RGB Composite", color='white', fontweight='bold', fontsize=11)
    axes[0, 0].axis('off')

    axes[0, 1].imshow(R.astype(np.uint8), cmap='Reds_r')
    axes[0, 1].set_title(f"Red Channel (Weight: 29.9%)\nMean: {R.mean():.1f}", color='#f87171', fontweight='bold', fontsize=10)
    axes[0, 1].axis('off')

    axes[0, 2].imshow(G.astype(np.uint8), cmap='Greens_r')
    axes[0, 2].set_title(f"Green Channel (Weight: 58.7%)\nMean: {G.mean():.1f}", color='#4ade80', fontweight='bold', fontsize=10)
    axes[0, 2].axis('off')

    # [Row 2] Blue channel, Perceptual Gray, and Difference Map
    axes[1, 0].imshow(B.astype(np.uint8), cmap='Blues_r')
    axes[1, 0].set_title(f"Blue Channel (Weight: 11.4%)\nMean: {B.mean():.1f}", color='#60a5fa', fontweight='bold', fontsize=10)
    axes[1, 0].axis('off')

    axes[1, 1].imshow(gray_perceptual, cmap='gray')
    axes[1, 1].set_title("Human Perceptual Grayscale\n(0.299*R + 0.587*G + 0.114*B)", color='#38bdf8', fontweight='bold', fontsize=10)
    axes[1, 1].axis('off')

    diff_cax = axes[1, 2].imshow(diff_matrix, cmap='turbo')
    axes[1, 2].set_title(f"Absolute Difference Map\nMax: {max_diff:.1f} | Mean: {mean_diff:.2f}", color='#fbbf24', fontweight='bold', fontsize=10)
    axes[1, 2].axis('off')
    cbar = fig.colorbar(diff_cax, ax=axes[1, 2], fraction=0.046, pad=0.04)
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    plt.suptitle("RGB Decomposition and Human Perceptual Luminance Analysis", color='#e2e8f0', fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    output_path = 'outputs/example_02_rgb_luminance_python.png'
    plt.savefig(output_path, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"\n[SAVED] Visualization saved to: {output_path}")

if __name__ == '__main__':
    main()
