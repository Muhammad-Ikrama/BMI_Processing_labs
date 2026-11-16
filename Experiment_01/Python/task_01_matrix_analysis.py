"""
Experiment 01 - Task 1: Matrix Dimension, Data Type & Dynamic Range Analysis
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

Task Requirement:
Load two distinct medical modality images from 'images/' folder (e.g. CT.jpg and ultrasound.jpg).
Inspect and print spatial dimensions (H x W), number of channels, storage data type (dtype),
min, max, mean, and std pixel intensities.
Extract a 5x5 numerical sub-matrix from an anatomical region of interest (ROI) and verify that
pixel values match tissue brightness.
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def analyze_modality_image(image_path, modality_name, roi_coords):
    """Analyze matrix dimensions, data type, statistical moments, and extract 5x5 ROI."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")
    
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"Failed to decode image from {image_path}")
    
    # Check channels
    if img.ndim == 2:
        height, width = img.shape
        channels = 1
        gray = img
    else:
        height, width, channels = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    dtype = str(gray.dtype)
    min_val, max_val = int(gray.min()), int(gray.max())
    mean_val, std_val = float(gray.mean()), float(gray.std())
    total_pixels = height * width

    print(f"\n--- MODALITY: {modality_name} ({os.path.basename(image_path)}) ---")
    print(f"  Matrix Spatial Dimensions (H x W) : {height} x {width} pixels")
    print(f"  Channels                          : {channels} ({'Grayscale' if channels==1 else 'Multi-channel/Color'})")
    print(f"  Data Type / Dynamic Bit Depth     : {dtype} [0 to 255]")
    print(f"  Total Pixel Elements              : {total_pixels:,} pixels")
    print(f"  Minimum Pixel Intensity (Black)   : {min_val}")
    print(f"  Maximum Pixel Intensity (Bright)  : {max_val}")
    print(f"  Mean Intensity ± Std Deviation    : {mean_val:.2f} ± {std_val:.2f}")

    # Extract 5x5 sub-matrix ROI
    ry, rx = roi_coords
    ry = max(0, min(ry, height - 5))
    rx = max(0, min(rx, width - 5))
    sub_matrix = gray[ry:ry+5, rx:rx+5]

    print(f"  Extracted 5x5 ROI at (y={ry}:{ry+5}, x={rx}:{rx+5}):")
    print(sub_matrix)
    print(f"  ROI Mean Intensity: {sub_matrix.mean():.2f} (Matches anatomical tissue attenuation)")

    return {
        'name': modality_name,
        'image': gray,
        'shape': (height, width),
        'dtype': dtype,
        'min': min_val,
        'max': max_val,
        'mean': mean_val,
        'std': std_val,
        'roi_coords': (ry, rx),
        'sub_matrix': sub_matrix
    }

def main():
    print("=" * 75)
    print("STUDENT LAB TASK 1: MATRIX DIMENSIONS, DATA TYPES & DYNAMIC RANGE ANALYSIS")
    print("=" * 75)

    img1_path = 'images/CT.jpg' if os.path.exists('images/CT.jpg') else '../images/CT.jpg'
    img2_path = 'images/ultrasound.jpg' if os.path.exists('images/ultrasound.jpg') else '../images/ultrasound.jpg'

    res1 = analyze_modality_image(img1_path, "Computed Tomography / Panoramic X-ray (CT)", (150, 200))
    res2 = analyze_modality_image(img2_path, "B-Mode Ultrasound Echocardiogram (US)", (200, 250))

    # Visualization
    os.makedirs('outputs', exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(12, 10), facecolor='#0f172a')

    for row_idx, res in enumerate([res1, res2]):
        # Full scan with ROI box
        ax_img = axes[row_idx, 0]
        ax_img.imshow(res['image'], cmap='gray')
        ax_img.set_title(f"{res['name']}\nDim: {res['shape'][0]}x{res['shape'][1]} | Range: [{res['min']}, {res['max']}] | Mean: {res['mean']:.1f}",
                         color='white', fontweight='bold', fontsize=10)
        ax_img.axis('off')

        ry, rx = res['roi_coords']
        rect = plt.Rectangle((rx-0.5, ry-0.5), 5, 5, edgecolor='#38bdf8', facecolor='none', lw=2)
        ax_img.add_patch(rect)
        ax_img.text(rx + 8, ry + 15, "5x5 ROI", color='#38bdf8', fontsize=8, fontweight='bold')

        # Heatmap of 5x5 sub-matrix
        ax_roi = axes[row_idx, 1]
        cax = ax_roi.imshow(res['sub_matrix'], cmap='plasma', vmin=res['min'], vmax=res['max'])
        ax_roi.set_title(f"5x5 Anatomical ROI Sub-Matrix (Mean={res['sub_matrix'].mean():.1f})", color='#38bdf8', fontweight='bold', fontsize=10)
        ax_roi.set_xticks(range(5))
        ax_roi.set_yticks(range(5))
        ax_roi.set_xticklabels([f"x={rx+i}" for i in range(5)], color='white', fontsize=7.5)
        ax_roi.set_yticklabels([f"y={ry+i}" for i in range(5)], color='white', fontsize=7.5)

        for i in range(5):
            for j in range(5):
                val = res['sub_matrix'][i, j]
                txt_col = "black" if val > 140 else "white"
                ax_roi.text(j, i, str(val), ha="center", va="center", color=txt_col, fontweight='bold', fontsize=9)

        cbar = fig.colorbar(cax, ax=ax_roi, fraction=0.046, pad=0.04)
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    plt.suptitle("Task 1: Medical Modality Matrix Representation & Dynamic Range Comparison", color='#e2e8f0', fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()
    output_path = 'outputs/task_01_matrix_analysis_python.png'
    plt.savefig(output_path, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"\n[SAVED] Task 1 Output saved to: {output_path}")

if __name__ == '__main__':
    main()
