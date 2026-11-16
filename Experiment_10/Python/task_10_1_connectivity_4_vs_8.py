"""
Experiment 10: Task 10.1 - 4-Connected vs. 8-Connected Neighborhood Region Growing
Author: Muhammad Ikrama (Reg ID: 60140)
Department of Biomedical Engineering, Riphah International University, Lahore
Instructor: Engr. Rana Talha Khalid
"""

import os
import time
import cv2
import numpy as np
import pandas as pd
from scipy import ndimage
import matplotlib.pyplot as plt

def run_task_10_1():
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
    tol = 38
    
    # Ground truth
    gt_lesion = np.zeros_like(mri)
    gt_lesion[205:280, 290:365] = (mri_smooth[205:280, 290:365] > 162).astype(np.uint8) * 255
    gt_lesion = ndimage.binary_fill_holes(gt_lesion > 0).astype(np.uint8) * 255
    
    def srg(img, sy, sx, tol_val, neighbors):
        h, w = img.shape
        visited = np.zeros((h, w), dtype=bool)
        mask = np.zeros((h, w), dtype=np.uint8)
        stack = [(sy, sx)]
        visited[sy, sx] = True
        seed_val = float(img[sy, sx])
        while stack:
            cy, cx = stack.pop()
            if abs(float(img[cy, cx]) - seed_val) <= tol_val:
                mask[cy, cx] = 255
                for dy, dx in neighbors:
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                        visited[ny, nx] = True
                        stack.append((ny, nx))
        return mask

    conn_4_neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    conn_8_neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    # Benchmark timings (average of 3 runs)
    t0 = time.perf_counter()
    for _ in range(3):
        mask_4 = srg(mri_smooth, seed_y, seed_x, tol, conn_4_neighbors)
    time_4 = (time.perf_counter() - t0) / 3.0 * 1000.0  # ms
    
    t0 = time.perf_counter()
    for _ in range(3):
        mask_8 = srg(mri_smooth, seed_y, seed_x, tol, conn_8_neighbors)
    time_8 = (time.perf_counter() - t0) / 3.0 * 1000.0  # ms
    
    mask_4_filled = ndimage.binary_fill_holes(mask_4 > 0).astype(np.uint8) * 255
    mask_8_filled = ndimage.binary_fill_holes(mask_8 > 0).astype(np.uint8) * 255
    
    # Compute metrics
    def compute_metrics(pred, gt):
        g, p = (gt > 0), (pred > 0)
        intersection = np.logical_and(g, p).sum()
        union = np.logical_or(g, p).sum()
        dsc = 2.0 * intersection / (g.sum() + p.sum())
        iou = intersection / union
        area = int(p.sum())
        
        # Perimeter using contours
        contours, _ = cv2.findContours(pred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        perimeter = cv2.arcLength(contours[0], True) if contours else 0.0
        compactness = (4.0 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0.0
        return area, dsc, iou, perimeter, compactness

    area_4, dsc_4, iou_4, perim_4, comp_4 = compute_metrics(mask_4_filled, gt_lesion)
    area_8, dsc_8, iou_8, perim_8, comp_8 = compute_metrics(mask_8_filled, gt_lesion)
    
    print("\n" + "=" * 80)
    print("TASK 10.1: 4-CONNECTED VS 8-CONNECTED SEEDED REGION GROWING")
    print("=" * 80)
    print(f"{'Connectivity':<15} | {'Area (px)':<10} | {'DSC':<8} | {'IoU':<8} | {'Perimeter (px)':<15} | {'Compactness':<12} | {'Time (ms)':<10}")
    print("-" * 88)
    print(f"{'4-Connected':<15} | {area_4:<10d} | {dsc_4:<8.4f} | {iou_4:<8.4f} | {perim_4:<15.1f} | {comp_4:<12.4f} | {time_4:<10.2f}")
    print(f"{'8-Connected':<15} | {area_8:<10d} | {dsc_8:<8.4f} | {iou_8:<8.4f} | {perim_8:<15.1f} | {comp_8:<12.4f} | {time_8:<10.2f}")
    
    records = [
        {"Neighborhood": "4-Connected", "Neighbors": 4, "Area_px": area_4, "DSC": round(dsc_4, 4), "Jaccard_IoU": round(iou_4, 4), "Perimeter_px": round(perim_4, 2), "Compactness": round(comp_4, 4), "Exec_Time_ms": round(time_4, 2), "Stair_Stepping": "Severe (Orthogonal Only)"},
        {"Neighborhood": "8-Connected", "Neighbors": 8, "Area_px": area_8, "DSC": round(dsc_8, 4), "Jaccard_IoU": round(iou_8, 4), "Perimeter_px": round(perim_8, 2), "Compactness": round(comp_8, 4), "Exec_Time_ms": round(time_8, 2), "Stair_Stepping": "Smooth (Diagonal Infiltration)"}
    ]
    df = pd.DataFrame(records)
    csv_path = os.path.join(tables_dir, "exp10_task_10_1_connectivity.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SAVED] Task 10.1 table saved to: {csv_path}")
    
    # Plotting
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Zoom window around tumor
    zy1, zy2, zx1, zx2 = 190, 290, 280, 380
    zoom_mri = mri[zy1:zy2, zx1:zx2]
    
    # Overlay 4-connected
    ov4 = cv2.cvtColor(zoom_mri, cv2.COLOR_GRAY2BGR)
    cont4, _ = cv2.findContours(mask_4_filled[zy1:zy2, zx1:zx2], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(ov4, cont4, -1, (0, 165, 255), 2)  # Orange
    axes[0].imshow(cv2.cvtColor(ov4, cv2.COLOR_BGR2RGB))
    axes[0].set_title(f"(A) 4-Connected SRG (T=38)\nArea = {area_4} px | DSC = {dsc_4:.4f}\nNotice Orthogonal Stepping", fontsize=10, fontweight='bold')
    axes[0].axis('off')
    
    # Overlay 8-connected
    ov8 = cv2.cvtColor(zoom_mri, cv2.COLOR_GRAY2BGR)
    cont8, _ = cv2.findContours(mask_8_filled[zy1:zy2, zx1:zx2], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(ov8, cont8, -1, (0, 255, 0), 2)  # Green
    axes[1].imshow(cv2.cvtColor(ov8, cv2.COLOR_BGR2RGB))
    axes[1].set_title(f"(B) 8-Connected SRG (T=38)\nArea = {area_8} px | DSC = {dsc_8:.4f}\nOptimal Diagonal Capture", fontsize=10, fontweight='bold')
    axes[1].axis('off')
    
    # Difference / Boundary Comparison
    diff_mask = np.zeros((zy2 - zy1, zx2 - zx1, 3), dtype=np.uint8)
    diff_mask[mask_8_filled[zy1:zy2, zx1:zx2] > 0] = [0, 255, 0]      # Green = 8-conn
    diff_mask[mask_4_filled[zy1:zy2, zx1:zx2] > 0] = [0, 120, 255]    # Orange = 4-conn
    axes[2].imshow(diff_mask)
    axes[2].set_title(f"(C) Boundary Discrepancy Map\nGreen Rim = {area_8 - area_4} px missed by 4-conn\nDiagonal Infiltration Gap", fontsize=10, fontweight='bold')
    axes[2].axis('off')
    
    plt.tight_layout()
    fig_path = os.path.join(outputs_dir, "exp10_task_10_1_connectivity.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SAVED] Task 10.1 figure saved to: {fig_path}")

if __name__ == "__main__":
    run_task_10_1()
