"""
Task 13.5: Sliding-Window Local Texture Feature Map Generation
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

def run_task_13_5():
    print("=" * 80)
    print("TASK 13.5: SLIDING-WINDOW LOCAL TEXTURE FEATURE MAP GENERATION")
    print("=" * 80)
    
    mri = cv2.imread(os.path.join(IMG_DIR, "Brain_MRI.png"), cv2.IMREAD_GRAYSCALE)
    mri_tex = mri.copy()
    np.random.seed(113)
    grid_n = cv2.resize(np.random.normal(0, 38, (16, 16)), (48, 48), interpolation=cv2.INTER_NEAREST)
    mri_tex[219:267, 301:349] = np.clip(mri_tex[219:267, 301:349].astype(float) + grid_n, 0, 255).astype(np.uint8)
    
    t0 = time.perf_counter()
    win_size = 16
    stride = 8
    H, W = mri_tex.shape
    rows = list(range(0, H - win_size + 1, stride))
    cols = list(range(0, W - win_size + 1, stride))
    
    contrast_map = np.zeros((len(rows), len(cols)), dtype=float)
    entropy_map  = np.zeros((len(rows), len(cols)), dtype=float)
    homogeneity_map = np.zeros((len(rows), len(cols)), dtype=float)
    
    levels = 16
    q_img = np.clip((mri_tex.astype(int) * levels) // 256, 0, levels - 1)
    I, J = np.ogrid[0:levels, 0:levels]
    diff_sq = (I - J) ** 2
    idm_weight = 1.0 / (1.0 + diff_sq)
    
    for ri, r in enumerate(rows):
        for ci, c in enumerate(cols):
            patch = q_img[r:r+win_size, c:c+win_size]
            mat = np.zeros((levels, levels), dtype=float)
            # 0 deg
            np.add.at(mat, (patch[:, :-1].ravel(), patch[:, 1:].ravel()), 1)
            # 90 deg
            np.add.at(mat, (patch[1:, :].ravel(), patch[:-1, :].ravel()), 1)
            # 45 deg
            np.add.at(mat, (patch[1:, :-1].ravel(), patch[:-1, 1:].ravel()), 1)
            # 135 deg
            np.add.at(mat, (patch[1:, 1:].ravel(), patch[:-1, :-1].ravel()), 1)
            mat = mat + mat.T
            tot = mat.sum()
            if tot > 0:
                P = mat / tot
                contrast_map[ri, ci] = np.sum(P * diff_sq)
                homogeneity_map[ri, ci] = np.sum(P * idm_weight)
                nz = P > 0
                entropy_map[ri, ci] = -np.sum(P[nz] * np.log2(P[nz]))
                
    elapsed = time.perf_counter() - t0
    print(f"Generated 2D Texture Maps ({len(rows)}x{len(cols)} grid) in {elapsed:.2f} seconds.")
    print(f"  Contrast Map: min = {contrast_map.min():.3f}, max = {contrast_map.max():.3f}, mean = {contrast_map.mean():.3f}")
    print(f"  Entropy Map: min = {entropy_map.min():.3f}, max = {entropy_map.max():.3f}, mean = {entropy_map.mean():.3f}")
    print(f"  Homogeneity Map: min = {homogeneity_map.min():.3f}, max = {homogeneity_map.max():.3f}, mean = {homogeneity_map.mean():.3f}")
    
    # Save CSV
    df_stats = pd.DataFrame([{
        "Feature_Map": "GLCM Contrast",
        "Min": round(float(contrast_map.min()), 4),
        "Max": round(float(contrast_map.max()), 4),
        "Mean": round(float(contrast_map.mean()), 4),
        "Std": round(float(contrast_map.std()), 4)
    }, {
        "Feature_Map": "Shannon Entropy (bits)",
        "Min": round(float(entropy_map.min()), 4),
        "Max": round(float(entropy_map.max()), 4),
        "Mean": round(float(entropy_map.mean()), 4),
        "Std": round(float(entropy_map.std()), 4)
    }, {
        "Feature_Map": "GLCM Homogeneity",
        "Min": round(float(homogeneity_map.min()), 4),
        "Max": round(float(homogeneity_map.max()), 4),
        "Mean": round(float(homogeneity_map.mean()), 4),
        "Std": round(float(homogeneity_map.std()), 4)
    }])
    df_stats.to_csv(os.path.join(TAB_DIR, "exp13_task_13_5_texture_map_stats.csv"), index=False)
    
    # Save Figure (4 panels)
    fig, axes = plt.subplots(1, 4, figsize=(18, 4.5))
    
    axes[0].imshow(mri_tex, cmap="gray")
    axes[0].set_title("(A) Brain MRI with Tumor", fontsize=11, fontweight="bold")
    axes[0].axis("off")
    
    im1 = axes[1].imshow(contrast_map, cmap="plasma", interpolation="bilinear")
    axes[1].set_title("(B) Local GLCM Contrast Map\n(High at Tumor & Sulci)", fontsize=11, fontweight="bold")
    axes[1].axis("off")
    plt.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
    
    im2 = axes[2].imshow(entropy_map, cmap="viridis", interpolation="bilinear")
    axes[2].set_title("(C) Local Entropy Map (bits)\n(High in Chaotic Necrosis)", fontsize=11, fontweight="bold")
    axes[2].axis("off")
    plt.colorbar(im2, ax=axes[2], fraction=0.046, pad=0.04)
    
    im3 = axes[3].imshow(homogeneity_map, cmap="cividis", interpolation="bilinear")
    axes[3].set_title("(D) Local Homogeneity Map\n(High in Healthy Parenchyma)", fontsize=11, fontweight="bold")
    axes[3].axis("off")
    plt.colorbar(im3, ax=axes[3], fraction=0.046, pad=0.04)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "exp13_task_13_5_texture_maps.png"), dpi=300)
    plt.close()
    print(">>> Task 13.5 Complete. Parametric maps exported.")
    return contrast_map, entropy_map

if __name__ == "__main__":
    run_task_13_5()
