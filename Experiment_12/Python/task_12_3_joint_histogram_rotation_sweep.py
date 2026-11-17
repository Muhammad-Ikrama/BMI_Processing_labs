"""
Experiment 12: Task 12.3 - 2D Joint Histogram & Mutual Information Rotation Sweep
Course: Medical Image Processing (BMI-701) | Riphah International University
Student: Muhammad Ikrama (Reg ID: 60140)
Instructor: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def compute_mi_and_metrics(fixed, moving):
    h2d, _, _ = np.histogram2d(fixed.ravel(), moving.ravel(), bins=64, range=[[0, 256], [0, 256]])
    pxy = h2d / float(np.sum(h2d))
    px = np.sum(pxy, axis=1)
    py = np.sum(pxy, axis=0)
    nz = pxy > 0
    
    # Entropies
    h_f = -np.sum(px[px > 0] * np.log2(px[px > 0]))
    h_m = -np.sum(py[py > 0] * np.log2(py[py > 0]))
    h_fm = -np.sum(pxy[nz] * np.log2(pxy[nz]))
    mi = float(h_f + h_m - h_fm)
    
    # Normalized Cross Correlation
    f_c = fixed.astype(float) - fixed.mean()
    m_c = moving.astype(float) - moving.mean()
    denom = np.sqrt(np.sum(f_c**2) * np.sum(m_c**2))
    ncc = float(np.sum(f_c * m_c) / denom) if denom > 0 else 0.0
    
    # Mean Squared Error
    mse = float(np.mean((fixed.astype(float) - moving.astype(float)) ** 2))
    
    return mi, ncc, mse, h_fm, h2d

def run_task_12_3():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.abspath(os.path.join(script_dir, ".."))
    inputs_dir = os.path.join(exp_dir, "Inputs", "images")
    outputs_dir = os.path.join(exp_dir, "Outputs", "Python")
    tables_dir = os.path.join(exp_dir, "Tables")
    os.makedirs(outputs_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)
    
    mri = cv2.imread(os.path.join(inputs_dir, "Brain_MRI.png"), cv2.IMREAD_GRAYSCALE)
    pet_aligned = cv2.imread(os.path.join(inputs_dir, "Brain_PET_Aligned.png"), cv2.IMREAD_GRAYSCALE)
    if mri is None or pet_aligned is None:
        raise FileNotFoundError("Brain_MRI.png or Brain_PET_Aligned.png missing")
        
    h, w = mri.shape
    center = (w / 2.0, h / 2.0)
    
    angles = np.arange(-30, 31, 2)
    records = []
    histograms = {}
    key_angles = [-30, -10, 0, 10, 30]
    
    print("\n" + "=" * 90)
    print("TASK 12.3: 2D JOINT HISTOGRAM & MUTUAL INFORMATION ROTATION SWEEP (-30° to +30°)")
    print("=" * 90)
    print(f"{'Rotation Δθ (deg)':<20} | {'MI (bits)':<12} | {'Joint Entropy H(F,M)':<22} | {'NCC':<10} | {'MSE'}")
    print("-" * 90)
    
    for theta in angles:
        M = cv2.getRotationMatrix2D(center, float(theta), 1.0)
        pet_rotated = cv2.warpAffine(pet_aligned, M, (w, h), flags=cv2.INTER_LINEAR)
        
        mi, ncc, mse, h_fm, h2d = compute_mi_and_metrics(mri, pet_rotated)
        if theta in key_angles:
            histograms[theta] = h2d
            print(f"Δθ = {theta:+3d}° {'(PEAK)' if theta==0 else '':<10} | {mi:<12.4f} | {h_fm:<22.4f} | {ncc:<10.4f} | {mse:<10.2f}")
            
        records.append({
            "Delta_Theta_deg": int(theta),
            "Mutual_Information_MI": round(mi, 4),
            "Joint_Entropy": round(h_fm, 4),
            "Normalized_Cross_Corr_NCC": round(ncc, 4),
            "Mean_Squared_Error_MSE": round(mse, 2)
        })
        
    df = pd.DataFrame(records)
    csv_path = os.path.join(tables_dir, "exp12_task_12_3_rotation_sweep.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SAVED] Task 12.3 table saved to: {csv_path}")
    
    # Figure 1: Metric Optimization Curves Across Delta Theta
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Subplot 1: MI & Joint Entropy
    ax1.plot(df["Delta_Theta_deg"], df["Mutual_Information_MI"], "b-o", linewidth=2.0, markersize=4, label="Mutual Information (MI, bits)")
    ax1.axvline(0, color="green", linestyle="--", alpha=0.7, label="True Alignment (Δθ=0°)")
    ax1.set_title("Mutual Information vs. Rotation Angle Δθ\n(Sharp Global Peak at Perfect Registration)", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Rotation Misalignment Δθ (degrees)", fontsize=10)
    ax1.set_ylabel("Mutual Information (bits)", fontsize=10, color="blue")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left")
    
    ax1_twin = ax1.twinx()
    ax1_twin.plot(df["Delta_Theta_deg"], df["Joint_Entropy"], "r--s", linewidth=1.8, markersize=3, label="Joint Entropy H(F,M)")
    ax1_twin.set_ylabel("Joint Entropy (bits)", fontsize=10, color="red")
    ax1_twin.legend(loc="upper right")
    
    # Subplot 2: NCC & MSE
    ax2.plot(df["Delta_Theta_deg"], df["Normalized_Cross_Corr_NCC"], "m-^", linewidth=2.0, markersize=4, label="NCC (Cosine Similarity)")
    ax2.axvline(0, color="green", linestyle="--", alpha=0.7, label="True Alignment (Δθ=0°)")
    ax2.set_title("NCC & MSE Across Rotation Angle Δθ\n(Multi-Modal Correlation Dynamics)", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Rotation Misalignment Δθ (degrees)", fontsize=10)
    ax2.set_ylabel("Normalized Cross-Correlation", fontsize=10, color="purple")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="lower left")
    
    ax2_twin = ax2.twinx()
    ax2_twin.plot(df["Delta_Theta_deg"], df["Mean_Squared_Error_MSE"], "k:d", linewidth=1.8, markersize=3, label="MSE")
    ax2_twin.set_ylabel("Mean Squared Error (MSE)", fontsize=10, color="black")
    ax2_twin.legend(loc="lower right")
    
    plt.tight_layout()
    fig1_path = os.path.join(outputs_dir, "exp12_task_12_3_rotation_sweep.png")
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"[SAVED] Task 12.3 sweep plot saved to: {fig1_path}")
    
    # Figure 2: Multi-Angle 2D Joint Histogram Progression (5 Panels)
    fig, axes = plt.subplots(1, 5, figsize=(18, 3.8))
    for idx, th in enumerate(key_angles):
        h2d = histograms[th]
        row_match = df[df["Delta_Theta_deg"] == th].iloc[0]
        im = axes[idx].imshow(np.log1p(h2d), cmap="inferno", origin="lower", extent=[0, 255, 0, 255])
        axes[idx].set_title(f"Δθ = {th:+d}°\nMI = {row_match['Mutual_Information_MI']:.4f} bits", fontsize=10, fontweight="bold")
        axes[idx].set_xlabel("MRI Intensity", fontsize=9)
        if idx == 0:
            axes[idx].set_ylabel("PET Intensity", fontsize=9)
        else:
            axes[idx].set_yticklabels([])
            
    plt.tight_layout()
    fig2_path = os.path.join(outputs_dir, "exp12_task_12_3_joint_histograms_panels.png")
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"[SAVED] Task 12.3 joint histograms progression saved to: {fig2_path}")

if __name__ == "__main__":
    run_task_12_3()
