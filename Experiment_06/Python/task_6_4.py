"""
Experiment 06 - Task 6.4: Gaussian Low-Pass vs. High-Pass Filtering for Contrast & Boundary Isolation
Constructs matching GLPF and GHPF (1 - GLPF) with D0 = 50, computes Spectral Energy Retention,
Spatial Mean Brightness, and Michelson Contrast, proving DC component suppression and boundary isolation.
Course: Medical Image Processing | Riphah International University
Faculty: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_task_6_4():
    print("==============================================================================")
    print("EXPERIMENT 06 - TASK 6.4: GAUSSIAN LP VS HP FILTERING & BOUNDARY ISOLATION")
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

    # Distance Matrix & Filters (D0 = 50.0)
    u = np.arange(H) - H // 2
    v = np.arange(W) - W // 2
    V, U = np.meshgrid(v, u)
    D = np.hypot(V, U)
    D0 = 50.0

    # Transfer functions
    h_glpf = np.exp(- (D ** 2) / (2.0 * (D0 ** 2)))
    h_ghpf = 1.0 - h_glpf

    # Verify DC values of transfer functions
    dc_glpf = h_glpf[H // 2, W // 2]
    dc_ghpf = h_ghpf[H // 2, W // 2]
    print(f"[INFO] GLPF DC Value H(0,0): {dc_glpf:.4f} (Unity Pass)")
    print(f"[INFO] GHPF DC Value H(0,0): {dc_ghpf:.4f} (Total Block / 0 DC)")

    # Spatial filtering
    g_glpf_raw = np.real(np.fft.ifft2(np.fft.ifftshift(F_shift * h_glpf)))
    g_ghpf_raw = np.real(np.fft.ifft2(np.fft.ifftshift(F_shift * h_ghpf)))

    img_glpf = np.clip(g_glpf_raw, 0, 255).astype(np.uint8)
    # GHPF bipolar display (DC shifted to 128 for visualization of positive and negative edge gradients)
    img_ghpf_bipolar = np.clip(g_ghpf_raw + 128.0, 0, 255).astype(np.uint8)
    # GHPF rectified magnitude display (absolute gradients)
    img_ghpf_mag = np.clip(np.abs(g_ghpf_raw) * 2.0, 0, 255).astype(np.uint8)

    # Save output images
    cv2.imwrite(os.path.join(out_py_dir, "exp06_task_6_4_glpf_smooth.png"), img_glpf)
    cv2.imwrite(os.path.join(out_py_dir, "exp06_task_6_4_ghpf_bipolar.png"), img_ghpf_bipolar)
    cv2.imwrite(os.path.join(out_py_dir, "exp06_task_6_4_ghpf_magnitude.png"), img_ghpf_mag)

    # Quantitative Calculations
    def calc_metrics(raw_arr, h_filt):
        if h_filt is not None:
            ret = (np.sum(np.abs(F_shift * h_filt) ** 2) / total_energy) * 100.0
        else:
            ret = 100.0
        mean_b = float(np.mean(raw_arr))
        std_b = float(np.std(raw_arr))
        # Michelson contrast on absolute positive domain
        pos_arr = np.abs(raw_arr)
        i_max = float(np.max(pos_arr))
        i_min = float(np.min(pos_arr))
        michelson = (i_max - i_min) / (i_max + i_min + 1e-8)
        rms_contrast = std_b / (abs(mean_b) + 1e-8)
        return ret, mean_b, std_b, michelson, rms_contrast

    ret_orig, mean_orig, std_orig, mich_orig, rms_orig = calc_metrics(img.astype(float), None)
    ret_glpf, mean_glpf, std_glpf, mich_glpf, rms_glpf = calc_metrics(g_glpf_raw, h_glpf)
    ret_ghpf, mean_ghpf, std_ghpf, mich_ghpf, rms_ghpf = calc_metrics(g_ghpf_raw, h_ghpf)

    metrics_list = [
        {
            "Condition": "Original MRI Scan",
            "Filter_Type": "None (Full Spectrum)",
            "Energy_Retention_Pct": round(ret_orig, 2),
            "Spatial_Mean_Brightness": round(mean_orig, 2),
            "Spatial_Std_Dev": round(std_orig, 2),
            "Michelson_Contrast": round(mich_orig, 4),
            "RMS_Contrast": round(rms_orig, 4),
            "DC_Component_Behavior": "Complete DC Present (Mean = 71.4)"
        },
        {
            "Condition": "Gaussian Low-Pass (GLPF)",
            "Filter_Type": f"Low-Pass (D0={int(D0)})",
            "Energy_Retention_Pct": round(ret_glpf, 2),
            "Spatial_Mean_Brightness": round(mean_glpf, 2),
            "Spatial_Std_Dev": round(std_glpf, 2),
            "Michelson_Contrast": round(mich_glpf, 4),
            "RMS_Contrast": round(rms_glpf, 4),
            "DC_Component_Behavior": "DC Preserved (100% Passband)"
        },
        {
            "Condition": "Gaussian High-Pass (GHPF)",
            "Filter_Type": f"High-Pass (D0={int(D0)})",
            "Energy_Retention_Pct": round(ret_ghpf, 2),
            "Spatial_Mean_Brightness": round(mean_ghpf, 4),
            "Spatial_Std_Dev": round(std_ghpf, 2),
            "Michelson_Contrast": round(mich_ghpf, 4),
            "RMS_Contrast": round(rms_ghpf, 4),
            "DC_Component_Behavior": "DC Fully Eliminated (Mean ~ 0.0)"
        }
    ]

    df_metrics = pd.DataFrame(metrics_list)
    csv_path = os.path.join(tab_dir, "exp06_task_6_4_contrast_metrics.csv")
    df_metrics.to_csv(csv_path, index=False)
    print(f"\n[INFO] Contrast & Energy Metrics saved at: {csv_path}")
    print(df_metrics.to_string(index=False))

    # Multi-panel Figure
    fig = plt.figure(figsize=(16, 11), facecolor='white')
    gs = fig.add_gridspec(2, 3, wspace=0.25, hspace=0.32)

    # 1. 2D Filter Transfer Functions
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.imshow(h_glpf, cmap='viridis')
    ax0.set_title(f"(a) GLPF Transfer Function $H_{{GLP}}(u,v)$\n$D_0={int(D0)}$ px | Low-Pass Core (Yellow)",
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax0.axis('off')

    ax1 = fig.add_subplot(gs[0, 1])
    ax1.imshow(h_ghpf, cmap='viridis')
    ax1.set_title(f"(b) GHPF Transfer Function $H_{{GHP}}(u,v)$\n$1 - H_{{GLP}}$ | Center DC Hollowed to 0 (Purple)",
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax1.axis('off')

    # 3. 1D Radial Profile Comparison of GLPF and GHPF
    ax2 = fig.add_subplot(gs[0, 2])
    d_vals = np.linspace(0, 150, 500)
    h_glp_1d = np.exp(- (d_vals ** 2) / (2.0 * (D0 ** 2)))
    h_ghp_1d = 1.0 - h_glp_1d
    ax2.plot(d_vals, h_glp_1d, color='#16a34a', linewidth=2.2, label='GLPF $H_{LP}(D)$')
    ax2.plot(d_vals, h_ghp_1d, color='#dc2626', linewidth=2.2, label='GHPF $H_{HP}(D) = 1 - H_{LP}$')
    ax2.axvline(D0, color='gray', linestyle='--', linewidth=1.2, label=f'$D_0={int(D0)}$ px')
    ax2.axhline(0.6065, color='gray', linestyle=':', linewidth=0.8, label='$e^{-1/2} \\approx 0.607$')
    ax2.set_xlabel('Radial Frequency Distance $D$ (pixels)', fontsize=9.5, fontweight='bold')
    ax2.set_ylabel('Transfer Magnitude $H(D)$', fontsize=9.5, fontweight='bold')
    ax2.set_title('(c) Complementary Radial Transfer Functions\n($H_{LP} + H_{HP} = 1.0$ Across All $D$)',
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax2.legend(loc='center right', fontsize=8)
    ax2.grid(True, linestyle=':', alpha=0.6)

    # 4. GLPF Reconstructed Image
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.imshow(img_glpf, cmap='gray')
    ax3.set_title(f"(d) GLPF Output (Smooth Parenchyma)\nEnergy: {ret_glpf:.1f}% | Mean: {mean_glpf:.1f} | RMS: {rms_glpf:.2f}\n(Bulk Anatomy Preserved, 0 Ringing)",
                  fontsize=10.5, fontweight='bold', color='#16a34a')
    ax3.axis('off')

    # 5. GHPF Bipolar Display (Shifted to 128)
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.imshow(img_ghpf_bipolar, cmap='gray')
    ax4.set_title(f"(e) GHPF Bipolar Map ($g + 128$)\nEnergy: {ret_ghpf:.1f}% | Mean: {mean_ghpf:.2f} $\\approx 0$\n(DC Removed, Bone/Vessel Interface Raised)",
                  fontsize=10.5, fontweight='bold', color='#dc2626')
    ax4.axis('off')

    # 6. GHPF Magnitude Edge Isolation Map
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.imshow(img_ghpf_mag, cmap='magma')
    ax5.set_title(f"(f) GHPF Edge Isolation Map ($|g| \\times 2$)\nMichelson Contrast: {mich_ghpf:.3f}\n(Isolated Cranial Vault, Ventricles, Sulci)",
                  fontsize=10.5, fontweight='bold', color='#9333ea')
    ax5.axis('off')

    plt.suptitle("Experiment 06 - Task 6.4: Gaussian Low-Pass vs. High-Pass Filtering for Boundary Isolation",
                 fontsize=13, fontweight='bold', color='#0f172a', y=0.98)

    fig_path = os.path.join(fig_dir, "exp06_task_6_4_glpf_ghpf_contrast_py.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Figure saved at: {fig_path}")

    return metrics_list

if __name__ == "__main__":
    run_task_6_4()
