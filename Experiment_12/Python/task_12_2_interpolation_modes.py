"""
Experiment 12: Task 12.2 - Interpolation Method Comparison (Nearest vs. Bilinear vs. Bicubic)
Course: Medical Image Processing (BMI-701) | Riphah International University
Student: Muhammad Ikrama (Reg ID: 60140)
Instructor: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import pandas as pd
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt

def run_task_12_2():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.abspath(os.path.join(script_dir, ".."))
    inputs_dir = os.path.join(exp_dir, "Inputs", "images")
    outputs_dir = os.path.join(exp_dir, "Outputs", "Python")
    tables_dir = os.path.join(exp_dir, "Tables")
    os.makedirs(outputs_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)
    
    mri_path = os.path.join(inputs_dir, "Brain_MRI.png")
    mri = cv2.imread(mri_path, cv2.IMREAD_GRAYSCALE)
    if mri is None:
        raise FileNotFoundError(f"Brain_MRI.png not found at {mri_path}")
        
    h, w = mri.shape
    center = (w / 2.0, h / 2.0)
    theta = 15.0
    
    M_fwd = cv2.getRotationMatrix2D(center, theta, 1.0)
    M_bwd = cv2.getRotationMatrix2D(center, -theta, 1.0)
    
    # Intracranial evaluation mask
    brain_mask = (mri > 25).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (35, 35))
    eval_mask = (cv2.erode(brain_mask, kernel) > 0)
    
    modes = [
        ("Nearest-Neighbor", cv2.INTER_NEAREST, "0th-Order Step Discontinuities (Jagged Edges)"),
        ("Bilinear", cv2.INTER_LINEAR, "1st-Order Linear Weighting (Smooth, Standard)"),
        ("Bicubic", cv2.INTER_CUBIC, "3rd-Order Spline (Sharp, High-Fidelity)")
    ]
    
    print("\n" + "=" * 90)
    print("TASK 12.2: INTERPOLATION METHOD COMPARISON (NEAREST VS. BILINEAR VS. BICUBIC)")
    print("=" * 90)
    print(f"{'Interpolation Mode':<22} | {'PSNR (dB)':<12} | {'SSIM':<10} | {'MSE':<10} | {'MAE':<10} | {'Visual Quality'}")
    print("-" * 90)
    
    results = {}
    records = []
    
    for name, flag, desc in modes:
        # Rotate forward and backward
        fwd = cv2.warpAffine(mri, M_fwd, (w, h), flags=flag)
        bwd = cv2.warpAffine(fwd, M_bwd, (w, h), flags=flag)
        results[name] = bwd
        
        orig_px = mri[eval_mask].astype(float)
        bwd_px = bwd[eval_mask].astype(float)
        diff = np.abs(orig_px - bwd_px)
        
        mse = float(np.mean(diff ** 2))
        mae = float(np.mean(diff))
        psnr = float(10.0 * np.log10((255.0 ** 2) / (mse + 1e-12)))
        ssim_val = float(ssim(mri, bwd, data_range=255))
        
        print(f"{name:<22} | {psnr:<12.2f} | {ssim_val:<10.4f} | {mse:<10.2f} | {mae:<10.2f} | {desc.split('(')[0]}")
        records.append({
            "Interpolation_Method": name,
            "Evaluation_Region": "Intracranial Parenchyma",
            "PSNR_dB": round(psnr, 2),
            "SSIM": round(ssim_val, 4),
            "MSE": round(mse, 2),
            "MAE": round(mae, 2),
            "Observed_Artifact": desc
        })
        
    df = pd.DataFrame(records)
    csv_path = os.path.join(tables_dir, "exp12_task_12_2_interpolation_metrics.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SAVED] Task 12.2 table saved to: {csv_path}")
    
    # Figure: Full Images and Zoomed Cortical Sulci Comparison
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    
    # Crop region around tumor and cortical sulci
    rx, ry, rw, rh = 280, 210, 80, 80
    
    for col_idx, (name, flag, desc) in enumerate(modes):
        bwd = results[name]
        
        # Row 1: Full Image with Crop Box
        axes[0, col_idx].imshow(bwd, cmap="gray")
        rect = plt.Rectangle((rx, ry), rw, rh, linewidth=1.8, edgecolor="yellow", facecolor="none")
        axes[0, col_idx].add_patch(rect)
        axes[0, col_idx].set_title(f"{name} (Full Scan)\nPSNR = {records[col_idx]['PSNR_dB']:.2f} dB", fontsize=11, fontweight="bold")
        axes[0, col_idx].axis("off")
        
        # Row 2: Zoomed 80x80 Cortical Crop
        crop = bwd[ry:ry+rh, rx:rx+rw]
        axes[1, col_idx].imshow(crop, cmap="gray", interpolation="nearest")
        axes[1, col_idx].set_title(f"Zoomed Crop (Sulci Detail)\nSSIM = {records[col_idx]['SSIM']:.4f}", fontsize=10, fontweight="bold")
        axes[1, col_idx].axis("off")
        
    plt.tight_layout()
    fig_path = os.path.join(outputs_dir, "exp12_task_12_2_interpolation_comparison.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"[SAVED] Task 12.2 figure saved to: {fig_path}")

if __name__ == "__main__":
    run_task_12_2()
