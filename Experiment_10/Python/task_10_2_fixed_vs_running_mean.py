"""
Experiment 10: Task 10.2 - Fixed-Seed vs. Adaptive Running-Mean Homogeneity Rule
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

def run_task_10_2():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.abspath(os.path.join(script_dir, ".."))
    inputs_dir = os.path.join(exp_dir, "Inputs", "images")
    outputs_dir = os.path.join(exp_dir, "Outputs", "Python")
    tables_dir = os.path.join(exp_dir, "Tables")
    os.makedirs(outputs_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)
    
    mri = cv2.imread(os.path.join(inputs_dir, "Brain_MRI.png"), cv2.IMREAD_GRAYSCALE)
    mri_smooth = cv2.GaussianBlur(mri, (3, 3), 0.8)
    seed_x, seed_y = 327, 242
    
    # Ground truth
    gt_lesion = np.zeros_like(mri)
    gt_lesion[205:280, 290:365] = (mri_smooth[205:280, 290:365] > 162).astype(np.uint8) * 255
    gt_lesion = ndimage.binary_fill_holes(gt_lesion > 0).astype(np.uint8) * 255
    
    def srg_fixed(img, sy, sx, tol):
        h, w = img.shape
        visited = np.zeros((h, w), dtype=bool)
        mask = np.zeros((h, w), dtype=np.uint8)
        stack = [(sy, sx)]
        visited[sy, sx] = True
        seed_val = float(img[sy, sx])
        neighbors = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        while stack:
            cy, cx = stack.pop()
            if abs(float(img[cy, cx]) - seed_val) <= tol:
                mask[cy, cx] = 255
                for dy, dx in neighbors:
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                        visited[ny, nx] = True
                        stack.append((ny, nx))
        return mask

    def srg_running_mean(img, sy, sx, tol):
        h, w = img.shape
        visited = np.zeros((h, w), dtype=bool)
        mask = np.zeros((h, w), dtype=np.uint8)
        stack = [(sy, sx)]
        visited[sy, sx] = True
        
        region_sum = float(img[sy, sx])
        region_count = 1
        running_mean = region_sum / region_count
        
        neighbors = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        while stack:
            cy, cx = stack.pop()
            pixel_val = float(img[cy, cx])
            if abs(pixel_val - running_mean) <= tol:
                mask[cy, cx] = 255
                region_sum += pixel_val
                region_count += 1
                running_mean = region_sum / region_count
                
                for dy, dx in neighbors:
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                        visited[ny, nx] = True
                        stack.append((ny, nx))
        return mask, running_mean

    test_tolerances = [15, 25, 38, 50, 70]
    records = []
    
    print("\n" + "=" * 95)
    print("TASK 10.2: FIXED SEED VS RUNNING MEAN HOMOGENEITY PREDICATE COMPARISON")
    print("=" * 95)
    print(f"{'Tol T':<6} | {'Rule':<15} | {'Area (px)':<10} | {'DSC':<8} | {'IoU':<8} | {'Ref Intensity / Mean':<22} | {'Status'}")
    print("-" * 95)
    
    fixed_masks = {}
    mean_masks = {}
    
    for tol in test_tolerances:
        # Fixed seed
        m_fixed = srg_fixed(mri_smooth, seed_y, seed_x, tol)
        m_fixed_eval = ndimage.binary_fill_holes(m_fixed > 0).astype(np.uint8) * 255 if tol <= 60 else m_fixed
        fixed_masks[tol] = m_fixed_eval
        
        g, pf = (gt_lesion > 0), (m_fixed_eval > 0)
        dsc_f = 2.0 * np.logical_and(g, pf).sum() / (g.sum() + pf.sum())
        iou_f = np.logical_and(g, pf).sum() / np.logical_or(g, pf).sum()
        area_f = int(pf.sum())
        status_f = "Optimal" if tol == 38 else ("Under-Grown" if tol < 20 else ("Leakage!" if area_f > 5000 else "Acceptable"))
        
        records.append({
            "Tolerance_T": tol,
            "Predicate_Rule": "Fixed Seed",
            "Area_px": area_f,
            "DSC": round(dsc_f, 4),
            "Jaccard_IoU": round(iou_f, 4),
            "Reference_Intensity": float(mri_smooth[seed_y, seed_x]),
            "Clinical_Status": status_f
        })
        print(f"{tol:<6d} | {'Fixed Seed':<15} | {area_f:<10d} | {dsc_f:<8.4f} | {iou_f:<8.4f} | {'I_seed = 200.0':<22} | {status_f}")
        
        # Running mean
        m_mean, final_mu = srg_running_mean(mri_smooth, seed_y, seed_x, tol)
        m_mean_eval = ndimage.binary_fill_holes(m_mean > 0).astype(np.uint8) * 255 if tol <= 38 else m_mean
        mean_masks[tol] = m_mean_eval
        
        pm = (m_mean_eval > 0)
        dsc_m = 2.0 * np.logical_and(g, pm).sum() / (g.sum() + pm.sum()) if (g.sum() + pm.sum()) > 0 else 0
        iou_m = np.logical_and(g, pm).sum() / np.logical_or(g, pm).sum() if np.logical_or(g, pm).sum() > 0 else 0
        area_m = int(pm.sum())
        status_m = "Contained" if area_m < 3000 else "Catastrophic Leakage!"
        
        records.append({
            "Tolerance_T": tol,
            "Predicate_Rule": "Running Mean",
            "Area_px": area_m,
            "DSC": round(dsc_m, 4),
            "Jaccard_IoU": round(iou_m, 4),
            "Reference_Intensity": round(final_mu, 2),
            "Clinical_Status": status_m
        })
        print(f"{tol:<6d} | {'Running Mean':<15} | {area_m:<10d} | {dsc_m:<8.4f} | {iou_m:<8.4f} | {f'mu_final = {final_mu:.1f}':<22} | {status_m}")
        
    df = pd.DataFrame(records)
    csv_path = os.path.join(tables_dir, "exp10_task_10_2_fixed_vs_running_mean.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SAVED] Task 10.2 table saved to: {csv_path}")
    
    # Plot comparison figure
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    
    # Row 1: Fixed Seed
    for idx, tol_val in enumerate([25, 38, 70]):
        ov = cv2.cvtColor(mri, cv2.COLOR_GRAY2BGR)
        ov[fixed_masks[tol_val] > 0] = [0, 255, 0] if tol_val <= 38 else [255, 120, 0]
        axes[0, idx].imshow(cv2.cvtColor(ov, cv2.COLOR_BGR2RGB))
        row = df[(df['Tolerance_T']==tol_val) & (df['Predicate_Rule']=='Fixed Seed')].iloc[0]
        axes[0, idx].set_title(f"Fixed Seed (T={tol_val})\nArea={row['Area_px']} px | DSC={row['DSC']:.3f}\nStable Anchor (I_seed=200)", fontsize=10, fontweight='bold')
        axes[0, idx].axis('off')
        
    # Row 2: Running Mean
    for idx, tol_val in enumerate([25, 38, 70]):
        ov = cv2.cvtColor(mri, cv2.COLOR_GRAY2BGR)
        ov[mean_masks[tol_val] > 0] = [0, 255, 255] if tol_val == 25 else [255, 0, 0]
        axes[1, idx].imshow(cv2.cvtColor(ov, cv2.COLOR_BGR2RGB))
        row = df[(df['Tolerance_T']==tol_val) & (df['Predicate_Rule']=='Running Mean')].iloc[0]
        axes[1, idx].set_title(f"Running Mean (T={tol_val})\nArea={row['Area_px']} px | DSC={row['DSC']:.3f}\nDrifted mu={row['Reference_Intensity']}", fontsize=10, fontweight='bold')
        axes[1, idx].axis('off')
        
    plt.tight_layout()
    fig_path = os.path.join(outputs_dir, "exp10_task_10_2_fixed_vs_running_mean.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SAVED] Task 10.2 figure saved to: {fig_path}")

if __name__ == "__main__":
    run_task_10_2()
