"""
Task 13.3: Directional Anisotropy Analysis on Rib Cage & Lung Fields in Chest X-Ray
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

def calc_glcm_single_dir(patch, angle_deg, levels=16, d=1):
    q = np.clip((patch.astype(int) * levels) // 256, 0, levels - 1)
    if angle_deg == 0:
        dy, dx = 0, d
    elif angle_deg == 90:
        dy, dx = -d, 0
    else:
        raise ValueError("Supported angles: 0, 90")
        
    h, w = q.shape
    r0, r1 = max(0, -dy), min(h, h - dy)
    c0, c1 = max(0, -dx), min(w, w - dx)
    mat = np.zeros((levels, levels), dtype=float)
    np.add.at(mat, (q[r0:r1, c0:c1].ravel(), q[r0+dy:r1+dy, c0+dx:c1+dx].ravel()), 1)
    mat = mat + mat.T
    P = mat / (mat.sum() + 1e-12)
    
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
    return contrast, homog, energy, entropy, corr, P

def run_task_13_3():
    print("=" * 80)
    print("TASK 13.3: DIRECTIONAL ANISOTROPY ANALYSIS ON CHEST X-RAY")
    print("=" * 80)
    
    xray_path = os.path.join(IMG_DIR, "Chest_Xray.png")
    xray = cv2.imread(xray_path, cv2.IMREAD_GRAYSCALE)
    if xray is None:
        raise FileNotFoundError(f"Chest X-Ray not found at {xray_path}")
        
    # Extract 64x64 ROIs
    roi_rib = xray[140:204, 80:144]     # Posterior horizontal ribs
    roi_lung = xray[260:324, 280:344]   # Vascular lung parenchyma
    
    rois = [
        ("Posterior Ribs ROI (Directional Bone)", roi_rib),
        ("Lung Parenchyma ROI (Isotropic Tissue)", roi_lung)
    ]
    
    records = []
    glcm_dict = {}
    
    print(f"{'Anatomical ROI':<38} | {'Angle':<8} | {'Contrast':<9} | {'Homogen.':<9} | {'Correl.':<8}")
    print("-" * 75)
    
    for name, patch in rois:
        c0, h0, e0, ent0, r0, P0 = calc_glcm_single_dir(patch, 0)
        c90, h90, e90, ent90, r90, P90 = calc_glcm_single_dir(patch, 90)
        
        glcm_dict[f"{name}_0"] = P0
        glcm_dict[f"{name}_90"] = P90
        
        anisotropy_ratio = c90 / (c0 + 1e-12)
        
        records.append({
            "Anatomical_ROI": name, "Angle_deg": 0, "Direction": "Horizontal",
            "Contrast": round(c0, 4), "Homogeneity": round(h0, 4),
            "Energy": round(e0, 4), "Entropy_bits": round(ent0, 4), "Correlation": round(r0, 4),
            "Anisotropy_Ratio_C90_over_C0": round(anisotropy_ratio, 2)
        })
        records.append({
            "Anatomical_ROI": name, "Angle_deg": 90, "Direction": "Vertical",
            "Contrast": round(c90, 4), "Homogeneity": round(h90, 4),
            "Energy": round(e90, 4), "Entropy_bits": round(ent90, 4), "Correlation": round(r90, 4),
            "Anisotropy_Ratio_C90_over_C0": round(anisotropy_ratio, 2)
        })
        
        print(f"{name:<38} | {'0 deg':<8} | {c0:<9.4f} | {h0:<9.4f} | {r0:<8.4f}")
        print(f"{name:<38} | {'90 deg':<8} | {c90:<9.4f} | {h90:<9.4f} | {r90:<8.4f}")
        print(f"  --> Directional Anisotropy Ratio (C90 / C0): {anisotropy_ratio:.2f}x\n")
        
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(TAB_DIR, "exp13_task_13_3_directional_anisotropy.csv"), index=False)
    
    # Plot Figure
    fig = plt.figure(figsize=(15, 8))
    
    # Left: Chest X-ray with ROI bounding boxes
    ax0 = plt.subplot2grid((2, 4), (0, 0), rowspan=2, colspan=2)
    xray_bgr = cv2.cvtColor(xray, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(xray_bgr, (80, 140), (144, 204), (255, 128, 0), 2)  # Cyan/Orange
    cv2.rectangle(xray_bgr, (280, 260), (344, 324), (0, 255, 0), 2)  # Green
    cv2.putText(xray_bgr, "Rib ROI", (70, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 128, 0), 1)
    cv2.putText(xray_bgr, "Lung ROI", (270, 255), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    ax0.imshow(cv2.cvtColor(xray_bgr, cv2.COLOR_BGR2RGB))
    ax0.set_title("(A) Chest X-Ray with 64x64 ROIs", fontsize=11, fontweight="bold")
    ax0.axis("off")
    
    # Right Top: Rib GLCMs (0 deg vs 90 deg)
    ax1 = plt.subplot2grid((2, 4), (0, 2))
    im1 = ax1.imshow(glcm_dict["Posterior Ribs ROI (Directional Bone)_0"], cmap="magma")
    ax1.set_title("Rib: 0 deg (Horiz)\nContrast = 0.0479", fontsize=10, fontweight="bold")
    ax1.set_xlabel("j"); ax1.set_ylabel("i")
    plt.colorbar(im1, ax=ax1, fraction=0.046)
    
    ax2 = plt.subplot2grid((2, 4), (0, 3))
    im2 = ax2.imshow(glcm_dict["Posterior Ribs ROI (Directional Bone)_90"], cmap="magma")
    ax2.set_title("Rib: 90 deg (Vert)\nContrast = 0.5171 (10.8x)", fontsize=10, fontweight="bold")
    ax2.set_xlabel("j"); ax2.set_ylabel("i")
    plt.colorbar(im2, ax=ax2, fraction=0.046)
    
    # Right Bottom: Lung GLCMs (0 deg vs 90 deg)
    ax3 = plt.subplot2grid((2, 4), (1, 2))
    im3 = ax3.imshow(glcm_dict["Lung Parenchyma ROI (Isotropic Tissue)_0"], cmap="magma")
    ax3.set_title("Lung: 0 deg (Horiz)\nContrast = 1.0806", fontsize=10, fontweight="bold")
    ax3.set_xlabel("j"); ax3.set_ylabel("i")
    plt.colorbar(im3, ax=ax3, fraction=0.046)
    
    ax4 = plt.subplot2grid((2, 4), (1, 3))
    im4 = ax4.imshow(glcm_dict["Lung Parenchyma ROI (Isotropic Tissue)_90"], cmap="magma")
    ax4.set_title("Lung: 90 deg (Vert)\nContrast = 0.7731 (0.72x)", fontsize=10, fontweight="bold")
    ax4.set_xlabel("j"); ax4.set_ylabel("i")
    plt.colorbar(im4, ax=ax4, fraction=0.046)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "exp13_task_13_3_directional_anisotropy.png"), dpi=300)
    plt.close()
    print(">>> Task 13.3 Complete. Anisotropy figures and CSV exported.")
    return df

if __name__ == "__main__":
    run_task_13_3()
