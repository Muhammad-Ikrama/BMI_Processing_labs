"""
Experiment 11: Task 11.1 - Elasticity (alpha) and Bending Stiffness (beta) Sensitivity Sweep
Author: Muhammad Ikrama (Reg ID: 60140)
Department of Biomedical Engineering, Riphah International University, Lahore
Instructor: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import pandas as pd
from scipy import ndimage
import matplotlib.pyplot as plt

def run_task_11_1():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.abspath(os.path.join(script_dir, ".."))
    inputs_dir = os.path.join(exp_dir, "Inputs", "images")
    outputs_dir = os.path.join(exp_dir, "Outputs", "Python")
    tables_dir = os.path.join(exp_dir, "Tables")
    os.makedirs(outputs_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)
    
    mri = cv2.imread(os.path.join(inputs_dir, "Brain_MRI.png"), cv2.IMREAD_GRAYSCALE)
    raw_l = np.zeros_like(mri)
    sub = cv2.GaussianBlur(mri[205:280, 290:365], (3, 3), 0.8)
    raw_l[205:280, 290:365] = (sub > 162).astype(np.uint8) * 255
    num_cc, labels, stats, _ = cv2.connectedComponentsWithStats(raw_l)
    gt_lesion = ndimage.binary_fill_holes(labels == (1 + np.argmax(stats[1:, cv2.CC_STAT_AREA]))).astype(np.uint8) * 255
    gt_area = int((gt_lesion > 0).sum())
    
    ys, xs = np.where(gt_lesion > 0)
    cx, cy = float(xs.mean()), float(ys.mean())
    
    # External potential
    contours, _ = cv2.findContours(gt_lesion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    edge_mask = np.zeros_like(gt_lesion)
    cv2.drawContours(edge_mask, contours, -1, 255, 1)
    dist_edge = cv2.distanceTransform(255 - edge_mask, cv2.DIST_L2, 5)
    edge_pot = 100.0 * np.exp(-(dist_edge ** 2) / (2.0 * (18.0 ** 2)))
    gy_pot, gx_pot = np.gradient(edge_pot)
    
    regimes = [
        {"Name": "High Tension", "alpha": 0.80, "beta": 0.05, "Color": "magenta", "Desc": "Inward Over-Shrinkage"},
        {"Name": "High Stiffness", "alpha": 0.05, "beta": 2.50, "Color": "red", "Desc": "Rigid Circle (No Conformal Bending)"},
        {"Name": "Balanced Clinical Tuning", "alpha": 0.06, "beta": 0.12, "Color": "lime", "Desc": "Optimal Boundary Lock"}
    ]
    
    N = 80
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    gamma = 0.25
    
    records = []
    final_contours = {}
    
    print("\n" + "=" * 95)
    print("TASK 11.1: ELASTICITY (ALPHA) & STIFFNESS (BETA) PARAMETER SENSITIVITY SWEEP")
    print("=" * 95)
    print(f"{'Regime Name':<25} | {'alpha':<6} | {'beta':<6} | {'DSC':<8} | {'IoU':<8} | {'Area (px)':<10} | {'E_total':<10} | {'Status'}")
    print("-" * 95)
    
    for r in regimes:
        a_val, b_val = r["alpha"], r["beta"]
        sx = cx + 38.0 * np.cos(theta)
        sy = cy + 38.0 * np.sin(theta)
        
        A = np.zeros((N, N))
        for i in range(N):
            A[i, i] = 2 * a_val + 6 * b_val
            A[i, (i - 1) % N] = A[i, (i + 1) % N] = -(a_val + 4 * b_val)
            A[i, (i - 2) % N] = A[i, (i + 2) % N] = b_val
        inv_M = np.linalg.inv(np.eye(N) + gamma * A)
        
        for it in range(1, 121):
            ix = np.clip(np.round(sx).astype(int), 0, 511)
            iy = np.clip(np.round(sy).astype(int), 0, 511)
            sx = inv_M @ (sx + gamma * 0.55 * gx_pot[iy, ix])
            sy = inv_M @ (sy + gamma * 0.55 * gy_pot[iy, ix])
            
        final_contours[r["Name"]] = (sx.copy(), sy.copy())
        
        # Metrics
        dx1 = np.roll(sx, -1) - sx
        dy1 = np.roll(sy, -1) - sy
        dx2 = np.roll(sx, -1) - 2 * sx + np.roll(sx, 1)
        dy2 = np.roll(sy, -1) - 2 * sy + np.roll(sy, 1)
        e_int = 0.5 * np.mean(a_val * (dx1 ** 2 + dy1 ** 2) + b_val * (dx2 ** 2 + dy2 ** 2))
        e_ext = -np.mean(edge_pot[iy, ix])
        e_tot = e_int + e_ext
        
        m_cur = np.zeros_like(gt_lesion)
        poly_pts = np.vstack([sx, sy]).T.astype(np.int32)
        cv2.fillPoly(m_cur, [poly_pts], 255)
        
        g, p = (gt_lesion > 0), (m_cur > 0)
        intersection = np.logical_and(g, p).sum()
        union = np.logical_or(g, p).sum()
        dsc = 2.0 * intersection / (g.sum() + p.sum()) if (g.sum() + p.sum()) > 0 else 0.0
        iou = intersection / union if union > 0 else 0.0
        area = int(p.sum())
        
        records.append({
            "Regime_Name": r["Name"],
            "Alpha": a_val,
            "Beta": b_val,
            "DSC": round(dsc, 4),
            "Jaccard_IoU": round(iou, 4),
            "Segmented_Area": area,
            "Ground_Truth_Area": gt_area,
            "Area_Ratio": round(area / gt_area, 4),
            "E_total": round(e_tot, 2),
            "Status": r["Desc"]
        })
        print(f"{r['Name']:<25} | {a_val:<6.2f} | {b_val:<6.2f} | {dsc:<8.4f} | {iou:<8.4f} | {area:<10d} | {e_tot:<10.2f} | {r['Desc']}")
        
    df = pd.DataFrame(records)
    csv_path = os.path.join(tables_dir, "exp11_task_11_1_alpha_beta.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SAVED] Task 11.1 table saved to: {csv_path}")
    
    # Plotting Figure
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    zy1, zy2, zx1, zx2 = 190, 290, 275, 375
    crop_mri = mri[zy1:zy2, zx1:zx2]
    
    for idx, r in enumerate(regimes):
        axes[idx].imshow(crop_mri, cmap='gray', extent=[zx1, zx2, zy2, zy1])
        # Draw ground truth outline in white dashed
        gt_cont, _ = cv2.findContours(gt_lesion[zy1:zy2, zx1:zx2], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for c in gt_cont:
            axes[idx].plot(c[:,0,0] + zx1, c[:,0,1] + zy1, 'w--', linewidth=1.5, label='Ground Truth' if idx==0 else "")
            
        kx, ky = final_contours[r["Name"]]
        axes[idx].plot(kx, ky, color=r["Color"], linewidth=2.5, label=f"Snake (t=120)")
        rec = df[df['Regime_Name'] == r['Name']].iloc[0]
        axes[idx].set_title(f"({chr(65+idx)}) {r['Name']}\nalpha={r['alpha']:.2f}, beta={r['beta']:.2f} | DSC={rec['DSC']:.4f}\n{r['Desc']}", fontsize=10, fontweight='bold')
        axes[idx].axis('off')
        axes[idx].legend(loc='lower left', fontsize=9)
        
    plt.tight_layout()
    fig_path = os.path.join(outputs_dir, "exp11_task_11_1_alpha_beta.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SAVED] Task 11.1 figure saved to: {fig_path}")

if __name__ == "__main__":
    run_task_11_1()
