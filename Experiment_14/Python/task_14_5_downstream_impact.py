"""
Task 14.5: Impact of Lossy Compression on Downstream Segmentation & GLCM Features
Experiment 14: Medical Image Compression and Quality Evaluation
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

def srg(img, seed, tol=35):
    H, W = img.shape
    visited = np.zeros((H, W), dtype=bool)
    mask = np.zeros((H, W), dtype=bool)
    seed_y, seed_x = seed
    seed_val = float(img[seed_y, seed_x])
    stack = [seed]
    visited[seed] = True
    mask[seed] = True
    while stack:
        cy, cx = stack.pop()
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < H and 0 <= nx < W and not visited[ny, nx]:
                visited[ny, nx] = True
                if abs(float(img[ny, nx]) - seed_val) <= tol:
                    mask[ny, nx] = True
                    stack.append((ny, nx))
    return mask

def compute_glcm_features(patch, levels=16):
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
        if tot > 0: P_avg += mat / tot
    P = P_avg / len(offsets)
    I, J = np.ogrid[0:levels, 0:levels]
    contrast = np.sum(P * ((I - J) ** 2))
    homog = np.sum(P / (1.0 + (I - J) ** 2))
    nz = P > 0
    entropy = -np.sum(P[nz] * np.log2(P[nz]))
    return contrast, homog, entropy

def run_task_14_5():
    print("=" * 80)
    print("TASK 14.5: IMPACT OF LOSSY COMPRESSION ON DOWNSTREAM SEGMENTATION & GLCM")
    print("=" * 80)
    
    mri = cv2.imread(os.path.join(IMG_DIR, "Brain_MRI.png"), cv2.IMREAD_GRAYSCALE)
    mri_tex = mri.copy()
    np.random.seed(113)
    grid_n = cv2.resize(np.random.normal(0, 38, (16, 16)), (48, 48), interpolation=cv2.INTER_NEAREST)
    mri_tex[219:267, 301:349] = np.clip(mri_tex[219:267, 301:349].astype(float) + grid_n, 0, 255).astype(np.uint8)
    
    seed = (243, 325)
    gt_mask = srg(mri_tex, seed, tol=35)
    gt_con, gt_hom, gt_ent = compute_glcm_features(mri_tex[219:267, 301:349])
    
    records = []
    qualities = [100, 95, 85, 50, 25, 10, 5]
    
    print(f"{'JPEG Quality':<14} | {'Tumor Dice (DSC)':<18} | {'GLCM Contrast':<15} | {'Con. Error %':<14} | {'GLCM Entropy':<14} | {'Ent. Error %'}")
    print("-" * 92)
    
    dsc_masks = {}
    for q in qualities:
        if q == 100:
            dec = mri_tex.copy()
            dsc = 1.0000
        else:
            _, buf = cv2.imencode('.jpg', mri_tex, [cv2.IMWRITE_JPEG_QUALITY, q])
            dec = cv2.imdecode(buf, cv2.IMREAD_GRAYSCALE)
            seg_mask = srg(dec, seed, tol=35)
            inter = np.logical_and(gt_mask, seg_mask).sum()
            dsc = 2.0 * inter / (gt_mask.sum() + seg_mask.sum() + 1e-12)
            dsc_masks[q] = seg_mask
            
        c, h, e = compute_glcm_features(dec[219:267, 301:349])
        c_err = abs(c - gt_con) / gt_con * 100.0
        e_err = abs(e - gt_ent) / gt_ent * 100.0
        
        q_label = "Uncompressed (100)" if q == 100 else f"Lossy (Q={q})"
        records.append({
            "Quality_Setting": q_label, "Quality_Q": q,
            "Tumor_Dice_DSC": round(dsc, 4),
            "GLCM_Contrast": round(c, 4), "Contrast_Error_Pct": round(c_err, 2),
            "GLCM_Entropy_bits": round(e, 4), "Entropy_Error_Pct": round(e_err, 2)
        })
        print(f"{q_label:<14} | {dsc:<18.4f} | {c:<15.4f} | {c_err:<14.1f}% | {e:<14.4f} | {e_err:.1f}%")
        
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(TAB_DIR, "exp14_task_14_5_downstream_impact.csv"), index=False)
    
    # Plotting Figure (Curves + Segmentation Overlays)
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))
    
    # Panel 1: DSC vs Q
    q_vals = [r["Quality_Q"] for r in records if r["Quality_Q"] < 100]
    dsc_vals = [r["Tumor_Dice_DSC"] for r in records if r["Quality_Q"] < 100]
    axes[0].plot(q_vals, dsc_vals, "o-", color="#2ca02c", linewidth=2, markersize=6)
    axes[0].axhline(0.980, color="green", linestyle="--", label="High Concordance (0.98)")
    axes[0].axhline(0.950, color="red", linestyle=":", label="Degradation Limit (0.95)")
    axes[0].set_title("(A) Tumor Segmentation Dice (DSC) vs. Q", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("JPEG Quality Factor Q", fontsize=10)
    axes[0].set_ylabel("Dice Similarity Coefficient (DSC)", fontsize=10)
    axes[0].grid(True, linestyle="--", alpha=0.5)
    axes[0].invert_xaxis()
    axes[0].legend(fontsize=9)
    
    # Panel 2: GLCM Contrast Error % vs Q
    con_errs = [r["Contrast_Error_Pct"] for r in records if r["Quality_Q"] < 100]
    axes[1].plot(q_vals, con_errs, "s-", color="#d62728", linewidth=2, markersize=6)
    axes[1].axhline(5.0, color="green", linestyle="--", label="5% Error Tolerance")
    axes[1].axhline(20.0, color="red", linestyle=":", label="Severe Distortion (>20%)")
    axes[1].set_title("(B) GLCM Contrast Error (%) vs. Q", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("JPEG Quality Factor Q", fontsize=10)
    axes[1].set_ylabel("Relative Contrast Error (%)", fontsize=10)
    axes[1].grid(True, linestyle="--", alpha=0.5)
    axes[1].invert_xaxis()
    axes[1].legend(fontsize=9)
    
    # Panel 3: Visual overlay comparison (GT vs Q=5)
    overlay = cv2.cvtColor(mri_tex, cv2.COLOR_GRAY2BGR)
    overlay[gt_mask, 1] = 255 # Green = GT
    mask_q5 = dsc_masks[5]
    overlay[mask_q5, 2] = 255 # Red = Q=5 (Yellow where both overlap)
    axes[2].imshow(overlay[200:280, 280:360])
    axes[2].set_title("(C) Segmentation Overlay (Zoomed):\nGreen = GT, Red = Q=5, Yellow = Overlap", fontsize=10, fontweight="bold")
    axes[2].axis("off")
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "exp14_task_14_5_downstream_plots.png"), dpi=300)
    plt.close()
    print(">>> Task 14.5 Complete. Downstream impact figures and CSV exported.")
    return df

if __name__ == "__main__":
    run_task_14_5()
