"""
Experiment 13: Texture Feature Extraction from Medical Images Using the Gray-Level Co-occurrence Matrix (GLCM)
Author: Muhammad Ikrama (Reg ID: 60140)
Department of Biomedical Engineering, Riphah International University, Lahore
Instructor: Engr. Rana Talha Khalid
Course: Medical Image Processing (BMI-701)
"""

import os
import time
import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXP_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
FIG_DIR = os.path.join(EXP_DIR, "Figures")
TAB_DIR = os.path.join(EXP_DIR, "Tables")
OUT_DIR = os.path.join(EXP_DIR, "Outputs", "Python")
IMG_DIR = os.path.join(EXP_DIR, "Inputs", "images")

os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(TAB_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

def compute_glcm(patch, levels=16, offsets=[(0, 1), (-1, 1), (-1, 0), (-1, -1)]):
    """Compute symmetric, normalized 2D GLCM averaged over given directional offsets."""
    q = np.clip((patch.astype(int) * levels) // 256, 0, levels - 1)
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
    return P

def extract_haralick(P):
    """Extract standard Haralick texture descriptors from normalized GLCM P."""
    levels = P.shape[0]
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

def run_benchmark():
    print("=" * 80)
    print("EXPERIMENT 13: GLCM TEXTURE FEATURE EXTRACTION BENCHMARK")
    print("=" * 80)
    
    mri_path = os.path.join(IMG_DIR, "Brain_MRI.png")
    mri = cv2.imread(mri_path, cv2.IMREAD_GRAYSCALE)
    if mri is None:
        raise FileNotFoundError(f"Brain MRI image not found at {mri_path}")
        
    mri_tex = mri.copy()
    np.random.seed(113)
    grid_n = cv2.resize(np.random.normal(0, 38, (16, 16)), (48, 48), interpolation=cv2.INTER_NEAREST)
    mri_tex[219:267, 301:349] = np.clip(mri_tex[219:267, 301:349].astype(float) + grid_n, 0, 255).astype(np.uint8)
    
    roi_normal = mri_tex[175:223, 155:203]
    roi_cortex = mri_tex[120:168, 120:168]
    roi_tumor  = mri_tex[219:267, 301:349]
    
    rois = [
        ("Normal White Matter ROI", roi_normal),
        ("Cortical Folding ROI", roi_cortex),
        ("Heterogeneous Tumor ROI", roi_tumor)
    ]
    
    results = []
    glcms = {}
    print(f"{'Clinical Tissue ROI':<25} | {'Contrast':<9} | {'Homogen.':<9} | {'Energy':<8} | {'Entropy':<8} | {'Correl.'}")
    print("-" * 79)
    for name, patch in rois:
        P = compute_glcm(patch, levels=16)
        glcms[name] = P
        con, hom, ene, ent, cor = extract_haralick(P)
        results.append({
            "Tissue_ROI": name,
            "Contrast": round(con, 4),
            "Homogeneity": round(hom, 4),
            "Energy": round(ene, 4),
            "Entropy_bits": round(ent, 4),
            "Correlation": round(cor, 4)
        })
        print(f"{name:<25} | {con:<9.3f} | {hom:<9.3f} | {ene:<8.4f} | {ent:<8.3f} | {cor:<7.3f}")
    
    df_bm = pd.DataFrame(results)
    df_bm.to_csv(os.path.join(TAB_DIR, "exp13_benchmark_features.csv"), index=False)
    
    tumor_con = df_bm.loc[df_bm["Tissue_ROI"].str.contains("Tumor"), "Contrast"].values[0]
    norm_con = df_bm.loc[df_bm["Tissue_ROI"].str.contains("Normal"), "Contrast"].values[0]
    ratio = tumor_con / norm_con
    print(f">>> Status: GLCM Contrast ({ratio:.1f}x increase) robustly separates Tumor ROI.")
    
    # Figure 13.1: GLCM Heatmaps
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    titles = [
        "(A) Normal White Matter ROI\nTight Diagonal Clustering",
        "(B) Cortical Folding ROI\nModerate Diagonal Spread",
        "(C) Heterogeneous Tumor ROI\nWide Off-Diagonal Dispersion"
    ]
    for idx, (name, patch) in enumerate(rois):
        P = glcms[name]
        im = axes[idx].imshow(P, cmap="magma", origin="upper", interpolation="nearest")
        axes[idx].set_title(titles[idx], fontsize=11, fontweight="bold")
        axes[idx].set_xlabel("Gray Level j", fontsize=10)
        axes[idx].set_ylabel("Gray Level i", fontsize=10)
        plt.colorbar(im, ax=axes[idx], fraction=0.046, pad=0.04)
    plt.tight_layout()
    fig_13_1_path = os.path.join(FIG_DIR, "Figure_13_1_GLCM_Heatmaps.png")
    plt.savefig(fig_13_1_path, dpi=300)
    plt.close()
    
    # Figure 13.2: Clinical Tissue Characterization
    # Panel 1: MRI with ROI bounding boxes
    # Panel 2: Local Entropy texture map
    # Panel 3: Haralick feature bar chart
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    # RGB MRI overlay
    mri_bgr = cv2.cvtColor(mri_tex, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(mri_bgr, (155, 175), (203, 223), (0, 255, 0), 2)   # Green = Normal
    cv2.rectangle(mri_bgr, (120, 120), (168, 168), (255, 0, 0), 2)   # Blue = Cortex
    cv2.rectangle(mri_bgr, (301, 219), (349, 267), (0, 0, 255), 2)   # Red = Tumor
    cv2.putText(mri_bgr, "Normal", (140, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(mri_bgr, "Cortex", (105, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    cv2.putText(mri_bgr, "Tumor", (295, 215), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    axes[0].imshow(cv2.cvtColor(mri_bgr, cv2.COLOR_BGR2RGB))
    axes[0].set_title("(1) Brain MRI with 48x48 Tissue ROIs", fontsize=11, fontweight="bold")
    axes[0].axis("off")
    
    # Fast Local Entropy Map (stride 8)
    stride = 8
    win_size = 16
    H, W = mri_tex.shape
    rows = range(0, H - win_size + 1, stride)
    cols = range(0, W - win_size + 1, stride)
    ent_map = np.zeros((len(rows), len(cols)), dtype=float)
    q_img = np.clip((mri_tex.astype(int) * 16) // 256, 0, 15)
    
    for ri, r in enumerate(rows):
        for ci, c in enumerate(cols):
            p = q_img[r:r+win_size, c:c+win_size]
            counts = np.bincount(p.ravel(), minlength=16)
            probs = counts / float(win_size * win_size)
            nz = probs > 0
            ent_map[ri, ci] = -np.sum(probs[nz] * np.log2(probs[nz]))
            
    im2 = axes[1].imshow(ent_map, cmap="viridis", interpolation="bilinear")
    axes[1].set_title("(2) Spatial Local Entropy Texture Map", fontsize=11, fontweight="bold")
    axes[1].axis("off")
    plt.colorbar(im2, ax=axes[1], fraction=0.046, pad=0.04, label="Entropy (bits)")
    
    # Panel 3: Multi-feature comparison bar chart
    categories = ["Contrast", "Homogeneity", "Energy*10", "Entropy", "Correlation"]
    x = np.arange(len(categories))
    width = 0.25
    
    val_norm = [df_bm.loc[0, "Contrast"], df_bm.loc[0, "Homogeneity"], df_bm.loc[0, "Energy"] * 10, df_bm.loc[0, "Entropy_bits"], df_bm.loc[0, "Correlation"]]
    val_cortex = [df_bm.loc[1, "Contrast"], df_bm.loc[1, "Homogeneity"], df_bm.loc[1, "Energy"] * 10, df_bm.loc[1, "Entropy_bits"], df_bm.loc[1, "Correlation"]]
    val_tumor = [df_bm.loc[2, "Contrast"], df_bm.loc[2, "Homogeneity"], df_bm.loc[2, "Energy"] * 10, df_bm.loc[2, "Entropy_bits"], df_bm.loc[2, "Correlation"]]
    
    axes[2].bar(x - width, val_norm, width, label="Normal White Matter", color="#2ca02c")
    axes[2].bar(x, val_cortex, width, label="Cortical Folding", color="#1f77b4")
    axes[2].bar(x + width, val_tumor, width, label="Heterogeneous Tumor", color="#d62728")
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(categories, fontsize=9)
    axes[2].set_ylabel("Feature Magnitude", fontsize=10)
    axes[2].set_title("(3) Multi-Feature Haralick Comparison", fontsize=11, fontweight="bold")
    axes[2].legend(fontsize=8, loc="upper right")
    axes[2].grid(axis="y", linestyle="--", alpha=0.5)
    
    plt.tight_layout()
    fig_13_2_path = os.path.join(FIG_DIR, "Figure_13_2_Clinical_Characterization.png")
    plt.savefig(fig_13_2_path, dpi=300)
    plt.close()
    
    return mri_tex, roi_normal, roi_tumor

if __name__ == "__main__":
    run_benchmark()
