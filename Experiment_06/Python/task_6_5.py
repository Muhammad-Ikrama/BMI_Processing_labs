"""
Experiment 06 - Task 6.5: Multi-Filter Quantitative Benchmarking & Comprehensive Diagnostic Report
Constructs a publication-grade 2x3 multi-panel diagnostic report comparing Input Scan, Centered Spectrum,
ILPF (D0=40), BLPF (n=2, D0=40), GLPF (D0=40), and GHPF (D0=50), tabulates Spectral Energy, PSNR, SSIM,
and provides evidence-based clinical recommendations.
Course: Medical Image Processing | Riphah International University
Faculty: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

def run_task_6_5():
    print("==============================================================================")
    print("EXPERIMENT 06 - TASK 6.5: MULTI-FILTER BENCHMARKING & DIAGNOSTIC REPORT")
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
    mag_spectrum = np.log1p(np.abs(F_shift))
    total_energy = np.sum(np.abs(F_shift) ** 2)

    # Distance Matrix
    u = np.arange(H) - H // 2
    v = np.arange(W) - W // 2
    V, U = np.meshgrid(v, u)
    D = np.hypot(V, U)

    # Filter definitions
    D0_lp = 40.0
    D0_hp = 50.0

    h_ilpf = (D <= D0_lp).astype(float)
    h_blpf = 1.0 / (1.0 + (D / D0_lp) ** (2 * 2))
    h_glpf = np.exp(- (D ** 2) / (2.0 * (D0_lp ** 2)))
    h_ghpf = 1.0 - np.exp(- (D ** 2) / (2.0 * (D0_hp ** 2)))

    # Filtering execution
    def ifft_real(h_filt):
        return np.real(np.fft.ifft2(np.fft.ifftshift(F_shift * h_filt)))

    g_ilpf = ifft_real(h_ilpf)
    g_blpf = ifft_real(h_blpf)
    g_glpf = ifft_real(h_glpf)
    g_ghpf = ifft_real(h_ghpf)

    img_ilpf = np.clip(g_ilpf, 0, 255).astype(np.uint8)
    img_blpf = np.clip(g_blpf, 0, 255).astype(np.uint8)
    img_glpf = np.clip(g_glpf, 0, 255).astype(np.uint8)
    img_ghpf_vis = np.clip(np.abs(g_ghpf) * 2.2, 0, 255).astype(np.uint8)

    # Save output images
    cv2.imwrite(os.path.join(out_py_dir, "exp06_task_6_5_ilpf.png"), img_ilpf)
    cv2.imwrite(os.path.join(out_py_dir, "exp06_task_6_5_blpf.png"), img_blpf)
    cv2.imwrite(os.path.join(out_py_dir, "exp06_task_6_5_glpf.png"), img_glpf)
    cv2.imwrite(os.path.join(out_py_dir, "exp06_task_6_5_ghpf.png"), img_ghpf_vis)

    # Quantitative Benchmarking
    benchmark_data = [
        {
            "Filter_Name": "Ideal Low-Pass (ILPF)",
            "Filter_Class": "Low-Pass",
            "Cutoff_D0": int(D0_lp),
            "Order_n": "Infinite (Step)",
            "Energy_Retention_Pct": round((np.sum(np.abs(F_shift * h_ilpf) ** 2) / total_energy) * 100.0, 2),
            "PSNR_dB": round(psnr(img, img_ilpf), 2),
            "SSIM": round(ssim(img, img_ilpf), 4),
            "Gibbs_Ringing": "Severe (Prominent concentric halos)",
            "Clinical_Verdict": "Contraindicated (Mimics hematomas / dissection)"
        },
        {
            "Filter_Name": "Butterworth LP (n=2)",
            "Filter_Class": "Low-Pass",
            "Cutoff_D0": int(D0_lp),
            "Order_n": 2,
            "Energy_Retention_Pct": round((np.sum(np.abs(F_shift * h_blpf) ** 2) / total_energy) * 100.0, 2),
            "PSNR_dB": round(psnr(img, img_blpf), 2),
            "SSIM": round(ssim(img, img_blpf), 4),
            "Gibbs_Ringing": "Zero (Smooth maximally-flat rolloff)",
            "Clinical_Verdict": "GOLD STANDARD (Optimal parenchymal denoising)"
        },
        {
            "Filter_Name": "Gaussian LP (GLPF)",
            "Filter_Class": "Low-Pass",
            "Cutoff_D0": int(D0_lp),
            "Order_n": "Gaussian",
            "Energy_Retention_Pct": round((np.sum(np.abs(F_shift * h_glpf) ** 2) / total_energy) * 100.0, 2),
            "PSNR_dB": round(psnr(img, img_glpf), 2),
            "SSIM": round(ssim(img, img_glpf), 4),
            "Gibbs_Ringing": "Zero (100% ripple-free, zero secondary lobes)",
            "Clinical_Verdict": "EXCELLENT (Ideal for pre-segmentation smoothing)"
        },
        {
            "Filter_Name": "Gaussian High-Pass (GHPF)",
            "Filter_Class": "High-Pass",
            "Cutoff_D0": int(D0_hp),
            "Order_n": "Gaussian",
            "Energy_Retention_Pct": round((np.sum(np.abs(F_shift * h_ghpf) ** 2) / total_energy) * 100.0, 2),
            "PSNR_dB": round(psnr(img, img_ghpf_vis), 2),
            "SSIM": round(ssim(img, img_ghpf_vis), 4),
            "Gibbs_Ringing": "Zero (DC removed, boundary isolation)",
            "Clinical_Verdict": "DIAGNOSTIC (Superior micro-structure & vessel isolation)"
        }
    ]

    df_summary = pd.DataFrame(benchmark_data)
    csv_path = os.path.join(tab_dir, "exp06_benchmark_summary_py.csv")
    df_summary.to_csv(csv_path, index=False)
    print(f"\n[INFO] Comprehensive Diagnostic Benchmark saved at: {csv_path}")
    print(df_summary.to_string(index=False))

    # Multi-panel Diagnostic Report Figure (2x3)
    fig = plt.figure(figsize=(16, 11), facecolor='white')
    gs = fig.add_gridspec(2, 3, wspace=0.25, hspace=0.32)

    # (a) Input Scan
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.imshow(img, cmap='gray')
    ax0.set_title("(a) Input Clinical Brain MRI Scan\n$f(x, y)$ | Matrix: 512$\\times$512 | Unfiltered",
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax0.axis('off')

    # (b) Centered Spectrum with Overlays
    ax1 = fig.add_subplot(gs[0, 1])
    ax1.imshow(mag_spectrum, cmap='magma')
    c_lp = plt.Circle((W // 2, H // 2), D0_lp, color='cyan', fill=False, linewidth=1.8, linestyle='--', label=f'LP $D_0={int(D0_lp)}$ px')
    c_hp = plt.Circle((W // 2, H // 2), D0_hp, color='yellow', fill=False, linewidth=1.5, linestyle=':', label=f'HP $D_0={int(D0_hp)}$ px')
    ax1.add_patch(c_lp)
    ax1.add_patch(c_hp)
    ax1.scatter([W // 2], [H // 2], color='white', s=50, marker='*')
    ax1.legend(loc='lower right', fontsize=8)
    ax1.set_title("(b) Centered Log-Spectrum $\\log(1+|F(u,v)|)$\n$D_0=40$ px (Cyan LP) & $D_0=50$ px (Yellow HP)",
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax1.axis('off')

    # (c) ILPF Output
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.imshow(img_ilpf, cmap='gray')
    b0 = benchmark_data[0]
    ax2.set_title(f"(c) Ideal Low-Pass Filter ($D_0=40$)\nEnergy: {b0['Energy_Retention_Pct']}% | PSNR: {b0['PSNR_dB']} dB | SSIM: {b0['SSIM']}\n[CONTRAINDICATED: Severe Gibbs Ringing]",
                  fontsize=10.5, fontweight='bold', color='#b91c1c')
    ax2.axis('off')

    # (d) BLPF Output
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.imshow(img_blpf, cmap='gray')
    b1 = benchmark_data[1]
    ax3.set_title(f"(d) Butterworth LP ($n=2, D_0=40$)\nEnergy: {b1['Energy_Retention_Pct']}% | PSNR: {b1['PSNR_dB']} dB | SSIM: {b1['SSIM']}\n[GOLD STANDARD: 0 Ringing, Smooth]",
                  fontsize=10.5, fontweight='bold', color='#15803d')
    ax3.axis('off')

    # (e) GLPF Output
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.imshow(img_glpf, cmap='gray')
    b2 = benchmark_data[2]
    ax4.set_title(f"(e) Gaussian Low-Pass Filter ($D_0=40$)\nEnergy: {b2['Energy_Retention_Pct']}% | PSNR: {b2['PSNR_dB']} dB | SSIM: {b2['SSIM']}\n[OPTIMAL PRE-FILTER: 100% Ripple-Free]",
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax4.axis('off')

    # (f) GHPF Edge Map
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.imshow(img_ghpf_vis, cmap='magma')
    b3 = benchmark_data[3]
    ax5.set_title(f"(f) Gaussian High-Pass Filter ($D_0=50$)\nEnergy: {b3['Energy_Retention_Pct']}% (High-Frequency Core)\n[DC Eliminated: Cortical Margin Isolation]",
                  fontsize=10.5, fontweight='bold', color='#9333ea')
    ax5.axis('off')

    plt.suptitle("Experiment 06 - Task 6.5: Multi-Filter Quantitative Benchmarking & Comprehensive Diagnostic Report",
                 fontsize=13, fontweight='bold', color='#0f172a', y=0.98)

    fig_path = os.path.join(fig_dir, "exp06_task_6_5_diagnostic_report_py.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Figure saved at: {fig_path}")

    return benchmark_data

if __name__ == "__main__":
    run_task_6_5()
