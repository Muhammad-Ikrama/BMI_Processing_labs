"""
Task 14.4: 8x8 DCT Blocking Artifact & Residual Error Map Visualization
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

def run_task_14_4():
    print("=" * 80)
    print("TASK 14.4: 8x8 DCT BLOCKING ARTIFACT & RESIDUAL ERROR MAP VISUALIZATION")
    print("=" * 80)
    
    mri = cv2.imread(os.path.join(IMG_DIR, "Brain_MRI.png"), cv2.IMREAD_GRAYSCALE)
    if mri is None:
        raise FileNotFoundError("Missing Brain_MRI.png")
        
    qualities = [85, 25, 5]
    records = []
    error_maps = {}
    crops = {}
    
    # Tumor / ventricle 64x64 ROI: [215:279, 295:359]
    r0, r1, c0, c1 = 215, 279, 295, 359
    crop_orig = mri[r0:r1, c0:c1]
    
    print(f"{'JPEG Quality':<14} | {'Mean Absolute Err':<18} | {'Max Absolute Err':<18} | {'Root MSE':<12}")
    print("-" * 68)
    
    for q in qualities:
        _, buf = cv2.imencode('.jpg', mri, [cv2.IMWRITE_JPEG_QUALITY, q])
        dec = cv2.imdecode(buf, cv2.IMREAD_GRAYSCALE)
        
        diff = np.abs(mri.astype(float) - dec.astype(float))
        mae = float(np.mean(diff))
        max_err = float(np.max(diff))
        rmse = float(np.sqrt(np.mean(diff ** 2)))
        
        error_maps[q] = diff
        crops[q] = dec[r0:r1, c0:c1]
        
        records.append({
            "Quality_Q": q,
            "Mean_Absolute_Error": round(mae, 3),
            "Max_Absolute_Error": round(max_err, 2),
            "RMSE": round(rmse, 3)
        })
        print(f"JPEG Q={q:<8d} | {mae:<18.3f} | {max_err:<18.2f} | {rmse:<12.3f}")
        
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(TAB_DIR, "exp14_task_14_4_error_stats.csv"), index=False)
    
    # Plotting Figure (2 rows x 4 columns: Orig + 3 Qualities for crops and amplified error maps)
    fig, axes = plt.subplots(2, 4, figsize=(18, 9))
    
    # Row 1: 64x64 Magnified Crops
    axes[0, 0].imshow(crop_orig, cmap="gray", interpolation="nearest")
    axes[0, 0].set_title("(A1) Original 64x64 Crop\n(Bit-Exact Uncompressed)", fontsize=10, fontweight="bold")
    axes[0, 0].axis("off")
    
    for idx, q in enumerate(qualities, 1):
        axes[0, idx].imshow(crops[q], cmap="gray", interpolation="nearest")
        title_suffix = "Smooth Edge" if q == 85 else ("Moderate Tile" if q == 25 else "Severe 8x8 Mosaic")
        axes[0, idx].set_title(f"(A{idx+1}) JPEG Q={q} Crop\n{title_suffix}", fontsize=10, fontweight="bold")
        axes[0, idx].axis("off")
        
    # Row 2: Amplified Error Maps (|I - I_hat| x 5)
    axes[1, 0].imshow(mri, cmap="gray")
    axes[1, 0].set_title("(B1) Full Brain MRI\nReference Scan", fontsize=10, fontweight="bold")
    axes[1, 0].axis("off")
    
    for idx, q in enumerate(qualities, 1):
        amp_err = np.clip(error_maps[q] * 5.0, 0, 255)
        im = axes[1, idx].imshow(amp_err, cmap="hot", interpolation="nearest")
        axes[1, idx].set_title(f"(B{idx+1}) Error Map (Q={q}) x 5\nMAE = {df.loc[idx-1, 'Mean_Absolute_Error']:.2f}", fontsize=10, fontweight="bold")
        axes[1, idx].axis("off")
        plt.colorbar(im, ax=axes[1, idx], fraction=0.046, pad=0.04)
        
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "exp14_task_14_4_blocking_artifacts.png"), dpi=300)
    plt.close()
    print(">>> Task 14.4 Complete. Artifact maps and error statistics exported.")
    return df

if __name__ == "__main__":
    run_task_14_4()
