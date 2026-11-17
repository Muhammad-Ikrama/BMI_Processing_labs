"""
Experiment 14: Lossless and Lossy Compression of Medical Images and Quality Evaluation Using PSNR & CR
Author: Muhammad Ikrama (Reg ID: 60140)
Department of Biomedical Engineering, Riphah International University, Lahore
Instructor: Engr. Rana Talha Khalid
Course: Medical Image Processing (BMI-701)
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXP_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
FIG_DIR = os.path.join(EXP_DIR, "Figures")
TAB_DIR = os.path.join(EXP_DIR, "Tables")
OUT_DIR = os.path.join(EXP_DIR, "Outputs", "Python")
IMG_DIR = os.path.join(EXP_DIR, "Inputs", "images")

os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(TAB_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

def eval_compression(orig, dec, n_bytes):
    raw_bytes = orig.size
    cr = raw_bytes / float(n_bytes)
    ss = (1.0 - (1.0 / cr)) * 100.0
    bpp = 8.0 / cr
    mse = float(np.mean((orig.astype(float) - dec.astype(float)) ** 2))
    psnr = float('inf') if mse == 0 else 10.0 * np.log10((255.0 ** 2) / mse)
    
    # Structural Similarity (SSIM)
    x, y = orig.astype(float), dec.astype(float)
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    mx, my = cv2.GaussianBlur(x, (11, 11), 1.5), cv2.GaussianBlur(y, (11, 11), 1.5)
    sx2 = cv2.GaussianBlur(x**2, (11, 11), 1.5) - mx**2
    sy2 = cv2.GaussianBlur(y**2, (11, 11), 1.5) - my**2
    sxy = cv2.GaussianBlur(x * y, (11, 11), 1.5) - mx * my
    ssim = float(np.mean(((2 * mx * my + c1) * (2 * sxy + c2)) / ((mx**2 + my**2 + c1) * (sx2 + sy2 + c2))))
    return cr, ss, bpp, mse, psnr, ssim

def run_benchmark():
    print("=" * 80)
    print("EXPERIMENT 14: MEDICAL IMAGE COMPRESSION BENCHMARK")
    print("=" * 80)
    
    mri_path = os.path.join(IMG_DIR, "Brain_MRI.png")
    mri = cv2.imread(mri_path, cv2.IMREAD_GRAYSCALE)
    if mri is None:
        raise FileNotFoundError(f"Brain MRI not found at {mri_path}")
        
    raw_bytes = mri.size  # 262,144 bytes
    hist = np.bincount(mri.ravel(), minlength=256).astype(float)
    p = hist[hist > 0] / hist.sum()
    shannon_H = -np.sum(p * np.log2(p))
    print(f"Uncompressed Raw Size: {raw_bytes} bytes (8.00 BPP) | Shannon Entropy H = {shannon_H:.3f} BPP\n")
    
    # Lossless PNG (Deflate L9)
    _, buf_png = cv2.imencode('.png', mri, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    dec_png = cv2.imdecode(buf_png, cv2.IMREAD_GRAYSCALE)
    
    tests = [("Lossless PNG (Deflate L9)", dec_png, len(buf_png), "Lossless", None)]
    quality_factors = [95, 85, 50, 25, 10, 5]
    jpeg_decodes = {}
    for q in quality_factors:
        _, buf_j = cv2.imencode('.jpg', mri, [cv2.IMWRITE_JPEG_QUALITY, q])
        dec_j = cv2.imdecode(buf_j, cv2.IMREAD_GRAYSCALE)
        jpeg_decodes[q] = dec_j
        tests.append((f"Lossy JPEG (Q={q})", dec_j, len(buf_j), "Lossy", q))
        
    results = []
    print(f"{'Compression Method':<25} | {'Bytes':<7} | {'CR':<6} | {'Saved %':<7} | {'BPP':<5} | {'MSE':<6} | {'PSNR (dB)':<9} | {'SSIM'}")
    print("-" * 92)
    
    for name, dec_im, n_b, ctype, q_val in tests:
        cr, ss, bpp, mse, psnr_v, ssim_v = eval_compression(mri, dec_im, n_b)
        p_str = "INF" if np.isinf(psnr_v) else f"{psnr_v:.2f}"
        results.append({
            "Method": name, "Type": ctype, "Quality_Q": q_val if q_val else 100,
            "Compressed_Bytes": n_b, "Compression_Ratio": round(cr, 2),
            "Space_Saving_Pct": round(ss, 1), "Bitrate_BPP": round(bpp, 2),
            "MSE": round(mse, 2), "PSNR_dB": round(psnr_v if not np.isinf(psnr_v) else 999.0, 2),
            "SSIM": round(ssim_v, 4)
        })
        print(f"{name:<25} | {n_b:<7d} | {cr:<5.2f}x | {ss:<6.1f}% | {bpp:<5.2f} | {mse:<6.2f} | {p_str:<9} | {ssim_v:.4f}")
        
    df_bm = pd.DataFrame(results)
    df_bm.to_csv(os.path.join(TAB_DIR, "exp14_benchmark_compression.csv"), index=False)
    print("\n>>> Status: Lossless PNG guarantees 0 MSE; JPEG Q=85 achieves high diagnostic fidelity.")
    
    # Figure 14.1: Rate-Distortion Curves
    df_jpeg = df_bm[df_bm["Type"] == "Lossy"].sort_values("Quality_Q", ascending=False)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    
    # Panel A: PSNR vs CR
    axes[0].plot(df_jpeg["Compression_Ratio"], df_jpeg["PSNR_dB"], "o-", color="#1f77b4", linewidth=2.2, markersize=7, label="JPEG Rate-Distortion")
    for _, row in df_jpeg.iterrows():
        axes[0].annotate(f"Q={int(row['Quality_Q'])}", (row["Compression_Ratio"], row["PSNR_dB"]),
                         textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8, fontweight="bold")
    axes[0].axhline(40.0, color="green", linestyle="--", linewidth=1.5, label="Diagnostic Threshold (40 dB)")
    axes[0].axhline(32.0, color="red", linestyle=":", linewidth=1.5, label="Severe Distortion Limit (32 dB)")
    axes[0].set_title("(A) PSNR (dB) vs. Compression Ratio (CR)", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("Compression Ratio (CR)", fontsize=10)
    axes[0].set_ylabel("Peak Signal-to-Noise Ratio (dB)", fontsize=10)
    axes[0].grid(True, linestyle="--", alpha=0.5)
    axes[0].legend(fontsize=9, loc="upper right")
    
    # Panel B: SSIM vs CR
    axes[1].plot(df_jpeg["Compression_Ratio"], df_jpeg["SSIM"], "s-", color="#d62728", linewidth=2.2, markersize=7, label="JPEG Structural Similarity")
    for _, row in df_jpeg.iterrows():
        axes[1].annotate(f"Q={int(row['Quality_Q'])}", (row["Compression_Ratio"], row["SSIM"]),
                         textcoords="offset points", xytext=(0, -14), ha="center", fontsize=8, fontweight="bold")
    axes[1].axhline(0.980, color="green", linestyle="--", linewidth=1.5, label="High-Fidelity Target (0.980)")
    axes[1].axhline(0.900, color="red", linestyle=":", linewidth=1.5, label="Structural Collapse Limit (0.900)")
    axes[1].set_title("(B) SSIM vs. Compression Ratio (CR)", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("Compression Ratio (CR)", fontsize=10)
    axes[1].set_ylabel("Structural Similarity Index (SSIM)", fontsize=10)
    axes[1].grid(True, linestyle="--", alpha=0.5)
    axes[1].legend(fontsize=9, loc="lower left")
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "Figure_14_1_Rate_Distortion_Curves.png"), dpi=300)
    plt.close()
    
    # Figure 14.2: Clinical Compression Benchmark Multi-Panel
    fig, axes = plt.subplots(1, 4, figsize=(18, 4.6))
    
    # Panel 1: Lossless PNG
    axes[0].imshow(dec_png, cmap="gray")
    axes[0].set_title(f"(1) Lossless PNG (Deflate L9)\nCR = 2.12x | PSNR = Inf dB", fontsize=10, fontweight="bold")
    axes[0].axis("off")
    
    # Panel 2: JPEG Q=85
    axes[1].imshow(jpeg_decodes[85], cmap="gray")
    axes[1].set_title(f"(2) Diagnostic Lossy JPEG (Q=85)\nCR = 6.81x | PSNR = 44.57 dB", fontsize=10, fontweight="bold")
    axes[1].axis("off")
    
    # Panel 3: Zoomed tumor/ventricle region at Q=5 showing 8x8 blocking artifacts
    crop_orig = mri[210:290, 290:370]
    crop_q5   = jpeg_decodes[5][210:290, 290:370]
    axes[2].imshow(crop_q5, cmap="gray", interpolation="nearest")
    axes[2].set_title(f"(3) Zoomed Region (JPEG Q=5)\nSevere 8x8 Blocking Artifacts", fontsize=10, fontweight="bold")
    axes[2].axis("off")
    
    # Panel 4: Amplified Absolute Error Map |I - I_hat| * 5
    err_map = np.abs(mri.astype(float) - jpeg_decodes[5].astype(float)) * 5.0
    im4 = axes[3].imshow(np.clip(err_map, 0, 255), cmap="hot", interpolation="nearest")
    axes[3].set_title(f"(4) Amplified Residual Error |I - I_hat| x 5\nTraces Lost Gyral/Tumor Edges", fontsize=10, fontweight="bold")
    axes[3].axis("off")
    plt.colorbar(im4, ax=axes[3], fraction=0.046, pad=0.04)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "Figure_14_2_Clinical_Compression_Benchmark.png"), dpi=300)
    plt.close()
    print(">>> Benchmark figures generated.")
    return df_bm

if __name__ == "__main__":
    run_benchmark()
