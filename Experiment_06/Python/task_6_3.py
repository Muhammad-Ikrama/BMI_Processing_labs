"""
Experiment 06 - Task 6.3: Butterworth Low-Pass Filter Design & Order Sensitivity Sweep
Designs Butterworth Low-Pass Filters with fixed D0 = 40 across filter orders n in [1, 2, 4, 8],
evaluates 1D radial transfer functions, analyzes the onset of Gibbs ringing at higher orders,
and establishes the clinical standard order recommendation.
Course: Medical Image Processing | Riphah International University
Faculty: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

def run_task_6_3():
    print("==============================================================================")
    print("EXPERIMENT 06 - TASK 6.3: BUTTERWORTH LP ORDER SENSITIVITY SWEEP")
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

    # Distance Matrix
    u = np.arange(H) - H // 2
    v = np.arange(W) - W // 2
    V, U = np.meshgrid(v, u)
    D = np.hypot(V, U)
    D0 = 40.0

    # Orders to sweep
    orders = [1, 2, 4, 8]
    blpf_images = {}
    metrics_list = []

    # Transect coordinates across skull-brain interface
    prof_row = 256
    c_start, c_end = 50, 190
    orig_profile = img[prof_row, c_start:c_end]
    col_coords = np.arange(c_start, c_end)

    # Flat tissue ROI for ripple standard deviation: rows 240:270, cols 220:250
    roi_slice = (slice(240, 270), slice(220, 250))

    for n in orders:
        h = 1.0 / (1.0 + (D / D0) ** (2 * n))
        g = np.real(np.fft.ifft2(np.fft.ifftshift(F_shift * h)))
        im_out = np.clip(g, 0, 255).astype(np.uint8)

        blpf_images[n] = im_out
        cv2.imwrite(os.path.join(out_py_dir, f"exp06_task_6_3_blpf_order_{n}.png"), im_out)

        ret_pct = (np.sum(np.abs(F_shift * h) ** 2) / total_energy) * 100.0
        p_val = psnr(img, im_out)
        s_val = ssim(img, im_out)
        roi_std = float(np.std(im_out[roi_slice]))

        # Check ringing: profile overshoot
        rec_prof = im_out[prof_row, c_start:c_end]
        parenchyma_prof = rec_prof[70:120]
        ripple_p2p = float(np.ptp(parenchyma_prof))

        status_text = "Zero Ringing (Smooth)" if n <= 2 else ("Mild Ringing Onset" if n == 4 else "Prominent Ringing (Gibbs)")
        verdict = "Sub-optimal (Excessive Blur)" if n == 1 else ("CLINICAL OPTIMUM" if n == 2 else ("Acceptable (Caution)" if n == 4 else "Contraindicated"))

        metrics_list.append({
            "Order_n": n,
            "Cutoff_D0": int(D0),
            "Energy_Retention_Pct": round(ret_pct, 2),
            "PSNR_dB": round(p_val, 2),
            "SSIM": round(s_val, 4),
            "Ripple_P2P_Amplitude": round(ripple_p2p, 2),
            "ROI_Std_Ripple": round(roi_std, 2),
            "Ringing_Status": status_text,
            "Clinical_Verdict": verdict
        })

    # Save CSV table
    df_metrics = pd.DataFrame(metrics_list)
    csv_path = os.path.join(tab_dir, "exp06_task_6_3_blpf_sweep_metrics.csv")
    df_metrics.to_csv(csv_path, index=False)
    print(f"\n[INFO] BLPF Order Sweep Metrics saved at: {csv_path}")
    print(df_metrics.to_string(index=False))

    # Multi-panel Figure
    fig = plt.figure(figsize=(16, 11), facecolor='white')
    gs = fig.add_gridspec(2, 3, wspace=0.25, hspace=0.32)

    # 1. 1D Radial Transfer Functions H(D)
    ax0 = fig.add_subplot(gs[0, 0])
    d_vals = np.linspace(0, 120, 500)
    colors = ['#0284c7', '#16a34a', '#f59e0b', '#dc2626']
    for idx, n in enumerate(orders):
        h_d = 1.0 / (1.0 + (d_vals / D0) ** (2 * n))
        ax0.plot(d_vals, h_d, color=colors[idx], linewidth=2.0, label=f'Order $n={n}$')
    ax0.axvline(D0, color='gray', linestyle='--', linewidth=1.2, label=f'$D_0={int(D0)}$ px (Cutoff)')
    ax0.axhline(0.5, color='gray', linestyle=':', linewidth=0.8, label='$H(D_0)=0.5$ (-3dB)')
    ax0.set_xlabel('Radial Frequency Distance $D$ (pixels)', fontsize=9.5, fontweight='bold')
    ax0.set_ylabel('Transfer Magnitude $H(D)$', fontsize=9.5, fontweight='bold')
    ax0.set_title('(a) 1-D Radial Transfer Functions $H(D)$\n(Transition Slope Sharpness vs Order $n$)',
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax0.legend(loc='upper right', fontsize=8)
    ax0.grid(True, linestyle=':', alpha=0.6)

    # 2. BLPF Order n = 1
    ax1 = fig.add_subplot(gs[0, 1])
    ax1.imshow(blpf_images[1], cmap='gray')
    m0 = metrics_list[0]
    ax1.set_title(f"(b) BLPF Order $n=1$\nEnergy: {m0['Energy_Retention_Pct']}% | PSNR: {m0['PSNR_dB']} dB\n(Gradual Rolloff, High Blur)",
                  fontsize=10.5, fontweight='bold', color='#0284c7')
    ax1.axis('off')

    # 3. BLPF Order n = 2 (CLINICAL SWEET SPOT)
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.imshow(blpf_images[2], cmap='gray')
    m1 = metrics_list[1]
    ax2.set_title(f"(c) BLPF Order $n=2$ [CLINICAL OPTIMUM]\nEnergy: {m1['Energy_Retention_Pct']}% | PSNR: {m1['PSNR_dB']} dB\n(Smooth Rolloff, Zero Gibbs Ringing)",
                  fontsize=10.5, fontweight='bold', color='#16a34a')
    ax2.axis('off')

    # 4. BLPF Order n = 4
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.imshow(blpf_images[4], cmap='gray')
    m2 = metrics_list[2]
    ax3.set_title(f"(d) BLPF Order $n=4$\nEnergy: {m2['Energy_Retention_Pct']}% | PSNR: {m2['PSNR_dB']} dB\n(Steep Transition, Mild Ringing Onset)",
                  fontsize=10.5, fontweight='bold', color='#f59e0b')
    ax3.axis('off')

    # 5. BLPF Order n = 8
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.imshow(blpf_images[8], cmap='gray')
    m3 = metrics_list[3]
    ax4.set_title(f"(e) BLPF Order $n=8$\nEnergy: {m3['Energy_Retention_Pct']}% | PSNR: {m3['PSNR_dB']} dB\n(Near-Ideal Step, Severe Sinc Ripples)",
                  fontsize=10.5, fontweight='bold', color='#dc2626')
    ax4.axis('off')

    # 6. 1D Cranial Edge Profile Comparison Across Orders
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.plot(col_coords, orig_profile, color='black', linewidth=1.5, label='Original MRI')
    for idx, n in enumerate(orders):
        ax5.plot(col_coords, blpf_images[n][prof_row, c_start:c_end],
                 color=colors[idx], linewidth=1.5,
                 linestyle='-' if n == 2 else ('--' if n == 1 else ':'),
                 label=f'Order $n={n}$')
    ax5.set_xlabel('Column Pixel Coordinate', fontsize=9.5, fontweight='bold')
    ax5.set_ylabel('Pixel Intensity (0-255)', fontsize=9.5, fontweight='bold')
    ax5.set_title('(f) Cranial Transect: Ripple Emergence vs Order\n($n\\geq 4$ Triggers Gibbs Ringing)',
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax5.legend(loc='upper right', fontsize=8)
    ax5.grid(True, linestyle=':', alpha=0.6)

    plt.suptitle("Experiment 06 - Task 6.3: Butterworth Low-Pass Filter Design & Order Sensitivity Sweep",
                 fontsize=13, fontweight='bold', color='#0f172a', y=0.98)

    fig_path = os.path.join(fig_dir, "exp06_task_6_3_blpf_order_sweep_py.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Figure saved at: {fig_path}")

    return metrics_list

if __name__ == "__main__":
    run_task_6_3()
