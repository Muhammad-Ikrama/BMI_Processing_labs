"""
Experiment 06 - Task 6.1: 2-D Discrete Fourier Transform & Magnitude Spectrum Computation
Computes uncentered and centered 2D-DFT, log-compressed magnitude spectra, phase spectrum,
DC component localization, energy distribution analysis, and crosshair windowing artifact explanation.
Course: Medical Image Processing | Riphah International University
Faculty: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def run_task_6_1():
    print("==============================================================================")
    print("EXPERIMENT 06 - TASK 6.1: 2-D DFT & MAGNITUDE SPECTRUM COMPUTATION")
    print("==============================================================================")

    # Resolve paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.abspath(os.path.join(script_dir, ".."))
    img_path = os.path.join(exp_dir, "Inputs", "images", "MRI.jpg")
    if not os.path.exists(img_path):
        img_path = os.path.join(exp_dir, "..", "..", "images", "MRI.jpg")

    out_py_dir = os.path.join(exp_dir, "Outputs", "Python")
    fig_dir = os.path.join(exp_dir, "Figures")
    os.makedirs(out_py_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    # Load image
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Cannot load image at {img_path}")
    H, W = img.shape
    mean_intensity = np.mean(img)

    # 1. Forward 2D-DFT
    F_raw = np.fft.fft2(img.astype(float))
    F_shift = np.fft.fftshift(F_raw)

    # 2. Magnitude and Phase Spectra
    mag_raw = np.abs(F_raw)
    mag_shift = np.abs(F_shift)
    log_mag_raw = np.log1p(mag_raw)
    log_mag_shift = np.log1p(mag_shift)
    phase_shift = np.angle(F_shift)

    # 3. DC Component Analysis
    # In uncentered DFT: DC component is at (0, 0)
    # In centered DFT: DC component is at (H//2, W//2)
    dc_uncentered_coord = (0, 0)
    dc_centered_coord = (H // 2, W // 2)

    dc_val_uncentered = mag_raw[dc_uncentered_coord]
    dc_val_centered = mag_shift[dc_centered_coord]
    theoretical_dc = np.sum(img.astype(float))

    total_energy = np.sum(mag_shift ** 2)
    dc_energy = dc_val_centered ** 2
    dc_energy_fraction = (dc_energy / total_energy) * 100.0

    print(f"[INFO] Image Dimensions: {H} x {W} pixels")
    print(f"[INFO] Spatial Mean Intensity: {mean_intensity:.2f}")
    print(f"[INFO] Theoretical DC Component (Sum of Pixels): {theoretical_dc:.2f}")
    print(f"[INFO] Uncentered DC Coordinate: {dc_uncentered_coord} | Measured DC Value: {dc_val_uncentered:.2f}")
    print(f"[INFO] Centered DC Coordinate: {dc_centered_coord} | Measured DC Value: {dc_val_centered:.2f}")
    print(f"[INFO] Total Spectral Energy: {total_energy:.3e}")
    print(f"[INFO] DC Energy Fraction: {dc_energy_fraction:.2f}% of Total Power")

    # 4. Radial Energy Accumulation Curve
    u = np.arange(H) - H // 2
    v = np.arange(W) - W // 2
    V, U = np.meshgrid(v, u)
    D = np.hypot(V, U)

    max_radius = int(min(H, W) // 2)
    radial_distances = np.arange(1, max_radius + 1)
    cumulative_energy = []
    for r in radial_distances:
        mask = (D <= r)
        retained_energy = np.sum(mag_shift[mask] ** 2)
        cumulative_energy.append((retained_energy / total_energy) * 100.0)
    cumulative_energy = np.array(cumulative_energy)

    r_90 = radial_distances[np.argmax(cumulative_energy >= 90.0)]
    r_95 = radial_distances[np.argmax(cumulative_energy >= 95.0)]
    r_99 = radial_distances[np.argmax(cumulative_energy >= 99.0)]
    print(f"[INFO] Radial Radius for 90% Energy Retention: D <= {r_90} pixels")
    print(f"[INFO] Radial Radius for 95% Energy Retention: D <= {r_95} pixels")
    print(f"[INFO] Radial Radius for 99% Energy Retention: D <= {r_99} pixels")

    # 5. Crosshair Arm Intensity Profile Analysis
    # Profile along center horizontal line (u = 0, along v)
    horiz_arm = log_mag_shift[H // 2, :]
    # Diagonal profile (45 degrees)
    diag_indices = [int(i) for i in np.linspace(0, min(H, W) - 1, min(H, W))]
    diag_profile = np.array([log_mag_shift[i, i] for i in diag_indices])

    # Save output images
    norm_log_raw = cv2.normalize(log_mag_raw, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    norm_log_shift = cv2.normalize(log_mag_shift, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    norm_phase = cv2.normalize(phase_shift, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    cv2.imwrite(os.path.join(out_py_dir, "exp06_task_6_1_raw_log_spectrum.png"), norm_log_raw)
    cv2.imwrite(os.path.join(out_py_dir, "exp06_task_6_1_centered_log_spectrum.png"), norm_log_shift)
    cv2.imwrite(os.path.join(out_py_dir, "exp06_task_6_1_phase_spectrum.png"), norm_phase)

    # Multi-panel visualization
    fig = plt.figure(figsize=(16, 10), facecolor='white')
    gs = fig.add_gridspec(2, 3, wspace=0.25, hspace=0.32)

    # (a) Input Image
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.imshow(img, cmap='gray')
    ax0.set_title(f"(a) Clinical Brain MRI Scan\n$f(x, y)$ | Size: {W}$\\times${H} px | Mean: {mean_intensity:.1f}",
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax0.axis('off')

    # (b) Uncentered Spectrum
    ax1 = fig.add_subplot(gs[0, 1])
    ax1.imshow(log_mag_raw, cmap='inferno')
    ax1.scatter([0], [0], color='cyan', s=60, marker='o', edgecolors='black', label='DC (0, 0)')
    ax1.legend(loc='lower right', fontsize=8)
    ax1.set_title("(b) Uncentered Log-Spectrum $\\log(1+|F(u,v)|)$\nDC Component at Top-Left Corner (0,0)",
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax1.axis('off')

    # (c) Centered Spectrum
    ax2 = fig.add_subplot(gs[0, 2])
    im2 = ax2.imshow(log_mag_shift, cmap='inferno')
    ax2.scatter([W // 2], [H // 2], color='cyan', s=70, marker='*', edgecolors='black', label=f'DC ({W//2}, {H//2})')
    # Draw crosshair pointers
    ax2.axhline(H // 2, color='white', linestyle=':', alpha=0.4, linewidth=0.8)
    ax2.axvline(W // 2, color='white', linestyle=':', alpha=0.4, linewidth=0.8)
    ax2.legend(loc='lower right', fontsize=8)
    ax2.set_title(f"(c) Centered Log-Spectrum (via fftshift)\nCentral DC Star ({W//2}, {H//2}) & Crosshairs",
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax2.axis('off')

    # (d) Phase Spectrum
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.imshow(phase_shift, cmap='hsv')
    ax3.set_title("(d) 2-D Phase Spectrum $\\phi(u, v) = \\angle F(u,v)$\nEncodes Structural Spatial Alignment",
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax3.axis('off')

    # (e) Cumulative Energy Retention Curve
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(radial_distances, cumulative_energy, color='#2563eb', linewidth=2.2, label='Cumulative Energy %')
    ax4.axhline(90.0, color='#10b981', linestyle='--', linewidth=1.2, label=f'90% at $D\\leq{r_90}$ px')
    ax4.axhline(95.0, color='#f59e0b', linestyle='--', linewidth=1.2, label=f'95% at $D\\leq{r_95}$ px')
    ax4.axhline(99.0, color='#ef4444', linestyle='--', linewidth=1.2, label=f'99% at $D\\leq{r_99}$ px')
    ax4.set_xlabel('Radial Frequency Radius $D$ (pixels)', fontsize=9.5, fontweight='bold')
    ax4.set_ylabel('Spectral Energy Retained (%)', fontsize=9.5, fontweight='bold')
    ax4.set_title('(e) Radial Energy Concentration Curve\n(>95% Energy in Low-Frequency Core)',
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax4.set_xlim(0, 150)
    ax4.set_ylim(50, 100.5)
    ax4.legend(loc='lower right', fontsize=8)
    ax4.grid(True, linestyle=':', alpha=0.6)

    # (f) Crosshair vs Off-Axis Profile Analysis
    ax5 = fig.add_subplot(gs[1, 2])
    v_axis = np.arange(W) - W // 2
    diag_axis = np.linspace(-len(diag_profile)//2, len(diag_profile)//2, len(diag_profile))
    ax5.plot(v_axis, horiz_arm, color='#dc2626', linewidth=1.8, label='Horizontal Crosshair ($u=0$)')
    ax5.plot(diag_axis, diag_profile, color='#475569', linewidth=1.5, linestyle='--', label='Diagonal Transect ($45^\\circ$)')
    ax5.set_xlabel('Frequency Coordinate Distance from Center', fontsize=9.5, fontweight='bold')
    ax5.set_ylabel('Log-Magnitude Intensity', fontsize=9.5, fontweight='bold')
    ax5.set_title('(f) Crosshair Boundary Artifact vs Diagonal\n(Finite Rectangular Windowing Leakage)',
                  fontsize=10.5, fontweight='bold', color='#1e3a8a')
    ax5.set_xlim(-150, 150)
    ax5.legend(loc='upper right', fontsize=8)
    ax5.grid(True, linestyle=':', alpha=0.6)

    plt.suptitle("Experiment 06 - Task 6.1: 2-D Discrete Fourier Transform & Magnitude Spectrum Analysis",
                 fontsize=13, fontweight='bold', color='#0f172a', y=0.98)

    fig_path = os.path.join(fig_dir, "exp06_task_6_1_dft_spectrum_py.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Figure saved at: {fig_path}")

    return {
        "dc_uncentered": dc_uncentered_coord,
        "dc_centered": dc_centered_coord,
        "total_energy": float(total_energy),
        "dc_energy_fraction": float(dc_energy_fraction),
        "r_90": int(r_90),
        "r_95": int(r_95),
        "r_99": int(r_99)
    }

if __name__ == "__main__":
    run_task_6_1()
