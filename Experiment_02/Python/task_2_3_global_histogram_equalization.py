"""
Experiment 02 - Task 2.3: Global Histogram Equalization & Saturation Artifact Identification
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

Task Requirement:
Implement Global Histogram Equalization (GHE) using the discrete mathematical equation:
  s_k = round((L - 1) * CDF(r_k))
Apply to 'images/Lung-HR-contrast.png'.
Display side-by-side subplots of original vs equalized scan with histograms.
Quantify saturated pixel percentage (r == 0 or r == 255).
Evaluate why GHE washes out trabecular bone structures.
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def manual_global_histogram_equalization(img, L=256):
    """
    Manual implementation of Global Histogram Equalization (GHE)
    using the exact mathematical formula: s_k = round((L - 1) * CDF(r_k)).
    """
    H, W = img.shape
    total_pixels = H * W
    
    # 1. Histogram & PDF
    hist, _ = np.histogram(img.flatten(), L, [0, L])
    pdf = hist / float(total_pixels)
    
    # 2. Cumulative Distribution Function
    cdf = pdf.cumsum()
    
    # 3. Transformation mapping function T(r_k)
    transform_map = np.round((L - 1) * cdf).astype(np.uint8)
    
    # 4. Map original pixel intensities to new equalized levels
    equalized_img = transform_map[img]
    
    return equalized_img, transform_map, hist, cdf

def main():
    print("=" * 70)
    print("TASK 2.3: GLOBAL HISTOGRAM EQUALIZATION & SATURATION ARTIFACTS")
    print("=" * 70)

    possible_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'Inputs', 'images', 'Lung-HR-contrast.png'),
        os.path.join(os.path.dirname(__file__), '..', '..', '..', 'images', 'Lung-HR-contrast.png'),
        'images/Lung-HR-contrast.png'
    ]
    img_path = next((p for p in possible_paths if os.path.exists(p)), None)
    if not img_path:
        raise FileNotFoundError("Could not locate Lung-HR-contrast.png")

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    H, W = img.shape
    total_pixels = H * W

    # Apply manual GHE
    ghe_img, T_map, orig_hist, orig_cdf = manual_global_histogram_equalization(img)

    # Compute saturation statistics
    orig_sat_0 = np.sum(img == 0)
    orig_sat_255 = np.sum(img == 255)
    orig_sat_total = orig_sat_0 + orig_sat_255
    orig_sat_pct = (orig_sat_total / float(total_pixels)) * 100.0

    ghe_sat_0 = np.sum(ghe_img == 0)
    ghe_sat_255 = np.sum(ghe_img == 255)
    ghe_sat_total = ghe_sat_0 + ghe_sat_255
    ghe_sat_pct = (ghe_sat_total / float(total_pixels)) * 100.0

    # Information entropy
    def get_entropy(im):
        h, _ = np.histogram(im.flatten(), 256, [0, 256])
        p = h / float(im.size); p_nz = p[p > 0]
        return -np.sum(p_nz * np.log2(p_nz))

    ent_orig = get_entropy(img)
    ent_ghe = get_entropy(ghe_img)

    print(f"Original Scan Saturated Pixels : {orig_sat_total:,} ({orig_sat_pct:.2f}%) [r=0: {orig_sat_0:,}, r=255: {orig_sat_255:,}]")
    print(f"Global HE Saturated Pixels     : {ghe_sat_total:,} ({ghe_sat_pct:.2f}%) [r=0: {ghe_sat_0:,}, r=255: {ghe_sat_255:,}]")
    print(f"Original Shannon Entropy       : {ent_orig:.4f} bits/pixel")
    print(f"Global HE Shannon Entropy      : {ent_ghe:.4f} bits/pixel")
    print(f"Diagnostic Bone Washout Cause  : Saturated bone pixels ({ghe_sat_255:,}) blown out to pure white 255")

    # Plotting
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'Outputs', 'Python')
    fig_dir = os.path.join(os.path.dirname(__file__), '..', 'Figures')
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(15, 12), facecolor='#0f172a')

    # [0, 0] Original Image
    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title(f"(A) Original Low-Contrast Radiograph\nEntropy: {ent_orig:.2f} bits | Saturated: {orig_sat_pct:.2f}%",
                         color='white', fontweight='bold', fontsize=11)
    axes[0, 0].axis('off')

    # [0, 1] Global HE Image
    axes[0, 1].imshow(ghe_img, cmap='gray')
    axes[0, 1].set_title(f"(B) Global Histogram Equalized (GHE)\nEntropy: {ent_ghe:.2f} bits | Saturated: {ghe_sat_pct:.2f}% (BONE WASHOUT)",
                         color='#f87171', fontweight='bold', fontsize=11)
    axes[0, 1].axis('off')

    # [1, 0] Original Histogram
    axes[1, 0].bar(range(256), orig_hist, color='#38bdf8', width=1.0, edgecolor='none')
    axes[1, 0].set_facecolor('#1e293b')
    axes[1, 0].set_title("Original Clumped Histogram (Narrow Dynamic Range)", color='white', fontweight='bold', fontsize=11)
    axes[1, 0].set_xlabel("Intensity Level", color='#94a3b8')
    axes[1, 0].set_ylabel("Pixel Frequency", color='#94a3b8')
    axes[1, 0].tick_params(colors='#94a3b8')
    axes[1, 0].set_xlim([0, 255])
    axes[1, 0].grid(True, color='#334155', linestyle='--', alpha=0.5)

    # [1, 1] GHE Histogram
    ghe_hist, _ = np.histogram(ghe_img.flatten(), 256, [0, 256])
    axes[1, 1].bar(range(256), ghe_hist, color='#f87171', width=1.0, edgecolor='none')
    axes[1, 1].set_facecolor('#1e293b')
    axes[1, 1].set_title("Equalized Histogram: Note 'Comb Gaps' & Saturated Spikes", color='#f87171', fontweight='bold', fontsize=11)
    axes[1, 1].set_xlabel("Intensity Level", color='#94a3b8')
    axes[1, 1].set_ylabel("Pixel Frequency", color='#94a3b8')
    axes[1, 1].tick_params(colors='#94a3b8')
    axes[1, 1].set_xlim([0, 255])
    axes[1, 1].grid(True, color='#334155', linestyle='--', alpha=0.5)

    plt.suptitle("Task 2.3: Global Histogram Equalization & Over-Saturation Artifacts", color='#38bdf8', fontsize=14, fontweight='bold')
    plt.tight_layout()

    out_file1 = os.path.join(out_dir, 'task_2_3_global_histogram_equalization_python.png')
    out_file2 = os.path.join(fig_dir, 'task_2_3_global_histogram_equalization_python.png')
    plt.savefig(out_file1, dpi=200, facecolor=fig.get_facecolor())
    plt.savefig(out_file2, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"[SAVED] Generated Task 2.3 figures:\n  {out_file1}\n  {out_file2}")

if __name__ == '__main__':
    main()
