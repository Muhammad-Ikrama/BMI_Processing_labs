"""
Experiment 11: Task 11.5 - Intracranial Skull Boundary Extraction on Head CT
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

def run_task_11_5():
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
    total_pixels = h * w
    
    # Bone edge potential
    # Dense bone threshold
    bone_mask = (ct > 180).astype(np.uint8) * 255
    # Keep outermost calvarium contour
    contours, _ = cv2.findContours(bone_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    outer_bone_mask = np.zeros_like(ct)
    if contours:
        # Find largest contour by area
        c_max = max(contours, key=cv2.contourArea)
        cv2.drawContours(outer_bone_mask, [c_max], -1, 255, 2)
        
    dist_bone = cv2.distanceTransform(255 - outer_bone_mask, cv2.DIST_L2, 5)
    edge_pot = 100.0 * np.exp(-(dist_bone ** 2) / (2.0 * (15.0 ** 2)))
    gy_pot, gx_pot = np.gradient(edge_pot)
    
    # Initialize outer circular snake (r0 = 235 px, N = 120 points)
    N = 120
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    r0 = 235.0
    sx = cx + r0 * np.cos(theta)
    sy = cy + r0 * np.sin(theta)
    
    alpha, beta, gamma = 0.08, 0.15, 0.25
    A = np.zeros((N, N))
    for i in range(N):
        A[i, i] = 2 * alpha + 6 * beta
        A[i, (i - 1) % N] = A[i, (i + 1) % N] = -(alpha + 4 * beta)
        A[i, (i - 2) % N] = A[i, (i + 2) % N] = beta
    inv_M = np.linalg.inv(np.eye(N) + gamma * A)
    
    history = {0: (sx.copy(), sy.copy())}
    records = []
    
    print("\n" + "=" * 95)
    print("TASK 11.5: INTRACRANIAL SKULL BOUNDARY EXTRACTION ON HEAD CT")
    print("=" * 95)
    print(f"{'Iteration':<12} | {'Enclosed Area (px)':<20} | {'Perimeter (px)':<16} | {'Circularity':<14} | {'Status'}")
    print("-" * 95)
    
    for it in range(1, 101):
        ix = np.clip(np.round(sx).astype(int), 0, w - 1)
        iy = np.clip(np.round(sy).astype(int), 0, h - 1)
        
        # Balloon deflation force inward towards center
        dx_c = cx - sx
        dy_c = cy - sy
        norm_c = np.hypot(dx_c, dy_c) + 1e-5
        balloon_x = 0.8 * (dx_c / norm_c)
        balloon_y = 0.8 * (dy_c / norm_c)
        
        sx = inv_M @ (sx + gamma * (0.6 * gx_pot[iy, ix] + balloon_x))
        sy = inv_M @ (sy + gamma * (0.6 * gy_pot[iy, ix] + balloon_y))
        
        if it in (30, 60, 100):
            history[it] = (sx.copy(), sy.copy())
            
            # Compute geometric properties
            poly_pts = np.vstack([sx, sy]).T.astype(np.int32)
            m_poly = np.zeros_like(ct)
            cv2.fillPoly(m_poly, [poly_pts], 255)
            area = int((m_poly > 0).sum())
            
            cont_p, _ = cv2.findContours(m_poly, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            perim = cv2.arcLength(cont_p[0], True) if cont_p else 0.0
            circularity = (4.0 * np.pi * area) / (perim ** 2) if perim > 0 else 0.0
            
            status = "Contracting" if it < 100 else "Locked on Outer Skull"
            records.append({
                "Iteration": it,
                "Enclosed_Area_px": area,
                "Perimeter_px": round(perim, 2),
                "Circularity": round(circularity, 4),
                "Head_Field_Percentage": round((area / total_pixels) * 100, 2),
                "Status": status
            })
            print(f"Iter {it:<7d} | {area:<20d} | {perim:<16.1f} | {circularity:<14.4f} | {status}")
            
    df = pd.DataFrame(records)
    csv_path = os.path.join(tables_dir, "exp11_task_11_5_head_ct_skull.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SAVED] Task 11.5 table saved to: {csv_path}")
    
    # 4-panel composite figure
    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    plot_iters = [0, 30, 60, 100]
    colors = {0: 'red', 30: 'orange', 60: 'cyan', 100: 'lime'}
    
    for idx, it_k in enumerate(plot_iters):
        axes[idx].imshow(ct, cmap='gray')
        kx, ky = history[it_k]
        ls = '--' if it_k == 0 else '-'
        axes[idx].plot(kx, ky, color=colors[it_k], linestyle=ls, linewidth=2.2, label=f'Iter {it_k}')
        
        if it_k == 0:
            axes[idx].set_title("(1) Initial Circular Snake\nr0 = 235 px (Outer Cranium)", fontsize=10, fontweight='bold')
        else:
            rec = df[df['Iteration'] == it_k].iloc[0]
            axes[idx].set_title(f"({idx+1}) Iteration {it_k}\nArea = {rec['Enclosed_Area_px']} px\nCircularity = {rec['Circularity']:.3f}", fontsize=10, fontweight='bold')
        axes[idx].axis('off')
        axes[idx].legend(loc='lower left', fontsize=9)
        
    plt.tight_layout()
    fig_path = os.path.join(outputs_dir, "exp11_task_11_5_head_ct_skull.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SAVED] Task 11.5 figure saved to: {fig_path}")

if __name__ == "__main__":
    run_task_11_5()
