"""
Experiment 12: Task 12.1 - 2D Homogeneous Rigid Transformation Matrix Construction
Course: Medical Image Processing (BMI-701) | Riphah International University
Student: Muhammad Ikrama (Reg ID: 60140)
Instructor: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def build_rigid_matrix_2d(tx, ty, theta_deg, cx=256.0, cy=256.0):
    rad = np.radians(theta_deg)
    cos_t = np.cos(rad)
    sin_t = np.sin(rad)
    
    # Translation to origin
    T_to_orig = np.array([
        [1.0, 0.0, -cx],
        [0.0, 1.0, -cy],
        [0.0, 0.0, 1.0]
    ])
    # Pure rotation around origin
    R = np.array([
        [cos_t, -sin_t, 0.0],
        [sin_t, cos_t, 0.0],
        [0.0, 0.0, 1.0]
    ])
    # Translation back from origin plus user shift (tx, ty)
    T_back = np.array([
        [1.0, 0.0, cx + tx],
        [0.0, 1.0, cy + ty],
        [0.0, 0.0, 1.0]
    ])
    
    # Full composite transformation: T_composite = T_back @ R @ T_to_orig
    T_composite = T_back @ R @ T_to_orig
    return T_composite

def run_task_12_1():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.abspath(os.path.join(script_dir, ".."))
    inputs_dir = os.path.join(exp_dir, "Inputs", "images")
    outputs_dir = os.path.join(exp_dir, "Outputs", "Python")
    tables_dir = os.path.join(exp_dir, "Tables")
    os.makedirs(outputs_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)
    
    ct_path = os.path.join(inputs_dir, "Head_CT.png")
    ct = cv2.imread(ct_path, cv2.IMREAD_GRAYSCALE)
    if ct is None:
        raise FileNotFoundError(f"Head_CT.png not found at {ct_path}")
        
    h, w = ct.shape
    cx, cy = w / 2.0, h / 2.0
    
    # 1. Construct 3x3 Forward Transformation Matrix
    tx, ty, theta_deg = -15.0, +12.0, 22.0
    T_forward = build_rigid_matrix_2d(tx, ty, theta_deg, cx, cy)
    
    # 2. Invert analytically
    T_inv = np.linalg.inv(T_forward)
    
    # 3. Apply Forward & Inverse Transformations
    ct_forward = cv2.warpAffine(ct, T_forward[:2, :], (w, h), flags=cv2.INTER_LINEAR)
    ct_recovered = cv2.warpAffine(ct_forward, T_inv[:2, :], (w, h), flags=cv2.INTER_LINEAR)
    
    # 4. Restrict quantitative error analysis to intracranial brain parenchyma (erode boundary to avoid FOV edge artifacts)
    brain_mask = cv2.inRange(ct, 20, 180)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (35, 35))
    inner_parenchyma_mask = cv2.erode(brain_mask, kernel) > 0
    num_eval_pixels = int(inner_parenchyma_mask.sum())
    
    orig_eval = ct[inner_parenchyma_mask].astype(float)
    rec_eval = ct_recovered[inner_parenchyma_mask].astype(float)
    diff_eval = np.abs(orig_eval - rec_eval)
    
    mse = float(np.mean(diff_eval ** 2))
    mae = float(np.mean(diff_eval))
    max_err = float(np.max(diff_eval))
    psnr = float(10.0 * np.log10((255.0 ** 2) / (mse + 1e-12)))
    
    print("\n" + "=" * 90)
    print("TASK 12.1: 2D HOMOGENEOUS RIGID TRANSFORMATION MATRIX CONSTRUCTION")
    print("=" * 90)
    print(f"{'Evaluation Region':<25} | {'Evaluated Px':<14} | {'MAE (Int)':<10} | {'MSE':<10} | {'Max Error':<10} | {'PSNR (dB)'}")
    print("-" * 90)
    print(f"{'Intracranial Parenchyma':<25} | {num_eval_pixels:<14d} | {mae:<10.4f} | {mse:<10.4f} | {max_err:<10.2f} | {psnr:.2f} dB")
    
    # Verify Identity Reconstruction
    T_identity = T_forward @ T_inv
    frob_norm_diff = float(np.linalg.norm(T_identity - np.eye(3)))
    print(f">>> Forward-Inverse Matrix Verification: ||T_fwd @ T_inv - I|| = {frob_norm_diff:.2e}")
    
    records = [{
        "Transformation_Type": "Rigid (tx=-15, ty=+12, theta=22 deg)",
        "Matrix_Determinant": round(float(np.linalg.det(T_forward)), 6),
        "Identity_Deviation": frob_norm_diff,
        "Evaluated_Parenchyma_Pixels": num_eval_pixels,
        "Mean_Absolute_Error_MAE": round(mae, 4),
        "Mean_Squared_Error_MSE": round(mse, 4),
        "Max_Intensity_Error": round(max_err, 2),
        "Parenchyma_PSNR_dB": round(psnr, 2)
    }]
    df = pd.DataFrame(records)
    csv_path = os.path.join(tables_dir, "exp12_task_12_1_matrix_error.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SAVED] Task 12.1 table saved to: {csv_path}")
    
    # Figure: Multi-Panel Visualization
    fig, axes = plt.subplots(1, 4, figsize=(16, 4.2))
    
    axes[0].imshow(ct, cmap="gray")
    axes[0].set_title("1. Original Reference Head CT\n(Unmoved Base Pose)", fontsize=10, fontweight="bold")
    axes[0].axis("off")
    
    axes[1].imshow(ct_forward, cmap="gray")
    axes[1].set_title(f"2. Forward Transformed\n(θ=+22°, tx=-15, ty=+12)", fontsize=10, fontweight="bold")
    axes[1].axis("off")
    
    axes[2].imshow(ct_recovered, cmap="gray")
    axes[2].set_title(f"3. Inverse Recovered T^(-1)\n(PSNR = {psnr:.2f} dB)", fontsize=10, fontweight="bold")
    axes[2].axis("off")
    
    # Difference map inside parenchyma
    diff_map = np.zeros_like(ct, dtype=float)
    diff_map[inner_parenchyma_mask] = np.abs(ct.astype(float) - ct_recovered.astype(float))[inner_parenchyma_mask]
    im_d = axes[3].imshow(diff_map, cmap="hot", vmin=0, vmax=15)
    axes[3].set_title(f"4. Parenchyma Error Map\n(MAE = {mae:.2f} intensity units)", fontsize=10, fontweight="bold")
    axes[3].axis("off")
    plt.colorbar(im_d, ax=axes[3], fraction=0.046, pad=0.04)
    
    plt.tight_layout()
    fig_path = os.path.join(outputs_dir, "exp12_task_12_1_homogeneous_matrix.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"[SAVED] Task 12.1 figure saved to: {fig_path}")

if __name__ == "__main__":
    run_task_12_1()
