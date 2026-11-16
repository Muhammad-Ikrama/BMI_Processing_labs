"""
Experiment 02 - Task 2.2: Dual-Axis Histogram and Cumulative Distribution Function (CDF) Curve
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

Task Requirement:
Calculate empirical Cumulative Distribution Function CDF(r_k).
Generate publication-quality figure:
  - Left panel: Medical scan.
  - Right panel: Dual-axis plot (Histogram bars on left Y-axis, CDF curve [0.0 to 1.0] on right Y-axis).
Identify the steepest slope segment on the CDF curve and correlate with anatomical tissue volume.
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("=" * 70)
    print("TASK 2.2: DUAL-AXIS HISTOGRAM & CUMULATIVE DISTRIBUTION FUNCTION (CDF)")
    print("=" * 70)

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

    # Compute histogram and normalized PDF
    hist, bins = np.histogram(img.flatten(), 256, [0, 256])
    pdf = hist / float(total_pixels)
    cdf = pdf.cumsum()

    # Find the steepest slope segment in the CDF
    # d(CDF)/dr is directly proportional to histogram count h(r_k)
    max_slope_intensity = int(np.argmax(hist))
    max_slope_count = int(hist[max_slope_intensity])
    max_slope_prob = float(pdf[max_slope_intensity])

    # Find the 10-intensity range with highest accumulated slope
    window = 10
    slope_accum = [np.sum(hist[k:k+window]) for k in range(256 - window)]
    best_start = int(np.argmax(slope_accum))
    best_range = (best_start, best_start + window)

    print(f"Max CDF Derivative Intensity: r_k = {max_slope_intensity} (Count = {max_slope_count:,}, PDF = {max_slope_prob:.4f})")
    print(f"Steepest 10-bin Slope Window : Gray levels [{best_range[0]} to {best_range[1]}]")
    print(f"Anatomical Tissue Origin     : Dense soft-tissue and thoracic mediastinum/rib overlap")

    # Plotting
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'Outputs', 'Python')
    fig_dir = os.path.join(os.path.dirname(__file__), '..', 'Figures')
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(15, 6), facecolor='#0f172a')

    # Left: Medical Radiograph
    axes[0].imshow(img, cmap='gray')
    axes[0].set_title(f"Clinical Chest Radiograph (Xray.jpg)\nResolution: {W} x {H} | Dynamic Range: [{img.min()}, {img.max()}]",
                      color='white', fontweight='bold', fontsize=12)
    axes[0].axis('off')

    # Right: Dual-Axis Plot
    ax1 = axes[1]
    ax1.set_facecolor('#1e293b')

    # Primary Axis (Histogram bars)
    color_bar = '#38bdf8'
    bars = ax1.bar(range(256), hist, color=color_bar, alpha=0.75, width=1.0, edgecolor='none', label='Histogram h(r_k)')
    ax1.set_xlabel('Gray Level Intensity r_k (0 to 255)', color='#94a3b8', fontsize=11)
    ax1.set_ylabel('Pixel Frequency Count (n_k)', color=color_bar, fontsize=11)
    ax1.tick_params(axis='y', labelcolor=color_bar)
    ax1.tick_params(axis='x', colors='#94a3b8')
    ax1.set_xlim([0, 255])

    # Secondary Axis (CDF curve)
    ax2 = ax1.twinx()
    color_cdf = '#4ade80'
    line = ax2.plot(range(256), cdf, color=color_cdf, linewidth=2.8, label='Cumulative Distribution (CDF)')
    ax2.set_ylabel('Cumulative Probability P(r_k)', color=color_cdf, fontsize=11)
    ax2.tick_params(axis='y', labelcolor=color_cdf)
    ax2.set_ylim([0, 1.05])

    # Highlight steepest slope point
    ax2.plot(max_slope_intensity, cdf[max_slope_intensity], 'ro', markersize=8, label=f'Steepest Slope (r={max_slope_intensity})')
    ax2.annotate(f'Steepest Slope: r={max_slope_intensity}\n(Anatomical Peak)',
                 xy=(max_slope_intensity, cdf[max_slope_intensity]),
                 xytext=(max_slope_intensity - 70, cdf[max_slope_intensity] + 0.15),
                 color='#f87171', fontsize=9, fontweight='bold',
                 arrowprops=dict(facecolor='#f87171', shrink=0.08, width=1.5, headwidth=6))

    ax1.set_title("Dual-Axis Intensity Histogram and Empirical CDF Curve", color='white', fontweight='bold', fontsize=12)
    ax1.grid(True, color='#334155', linestyle='--', alpha=0.5)

    plt.suptitle("Task 2.2: Dual-Axis Histogram Analysis and CDF Slope Identification", color='#38bdf8', fontsize=14, fontweight='bold')
    plt.tight_layout()

    out_file1 = os.path.join(out_dir, 'task_2_2_dual_axis_cdf_python.png')
    out_file2 = os.path.join(fig_dir, 'task_2_2_dual_axis_cdf_python.png')
    plt.savefig(out_file1, dpi=200, facecolor=fig.get_facecolor())
    plt.savefig(out_file2, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"[SAVED] Generated Task 2.2 figures:\n  {out_file1}\n  {out_file2}")

if __name__ == '__main__':
    main()
