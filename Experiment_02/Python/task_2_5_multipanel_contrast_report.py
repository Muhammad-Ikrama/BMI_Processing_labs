"""
Experiment 02 - Task 2.5: Clinical Multi-Panel Radiograph Contrast Report with ROI Benchmarking
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

Task Requirement:
Construct publication-grade 2 x 3 multi-panel diagnostic report comparing:
  (a) Original Scan
  (b) Global HE
  (c) CLAHE (Clip=2.0)
Top row: Enhanced medical scans with two highlighted ROIs:
  - ROI 1: Lung Parenchyma (Cyan box)
  - ROI 2: Background Air (Yellow box)
Bottom row: Corresponding intensity histograms and formatted quantitative benchmark table:
  - Mean Brightness
  - RMS Contrast
  - Shannon Information Entropy
  - Background Noise Floor Variance
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def get_metrics(im, roi1_slice, roi2_slice):
    h, _ = np.histogram(im.flatten(), 256, [0, 256])
    p = h / float(im.size); p_nz = p[p > 0]
    ent = -np.sum(p_nz * np.log2(p_nz))
    mean_val = float(im.mean())
    rms_contrast = float(im.std())
    min_val, max_val = float(im.min()), float(im.max())
    michelson = (max_val - min_val) / (max_val + min_val) if (max_val + min_val) > 0 else 0.0
    
    # ROI 1 = Lung Parenchyma mean and std
    roi1_mean = float(np.mean(im[roi1_slice]))
    roi1_std = float(np.std(im[roi1_slice]))
    
    # ROI 2 = Background Air noise variance
    bg_noise_var = float(np.var(im[roi2_slice]))
    
    # Saturation percentage
    sat_pct = (float(np.sum(im == 0) + np.sum(im == 255)) / float(im.size)) * 100.0
    
    return {
        'mean': mean_val,
        'rms': rms_contrast,
        'entropy': ent,
        'bg_var': bg_noise_var,
        'roi1_mean': roi1_mean,
        'roi1_std': roi1_std,
        'michelson': michelson,
        'sat_pct': sat_pct
    }

def main():
    print("=" * 70)
    print("TASK 2.5: CLINICAL MULTI-PANEL RADIOGRAPH CONTRAST REPORT WITH ROI BENCHMARKING")
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

    # Contrast enhancements
    ghe_img = cv2.equalizeHist(img)
    clahe_img = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(img)

    # Define ROIs (y, x, h, w)
    # ROI 1: Mid-lung parenchyma
    r1_y, r1_x, r1_h, r1_w = int(H * 0.45), int(W * 0.65), 100, 100
    roi1_slice = (slice(r1_y, r1_y + r1_h), slice(r1_x, r1_x + r1_w))

    # ROI 2: Upper corner background air
    r2_y, r2_x, r2_h, r2_w = int(H * 0.05), int(W * 0.05), 80, 80
    roi2_slice = (slice(r2_y, r2_y + r2_h), slice(r2_x, r2_x + r2_w))

    m_orig = get_metrics(img, roi1_slice, roi2_slice)
    m_ghe = get_metrics(ghe_img, roi1_slice, roi2_slice)
    m_clahe = get_metrics(clahe_img, roi1_slice, roi2_slice)

    print(f"\n--- QUANTITATIVE CLINICAL BENCHMARKING REPORT ---")
    print(f"{'Evaluation Metric':<28} | {'Original Scan':<15} | {'Global HE (GHE)':<17} | {'CLAHE (Clip=2.0)':<18}")
    print("-" * 85)
    print(f"{'Mean Brightness (0-255)':<28} | {m_orig['mean']:<15.2f} | {m_ghe['mean']:<17.2f} | {m_clahe['mean']:<18.2f}")
    print(f"{'RMS Contrast (Std Dev)':<28} | {m_orig['rms']:<15.2f} | {m_ghe['rms']:<17.2f} | {m_clahe['rms']:<18.2f}")
    print(f"{'Information Entropy (bits)':<28} | {m_orig['entropy']:<15.4f} | {m_ghe['entropy']:<17.4f} | {m_clahe['entropy']:<18.4f}")
    print(f"{'Background Noise Variance':<28} | {m_orig['bg_var']:<15.2f} | {m_ghe['bg_var']:<17.2f} | {m_clahe['bg_var']:<18.2f}")
    print(f"{'Lung Parenchyma Mean':<28} | {m_orig['roi1_mean']:<15.2f} | {m_ghe['roi1_mean']:<17.2f} | {m_clahe['roi1_mean']:<18.2f}")
    print(f"{'Boundary Saturation (%)':<28} | {m_orig['sat_pct']:<15.2f}% | {m_ghe['sat_pct']:<17.2f}% | {m_clahe['sat_pct']:<18.2f}%")

    # Export CSV table
    out_table = os.path.join(os.path.dirname(__file__), '..', 'Tables', 'task_2_5_contrast_benchmark_summary.csv')
    os.makedirs(os.path.dirname(out_table), exist_ok=True)
    with open(out_table, 'w', encoding='utf-8') as f:
        f.write("Metric,Original_Scan,Global_HE,CLAHE_Clip20\n")
        f.write(f"Mean_Brightness,{m_orig['mean']:.2f},{m_ghe['mean']:.2f},{m_clahe['mean']:.2f}\n")
        f.write(f"RMS_Contrast,{m_orig['rms']:.2f},{m_ghe['rms']:.2f},{m_clahe['rms']:.2f}\n")
        f.write(f"Information_Entropy_bits,{m_orig['entropy']:.4f},{m_ghe['entropy']:.4f},{m_clahe['entropy']:.4f}\n")
        f.write(f"Background_Noise_Variance,{m_orig['bg_var']:.2f},{m_ghe['bg_var']:.2f},{m_clahe['bg_var']:.2f}\n")
        f.write(f"Lung_ROI_Mean,{m_orig['roi1_mean']:.2f},{m_ghe['roi1_mean']:.2f},{m_clahe['roi1_mean']:.2f}\n")
        f.write(f"Saturation_Percentage,{m_orig['sat_pct']:.2f},{m_ghe['sat_pct']:.2f},{m_clahe['sat_pct']:.2f}\n")
    print(f"[SAVED] Exported benchmark table to: {out_table}")

    # Plotting 2 x 3 diagnostic multi-panel
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'Outputs', 'Python')
    fig_dir = os.path.join(os.path.dirname(__file__), '..', 'Figures')
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    fig, axes = plt.subplots(2, 3, figsize=(18, 12), facecolor='#0f172a')

    # Images with ROI boxes
    dataset_tuples = [
        ("Original Low-Contrast Scan", img, m_orig, '#94a3b8'),
        ("Global Histogram Equalization (GHE)", ghe_img, m_ghe, '#f87171'),
        ("CLAHE (Clip=2.0, 8x8 Grid) [OPTIMAL]", clahe_img, m_clahe, '#4ade80')
    ]

    for col, (title, im, m, border_col) in enumerate(dataset_tuples):
        ax_img = axes[0, col]
        ax_img.imshow(im, cmap='gray')
        ax_img.set_title(f"{title}\nH={m['entropy']:.2f} | RMS={m['rms']:.1f} | Var_bg={m['bg_var']:.1f}",
                         color=border_col, fontweight='bold', fontsize=11, pad=6)
        
        # Add ROI Rectangles
        rect_roi1 = patches.Rectangle((r1_x, r1_y), r1_w, r1_h, linewidth=2, edgecolor='#38bdf8', facecolor='none', linestyle='-')
        rect_roi2 = patches.Rectangle((r2_x, r2_y), r2_w, r2_h, linewidth=2, edgecolor='#fde047', facecolor='none', linestyle='--')
        ax_img.add_patch(rect_roi1)
        ax_img.add_patch(rect_roi2)
        ax_img.text(r1_x + 5, r1_y - 15, "ROI 1: Lung", color='#38bdf8', fontsize=8, fontweight='bold')
        ax_img.text(r2_x + 5, r2_y - 15, "ROI 2: Air", color='#fde047', fontsize=8, fontweight='bold')
        ax_img.axis('off')

        # Bottom row: Histograms
        ax_hist = axes[1, col]
        ax_hist.set_facecolor('#1e293b')
        h, _ = np.histogram(im.flatten(), 256, [0, 256])
        ax_hist.bar(range(256), h, color=border_col, width=1.0, edgecolor='none')
        ax_hist.set_title(f"Histogram: {title.split()[0]}", color='white', fontsize=11, fontweight='bold')
        ax_hist.set_xlabel("Gray Level Intensity r_k", color='#94a3b8')
        ax_hist.set_ylabel("Pixel Frequency n_k", color='#94a3b8')
        ax_hist.tick_params(colors='#94a3b8')
        ax_hist.set_xlim([0, 255])
        ax_hist.grid(True, color='#334155', linestyle='--', alpha=0.5)

        # Highlight saturation
        sat_text = f"Entropy: {m['entropy']:.3f}\nNoise Var: {m['bg_var']:.1f}\nSat: {m['sat_pct']:.2f}%"
        ax_hist.text(0.05, 0.95, sat_text, transform=ax_hist.transAxes, verticalalignment='top',
                     fontsize=9, color='white', bbox=dict(boxstyle='square,pad=0.4', fc='#0f172a', ec=border_col, lw=1))

    plt.suptitle("Task 2.5: Clinical Multi-Panel Radiograph Contrast Report with ROI Benchmarking", color='#38bdf8', fontsize=15, fontweight='bold')
    plt.tight_layout()

    out_file1 = os.path.join(out_dir, 'task_2_5_multipanel_contrast_report_python.png')
    out_file2 = os.path.join(fig_dir, 'task_2_5_multipanel_contrast_report_python.png')
    plt.savefig(out_file1, dpi=200, facecolor=fig.get_facecolor())
    plt.savefig(out_file2, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"[SAVED] Generated Task 2.5 figures:\n  {out_file1}\n  {out_file2}")

if __name__ == '__main__':
    main()
