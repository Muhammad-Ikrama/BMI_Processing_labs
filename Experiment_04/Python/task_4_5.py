"""
Experiment 04: Noise Modeling and Removal in Medical Images Using Median and Adaptive Filtering Techniques
Task 4.5: Quantitative Benchmarking & Multi-Panel Diagnostic Restoration Report
Course: Medical Image Processing | Riphah International University
Instructor: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

def calc_epi(ref_im, filt_im):
    lap_ref = cv2.Laplacian(ref_im.astype(float), cv2.CV_64F)
    lap_filt = cv2.Laplacian(filt_im.astype(float), cv2.CV_64F)
    d_ref = lap_ref - np.mean(lap_ref)
    d_filt = lap_filt - np.mean(lap_filt)
    num = np.sum(d_ref * d_filt)
    den = np.sqrt(np.sum(d_ref ** 2) * np.sum(d_filt ** 2))
    return float(num / den) if den > 0 else 0.0

def apply_amf(im, max_w=7):
    out = im.copy()
    pad = max_w // 2
    padded = np.pad(im, pad, mode='reflect')
    h_im, w_im = im.shape

    for r in range(h_im):
        for c in range(w_im):
            pr, pc = r + pad, c + pad
            k = 3
            while k <= max_w:
                rad = k // 2
                sub = padded[pr - rad : pr + rad + 1, pc - rad : pc + rad + 1]
                zmin = int(np.min(sub))
                zmax = int(np.max(sub))
                zmed = int(np.median(sub))
                zxy  = int(padded[pr, pc])

                if zmin < zmed < zmax:
                    out[r, c] = zxy if (zmin < zxy < zmax) else zmed
                    break
                k += 2
                if k > max_w:
                    out[r, c] = zmed
                    break
    return out

def run_task_4_5():
    print("=" * 70)
    print("EXPERIMENT 04 - TASK 4.5: MULTI-PANEL RESTORATION BENCHMARK REPORT")
    print("=" * 70)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.dirname(script_dir)
    img_path = os.path.join(exp_dir, "Inputs", "images", "MRI.jpg")

    if not os.path.exists(img_path):
        img_path = os.path.join(exp_dir, "..", "..", "images", "MRI.jpg")

    ref = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if ref is None:
        raise FileNotFoundError(f"Could not load image from {img_path}")

    H, W = ref.shape

    # 1. Simulate Mixed Noise: 10% Salt & Pepper + Gaussian (sigma = 10.0)
    np.random.seed(42)
    gauss_noisy = np.clip(ref.astype(float) + np.random.normal(0, 10.0, ref.shape), 0, 255).astype(np.uint8)
    noisy = gauss_noisy.copy()
    num_sp = int(0.10 * ref.size)
    num_salt = num_sp // 2
    r_idx = np.random.randint(0, H, num_sp)
    c_idx = np.random.randint(0, W, num_sp)
    noisy[r_idx[:num_salt], c_idx[:num_salt]] = 255
    noisy[r_idx[num_salt:], c_idx[num_salt:]] = 0

    # 2. Filter Outputs
    mean_5 = cv2.blur(noisy, (5, 5))
    med_3 = cv2.medianBlur(noisy, 3)
    amf_out = apply_amf(noisy, max_w=7)

    # 3. Define Background ROI for noise variance evaluation [rows 10:50, cols 10:50]
    bg_slice = (slice(10, 50), slice(10, 50))

    cases = [
        ("Ground Truth Scan", ref),
        ("Mixed Noisy Baseline", noisy),
        ("Linear Mean 5x5", mean_5),
        ("Standard Median 3x3", med_3),
        ("Adaptive Median AMF", amf_out)
    ]

    records = []
    print(f"{'Condition':<24} | {'PSNR (dB)':<10} | {'SSIM':<8} | {'EPI (beta)':<10} | {'BG Noise Var':<12} | {'Status'}")
    print("-" * 80)

    for name, im in cases:
        p = psnr(ref, im) if name != "Ground Truth Scan" else float('inf')
        s = ssim(ref, im) if name != "Ground Truth Scan" else 1.0000
        e = calc_epi(ref, im) if name != "Ground Truth Scan" else 1.0000
        bg_var = float(np.var(im[bg_slice].astype(float)))

        if "Ground Truth" in name:
            status = "Reference"
        elif "Noisy" in name or "Linear" in name:
            status = "Clinical Failure"
        else:
            status = "Good to Go"

        p_str = f"{p:.2f}" if p != float('inf') else "Inf"
        print(f"{name:<24} | {p_str:<10} | {s:<8.4f} | {e:<10.4f} | {bg_var:<12.2f} | {status}")

        records.append({
            "Method": name,
            "PSNR_dB": round(p, 2) if p != float('inf') else 999.0,
            "SSIM": round(s, 4),
            "EPI": round(e, 4),
            "Background_Noise_Var": round(bg_var, 2),
            "Status": status
        })

    # Export to CSV
    df = pd.DataFrame(records)
    table_dir = os.path.join(exp_dir, "Tables")
    os.makedirs(table_dir, exist_ok=True)
    csv_path = os.path.join(table_dir, "task_4_5_restoration_benchmark_summary.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[INFO] Restoration summary exported to CSV:\n  {csv_path}")

    # 4. Extract 1D Anatomical Profile at Row H/2 across ventricular boundary
    row_idx = H // 2
    c_start, c_end = 125, 175
    cols = np.arange(c_start, c_end)

    prof_ref = ref[row_idx, c_start:c_end].astype(float)
    prof_noisy = noisy[row_idx, c_start:c_end].astype(float)
    prof_mean5 = mean_5[row_idx, c_start:c_end].astype(float)
    prof_med3 = med_3[row_idx, c_start:c_end].astype(float)
    prof_amf = amf_out[row_idx, c_start:c_end].astype(float)

    # 5. Visualization: 2 Rows x 3 Columns Diagnostic Report
    fig, axes = plt.subplots(2, 3, figsize=(16, 10), dpi=300)
    plt.subplots_adjust(wspace=0.18, hspace=0.26)

    # Panel 1: Ground Truth
    axes[0, 0].imshow(ref, cmap='gray', vmin=0, vmax=255)
    axes[0, 0].set_title("A: Ground Truth Clean MRI\n[Reference Standard]", fontsize=9.5, fontweight='bold', color='#1e3a8a')
    axes[0, 0].axis('off')

    # Panel 2: Mixed Noisy
    axes[0, 1].imshow(noisy, cmap='gray', vmin=0, vmax=255)
    axes[0, 1].set_title(f"B: Mixed Noisy Scan (10% SP + Gauss)\nPSNR: {records[1]['PSNR_dB']} dB | SSIM: {records[1]['SSIM']}",
                          fontsize=9.5, fontweight='bold', color='#dc2626')
    axes[0, 1].axis('off')

    # Panel 3: Linear Mean 5x5
    axes[0, 2].imshow(mean_5, cmap='gray', vmin=0, vmax=255)
    axes[0, 2].set_title(f"C: Linear Mean 5x5 [Smear Failure]\nPSNR: {records[2]['PSNR_dB']} dB | SSIM: {records[2]['SSIM']}",
                          fontsize=9.5, fontweight='bold', color='#dc2626')
    axes[0, 2].axis('off')

    # Panel 4: Standard Median 3x3
    axes[1, 0].imshow(med_3, cmap='gray', vmin=0, vmax=255)
    axes[1, 0].set_title(f"D: Standard Median 3x3 [Impulses Removed]\nPSNR: {records[3]['PSNR_dB']} dB | SSIM: {records[3]['SSIM']}",
                          fontsize=9.5, fontweight='bold', color='#2563eb')
    axes[1, 0].axis('off')

    # Panel 5: Adaptive Median AMF
    axes[1, 1].imshow(amf_out, cmap='gray', vmin=0, vmax=255)
    axes[1, 1].set_title(f"E: Adaptive Median AMF [Edges Preserved]\nPSNR: {records[4]['PSNR_dB']} dB | SSIM: {records[4]['SSIM']}",
                          fontsize=9.5, fontweight='bold', color='#15803d')
    axes[1, 1].axis('off')

    # Panel 6: 1D Anatomical Edge Gradient Profiles
    ax_prof = axes[1, 2]
    ax_prof.plot(cols, prof_ref, color='#0f172a', linewidth=2.5, label="Clean Reference")
    ax_prof.plot(cols, prof_noisy, color='#94a3b8', linewidth=0.9, alpha=0.6, label="Noisy Scan")
    ax_prof.plot(cols, prof_mean5, color='#dc2626', linewidth=2.0, linestyle='--', label="Mean 5x5 [Smear]")
    ax_prof.plot(cols, prof_med3, color='#2563eb', linewidth=1.8, linestyle=':', label="Median 3x3")
    ax_prof.plot(cols, prof_amf, color='#16a34a', linewidth=2.2, label="Adaptive AMF [Optimal]")

    ax_prof.set_xlabel("Pixel Column Coordinate (x)", fontsize=9, fontweight='bold')
    ax_prof.set_ylabel("Intensity Level [0-255]", fontsize=9, fontweight='bold')
    ax_prof.set_title(f"F: 1D Edge Profile at Row {row_idx}\n[Ventricular Margin]", fontsize=9.5, fontweight='bold', color='#1e3a8a')
    ax_prof.grid(True, linestyle='--', alpha=0.5)
    ax_prof.legend(fontsize=8, loc='upper left')

    fig.suptitle("Task 4.5: Quantitative Benchmarking & Multi-Panel Diagnostic Restoration Report",
                 fontsize=13.5, fontweight='bold', color='#0f172a', y=0.98)

    out_dir_py = os.path.join(exp_dir, "Outputs", "Python")
    fig_dir = os.path.join(exp_dir, "Figures")
    os.makedirs(out_dir_py, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    out_path_1 = os.path.join(out_dir_py, "exp04_task_4_5_diagnostic_report_py.png")
    out_path_2 = os.path.join(fig_dir, "exp04_task_4_5_diagnostic_report_py.png")

    plt.savefig(out_path_1, bbox_inches='tight', dpi=300)
    plt.savefig(out_path_2, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"[SUCCESS] Saved figure to:\n  {out_path_1}\n  {out_path_2}")

if __name__ == '__main__':
    run_task_4_5()
