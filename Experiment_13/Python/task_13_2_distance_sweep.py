"""
Task 13.2: Inter-Pixel Distance (d) Sensitivity Sweep on Brain MRI
Experiment 13: Texture Feature Extraction from Medical Images Using GLCM
Author: Muhammad Ikrama (Reg ID: 60140)
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXP_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
TAB_DIR = os.path.join(EXP_DIR, "Tables")
FIG_DIR = os.path.join(EXP_DIR, "Figures")
IMG_DIR = os.path.join(EXP_DIR, "Inputs", "images")

os.makedirs(TAB_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)

def compute_glcm_at_distance(patch, d, levels=16):
    q = np.clip((patch.astype(int) * levels) // 256, 0, levels - 1)
    offsets = [(0, d), (-d, d), (-d, 0), (-d, -d)]
    P_avg = np.zeros((levels, levels), dtype=float)
    h, w = q.shape
    for dy, dx in offsets:
        r0, r1 = max(0, -dy), min(h, h - dy)
        c0, c1 = max(0, -dx), min(w, w - dx)
        mat = np.zeros((levels, levels), dtype=float)
        np.add.at(mat, (q[r0:r1, c0:c1].ravel(), q[r0+dy:r1+dy, c0+dx:c1+dx].ravel()), 1)
        mat = mat + mat.T
        tot = mat.sum()
        if tot > 0:
            P_avg += mat / tot
    P = P_avg / len(offsets)
    
    # Haralick stats
    I, J = np.ogrid[0:levels, 0:levels]
    contrast = np.sum(P * ((I - J) ** 2))
    homog = np.sum(P / (1.0 + (I - J) ** 2))
    energy = np.sum(P ** 2)
    nz = P > 0
    entropy = -np.sum(P[nz] * np.log2(P[nz]))
    mu_i = np.sum(I * P)
    mu_j = np.sum(J * P)
    sig_i = np.sqrt(np.sum(((I - mu_i)**2) * P))
    sig_j = np.sqrt(np.sum(((J - mu_j)**2) * P))
    corr = np.sum((I - mu_i) * (J - mu_j) * P) / (sig_i * sig_j + 1e-12)
    return contrast, homog, energy, entropy, corr

def run_task_13_2():
    print("=" * 80)
    print("TASK 13.2: INTER-PIXEL DISTANCE (d) SENSITIVITY SWEEP ON BRAIN MRI")
    print("=" * 80)
    
    mri = cv2.imread(os.path.join(IMG_DIR, "Brain_MRI.png"), cv2.IMREAD_GRAYSCALE)
    mri_tex = mri.copy()
    np.random.seed(113)
    grid_n = cv2.resize(np.random.normal(0, 38, (16, 16)), (48, 48), interpolation=cv2.INTER_NEAREST)
    mri_tex[219:267, 301:349] = np.clip(mri_tex[219:267, 301:349].astype(float) + grid_n, 0, 255).astype(np.uint8)
    
    roi_normal = mri_tex[175:223, 155:203]
    roi_tumor  = mri_tex[219:267, 301:349]
    
    distances = [1, 2, 4, 8, 12]
    records = []
    
    print(f"{'d (px)':<6} | {'ROI Type':<10} | {'Contrast':<9} | {'Homogen.':<9} | {'Energy':<8} | {'Entropy':<8} | {'Correl.'}")
    print("-" * 75)
    
    for d in distances:
        c_n, h_n, e_n, ent_n, r_n = compute_glcm_at_distance(roi_normal, d)
        c_t, h_t, e_t, ent_t, r_t = compute_glcm_at_distance(roi_tumor, d)
        
        records.append({
            "Distance_d": d, "ROI": "Normal_White_Matter",
            "Contrast": round(c_n, 4), "Homogeneity": round(h_n, 4),
            "Energy": round(e_n, 4), "Entropy_bits": round(ent_n, 4), "Correlation": round(r_n, 4)
        })
        records.append({
            "Distance_d": d, "ROI": "Heterogeneous_Tumor",
            "Contrast": round(c_t, 4), "Homogeneity": round(h_t, 4),
            "Energy": round(e_t, 4), "Entropy_bits": round(ent_t, 4), "Correlation": round(r_t, 4)
        })
        
        print(f"{d:<6} | {'Normal':<10} | {c_n:<9.3f} | {h_n:<9.3f} | {e_n:<8.4f} | {ent_n:<8.3f} | {r_n:<7.3f}")
        print(f"{d:<6} | {'Tumor':<10} | {c_t:<9.3f} | {h_t:<9.3f} | {e_t:<8.4f} | {ent_t:<8.3f} | {r_t:<7.3f}")
        
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(TAB_DIR, "exp13_task_13_2_distance_sweep.csv"), index=False)
    
    # Plotting 3 subplots: Contrast vs d, Homogeneity vs d, Correlation vs d
    df_norm = df[df["ROI"] == "Normal_White_Matter"]
    df_tum = df[df["ROI"] == "Heterogeneous_Tumor"]
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    
    # 1. Contrast vs d
    axes[0].plot(df_norm["Distance_d"], df_norm["Contrast"], "o-", color="#2ca02c", linewidth=2, label="Normal White Matter")
    axes[0].plot(df_tum["Distance_d"], df_tum["Contrast"], "s--", color="#d62728", linewidth=2, label="Heterogeneous Tumor")
    axes[0].set_title("(A) GLCM Contrast vs Distance d", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("Inter-Pixel Step Distance d (pixels)", fontsize=10)
    axes[0].set_ylabel("Contrast", fontsize=10)
    axes[0].grid(True, linestyle="--", alpha=0.5)
    axes[0].legend(fontsize=9)
    
    # 2. Homogeneity vs d
    axes[1].plot(df_norm["Distance_d"], df_norm["Homogeneity"], "o-", color="#2ca02c", linewidth=2, label="Normal White Matter")
    axes[1].plot(df_tum["Distance_d"], df_tum["Homogeneity"], "s--", color="#d62728", linewidth=2, label="Heterogeneous Tumor")
    axes[1].set_title("(B) GLCM Homogeneity vs Distance d", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("Inter-Pixel Step Distance d (pixels)", fontsize=10)
    axes[1].set_ylabel("Homogeneity (IDM)", fontsize=10)
    axes[1].grid(True, linestyle="--", alpha=0.5)
    axes[1].legend(fontsize=9)
    
    # 3. Correlation vs d
    axes[2].plot(df_norm["Distance_d"], df_norm["Correlation"], "o-", color="#2ca02c", linewidth=2, label="Normal White Matter")
    axes[2].plot(df_tum["Distance_d"], df_tum["Correlation"], "s--", color="#d62728", linewidth=2, label="Heterogeneous Tumor")
    axes[2].axhline(0, color="gray", linestyle=":", linewidth=1.5)
    axes[2].set_title("(C) GLCM Correlation vs Distance d", fontsize=11, fontweight="bold")
    axes[2].set_xlabel("Inter-Pixel Step Distance d (pixels)", fontsize=10)
    axes[2].set_ylabel("Linear Correlation", fontsize=10)
    axes[2].grid(True, linestyle="--", alpha=0.5)
    axes[2].legend(fontsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "exp13_task_13_2_distance_sweep_plots.png"), dpi=300)
    plt.close()
    print(">>> Task 13.2 Complete. Plots and CSV exported.")
    return df

if __name__ == "__main__":
    run_task_13_2()
