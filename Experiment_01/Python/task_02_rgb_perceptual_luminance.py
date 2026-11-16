"""
Experiment 01 - Task 2: RGB Color Plane Extraction & Perceptual Luminance Computation
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

Task Requirement:
Load a 3-channel color medical image ('images/PET.jpg').
Separate into individual 2D matrices: Red (R), Green (G), and Blue (B).
Implement manual Human Perceptual Luminance equation: Y = 0.299*R + 0.587*G + 0.114*B
Compare its visual contrast against simple unweighted arithmetic average: Y_unweighted = (R+G+B)/3
Quantify the maximum absolute intensity difference and statistical distribution between both methods.
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("=" * 75)
    print("STUDENT LAB TASK 2: RGB DECOMPOSITION & PERCEPTUAL LUMINANCE CONVERSION")
    print("=" * 75)

    # 1. Load 3-channel color image
    img_path = 'images/PET.jpg' if os.path.exists('images/PET.jpg') else '../images/PET.jpg'
    img_bgr = cv2.imread(img_path)
    if img_bgr is None:
        raise FileNotFoundError(f"Cannot load image from {img_path}")
    
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    height, width, channels = img_rgb.shape

    print(f"Loaded Medical Image: {img_path}")
    print(f"Matrix Dimensions: {height} Rows x {width} Columns x {channels} Color Channels")

    # 2. Extract 2D color planes
    R = img_rgb[:, :, 0].astype(np.float64)
    G = img_rgb[:, :, 1].astype(np.float64)
    B = img_rgb[:, :, 2].astype(np.float64)

    print(f"\nColor Plane Statistics:")
    print(f"  Red Channel (R)   : Mean = {R.mean():.2f}, Range = [{R.min():.0f}, {R.max():.0f}], Std = {R.std():.2f}")
    print(f"  Green Channel (G) : Mean = {G.mean():.2f}, Range = [{G.min():.0f}, {G.max():.0f}], Std = {G.std():.2f}")
    print(f"  Blue Channel (B)  : Mean = {B.mean():.2f}, Range = [{B.min():.0f}, {B.max():.0f}], Std = {B.std():.2f}")

    # 3. Compute Perceptual Luminance (ITU-R BT.601) vs Unweighted Average
    # Formula: Y = 0.299*R + 0.587*G + 0.114*B
    gray_perceptual_float = 0.299 * R + 0.587 * G + 0.114 * B
    gray_perceptual = np.clip(np.round(gray_perceptual_float), 0, 255).astype(np.uint8)

    # Formula: Y = (R + G + B) / 3.0
    gray_unweighted_float = (R + G + B) / 3.0
    gray_unweighted = np.clip(np.round(gray_unweighted_float), 0, 255).astype(np.uint8)

    # Built-in OpenCV conversion for benchmark comparison
    gray_opencv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # 4. Error and Difference Metrics
    abs_diff = np.abs(gray_perceptual.astype(np.float64) - gray_unweighted.astype(np.float64))
    max_diff = float(abs_diff.max())
    mean_diff = float(abs_diff.mean())
    std_diff = float(abs_diff.std())

    # Comparison with OpenCV's internal implementation
    diff_with_opencv = np.abs(gray_perceptual.astype(np.float64) - gray_opencv.astype(np.float64))
    max_opencv_diff = float(diff_with_opencv.max())

    print(f"\n--- LUMINANCE COMPARISON & ERROR METRICS ---")
    print(f"  Perceptual Grayscale Mean Intensity   : {gray_perceptual.mean():.2f}")
    print(f"  Unweighted Average Mean Intensity     : {gray_unweighted.mean():.2f}")
    print(f"  Maximum Absolute Intensity Discrepancy: {max_diff:.2f} grayscale levels")
    print(f"  Mean Absolute Difference (MAD)        : {mean_diff:.2f} levels")
    print(f"  Standard Deviation of Discrepancy     : {std_diff:.2f} levels")
    print(f"  Discrepancy with OpenCV Builtin       : {max_opencv_diff:.2f} levels (Perfect Match <= 1 level rounding)")

    # 5. Publication-grade Visualization
    os.makedirs('outputs', exist_ok=True)
    fig = plt.figure(figsize=(15, 9), facecolor='#0f172a')

    # Grid layout: 2 rows x 3 columns
    gs = fig.add_gridspec(2, 3, hspace=0.28, wspace=0.2)

    # 1. Original RGB
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.imshow(img_rgb)
    ax1.set_title("1. Original RGB Composite (PET)", color='white', fontweight='bold', fontsize=10)
    ax1.axis('off')

    # 2. Red Plane
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.imshow(R.astype(np.uint8), cmap='Reds_r')
    ax2.set_title(f"2. Red Plane (R: 29.9%)\nMean: {R.mean():.1f}", color='#f87171', fontweight='bold', fontsize=9.5)
    ax2.axis('off')

    # 3. Green Plane
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.imshow(G.astype(np.uint8), cmap='Greens_r')
    ax3.set_title(f"3. Green Plane (G: 58.7%)\nMean: {G.mean():.1f}", color='#4ade80', fontweight='bold', fontsize=9.5)
    ax3.axis('off')

    # 4. Blue Plane
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.imshow(B.astype(np.uint8), cmap='Blues_r')
    ax4.set_title(f"4. Blue Plane (B: 11.4%)\nMean: {B.mean():.1f}", color='#60a5fa', fontweight='bold', fontsize=9.5)
    ax4.axis('off')

    # 5. Perceptual Grayscale vs Unweighted comparison
    ax5 = fig.add_subplot(gs[1, 1])
    ax5.imshow(gray_perceptual, cmap='gray')
    ax5.set_title("5. Human Perceptual Grayscale (Y)\n0.299*R + 0.587*G + 0.114*B", color='#38bdf8', fontweight='bold', fontsize=9.5)
    ax5.axis('off')

    # 6. Discrepancy Heatmap
    ax6 = fig.add_subplot(gs[1, 2])
    cax = ax6.imshow(abs_diff, cmap='turbo')
    ax6.set_title(f"6. Discrepancy Map (|Perceptual - Unweighted|)\nMax Diff = {max_diff:.1f} | MAD = {mean_diff:.2f}", color='#fbbf24', fontweight='bold', fontsize=9.5)
    ax6.axis('off')
    cbar = fig.colorbar(cax, ax=ax6, fraction=0.046, pad=0.04)
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    plt.suptitle("Task 2: RGB Decomposition and Mathematical Human Perceptual Luminance Verification",
                 color='#e2e8f0', fontsize=13, fontweight='bold', y=0.98)
    
    out_path = 'outputs/task_02_rgb_perceptual_luminance_python.png'
    plt.savefig(out_path, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"\n[SAVED] Task 2 Output saved to: {out_path}")

if __name__ == '__main__':
    main()
