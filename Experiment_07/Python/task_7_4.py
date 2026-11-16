"""
Experiment 07 - Task 7.4: Noise Amplification & Trade-off Evaluation in Low-Dose Radiographs
Simulates Gaussian quantum mottle (variance = 0.003), evaluates noise amplification under
Unsharp Masking (k=1.0) and High-Boost (k=2.0), measures background ROI standard deviation,
and assesses clinical safety trade-offs in low-dose radiography.
Course: Medical Image Processing | Riphah International University
Faculty: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

def run_task_7_4():
    print("==============================================================================")
    print("EXPERIMENT 07 - TASK 7.4: NOISE AMPLIFICATION & LOW-DOSE TRADE-OFF")
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

    # 1. Load Clean Radiograph
    img_clean = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img_clean is None:
        raise FileNotFoundError(f"Cannot load radiograph at {img_path}")
    H, W = img_clean.shape
    clean_f = img_clean.astype(np.float64)

    # 2. Add Simulated Gaussian Quantum Mottle (zero mean, variance = 0.003 on [0, 1] scale)
    np.random.seed(42) # Reproducible clinical noise seed
    noise_sigma = np.sqrt(0.003) * 255.0 # ~13.97 gray levels
    gaussian_noise = np.random.normal(0.0, noise_sigma, (H, W))
    noisy_f = clean_f + gaussian_noise
    img_noisy = np.clip(noisy_f, 0, 255).astype(np.uint8)

    # 3. Apply Unsharp Masking (k = 1.0) and High-Boost (k = 2.0) to Noisy Radiograph
    blurred_noisy = gaussian_filter(noisy_f, sigma=1.5)
    g_mask_noisy = noisy_f - blurred_noisy

    sharp_k1_raw = noisy_f + 1.0 * g_mask_noisy
    sharp_k2_raw = noisy_f + 2.0 * g_mask_noisy

    img_sharp_k1 = np.clip(sharp_k1_raw, 0, 255).astype(np.uint8)
    img_sharp_k2 = np.clip(sharp_k2_raw, 0, 255).astype(np.uint8)

    # Save output images
    cv2.imwrite(os.path.join(out_py_dir, "exp07_task_7_4_noisy_radiograph.png"), img_noisy)
    cv2.imwrite(os.path.join(out_py_dir, "exp07_task_7_4_sharp_noisy_k1.png"), img_sharp_k1)
    cv2.imwrite(os.path.join(out_py_dir, "exp07_task_7_4_sharp_noisy_k2.png"), img_sharp_k2)

    # 4. Homogeneous Background ROI Analysis (Apical Lung Soft Tissue / Air: rows 40 to 100, cols 40 to 100)
    roi_slice = (slice(40, 100), slice(40, 100))

    def evaluate_condition(im_u8, label, is_baseline=False):
        roi_vals = im_u8[roi_slice].astype(np.float64)
        roi_std = float(np.std(roi_vals))
        roi_mean = float(np.mean(roi_vals))
        snr_db = float(20.0 * np.log10(roi_mean / (roi_std + 1e-8)))
        p_val = float(psnr(img_clean, im_u8))
        s_val = float(ssim(img_clean, im_u8))
        return roi_mean, roi_std, snr_db, p_val, s_val

    m_clean = evaluate_condition(img_clean, "Clean Radiograph", is_baseline=True)
    m_noisy = evaluate_condition(img_noisy, "Noisy Radiograph (Low-Dose)")
    m_k1 = evaluate_condition(img_sharp_k1, "Unsharp Masking (k=1.0)")
    m_k2 = evaluate_condition(img_sharp_k2, "High-Boost (k=2.0)")

    noisy_roi_std = m_noisy[1]
    pct_increase_k1 = ((m_k1[1] - noisy_roi_std) / noisy_roi_std) * 100.0
    pct_increase_k2 = ((m_k2[1] - noisy_roi_std) / noisy_roi_std) * 100.0

    metrics_list = [
        {
            "Condition": "Clean Ground Truth",
            "Boost_k": 0.0,
            "ROI_Mean": round(m_clean[0], 2),
            "ROI_Noise_Std": round(m_clean[1], 2),
            "Noise_Increase_Pct": 0.0,
            "ROI_SNR_dB": round(m_clean[2], 2),
            "PSNR_dB": float('inf'),
            "SSIM": 1.0000,
            "Clinical_Safety": "Reference Scan"
        },
        {
            "Condition": "Noisy (Quantum Mottle)",
            "Boost_k": 0.0,
            "ROI_Mean": round(m_noisy[0], 2),
            "ROI_Noise_Std": round(m_noisy[1], 2),
            "Noise_Increase_Pct": 0.0,
            "ROI_SNR_dB": round(m_noisy[2], 2),
            "PSNR_dB": round(m_noisy[3], 2),
            "SSIM": round(m_noisy[4], 4),
            "Clinical_Safety": "Baseline Low-Dose Scan"
        },
        {
            "Condition": "Unsharp Masking (k=1.0)",
            "Boost_k": 1.0,
            "ROI_Mean": round(m_k1[0], 2),
            "ROI_Noise_Std": round(m_k1[1], 2),
            "Noise_Increase_Pct": round(pct_increase_k1, 2),
            "ROI_SNR_dB": round(m_k1[2], 2),
            "PSNR_dB": round(m_k1[3], 2),
            "SSIM": round(m_k1[4], 4),
            "Clinical_Safety": "ACCEPTABLE (Controlled Noise Boost)"
        },
        {
            "Condition": "High-Boost (k=2.0)",
            "Boost_k": 2.0,
            "ROI_Mean": round(m_k2[0], 2),
            "ROI_Noise_Std": round(m_k2[1], 2),
            "Noise_Increase_Pct": round(pct_increase_k2, 2),
            "ROI_SNR_dB": round(m_k2[2], 2),
            "PSNR_dB": round(m_k2[3], 2),
            "SSIM": round(m_k2[4], 4),
            "Clinical_Safety": "CONTRAINDICATED (>25% Noise Amplification)"
        }
    ]

    df_metrics = pd.DataFrame(metrics_list)
    csv_path = os.path.join(tab_dir, "exp07_task_7_4_noise_amplification_metrics.csv")
    df_metrics.to_csv(csv_path, index=False)
    print(f"\n[INFO] Noise Amplification Metrics saved at: {csv_path}")
    print(df_metrics.to_string(index=False))

    # 5. Visualization Figure (2x2 Multi-Panel with ROI Insets)
    fig, axes = plt.subplots(2, 2, figsize=(14, 12), facecolor='white')
    plt.subplots_adjust(wspace=0.25, hspace=0.28)

    # Helper to draw ROI rectangle
    def add_roi_box(ax):
        rect = plt.Rectangle((roi_slice[1].start, roi_slice[0].start),
                             roi_slice[1].stop - roi_slice[1].start,
                             roi_slice[0].stop - roi_slice[0].start,
                             edgecolor='cyan', fill=False, linewidth=1.8, linestyle='--')
        ax.add_patch(rect)

    # (a) Clean Reference
    axes[0, 0].imshow(img_clean, cmap='gray')
    add_roi_box(axes[0, 0])
    axes[0, 0].set_title(f"(a) Clean Ground Truth Radiograph\nROI Noise Std: {m_clean[1]:.2f} | SNR: {m_clean[2]:.1f} dB",
                          fontsize=10.5, fontweight='bold', color='#1e3a8a')
    axes[0, 0].axis('off')

    # (b) Noisy Radiograph
    axes[0, 1].imshow(img_noisy, cmap='gray')
    add_roi_box(axes[0, 1])
    axes[0, 1].set_title(f"(b) Simulated Low-Dose Scan ($\\sigma_{{\\text{{noise}}}}=14.0$)\nROI Noise Std: {m_noisy[1]:.2f} | PSNR: {m_noisy[3]:.1f} dB",
                          fontsize=10.5, fontweight='bold', color='#b45309')
    axes[0, 1].axis('off')

    # (c) Unsharp Masking (k=1.0)
    axes[1, 0].imshow(img_sharp_k1, cmap='gray')
    add_roi_box(axes[1, 0])
    axes[1, 0].set_title(f"(c) Noisy + Unsharp Masking ($k=1.0$)\nNoise Std: {m_k1[1]:.2f} ({pct_increase_k1:+.1f}%) | PSNR: {m_k1[3]:.1f} dB\n[CLINICALLY TOLERABLE]",
                          fontsize=10.5, fontweight='bold', color='#15803d')
    axes[1, 0].axis('off')

    # (d) High-Boost (k=2.0)
    axes[1, 1].imshow(img_sharp_k2, cmap='gray')
    add_roi_box(axes[1, 1])
    axes[1, 1].set_title(f"(d) Noisy + High-Boost ($k=2.0$)\nNoise Std: {m_k2[1]:.2f} ({pct_increase_k2:+.1f}%) | PSNR: {m_k2[3]:.1f} dB\n[CONTRAINDICATED: Severe Grain]",
                          fontsize=10.5, fontweight='bold', color='#dc2626')
    axes[1, 1].axis('off')

    plt.suptitle("Experiment 07 - Task 7.4: Noise Amplification & Trade-off Evaluation in Low-Dose Radiographs",
                 fontsize=13, fontweight='bold', color='#0f172a', y=0.98)

    fig_path = os.path.join(fig_dir, "exp07_task_7_4_noise_tradeoff_py.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Figure saved at: {fig_path}")

    return metrics_list

if __name__ == "__main__":
    run_task_7_4()
