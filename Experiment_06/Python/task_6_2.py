"""
Experiment 06 - Task 6.2: Gibbs Phenomenon & Ringing Artifact Analysis of Ideal Low-Pass Filters
Evaluates Ideal Low-Pass Filters (ILPF) across cutoff frequencies D0 in [20, 40, 80] pixels,
extracts 1D edge profiles across the cranial boundary, quantifies ringing ripple amplitude,
and explains clinical failure modes of Gibbs ringing.
Course: Medical Image Processing | Riphah International University
Faculty: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

def run_task_6_2():
    print("==============================================================================")
    print("EXPERIMENT 06 - TASK 6.2: GIBBS PHENOMENON & RINGING ARTIFACT ANALYSIS (ILPF)")
    print("==============================================================================")

    # Resolve paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.abspath(os.path.join(script_dir, ".."))
    img_path = os.path.join(exp_dir, "Inputs", "images", "MRI.jpg")
    if not os.path.exists(img_path):
        img_path = os.path.join(exp_dir, "..", "..", "images", "MRI.jpg")

    out_py_dir = os.path.join(exp_dir, "Outputs", "Python")
    fig_dir = os.path.join(exp_dir, "Figures")
    tab_dir = os.path.join(exp_dir, "Tables")
    os.makedirs(out_py_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(tab_dir, exist_ok=True)

    # Load image
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Cannot load image at {img_path}")
    H, W = img.shape

    # 2D-DFT & Centering
    F = np.fft.fft2(img.astype(float))
    F_shift = np.fft.fftshift(F)
    total_energy = np.sum(np.abs(F_shift) ** 2)

    # Radial Distance Matrix
    u = np.arange(H) - H // 2
    v = np.arange(W) - W // 2
    V, U = np.meshgrid(v, u)
    D = np.hypot(V, U)

    # Cutoff sweep parameters
    cutoffs = [20.0, 40.0, 80.0]
    ilpf_images = {}
    ilpf_masks = {}
    metrics_list = []

    # Anatomical Transect Coordinates for 1D Edge Profile across Skull-Brain Interface
    # Horizontal line across row 256 from column 50 to column 180 (spans background air -> skull -> CSF -> cortex)
    prof_row = 256
    c_start, c_end = 50, 190
    orig_profile = img[prof_row, c_start:c_end]
    col_coords = np.arange(c_start, c_end)

    # Uniform brain parenchyma ROI for ripple variance quantification: rows 240:270, cols 220:250
    roi_slice = (slice(240, 270), slice(220, 250))
    orig_roi_std = np.std(img[roi_slice])

    for D0 in cutoffs:
        h = (D <= D0).astype(float)
        g = np.real(np.fft.ifft2(np.fft.ifftshift(F_shift * h)))
        im_out = np.clip(g, 0, 255).astype(np.uint8)

        ilpf_images[D0] = im_out
        ilpf_masks[D0] = h

        # Save individual filtered image
        cv2.imwrite(os.path.join(out_py_dir, f"exp06_task_6_2_ilpf_D0_{int(D0)}.png"), im_out)

        # Quantitative Metrics
        ret_pct = (np.sum(np.abs(F_shift * h) ** 2) / total_energy) * 100.0
        p_val = psnr(img, im_out)
        s_val = ssim(img, im_out)

        # Ringing profile analysis
        recon_profile = im_out[prof_row, c_start:c_end]
        # In the parenchyma region of profile (cols 120-170), find peak-to-peak ripple amplitude
        parenchyma_prof = recon_profile[70:120]
        ripple_p2p = float(np.ptp(parenchyma_prof))
        ripple_std = float(np.std(im_out[roi_slice]))

        metrics_list.append({
            "Cutoff_D0": int(D0),
            "Energy_Retention_Pct": round(ret_pct, 2),
            "PSNR_dB": round(p_val, 2),
            "SSIM": round(s_val, 4),
            "Ripple_P2P_Amplitude": round(ripple_p2p, 2),
            "ROI_Std_Ripple": round(ripple_std, 2),
            "Visual_Ringing": "Severe (Broad)" if D0 == 20 else ("Moderate (Distinct)" if D0 == 40 else "High-Frequency Ripples")
        })

    # Save CSV table
    df_metrics = pd.DataFrame(metrics_list)
    csv_path = os.path.join(tab_dir, "exp06_task_6_2_ilpf_ringing_metrics.csv")
    df_metrics.to_csv(csv_path, index=False)
    print(f"\n[INFO] ILPF Sensitivity Sweep Metrics saved at: {csv_path}")
    print(df_metrics.to_string(index=False))

    # Multi-panel Figure
    fig = plt.figure(figsize=(16, 11), facecolor='white')
    gs = fig.add_gridspec(2, 3, wspace=0.25, hspace=0.32)

    # 1. Original scan with transect line annotated
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.imshow(img, cmap='gray')
    ax0.axhline(prof_row, xmin=c_start/W, xmax=c_end/W, color='cyan', linewidth=2, label='Transect Line')
    rect = plt.Rectangle((roi_slice[1].start, roi_slice[0].start),
                         roi_slice[1].stop - roi_slice[1].start,
                         roi_slice[0].stop - roi_slice[0].start,
                         edgecolor='yellow', fill=False, linewidth=1.5, linestyle='--', label='ROI')
    ax0.add_patch(rect)
    ax0.set_title(f"(a) Clinical MRI with Transect (Cyan)\nRow {prof_row}, Cols [{c_start}, {c_end}]",
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax0.legend(loc='lower right', fontsize=8)
    ax0.axis('off')

    # 2. ILPF D0 = 20
    ax1 = fig.add_subplot(gs[0, 1])
    ax1.imshow(ilpf_images[20.0], cmap='gray')
    m0 = metrics_list[0]
    ax1.set_title(f"(b) ILPF ($D_0=20$ px)\nEnergy: {m0['Energy_Retention_Pct']}% | PSNR: {m0['PSNR_dB']} dB\nSevere Low-Frequency Ringing",
                  fontsize=10.5, fontweight='bold', color='#b91c1c')
    ax1.axis('off')

    # 3. ILPF D0 = 40
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.imshow(ilpf_images[40.0], cmap='gray')
    m1 = metrics_list[1]
    ax2.set_title(f"(c) ILPF ($D_0=40$ px)\nEnergy: {m1['Energy_Retention_Pct']}% | PSNR: {m1['PSNR_dB']} dB\nNoticeable Sinc Ripple Halos",
                  fontsize=10.5, fontweight='bold', color='#b91c1c')
    ax2.axis('off')

    # 4. ILPF D0 = 80
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.imshow(ilpf_images[80.0], cmap='gray')
    m2 = metrics_list[2]
    ax3.set_title(f"(d) ILPF ($D_0=80$ px)\nEnergy: {m2['Energy_Retention_Pct']}% | PSNR: {m2['PSNR_dB']} dB\nTight High-Frequency Ringing",
                  fontsize=10.5, fontweight='bold', color='#b91c1c')
    ax3.axis('off')

    # 5. 1D Intensity Transect Profiles across Cranial Edge
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(col_coords, orig_profile, color='black', linewidth=1.5, label='Original MRI Edge')
    ax4.plot(col_coords, ilpf_images[20.0][prof_row, c_start:c_end], color='#ef4444', linewidth=1.5, linestyle='--', label='$D_0=20$ px (Broad Ripple)')
    ax4.plot(col_coords, ilpf_images[40.0][prof_row, c_start:c_end], color='#3b82f6', linewidth=1.5, label='$D_0=40$ px (Sharp Ripple)')
    ax4.plot(col_coords, ilpf_images[80.0][prof_row, c_start:c_end], color='#10b981', linewidth=1.2, linestyle=':', label='$D_0=80$ px (Fast Ripple)')
    ax4.set_xlabel('Column Pixel Coordinate', fontsize=9.5, fontweight='bold')
    ax4.set_ylabel('Pixel Intensity (0-255)', fontsize=9.5, fontweight='bold')
    ax4.set_title('(e) 1-D Cranial Edge Profile Comparison\n(Gibbs Overshoot & Undershoot Ripples)',
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax4.legend(loc='upper right', fontsize=8)
    ax4.grid(True, linestyle=':', alpha=0.6)

    # 6. Ripple Metrics Bar Chart
    ax5 = fig.add_subplot(gs[1, 2])
    x_pos = np.arange(len(cutoffs))
    bar_width = 0.35
    p2p_vals = [m['Ripple_P2P_Amplitude'] for m in metrics_list]
    std_vals = [m['ROI_Std_Ripple'] for m in metrics_list]

    b1 = ax5.bar(x_pos - bar_width/2, p2p_vals, bar_width, label='P2P Ripple Amp (px)', color='#f87171', edgecolor='#991b1b')
    b2 = ax5.bar(x_pos + bar_width/2, std_vals, bar_width, label='ROI Ripple Std Dev', color='#fbbf24', edgecolor='#b45309')
    ax5.axhline(orig_roi_std, color='gray', linestyle='--', linewidth=1, label=f'Baseline ROI Std ({orig_roi_std:.1f})')
    ax5.set_xticks(x_pos)
    ax5.set_xticklabels([f"$D_0={int(c)}$" for c in cutoffs], fontsize=9.5, fontweight='bold')
    ax5.set_ylabel('Intensity Variation', fontsize=9.5, fontweight='bold')
    ax5.set_title('(f) Ringing Severity & Artifact Quantification', fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax5.legend(loc='upper right', fontsize=8)
    ax5.grid(True, linestyle=':', alpha=0.6)

    for b in b1:
        ax5.annotate(f"{b.get_height():.1f}", xy=(b.get_x() + b.get_width()/2, b.get_height()),
                     xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=8)
    for b in b2:
        ax5.annotate(f"{b.get_height():.1f}", xy=(b.get_x() + b.get_width()/2, b.get_height()),
                     xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=8)

    plt.suptitle("Experiment 06 - Task 6.2: Gibbs Phenomenon & Ringing Artifact Analysis of Ideal Low-Pass Filters",
                 fontsize=13, fontweight='bold', color='#0f172a', y=0.98)

    fig_path = os.path.join(fig_dir, "exp06_task_6_2_ilpf_gibbs_ringing_py.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Figure saved at: {fig_path}")

    return metrics_list

if __name__ == "__main__":
    run_task_6_2()
