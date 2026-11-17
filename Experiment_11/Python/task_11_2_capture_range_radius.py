"""
Experiment 11: Task 11.2 - Capture Range & Initial Contour Radius Evaluation
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

def run_task_11_2():
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
    
    contours, _ = cv2.findContours(gt_lesion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    edge_mask = np.zeros_like(gt_lesion)
    cv2.drawContours(edge_mask, contours, -1, 255, 1)
    dist_edge = cv2.distanceTransform(255 - edge_mask, cv2.DIST_L2, 5)
    
    # Precompute external potentials for sigma = 12.0 and sigma = 24.0
    pot_12 = 100.0 * np.exp(-(dist_edge ** 2) / (2.0 * (12.0 ** 2)))
    gy_12, gx_12 = np.gradient(pot_12)
    
    pot_24 = 100.0 * np.exp(-(dist_edge ** 2) / (2.0 * (24.0 ** 2)))
    gy_24, gx_24 = np.gradient(pot_24)
    
    test_configs = [
        {"r0": 28, "sigma": 12.0, "pot_gx": gx_12, "pot_gy": gy_12, "Label": "r0=28 px (Interior)"},
        {"r0": 38, "sigma": 12.0, "pot_gx": gx_12, "pot_gy": gy_12, "Label": "r0=38 px (Optimal Baseline)"},
        {"r0": 52, "sigma": 12.0, "pot_gx": gx_12, "pot_gy": gy_12, "Label": "r0=52 px (Extended Margin)"},
        {"r0": 70, "sigma": 12.0, "pot_gx": gx_12, "pot_gy": gy_12, "Label": "r0=70 px (Outside Capture sigma=12)"},
        {"r0": 70, "sigma": 24.0, "pot_gx": gx_24, "pot_gy": gy_24, "Label": "r0=70 px (Expanded sigma=24)"}
    ]
    
    N = 80
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    alpha, beta, gamma = 0.06, 0.12, 0.25
    A = np.zeros((N, N))
    for i in range(N):
        A[i, i] = 2 * alpha + 6 * beta
        A[i, (i - 1) % N] = A[i, (i + 1) % N] = -(alpha + 4 * beta)
        A[i, (i - 2) % N] = A[i, (i + 2) % N] = beta
    inv_M = np.linalg.inv(np.eye(N) + gamma * A)
    
    records = []
    final_contours = {}
    init_contours = {}
    
    print("\n" + "=" * 95)
    print("TASK 11.2: CAPTURE RANGE & INITIAL CONTOUR RADIUS EVALUATION")
    print("=" * 95)
    print(f"{'Configuration':<32} | {'r0 (px)':<8} | {'sigma':<6} | {'Final DSC':<10} | {'Final IoU':<10} | {'Status'}")
    print("-" * 95)
    
    for cfg in test_configs:
        r0 = cfg["r0"]
        gx = cfg["pot_gx"]
        gy = cfg["pot_gy"]
        
        sx = cx + r0 * np.cos(theta)
        sy = cy + r0 * np.sin(theta)
        init_contours[cfg["Label"]] = (sx.copy(), sy.copy())
        
        for it in range(1, 121):
            ix = np.clip(np.round(sx).astype(int), 0, 511)
            iy = np.clip(np.round(sy).astype(int), 0, 511)
            sx = inv_M @ (sx + gamma * 0.55 * gx[iy, ix])
            sy = inv_M @ (sy + gamma * 0.55 * gy[iy, ix])
            
        final_contours[cfg["Label"]] = (sx.copy(), sy.copy())
        
        m_cur = np.zeros_like(gt_lesion)
        poly_pts = np.vstack([sx, sy]).T.astype(np.int32)
        cv2.fillPoly(m_cur, [poly_pts], 255)
        
        g, p = (gt_lesion > 0), (m_cur > 0)
        intersection = np.logical_and(g, p).sum()
        union = np.logical_or(g, p).sum()
        dsc = 2.0 * intersection / (g.sum() + p.sum()) if (g.sum() + p.sum()) > 0 else 0.0
        iou = intersection / union if union > 0 else 0.0
        area = int(p.sum())
        
        if dsc >= 0.95:
            status = "Optimal Convergence"
        elif dsc >= 0.85:
            status = "Acceptable Capture"
        elif dsc >= 0.50:
            status = "Partial Capture"
        else:
            status = "Stalled Outside Capture Range"
            
        records.append({
            "Configuration": cfg["Label"],
            "Initial_Radius_r0": r0,
            "Sigma_Capture": cfg["sigma"],
            "DSC": round(dsc, 4),
            "Jaccard_IoU": round(iou, 4),
            "Final_Area_px": area,
            "Ground_Truth_px": gt_area,
            "Status": status
        })
        print(f"{cfg['Label']:<32} | {r0:<8d} | {cfg['sigma']:<6.1f} | {dsc:<10.4f} | {iou:<10.4f} | {status}")
        
    df = pd.DataFrame(records)
    csv_path = os.path.join(tables_dir, "exp11_task_11_2_capture_range.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SAVED] Task 11.2 table saved to: {csv_path}")
    
    # Composite Figure (4 subplots)
    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    zy1, zy2, zx1, zx2 = 170, 315, 250, 400
    crop_mri = mri[zy1:zy2, zx1:zx2]
    
    display_keys = [
        "r0=28 px (Interior)",
        "r0=38 px (Optimal Baseline)",
        "r0=70 px (Outside Capture sigma=12)",
        "r0=70 px (Expanded sigma=24)"
    ]
    
    for idx, key in enumerate(display_keys):
        axes[idx].imshow(crop_mri, cmap='gray', extent=[zx1, zx2, zy2, zy1])
        i_x, i_y = init_contours[key]
        f_x, f_y = final_contours[key]
        axes[idx].plot(i_x, i_y, 'r--', linewidth=1.8, label='Initial Snake')
        axes[idx].plot(f_x, f_y, 'lime', linewidth=2.4, label='Final Snake')
        rec = df[df['Configuration'] == key].iloc[0]
        axes[idx].set_title(f"({chr(65+idx)}) {key.split('(')[0].strip()}\nDSC = {rec['DSC']:.4f} | {rec['Status']}", fontsize=10, fontweight='bold')
        axes[idx].axis('off')
        axes[idx].legend(loc='lower left', fontsize=8.5)
        
    plt.tight_layout()
    fig_path = os.path.join(outputs_dir, "exp11_task_11_2_capture_range.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SAVED] Task 11.2 figure saved to: {fig_path}")

if __name__ == "__main__":
    run_task_11_2()
