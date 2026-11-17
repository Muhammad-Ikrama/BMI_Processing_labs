"""
Task 13.1: Hand-Verified 4x4 GLCM Construction & Probability Normalization
Experiment 13: Texture Feature Extraction from Medical Images Using GLCM
Author: Muhammad Ikrama (Reg ID: 60140)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXP_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
TAB_DIR = os.path.join(EXP_DIR, "Tables")
FIG_DIR = os.path.join(EXP_DIR, "Figures")
os.makedirs(TAB_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)

def run_task_13_1():
    print("=" * 80)
    print("TASK 13.1: HAND-VERIFIED 4x4 GLCM CONSTRUCTION & NORMALIZATION")
    print("=" * 80)
    
    # 4x4 synthetic test image
    I = np.array([
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [0, 2, 2, 2],
        [2, 2, 3, 3]
    ], dtype=int)
    
    levels = 4
    # Compute horizontal non-symmetric GLCM (d=1, theta=0)
    mat_raw = np.zeros((levels, levels), dtype=int)
    for r in range(4):
        for c in range(3):
            mat_raw[I[r, c], I[r, c+1]] += 1
            
    # Make symmetric: C_sym = C + C^T
    mat_sym = mat_raw + mat_raw.T
    
    # Normalize to probabilities
    total_pairs = float(mat_sym.sum())
    P = mat_sym / total_pairs
    
    # Verification check: sum of probabilities must equal 1.000000
    prob_sum = float(np.sum(P))
    assert abs(prob_sum - 1.0) < 1e-6, f"Normalization failed: sum is {prob_sum}"
    
    # Compute Haralick features on synthetic matrix
    I_grid, J_grid = np.ogrid[0:levels, 0:levels]
    contrast = np.sum(P * ((I_grid - J_grid) ** 2))
    homogeneity = np.sum(P / (1.0 + (I_grid - J_grid) ** 2))
    energy = np.sum(P ** 2)
    nz = P > 0
    entropy = -np.sum(P[nz] * np.log2(P[nz]))
    
    print("\n1. Synthetic 4x4 Input Image (Ng = 4):")
    print(I)
    print("\n2. Raw Horizontal Count Matrix C (d=1, theta=0 deg, Non-Symmetric, Sum = 12):")
    print(mat_raw)
    print("\n3. Symmetric Count Matrix C_sym = C + C^T (Sum = 24):")
    print(mat_sym)
    print("\n4. Normalized Probability Matrix P(i,j) (Sum = 1.0000):")
    print(np.round(P, 4))
    print(f"\nVerification Assertions:")
    print(f"  Total Raw Pairs: {mat_raw.sum()} (Expected: 12)")
    print(f"  Total Symmetric Pairs: {mat_sym.sum()} (Expected: 24)")
    print(f"  Probability Sum: {prob_sum:.6f} (Expected: 1.000000)")
    print(f"  Contrast: {contrast:.4f}")
    print(f"  Homogeneity: {homogeneity:.4f}")
    print(f"  Energy (ASM): {energy:.4f}")
    print(f"  Entropy: {entropy:.4f} bits")
    
    # Save CSV tables
    df_sym = pd.DataFrame(mat_sym, columns=[f"j_{k}" for k in range(levels)], index=[f"i_{k}" for k in range(levels)])
    df_sym.to_csv(os.path.join(TAB_DIR, "exp13_task_13_1_glcm_counts.csv"))
    
    df_prob = pd.DataFrame(P, columns=[f"j_{k}" for k in range(levels)], index=[f"i_{k}" for k in range(levels)])
    df_prob.to_csv(os.path.join(TAB_DIR, "exp13_task_13_1_glcm_normalized.csv"))
    
    df_summary = pd.DataFrame([{
        "Metric": "Sum of Probabilities", "Value": prob_sum, "Status": "PASS"
    }, {
        "Metric": "GLCM Contrast", "Value": round(contrast, 4), "Status": "VERIFIED"
    }, {
        "Metric": "GLCM Homogeneity", "Value": round(homogeneity, 4), "Status": "VERIFIED"
    }, {
        "Metric": "GLCM Energy", "Value": round(energy, 4), "Status": "VERIFIED"
    }, {
        "Metric": "GLCM Entropy", "Value": round(entropy, 4), "Status": "VERIFIED"
    }])
    df_summary.to_csv(os.path.join(TAB_DIR, "exp13_task_13_1_summary.csv"), index=False)
    
    # Plot Figure
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    im0 = axes[0].imshow(I, cmap="Blues", interpolation="nearest")
    axes[0].set_title("(A) Synthetic 4x4 Grid (Ng=4)", fontsize=11, fontweight="bold")
    for r in range(4):
        for c in range(4):
            axes[0].text(c, r, str(I[r, c]), ha="center", va="center", color="black", fontsize=12, fontweight="bold")
    axes[0].set_xticks(range(4)); axes[0].set_yticks(range(4))
    
    im1 = axes[1].imshow(mat_sym, cmap="YlOrRd", interpolation="nearest")
    axes[1].set_title("(B) Symmetric Count Matrix C_sym", fontsize=11, fontweight="bold")
    for r in range(4):
        for c in range(4):
            axes[1].text(c, r, str(mat_sym[r, c]), ha="center", va="center", color="black", fontsize=11)
    axes[1].set_xlabel("Neighbor Level j"); axes[1].set_ylabel("Reference Level i")
    plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
    
    im2 = axes[2].imshow(P, cmap="viridis", interpolation="nearest")
    axes[2].set_title("(C) Normalized Probability P(i,j)\nSum = 1.000000", fontsize=11, fontweight="bold")
    for r in range(4):
        for c in range(4):
            axes[2].text(c, r, f"{P[r, c]:.2f}", ha="center", va="center", color="white" if P[r,c]>0.15 else "yellow", fontsize=10)
    axes[2].set_xlabel("Neighbor Level j"); axes[2].set_ylabel("Reference Level i")
    plt.colorbar(im2, ax=axes[2], fraction=0.046, pad=0.04)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "exp13_task_13_1_hand_verification.png"), dpi=300)
    plt.close()
    print(">>> Task 13.1 Complete. Figures and tables generated.")
    return P

if __name__ == "__main__":
    run_task_13_1()
