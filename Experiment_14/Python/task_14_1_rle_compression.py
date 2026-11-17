"""
Task 14.1: Custom Run-Length Encoding (RLE) Compressor & Bit-Exact Verification
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

def rle_encode(img):
    flat = img.ravel()
    n = len(flat)
    if n == 0: return []
    runs = []
    val = flat[0]
    count = 1
    for i in range(1, n):
        if flat[i] == val:
            count += 1
        else:
            runs.append((int(val), int(count)))
            val = flat[i]
            count = 1
    runs.append((int(val), int(count)))
    return runs

def rle_decode(runs, shape):
    out = []
    for val, count in runs:
        out.extend([val] * count)
    return np.array(out, dtype=np.uint8).reshape(shape)

def run_task_14_1():
    print("=" * 80)
    print("TASK 14.1: CUSTOM RUN-LENGTH ENCODING (RLE) COMPRESSOR")
    print("=" * 80)
    
    mri_path = os.path.join(IMG_DIR, "Brain_MRI.png")
    mri = cv2.imread(mri_path, cv2.IMREAD_GRAYSCALE)
    if mri is None:
        raise FileNotFoundError(f"Brain MRI not found at {mri_path}")
        
    # Generate binary mask via Otsu's thresholding
    _, bin_mask = cv2.threshold(mri, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    records = []
    inputs = [("Binary Otsu Mask (High Redundancy)", bin_mask),
              ("Raw 8-bit Grayscale MRI (Noisy Pixels)", mri)]
              
    print(f"{'Input Target':<38} | {'Raw Bytes':<10} | {'Runs':<7} | {'RLE Bytes':<10} | {'CR':<6} | {'MSE':<6} | {'Status'}")
    print("-" * 88)
    
    dec_images = {}
    for name, img in inputs:
        runs = rle_encode(img)
        raw_b = img.size
        # Each run stores (value: 1 byte uint8, count: 2 bytes uint16) = 3 bytes
        comp_b = len(runs) * 3
        cr = raw_b / float(comp_b)
        ss = (1.0 - (1.0 / cr)) * 100.0
        dec = rle_decode(runs, img.shape)
        dec_images[name] = dec
        mse = float(np.mean((img.astype(float) - dec.astype(float)) ** 2))
        
        assert mse == 0.0, f"RLE reconstruction error: MSE = {mse}"
        status = "BIT-EXACT (PASS)"
        
        records.append({
            "Input_Type": name,
            "Raw_Bytes": raw_b,
            "Total_Runs": len(runs),
            "RLE_Compressed_Bytes": comp_b,
            "Compression_Ratio": round(cr, 2),
            "Space_Saving_Pct": round(ss, 1),
            "MSE": round(mse, 4),
            "Reconstruction_Status": status
        })
        print(f"{name:<38} | {raw_b:<10d} | {len(runs):<7d} | {comp_b:<10d} | {cr:<5.2f}x | {mse:<6.4f} | {status}")
        
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(TAB_DIR, "exp14_task_14_1_rle_summary.csv"), index=False)
    
    # Plotting Figure
    fig, axes = plt.subplots(1, 4, figsize=(18, 4.5))
    
    axes[0].imshow(bin_mask, cmap="gray")
    axes[0].set_title("(A) Binary Otsu Mask\nRaw: 262,144 Bytes", fontsize=10, fontweight="bold")
    axes[0].axis("off")
    
    axes[1].imshow(dec_images["Binary Otsu Mask (High Redundancy)"], cmap="gray")
    cr_b = df.loc[0, "Compression_Ratio"]
    axes[1].set_title(f"(B) Decoded Binary Mask\nCR = {cr_b:.2f}x (MSE = 0.000)", fontsize=10, fontweight="bold")
    axes[1].axis("off")
    
    axes[2].imshow(mri, cmap="gray")
    axes[2].set_title("(C) Raw 8-bit Grayscale MRI\nRaw: 262,144 Bytes", fontsize=10, fontweight="bold")
    axes[2].axis("off")
    
    axes[3].imshow(dec_images["Raw 8-bit Grayscale MRI (Noisy Pixels)"], cmap="gray")
    cr_g = df.loc[1, "Compression_Ratio"]
    axes[3].set_title(f"(D) Decoded Grayscale MRI\nCR = {cr_g:.2f}x (Expansion! MSE = 0.000)", fontsize=10, fontweight="bold")
    axes[3].axis("off")
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "exp14_task_14_1_rle_plots.png"), dpi=300)
    plt.close()
    print(">>> Task 14.1 Complete. RLE figures and CSV exported.")
    return df

if __name__ == "__main__":
    run_task_14_1()
