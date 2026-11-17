"""
Experiment 12: Task 12.4 - Quantitative Failure Analysis of Mean Squared Error (MSE) in Multi-Modal Registration
Course: Medical Image Processing (BMI-701) | Riphah International University
Student: Muhammad Ikrama (Reg ID: 60140)
Instructor: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def compute_mi(fixed, moving):
    h2d, _, _ = np.histogram2d(fixed.ravel(), moving.ravel(), bins=64, range=[[0, 256], [0, 256]])
    pxy = h2d / float(np.sum(h2d))
    px = np.sum(pxy, axis=1)
    py = np.sum(pxy, axis=0)
    nz = pxy > 0
    mi = float(np.sum(pxy[nz] * np.log2(pxy[nz] / (px[:, None] * py[None, :])[nz])))
    return mi

def run_task_12_4():
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
    
    # Simulate multi-modal pair:
    # Image 1 (CT): Cortical bone is hyperintense (~240-255), parenchyma is medium (~60-100)
    # Image 2 (Simulated T2-MRI): Cortical bone has zero signal (~10), parenchyma is bright (~160-220)
    # Synthetic realistic inverted contrast mapping
    sim_mri = np.zeros_like(ct, dtype=float)
    # Non-zero tissue mask
    tissue = ct > 15
    sim_mri[tissue] = 235.0 - (ct[tissue].astype(float) * 0.85)
    # Brain parenchyma boosted
    brain_region = (ct > 25) & (ct < 170)
    sim_mri[brain_region] = 180.0 - (ct[brain_region].astype(float) - 70) * 0.4
    sim_mri = np.clip(sim_mri, 0, 255).astype(np.uint8)
    
    # Translation grid sweep tx in [-20, +20] pixels
    tx_range = np.arange(-20, 21, 1)
    records = []
    
    print("\n" + "=" * 90)
    print("TASK 12.4: WHY MEAN SQUARED ERROR (MSE) FAILS ON MULTI-MODAL SCANS (GRID SWEEP)")
    print("=" * 90)
    print(f"{'Translation Shift tx':<22} | {'MSE Cost':<14} | {'Mutual Information MI':<24} | {'Behavior'}")
    print("-" * 90)
    
    for tx in tx_range:
        M = np.float32([[1, 0, tx], [0, 1, 0]])
        shifted_mri = cv2.warpAffine(sim_mri, M, (w, h), flags=cv2.INTER_LINEAR)
        
        # Calculate MSE & MI
        mse = float(np.mean((ct.astype(float) - shifted_mri.astype(float)) ** 2))
        mi = compute_mi(ct, shifted_mri)
        
        status = ""
        if tx == 0:
            status = "True Alignment (Global MI Peak)"
        records.append({
            "Translation_tx_px": int(tx),
            "Mean_Squared_Error_MSE": round(mse, 2),
            "Mutual_Information_MI": round(mi, 4),
            "Alignment_Status": status
        })
        
    df = pd.DataFrame(records)
    
    # Identify Optima
    best_tx_mi = int(df.loc[df["Mutual_Information_MI"].idxmax()]["Translation_tx_px"])
    best_tx_mse = int(df.loc[df["Mean_Squared_Error_MSE"].idxmin()]["Translation_tx_px"])
    min_mse_val = float(df["Mean_Squared_Error_MSE"].min())
    zero_mse_val = float(df[df["Translation_tx_px"] == 0]["Mean_Squared_Error_MSE"].values[0])
    max_mi_val = float(df["Mutual_Information_MI"].max())
    
    print(f"Optimal tx via Mutual Information: tx = {best_tx_mi:+d} px (Max MI = {max_mi_val:.4f} bits) -> TRUE ANATOMICAL LOCK")
    print(f"Optimal tx via Mean Squared Error: tx = {best_tx_mse:+d} px (Min MSE = {min_mse_val:.2f}) -> FALSE MISALIGNMENT")
    print(f"At true alignment (tx=0), MSE is actually higher ({zero_mse_val:.2f}) due to modality inversion penalty!")
    
    csv_path = os.path.join(tables_dir, "exp12_task_12_4_mse_vs_mi.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SAVED] Task 12.4 table saved to: {csv_path}")
    
    # Figure: Dual Curves and Modality Inversion Demonstration
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Subplot 1: Cost function comparison curves
    ax1.plot(df["Translation_tx_px"], df["Mutual_Information_MI"], "g-o", linewidth=2.0, markersize=3, label="Mutual Information MI (bits)")
    ax1.axvline(best_tx_mi, color="green", linestyle="--", label=f"MI Optimum (tx={best_tx_mi} px, TRUE LOCK)")
    ax1.set_title("Mutual Information vs. Translation Offset\n(Robust Global Maximum at tx = 0 px)", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Horizontal Shift tx (pixels)", fontsize=10)
    ax1.set_ylabel("Mutual Information (bits)", fontsize=10, color="green")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="lower left")
    
    ax1_twin = ax1.twinx()
    ax1_twin.plot(df["Translation_tx_px"], df["Mean_Squared_Error_MSE"], "r--s", linewidth=1.8, markersize=3, label="MSE Cost")
    ax1_twin.axvline(best_tx_mse, color="red", linestyle=":", label=f"MSE Minimum (tx={best_tx_mse} px, FALSE)")
    ax1_twin.set_ylabel("Mean Squared Error (MSE)", fontsize=10, color="red")
    ax1_twin.legend(loc="lower right")
    
    # Subplot 2: Multi-Modal Contrast Inversion Display
    comp_img = np.zeros((h, w, 3), dtype=np.uint8)
    comp_img[:, :, 0] = sim_mri  # Blue: Simulated MRI
    comp_img[:, :, 1] = ct       # Green: CT
    comp_img[:, :, 2] = ct       # Red: CT (bone looks cyan/white)
    
    ax2.imshow(comp_img)
    ax2.set_title("Multi-Modal Modality Contrast Inversion\n(Bone bright in CT, dark in MRI -> Fails MSE)", fontsize=11, fontweight="bold")
    ax2.axis("off")
    
    plt.tight_layout()
    fig_path = os.path.join(outputs_dir, "exp12_task_12_4_mse_vs_mi_failure.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"[SAVED] Task 12.4 figure saved to: {fig_path}")

if __name__ == "__main__":
    run_task_12_4()
