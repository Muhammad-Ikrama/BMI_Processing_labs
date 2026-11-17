"""
Task 13.4: Gray-Level Quantization (Ng) Trade-off Evaluation
Experiment 13: Texture Feature Extraction from Medical Images Using GLCM
Author: Muhammad Ikrama (Reg ID: 60140)
"""

import os
import time
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

def compute_glcm_ng(patch, levels):
    q = np.clip((patch.astype(int) * levels) // 256, 0, levels - 1)
    offsets = [(0, 1), (-1, 1), (-1, 0), (-1, -1)]
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
    
    I, J = np.ogrid[0:levels, 0:levels]
    contrast = np.sum(P * ((I - J) ** 2))
    homog = np.sum(P / (1.0 + (I - J) ** 2))
    sparsity = float(np.mean(P == 0) * 100.0)
    return P, contrast, homog, sparsity

def run_task_13_4():
    print("=" * 80)
    print("TASK 13.4: GRAY-LEVEL QUANTIZATION (Ng) TRADE-OFF EVALUATION")
    print("=" * 80)
    
    mri = cv2.imread(os.path.join(IMG_DIR, "Brain_MRI.png"), cv2.IMREAD_GRAYSCALE)
    mri_tex = mri.copy()
    np.random.seed(113)
    grid_n = cv2.resize(np.random.normal(0, 38, (16, 16)), (48, 48), interpolation=cv2.INTER_NEAREST)
    mri_tex[219:267, 301:349] = np.clip(mri_tex[219:267, 301:349].astype(float) + grid_n, 0, 255).astype(np.uint8)
    
    roi_normal = mri_tex[175:223, 155:203]
    roi_tumor  = mri_tex[219:267, 301:349]
    
    levels_list = [8, 16, 32, 64, 256]
    records = []
    
    print(f"{'Ng Levels':<10} | {'Matrix Size':<12} | {'Time (ms)':<10} | {'Sparsity (%)':<13} | {'C_Norm':<9} | {'C_Tumor':<9} | {'Ratio'}")
    print("-" * 80)
    
    for ng in levels_list:
        # Benchmark timing over 40 runs
        t0 = time.perf_counter()
        for _ in range(40):
            _ = compute_glcm_ng(roi_normal, ng)
        elapsed_ms = (time.perf_counter() - t0) / 40.0 * 1000.0
        
        _, c_norm, h_norm, sp_norm = compute_glcm_ng(roi_normal, ng)
        _, c_tumor, h_tumor, sp_tumor = compute_glcm_ng(roi_tumor, ng)
        
        ratio = c_tumor / (c_norm + 1e-12)
        
        records.append({
            "Ng_Levels": ng,
            "Matrix_Dimension": f"{ng}x{ng}",
            "Total_Cells": ng * ng,
            "Exec_Time_ms": round(elapsed_ms, 3),
            "Sparsity_Percent": round(sp_norm, 1),
            "Contrast_Normal": round(c_norm, 4),
            "Contrast_Tumor": round(c_tumor, 4),
            "Tumor_to_Normal_Ratio": round(ratio, 2)
        })
        
        print(f"{ng:<10} | {f'{ng}x{ng}':<12} | {elapsed_ms:<10.3f} | {sp_norm:<13.1f} | {c_norm:<9.3f} | {c_tumor:<9.3f} | {ratio:.2f}x")
        
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(TAB_DIR, "exp13_task_13_4_quantization_tradeoff.csv"), index=False)
    
    # Plotting trade-off curves
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    
    # 1. Sparsity vs Ng
    axes[0].plot([str(x) for x in levels_list], df["Sparsity_Percent"], "o-", color="#d62728", linewidth=2)
    axes[0].axhspan(90, 100, color="red", alpha=0.15, label="Severe Sparsity (>90%)")
    axes[0].set_title("(A) GLCM Matrix Sparsity vs Ng", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("Quantization Levels Ng", fontsize=10)
    axes[0].set_ylabel("Matrix Sparsity (% Empty Zeros)", fontsize=10)
    axes[0].grid(True, linestyle="--", alpha=0.5)
    axes[0].legend(fontsize=9)
    
    # 2. Execution Time vs Ng
    axes[1].plot([str(x) for x in levels_list], df["Exec_Time_ms"], "s-", color="#1f77b4", linewidth=2)
    axes[1].set_title("(B) Computation Time vs Ng", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("Quantization Levels Ng", fontsize=10)
    axes[1].set_ylabel("Execution Time (ms)", fontsize=10)
    axes[1].grid(True, linestyle="--", alpha=0.5)
    
    # 3. Tumor vs Normal Contrast Ratio
    axes[2].plot([str(x) for x in levels_list], df["Tumor_to_Normal_Ratio"], "^-", color="#2ca02c", linewidth=2)
    axes[2].axvspan(1, 2, color="green", alpha=0.15, label="Optimal Sweet-Spot (Ng=16, 32)")
    axes[2].set_title("(C) Diagnostic Contrast Ratio vs Ng", fontsize=11, fontweight="bold")
    axes[2].set_xlabel("Quantization Levels Ng", fontsize=10)
    axes[2].set_ylabel("Tumor / Normal Contrast Ratio", fontsize=10)
    axes[2].grid(True, linestyle="--", alpha=0.5)
    axes[2].legend(fontsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "exp13_task_13_4_quantization_plots.png"), dpi=300)
    plt.close()
    print(">>> Task 13.4 Complete. Quantization trade-off figures and CSV exported.")
    return df

if __name__ == "__main__":
    run_task_13_4()
