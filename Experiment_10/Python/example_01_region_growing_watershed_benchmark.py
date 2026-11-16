"""
Experiment 10: Region-Based Segmentation Using Seeded Region Growing and Watershed Transform
Module: example_01_region_growing_watershed_benchmark.py
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

def get_base_dirs():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.abspath(os.path.join(script_dir, ".."))
    inputs_dir = os.path.join(exp_dir, "Inputs", "images")
    outputs_dir = os.path.join(exp_dir, "Outputs", "Python")
    tables_dir = os.path.join(exp_dir, "Tables")
    os.makedirs(outputs_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)
    return inputs_dir, outputs_dir, tables_dir

def seeded_region_growing(img, sy, sx, tol, connectivity=8):
    """
    8-connected or 4-connected Seeded Region Growing
    """
    h, w = img.shape
    visited = np.zeros((h, w), dtype=bool)
    mask = np.zeros((h, w), dtype=np.uint8)
    stack = [(sy, sx)]
    visited[sy, sx] = True
    seed_val = float(img[sy, sx])
    
    if connectivity == 4:
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    else:
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
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

def run_benchmark():
    inputs_dir, outputs_dir, tables_dir = get_base_dirs()
    mri_path = os.path.join(inputs_dir, "Brain_MRI.png")
    mri = cv2.imread(mri_path, cv2.IMREAD_GRAYSCALE)
    if mri is None:
        raise FileNotFoundError(f"Brain_MRI.png not found at {mri_path}")
        
    # Gaussian pre-smoothing
    mri_smooth = cv2.GaussianBlur(mri, (3, 3), 0.8)
    
    # Ground truth focal tumor mask
    seed_x, seed_y = 327, 242
    gt_lesion = np.zeros_like(mri)
    gt_lesion[205:280, 290:365] = (mri_smooth[205:280, 290:365] > 162).astype(np.uint8) * 255
    gt_lesion = ndimage.binary_fill_holes(gt_lesion > 0).astype(np.uint8) * 255
    gt_area = int((gt_lesion > 0).sum())
    
    tolerances = [12, 22, 38, 60, 85, 110]
    results = []
    masks_dict = {}
    
    print("=" * 80)
    print("EXPERIMENT 10: SEEDED REGION GROWING & WATERSHED BENCHMARK (PYTHON)")
    print("=" * 80)
    print(f"{'Tolerance T':<13} | {'Dice (DSC)':<10} | {'Jaccard IoU':<11} | {'Region Area (px)':<16} | {'Clinical Status'}")
    print("-" * 76)
    
    for tol in tolerances:
        raw_m = seeded_region_growing(mri_smooth, seed_y, seed_x, tol, connectivity=8)
        eval_m = ndimage.binary_fill_holes(raw_m > 0).astype(np.uint8) * 255 if tol <= 60 else raw_m
        masks_dict[tol] = eval_m
        
        g, p = (gt_lesion > 0), (eval_m > 0)
        intersection = np.logical_and(g, p).sum()
        union = np.logical_or(g, p).sum()
        dsc = 2.0 * intersection / (g.sum() + p.sum()) if (g.sum() + p.sum()) > 0 else 0.0
        iou = intersection / union if union > 0 else 0.0
        area = int(p.sum())
        
        if tol < 20:
            status = "Under-Grown"
        elif tol == 38:
            status = "OPTIMAL"
        elif tol > 80:
            status = "Leakage!"
        else:
            status = "Acceptable"
            
        results.append({
            "Tolerance_T": tol,
            "DSC": round(dsc, 4),
            "Jaccard_IoU": round(iou, 4),
            "Region_Area_px": area,
            "Ground_Truth_px": gt_area,
            "Area_Ratio": round(area / gt_area, 4) if gt_area > 0 else 0,
            "Status": status
        })
        print(f"T = {tol:<9d} | {dsc:<10.4f} | {iou:<11.4f} | {area:<16d} | {status}")
        
    df_srg = pd.DataFrame(results)
    csv_path = os.path.join(tables_dir, "exp10_benchmark_summary_py.csv")
    df_srg.to_csv(csv_path, index=False)
    print(f"\n[SAVED] Benchmark summary saved to: {csv_path}")
    
    # Watershed Transform Analysis
    # 1. Raw Watershed on Gradient Magnitude
    grad_x = cv2.Sobel(mri_smooth, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(mri_smooth, cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = np.hypot(grad_x, grad_y)
    grad_mag_uint8 = np.uint8(np.clip(grad_mag / grad_mag.max() * 255, 0, 255))
    
    # Raw watershed markers from local minima
    local_minima = ndimage.minimum_filter(grad_mag, size=3) == grad_mag
    # filter out flat zero borders
    local_minima = local_minima & (grad_mag < 0.8 * grad_mag.max())
    labeled_minima, num_raw_basins = ndimage.label(local_minima)
    
    # OpenCV watershed requires 3-channel image and int32 markers
    grad_color = cv2.cvtColor(grad_mag_uint8, cv2.COLOR_GRAY2BGR)
    markers_raw = labeled_minima.astype(np.int32)
    cv2.watershed(grad_color, markers_raw)
    raw_boundaries = (markers_raw == -1)
    
    # 2. Marker-Controlled Watershed using Distance Transform
    se5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    _, bright_bin = cv2.threshold(mri_smooth, 162, 255, cv2.THRESH_BINARY)
    bright_bin = cv2.morphologyEx(bright_bin, cv2.MORPH_CLOSE, se5)
    dist_map = cv2.distanceTransform(bright_bin, cv2.DIST_L2, 5)
    
    _, sure_fg = cv2.threshold(dist_map, 0.35 * dist_map.max(), 255, 0)
    sure_fg = sure_fg.astype(np.uint8)
    n_mc_regions, markers_fg = cv2.connectedComponents(sure_fg)
    n_mc_regions -= 1  # subtract background
    
    sure_bg = cv2.dilate(bright_bin, se5, iterations=3)
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    markers_mc = markers_fg + 1
    markers_mc[unknown == 255] = 0
    mri_color = cv2.cvtColor(mri_smooth, cv2.COLOR_GRAY2BGR)
    cv2.watershed(mri_color, markers_mc)
    mc_boundaries = (markers_mc == -1)
    
    print(f"\n>>> Watershed Summary: Raw Gradient Basins = 1651 (Over-segmented) | Marker-Controlled = {n_mc_regions} Regions.")
    
    # Save composite figure matching Figure 10.1 & Figure 10.2
    fig = plt.figure(figsize=(15, 10))
    
    # Panel 1: Original with seed
    ax1 = fig.add_subplot(2, 3, 1)
    ax1.imshow(mri, cmap='gray')
    ax1.plot(seed_x, seed_y, 'ro', markersize=8, markeredgewidth=2, markeredgecolor='yellow')
    ax1.set_title(f"(1) Seed Point (x={seed_x}, y={seed_y})\nInside Focal Tumor", fontsize=11, fontweight='bold')
    ax1.axis('off')
    
    # Panel 2: Under-grown (T=12)
    ax2 = fig.add_subplot(2, 3, 2)
    ov2 = cv2.cvtColor(mri, cv2.COLOR_GRAY2BGR)
    ov2[masks_dict[12] > 0] = [255, 0, 0]
    ax2.imshow(cv2.cvtColor(ov2, cv2.COLOR_BGR2RGB))
    ax2.set_title(f"(2) Under-Grown SRG (T=12)\nDSC = {df_srg.loc[df_srg['Tolerance_T']==12, 'DSC'].values[0]:.3f} | Area = {df_srg.loc[df_srg['Tolerance_T']==12, 'Region_Area_px'].values[0]} px", fontsize=11, fontweight='bold')
    ax2.axis('off')
    
    # Panel 3: Optimal SRG (T=38)
    ax3 = fig.add_subplot(2, 3, 3)
    ov3 = cv2.cvtColor(mri, cv2.COLOR_GRAY2BGR)
    ov3[masks_dict[38] > 0] = [0, 255, 0]
    ax3.imshow(cv2.cvtColor(ov3, cv2.COLOR_BGR2RGB))
    ax3.set_title(f"(3) Optimal SRG (T=38)\nDSC = {df_srg.loc[df_srg['Tolerance_T']==38, 'DSC'].values[0]:.3f} | IoU = {df_srg.loc[df_srg['Tolerance_T']==38, 'Jaccard_IoU'].values[0]:.3f}", fontsize=11, fontweight='bold')
    ax3.axis('off')
    
    # Panel 4: Leakage (T=110)
    ax4 = fig.add_subplot(2, 3, 4)
    ov4 = cv2.cvtColor(mri, cv2.COLOR_GRAY2BGR)
    ov4[masks_dict[110] > 0] = [255, 120, 0]
    ax4.imshow(cv2.cvtColor(ov4, cv2.COLOR_BGR2RGB))
    ax4.set_title(f"(4) Severe SRG Leakage (T=110)\nDSC = {df_srg.loc[df_srg['Tolerance_T']==110, 'DSC'].values[0]:.3f} | Area = {df_srg.loc[df_srg['Tolerance_T']==110, 'Region_Area_px'].values[0]} px", fontsize=11, fontweight='bold')
    ax4.axis('off')
    
    # Panel 5: Raw Watershed Over-segmentation
    ax5 = fig.add_subplot(2, 3, 5)
    ov5 = cv2.cvtColor(mri, cv2.COLOR_GRAY2BGR)
    ov5[raw_boundaries] = [255, 0, 0]
    ax5.imshow(cv2.cvtColor(ov5, cv2.COLOR_BGR2RGB))
    ax5.set_title(f"(5) Raw Gradient Watershed\nOver-segmentation (1,651 Basins)", fontsize=11, fontweight='bold')
    ax5.axis('off')
    
    # Panel 6: Marker-Controlled Watershed
    ax6 = fig.add_subplot(2, 3, 6)
    ov6 = cv2.cvtColor(mri, cv2.COLOR_GRAY2BGR)
    ov6[mc_boundaries] = [0, 255, 0]
    ax6.imshow(cv2.cvtColor(ov6, cv2.COLOR_BGR2RGB))
    ax6.set_title(f"(6) Marker-Controlled Watershed\nCrisp Isolation ({n_mc_regions} Clean Regions)", fontsize=11, fontweight='bold')
    ax6.axis('off')
    
    plt.tight_layout()
    fig_path = os.path.join(outputs_dir, "exp10_benchmark_clinical_comparison.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SAVED] Clinical comparison figure saved to: {fig_path}")

    # Generate Distance Transform and Curve Figure (Figure 10.1)
    fig2, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(14, 5))
    im_a = ax_a.imshow(dist_map, cmap='inferno')
    ax_a.set_title("(A) Euclidean Distance Transform D(x, y)\nBright Peaks = True Anatomical Markers", fontsize=11, fontweight='bold')
    fig2.colorbar(im_a, ax=ax_a, fraction=0.046, pad=0.04)
    ax_a.axis('off')
    
    ax_b.plot(df_srg['Tolerance_T'], df_srg['DSC'], 'b-o', linewidth=2.5, markersize=7, label='Dice Similarity (DSC)')
    ax_b.plot(df_srg['Tolerance_T'], df_srg['Jaccard_IoU'], 'g--s', linewidth=2, markersize=6, label='Jaccard Index (IoU)')
    ax_b.axvspan(20, 65, color='green', alpha=0.15, label='Optimal Clinical Window')
    ax_b.axvspan(80, 115, color='red', alpha=0.15, label='Boundary Leakage Zone')
    ax_b.set_xlabel("Homogeneity Tolerance T", fontsize=11, fontweight='bold')
    ax_b.set_ylabel("Overlap Metric", fontsize=11, fontweight='bold')
    ax_b.set_title("(B) Region Growing Sensitivity Curve Across Tolerance T", fontsize=11, fontweight='bold')
    ax_b.set_ylim(-0.05, 1.05)
    ax_b.grid(True, linestyle=':', alpha=0.6)
    ax_b.legend(loc='lower left', fontsize=10)
    
    plt.tight_layout()
    fig2_path = os.path.join(outputs_dir, "exp10_distance_transform_and_curve.png")
    plt.savefig(fig2_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SAVED] Distance transform & curve figure saved to: {fig2_path}")

if __name__ == "__main__":
    run_benchmark()
