"""
Experiment 01 - Example 7.1: Loading Medical Image and Inspecting Matrix Properties
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("=" * 70)
    print("EXAMPLE 7.1: LOADING MEDICAL IMAGE & INSPECTING MATRIX PROPERTIES")
    print("=" * 70)

    # 1. Load image (Grayscale)
    image_path = 'images/MRI.jpg'
    if not os.path.exists(image_path):
        image_path = os.path.join('..', 'images', 'MRI.jpg')
    
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not load image from {image_path}")

    # 2. Inspect matrix properties
    height, width = img.shape
    total_pixels = height * width
    dtype = img.dtype
    min_val, max_val = int(img.min()), int(img.max())
    mean_val, std_val = float(img.mean()), float(img.std())

    print(f"Matrix Dimensions (H x W) : ({height}, {width}) Pixels")
    print(f"Data Type / Bit Depth     : {dtype} (8-bit Unsigned Integer, 0 to 255)")
    print(f"Total Number of Pixels    : {total_pixels:,} pixels")
    print(f"Min / Max Intensity       : {min_val} (Pure Black) / {max_val} (Brightest Tissue)")
    print(f"Mean / Std Dev Intensity  : {mean_val:.2f} / {std_val:.2f}")

    # 3. Center Pixel Value
    center_y, center_x = height // 2, width // 2
    center_val = int(img[center_y, center_x])
    print(f"Center Pixel Value (y={center_y}, x={center_x}): {center_val}")

    # 4. Extract 5x5 sub-matrix
    y_start, x_start = min(100, height - 6), min(120, width - 6)
    sub_matrix = img[y_start:y_start+5, x_start:x_start+5]
    print("\nExtracted 5x5 Intensity Sub-Matrix:")
    print(sub_matrix)

    # 5. Visualization
    os.makedirs('outputs', exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(11, 5), facecolor='#0f172a')

    # Full image with ROI box
    axes[0].imshow(img, cmap='gray')
    axes[0].set_title(f"Brain MRI Grayscale ({height}x{width})", color='white', fontsize=12, fontweight='bold')
    axes[0].axis('off')
    
    # Draw rectangle around 5x5 ROI
    rect = plt.Rectangle((x_start-0.5, y_start-0.5), 5, 5, edgecolor='#ef4444', facecolor='none', lw=2)
    axes[0].add_patch(rect)
    axes[0].plot(center_x, center_y, 'y+', markersize=12, markeredgewidth=2, label=f'Center ({center_val})')
    axes[0].legend(loc='upper right', facecolor='#1e293b', edgecolor='#475569', labelcolor='white')

    # Heatmap of 5x5 ROI
    cax = axes[1].imshow(sub_matrix, cmap='magma', vmin=min_val, vmax=max_val)
    axes[1].set_title("5x5 Numerical ROI Intensity Heatmap", color='white', fontsize=12, fontweight='bold')
    axes[1].set_xticks(range(5))
    axes[1].set_yticks(range(5))
    axes[1].set_xticklabels([f"x={x_start+i}" for i in range(5)], color='white', fontsize=8)
    axes[1].set_yticklabels([f"y={y_start+i}" for i in range(5)], color='white', fontsize=8)
    
    # Overlay numerical values
    for i in range(5):
        for j in range(5):
            val = sub_matrix[i, j]
            text_color = "black" if val > 128 else "white"
            axes[1].text(j, i, f"{val}", ha="center", va="center", color=text_color, fontweight='bold', fontsize=9)
    
    cbar = fig.colorbar(cax, ax=axes[1], fraction=0.046, pad=0.04)
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    plt.tight_layout()
    output_path = 'outputs/example_01_matrix_properties_python.png'
    plt.savefig(output_path, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"\n[SAVED] Visualization saved to: {output_path}")

if __name__ == '__main__':
    main()
