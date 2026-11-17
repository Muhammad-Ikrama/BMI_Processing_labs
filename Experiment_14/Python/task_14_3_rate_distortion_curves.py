"""
Task 14.3: Multi-Modality Rate-Distortion Curve Benchmarking
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

def eval_metrics(orig, dec, n_bytes):
    raw_b = orig.size
    cr = raw_b / float(n_bytes)
    mse = float(np.mean((orig.astype(float) - dec.astype(float)) ** 2))
    psnr = float('inf') if mse == 0 else 10.0 * np.log10((255.0 ** 2) / mse)
    x, y = orig.astype(float), dec.astype(float)
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    mx, my = cv2.GaussianBlur(x, (11, 11), 1.5), cv2.GaussianBlur(y, (11, 11), 1.5)
    sx2 = cv2.GaussianBlur(x**2, (11, 11), 1.5) - mx**2
    sy2 = cv2.GaussianBlur(y**2, (11, 11), 1.5) - my**2
    sxy = cv2.GaussianBlur(x * y, (11, 11), 1.5) - mx * my
    ssim = float(np.mean(((2 * mx * my + c1) * (2 * sxy + c2)) / ((mx**2 + my**2 + c1) * (sx2 + sy2 + c2))))
    return cr, mse, psnr, ssim

def run_task_14_3():
    print("=" * 80)
    print("TASK 14.3: MULTI-MODALITY RATE-DISTORTION CURVE BENCHMARKING")
    print("=" * 80)
    
    mri = cv2.imread(os.path.join(IMG_DIR, "Brain_MRI.png"), cv2.IMREAD_GRAYSCALE)
    xray = cv2.imread(os.path.join(IMG_DIR, "Chest_Xray.png"), cv2.IMREAD_GRAYSCALE)
    
    modalities = [("Brain MRI", mri), ("Chest X-Ray", xray)]
    qualities = [95, 85, 70, 50, 30, 15, 5]
    
    records = []
    print(f"{'Modality':<14} | {'Q Factor':<9} | {'CR':<6} | {'MSE':<7} | {'PSNR (dB)':<10} | {'SSIM'}")
    print("-" * 62)
    
    for mod_name, img in modalities:
        for q in qualities:
            _, buf = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, q])
            dec = cv2.imdecode(buf, cv2.IMREAD_GRAYSCALE)
            cr, mse, psnr_v, ssim_v = eval_metrics(img, dec, len(buf))
            records.append({
                "Modality": mod_name, "Quality_Q": q, "Compressed_Bytes": len(buf),
                "Compression_Ratio": round(cr, 2), "MSE": round(mse, 2),
                "PSNR_dB": round(psnr_v, 2), "SSIM": round(ssim_v, 4)
            })
            print(f"{mod_name:<14} | {q:<9d} | {cr:<5.2f}x | {mse:<7.2f} | {psnr_v:<10.2f} | {ssim_v:.4f}")
            
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(TAB_DIR, "exp14_task_14_3_multimodal_rd.csv"), index=False)
    
    # Plotting Overlapping Curves
    df_mri = df[df["Modality"] == "Brain MRI"]
    df_xray = df[df["Modality"] == "Chest X-Ray"]
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 1. PSNR vs CR
    axes[0].plot(df_mri["Compression_Ratio"], df_mri["PSNR_dB"], "o-", color="#1f77b4", linewidth=2, markersize=6, label="Brain MRI (Complex Sulci)")
    axes[0].plot(df_xray["Compression_Ratio"], df_xray["PSNR_dB"], "s--", color="#ff7f0e", linewidth=2, markersize=6, label="Chest X-Ray (Smooth Parenchyma)")
    axes[0].axhline(40.0, color="green", linestyle=":", linewidth=1.5, label="Diagnostic Limit (40 dB)")
    axes[0].set_title("(A) PSNR vs. Compression Ratio (CR)", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("Compression Ratio (CR)", fontsize=10)
    axes[0].set_ylabel("PSNR (dB)", fontsize=10)
    axes[0].grid(True, linestyle="--", alpha=0.5)
    axes[0].legend(fontsize=9)
    
    # 2. SSIM vs CR
    axes[1].plot(df_mri["Compression_Ratio"], df_mri["SSIM"], "o-", color="#1f77b4", linewidth=2, markersize=6, label="Brain MRI")
    axes[1].plot(df_xray["Compression_Ratio"], df_xray["SSIM"], "s--", color="#ff7f0e", linewidth=2, markersize=6, label="Chest X-Ray")
    axes[1].axhline(0.980, color="green", linestyle=":", linewidth=1.5, label="High Fidelity Limit (0.980)")
    axes[1].set_title("(B) SSIM vs. Compression Ratio (CR)", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("Compression Ratio (CR)", fontsize=10)
    axes[1].set_ylabel("Structural Similarity Index (SSIM)", fontsize=10)
    axes[1].grid(True, linestyle="--", alpha=0.5)
    axes[1].legend(fontsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "exp14_task_14_3_multimodal_rd_plots.png"), dpi=300)
    plt.close()
    print(">>> Task 14.3 Complete. Rate-distortion curves exported.")
    return df

if __name__ == "__main__":
    run_task_14_3()
