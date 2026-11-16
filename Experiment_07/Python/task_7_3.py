"""
Experiment 07 - Task 7.3: 1D Spatial Transect Profile Extraction & Mach Band Quantitative Measurement
Extracts a 1-D pixel intensity profile across Row 150 (Columns 100 to 250) intersecting the cortical bone
margin, quantifies edge slope steepening (dI/dx), overshoot peak height, and Mach band halo width.
Course: Medical Image Processing | Riphah International University
Faculty: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

def run_task_7_3():
    print("==============================================================================")
    print("EXPERIMENT 07 - TASK 7.3: 1D TRANSECT & MACH BAND QUANTITATIVE MEASUREMENT")
    print("==============================================================================")

    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.abspath(os.path.join(script_dir, ".."))
    img_path = os.path.join(exp_dir, "Inputs", "images", "Xray.jpg")
    if not os.path.exists(img_path):
        img_path = os.path.join(exp_dir, "..", "..", "images", "Xray.jpg")

    out_py_dir = os.path.join(exp_dir, "Outputs", "Python")
    fig_dir = os.path.join(exp_dir, "Figures")
    tab_dir = os.path.join(exp_dir, "Tables")
    os.makedirs(out_py_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(tab_dir, exist_ok=True)

    # 1. Load Image & Extract Mask
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Cannot load radiograph at {img_path}")
    H, W = img.shape
    img_f = img.astype(np.float64)

    blurred = gaussian_filter(img_f, sigma=1.5)
    g_mask = img_f - blurred

    # Sharpened versions
    sharp_k1_raw = img_f + 1.0 * g_mask
    sharp_k3_raw = img_f + 3.0 * g_mask

    sharp_k1 = np.clip(sharp_k1_raw, 0, 255).astype(np.uint8)
    sharp_k3 = np.clip(sharp_k3_raw, 0, 255).astype(np.uint8)

    # 2. Extract Transect across Row 150, Columns 100 to 250 (Bone to Lung Parenchyma)
    prof_row = 150
    c_start, c_end = 100, 250
    cols = np.arange(c_start, c_end)

    prof_orig = img_f[prof_row, c_start:c_end]
    prof_k1 = sharp_k1_raw[prof_row, c_start:c_end]
    prof_k3 = sharp_k3_raw[prof_row, c_start:c_end]

    # Save output cropped images and transect overlay
    im_transect = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.line(im_transect, (c_start, prof_row), (c_end, prof_row), (0, 255, 255), 2)
    cv2.imwrite(os.path.join(out_py_dir, "exp07_task_7_3_transect_overlay.png"), im_transect)

    # 3. Quantitative Measurements on Bone-Lung Interface (Cols 200 to 220)
    # Edge slope = max abs(diff) across the steep step transition
    def calc_profile_metrics(prof, label):
        diffs = np.abs(np.diff(prof))
        max_slope = float(np.max(diffs))
        
        # Step edge transition is between index 100 to 125 (cols 200 to 225)
        edge_region = prof[100:125]
        peak_val = float(np.max(edge_region))
        trough_val = float(np.min(edge_region))
        baseline_bone = float(np.mean(prof[40:70])) # columns 140:170
        baseline_lung = float(np.mean(prof[115:135])) # columns 215:235

        overshoot = max(0.0, peak_val - baseline_bone)
        undershoot = max(0.0, baseline_lung - trough_val)

        # Halo width (number of pixels where overshoot exceeds 50% of peak height)
        if overshoot > 1.0:
            half_max = baseline_bone + 0.5 * overshoot
            halo_width = float(np.sum(edge_region >= half_max))
        else:
            halo_width = 0.0

        return {
            "Condition": label,
            "Max_Edge_Slope": round(max_slope, 2),
            "Overshoot_Peak": round(overshoot, 2),
            "Undershoot_Trough": round(undershoot, 2),
            "Mach_Band_Halo_Width_Px": round(halo_width, 1),
            "Halo_Compliance": "Pass (<= 2.0 px)" if halo_width <= 2.0 else "FAIL (> 2.0 px, Broad Halo)"
        }

    m_orig = calc_profile_metrics(prof_orig, "Original Scan")
    m_k1 = calc_profile_metrics(prof_k1, "Unsharp Masking (k=1.0)")
    m_k3 = calc_profile_metrics(prof_k3, "Over-Boosted (k=3.0)")

    metrics_list = [m_orig, m_k1, m_k3]
    df_metrics = pd.DataFrame(metrics_list)
    csv_path = os.path.join(tab_dir, "exp07_task_7_3_mach_band_metrics.csv")
    df_metrics.to_csv(csv_path, index=False)
    print(f"\n[INFO] Transect & Mach Band Metrics saved at: {csv_path}")
    print(df_metrics.to_string(index=False))

    # 4. Multi-panel Visualization Figure (1x3 high-detail layout)
    fig = plt.figure(figsize=(16, 7), facecolor='white')
    gs = fig.add_gridspec(1, 3, width_ratios=[1.1, 1.4, 1.0], wspace=0.28)

    # (a) Radiograph with Transect Line
    ax0 = fig.add_subplot(gs[0])
    ax0.imshow(img, cmap='gray')
    ax0.plot([c_start, c_end], [prof_row, prof_row], color='cyan', linewidth=2.5, label=f'Transect Row {prof_row}')
    ax0.scatter([c_start, c_end], [prof_row, prof_row], color='yellow', s=50, zorder=5)
    ax0.set_title(f"(a) Chest Radiograph with Transect (Cyan)\nRow {prof_row}, Columns [{c_start}, {c_end}]",
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax0.legend(loc='lower right', fontsize=8.5)
    ax0.axis('off')

    # (b) 1-D Transect Intensity Profiles
    ax1 = fig.add_subplot(gs[1])
    ax1.plot(cols, prof_orig, color='#475569', linewidth=1.8, label='Original Radiograph')
    ax1.plot(cols, prof_k1, color='#16a34a', linewidth=2.2, label='Unsharp Mask ($k=1.0$) [Optimal]')
    ax1.plot(cols, prof_k3, color='#dc2626', linewidth=1.8, linestyle='--', label='Over-Boosted ($k=3.0$) [Halos]')
    ax1.set_xlabel('Column Pixel Coordinate', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Pixel Intensity (0-255)', fontsize=10, fontweight='bold')
    ax1.set_title('(b) 1-D Cortical Bone Transect Profile\n(Mach Band Overshoot & Edge Slope Steepening)',
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax1.legend(loc='upper right', fontsize=8.5)
    ax1.grid(True, linestyle=':', alpha=0.6)

    # Highlight the bone-lung step transition
    ax1.axvspan(200, 220, color='yellow', alpha=0.15, label='Bone-Lung Interface')

    # (c) Quantitative Metric Comparison Bar Chart
    ax2 = fig.add_subplot(gs[2])
    labels_bar = ["Original", "k=1.0", "k=3.0"]
    slopes = [m['Max_Edge_Slope'] for m in metrics_list]
    overshoots = [m['Overshoot_Peak'] for m in metrics_list]
    widths = [m['Mach_Band_Halo_Width_Px'] for m in metrics_list]

    x = np.arange(len(labels_bar))
    w = 0.28

    r1 = ax2.bar(x - w, slopes, w, label='Edge Slope (dI/dx)', color='#3b82f6', edgecolor='#1e3a8a')
    r2 = ax2.bar(x, overshoots, w, label='Overshoot (Units)', color='#ef4444', edgecolor='#991b1b')
    r3 = ax2.bar(x + w, widths, w, label='Halo Width (Px)', color='#10b981', edgecolor='#065f46')

    ax2.set_xticks(x)
    ax2.set_xticklabels(labels_bar, fontsize=9.5, fontweight='bold')
    ax2.set_ylabel('Metric Value', fontsize=10, fontweight='bold')
    ax2.set_title('(c) Quantitative Edge & Halo Metrics', fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax2.legend(loc='upper left', fontsize=8)
    ax2.grid(True, linestyle=':', alpha=0.6)

    for r in r1:
        ax2.annotate(f"{r.get_height():.1f}", xy=(r.get_x() + r.get_width()/2, r.get_height()),
                     xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=7.5)
    for r in r2:
        ax2.annotate(f"{r.get_height():.1f}", xy=(r.get_x() + r.get_width()/2, r.get_height()),
                     xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=7.5)
    for r in r3:
        ax2.annotate(f"{r.get_height():.1f}", xy=(r.get_x() + r.get_width()/2, r.get_height()),
                     xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=7.5)

    plt.suptitle("Experiment 07 - Task 7.3: 1D Spatial Transect Profile Extraction & Mach Band Quantitative Measurement",
                 fontsize=12.5, fontweight='bold', color='#0f172a', y=0.98)

    fig_path = os.path.join(fig_dir, "exp07_task_7_3_mach_band_profiles_py.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Figure saved at: {fig_path}")

    return metrics_list

if __name__ == "__main__":
    run_task_7_3()
