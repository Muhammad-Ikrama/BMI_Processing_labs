"""
Task 14.2: Shannon First-Order Entropy & Redundancy Comparison Across Modalities
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

def run_task_14_2():
    print("=" * 80)
    print("TASK 14.2: SHANNON ENTROPY & REDUNDANCY COMPARISON ACROSS MODALITIES")
    print("=" * 80)
    
    datasets = [
        ("Brain MRI", os.path.join(IMG_DIR, "Brain_MRI.png")),
        ("Head CT", os.path.join(IMG_DIR, "Head_CT.png")),
        ("Chest X-Ray", os.path.join(IMG_DIR, "Chest_Xray.png"))
    ]
    
    records = []
    hist_data = {}
    
    print(f"{'Medical Modality':<16} | {'Dimensions':<12} | {'Raw Bytes':<10} | {'Entropy H':<12} | {'Max 1st-Order CR':<17} | {'PNG Bytes':<10} | {'PNG CR'}")
    print("-" * 92)
    
    for name, path in datasets:
        im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if im is None:
            raise FileNotFoundError(f"Missing image {path}")
            
        raw_b = im.size
        hist = np.bincount(im.ravel(), minlength=256).astype(float)
        hist_data[name] = (im, hist)
        
        p = hist[hist > 0] / hist.sum()
        H = -np.sum(p * np.log2(p))
        cr_shannon = 8.0 / H
        
        _, buf_png = cv2.imencode('.png', im, [cv2.IMWRITE_PNG_COMPRESSION, 9])
        png_b = len(buf_png)
        cr_png = raw_b / float(png_b)
        ss_png = (1.0 - (1.0 / cr_png)) * 100.0
        
        records.append({
            "Modality": name,
            "Dimensions": f"{im.shape[0]}x{im.shape[1]}",
            "Raw_Bytes": raw_b,
            "Shannon_Entropy_bpp": round(H, 3),
            "Max_First_Order_CR": round(cr_shannon, 2),
            "PNG_Lossless_Bytes": png_b,
            "PNG_Compression_Ratio": round(cr_png, 2),
            "PNG_Space_Saving_Pct": round(ss_png, 1)
        })
        print(f"{name:<16} | {f'{im.shape[0]}x{im.shape[1]}':<12} | {raw_b:<10d} | {H:<12.3f} | {cr_shannon:<17.2f}x | {png_b:<10d} | {cr_png:.2f}x")
        
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(TAB_DIR, "exp14_task_14_2_entropy_comparison.csv"), index=False)
    
    # Plotting Figure (Images and Histograms)
    fig, axes = plt.subplots(2, 3, figsize=(16, 8))
    
    colors = ["#1f77b4", "#2ca02c", "#ff7f0e"]
    for idx, (name, path) in enumerate(datasets):
        im, hist = hist_data[name]
        H_val = df.loc[idx, "Shannon_Entropy_bpp"]
        cr_sh = df.loc[idx, "Max_First_Order_CR"]
        cr_p = df.loc[idx, "PNG_Compression_Ratio"]
        
        # Image row
        axes[0, idx].imshow(im, cmap="gray")
        axes[0, idx].set_title(f"{name}\nRaw: {im.size:,} Bytes", fontsize=11, fontweight="bold")
        axes[0, idx].axis("off")
        
        # Histogram row
        axes[1, idx].plot(hist, color=colors[idx], linewidth=1.5)
        axes[1, idx].set_title(f"Histogram: H = {H_val:.3f} bpp\n1st-Order CR: {cr_sh:.2f}x | PNG CR: {cr_p:.2f}x", fontsize=10, fontweight="bold")
        axes[1, idx].set_xlabel("Gray Level (0-255)", fontsize=9)
        axes[1, idx].set_ylabel("Pixel Frequency", fontsize=9)
        axes[1, idx].grid(True, linestyle="--", alpha=0.5)
        
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "exp14_task_14_2_entropy_histograms.png"), dpi=300)
    plt.close()
    print(">>> Task 14.2 Complete. Histograms and CSV exported.")
    return df

if __name__ == "__main__":
    run_task_14_2()
