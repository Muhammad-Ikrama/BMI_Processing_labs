"""
Experiment 02 - Task 2.1: Manual Discrete Histogram and Empirical PDF Computation
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

Task Requirement:
Compute the discrete histogram h(r_k) and normalized empirical PDF p(r_k) using primitive
nested loops and array indexing (WITHOUT calling np.histogram or cv2.calcHist).
Verify:
  1. sum(h(r_k)) == M x N
  2. sum(p(r_k)) == 1.000000
Plot the resulting histogram with annotated axis labels and gray-level range.
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def manual_histogram_and_pdf(img):
    """
    Primitive manual histogram computation using 2D nested loops.
    No high-level library functions utilized.
    """
    H, W = img.shape
    total_pixels = H * W
    
    # 256-element integer accumulator
    hist = np.zeros(256, dtype=np.int64)
    
    # Primitive loop traversal
    for r in range(H):
        for c in range(W):
            intensity = int(img[r, c])
            hist[intensity] += 1
            
    # Empirical PDF
    pdf = np.zeros(256, dtype=np.float64)
    for k in range(256):
        pdf[k] = hist[k] / float(total_pixels)
        
    return hist, pdf

def main():
    print("=" * 70)
    print("TASK 2.1: MANUAL DISCRETE HISTOGRAM & EMPIRICAL PDF COMPUTATION")
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

    # Compute manually
    hist_manual, pdf_manual = manual_histogram_and_pdf(img)

    # Verification checks
    sum_hist = int(np.sum(hist_manual))
    sum_pdf = float(np.sum(pdf_manual))

    print(f"Loaded Image       : {os.path.basename(img_path)} ({W} x {H} pixels)")
    print(f"Total Pixel Count  : {total_pixels:,}")
    print(f"Histogram Sum      : {sum_hist:,} -> {'VERIFIED [MATCH]' if sum_hist == total_pixels else 'MISMATCH'}")
    print(f"Empirical PDF Sum  : {sum_pdf:.6f} -> {'VERIFIED [EXACT 1.000000]' if abs(sum_pdf - 1.0) < 1e-9 else 'MISMATCH'}")
    
    # Compute moments
    mean_val = float(np.sum([k * pdf_manual[k] for k in range(256)]))
    var_val = float(np.sum([((k - mean_val) ** 2) * pdf_manual[k] for k in range(256)]))
    std_val = float(np.sqrt(var_val))

    print(f"Theoretical Mean   : {mean_val:.2f} (NumPy img.mean() = {img.mean():.2f})")
    print(f"Theoretical Std Dev: {std_val:.2f} (NumPy img.std()  = {img.std():.2f})")

    # Plotting
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'Outputs', 'Python')
    fig_dir = os.path.join(os.path.dirname(__file__), '..', 'Figures')
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor='#0f172a')

    # Panel 1: Medical Scan
    axes[0].imshow(img, cmap='gray')
    axes[0].set_title(f"Input Radiograph: Xray.jpg\n{W}x{H} ({total_pixels:,} pixels)", color='white', fontweight='bold', fontsize=12)
    axes[0].axis('off')

    # Panel 2: Manual Histogram with PDF Overlay
    axes[1].bar(range(256), hist_manual, color='#38bdf8', width=1.0, edgecolor='none', label='Discrete Histogram h(r_k)')
    axes[1].set_facecolor('#1e293b')
    axes[1].set_title(f"Manual Histogram & PDF (Sum={sum_hist:,}, PDF Sum={sum_pdf:.6f})", color='white', fontweight='bold', fontsize=12)
    axes[1].set_xlabel("Gray Level Intensity r_k (0 to 255)", color='#94a3b8', fontsize=11)
    axes[1].set_ylabel("Pixel Frequency n_k", color='#94a3b8', fontsize=11)
    axes[1].tick_params(colors='#94a3b8')
    axes[1].set_xlim([0, 255])
    axes[1].grid(True, color='#334155', linestyle='--', alpha=0.5)

    # Annotated Statistics box
    stats_text = (
        f"M x N = {total_pixels:,}\n"
        f"Sum h(r_k) = {sum_hist:,}\n"
        f"Sum p(r_k) = {sum_pdf:.6f}\n"
        f"Mean = {mean_val:.2f}\n"
        f"Std Dev = {std_val:.2f}"
    )
    axes[1].text(0.04, 0.95, stats_text, transform=axes[1].transAxes,
                 verticalalignment='top', fontsize=10, color='#fde047',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#0f172a', edgecolor='#fde047', alpha=0.9))

    plt.suptitle("Task 2.1: Manual Discrete Histogram and Empirical Probability Density Function", color='#38bdf8', fontsize=14, fontweight='bold')
    plt.tight_layout()

    out_file1 = os.path.join(out_dir, 'task_2_1_manual_histogram_python.png')
    out_file2 = os.path.join(fig_dir, 'task_2_1_manual_histogram_python.png')
    plt.savefig(out_file1, dpi=200, facecolor=fig.get_facecolor())
    plt.savefig(out_file2, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"[SAVED] Generated Task 2.1 figures:\n  {out_file1}\n  {out_file2}")

if __name__ == '__main__':
    main()
