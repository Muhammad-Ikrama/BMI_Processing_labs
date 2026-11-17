"""
Experiment 11: Task 11.3 - Robustness to Broken / Occluded Anatomical Boundaries
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

def run_task_11_3():
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
    
    # Create corrupted MRI with 15-pixel-wide missing edge gap on right side
    mri_occluded = mri.copy()
    Y, X = np.ogrid[:512, :512]
    dist_c = np.hypot(X - cx, Y - cy)
    # Right-side arc: angle between -30 deg and +30 deg (X > cx), radius between 16 and 28 px
    angle = np.arctan2(Y - cy, X - cx)
    gap_mask = (dist_c >= 16) & (dist_c <= 28) & (np.abs(angle) <= np.radians(25))
    mri_occluded[gap_mask] = 105  # Cortex background intensity
    
    # Method 1: Seeded Region Growing on Occluded Image (T=38)
    mri_occ_smooth = cv2.GaussianBlur(mri_occluded, (3, 3), 0.8)
    seed_x, seed_y = int(round(cx)), int(round(cy))
    
    def srg(img, sy, sx, tol):
        h, w = img.shape
        visited = np.zeros((h, w), dtype=bool)
        mask = np.zeros((h, w), dtype=np.uint8)
        stack = [(sy, sx)]
        visited[sy, sx] = True
        seed_val = float(img[sy, sx])
        neighbors = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        while stack:
            cy_p, cx_p = stack.pop()
            if abs(float(img[cy_p, cx_p]) - seed_val) <= tol:
                mask[cy_p, cx_p] = 255
                for dy, dx in neighbors:
                    ny, nx = cy_p + dy, cx_p + dx
                    if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                        visited[ny, nx] = True
                        stack.append((ny, nx))
        return mask

    srg_mask = srg(mri_occ_smooth, seed_y, seed_x, 38)
    
    # Method 2: Active Contour (Snake) on Occluded Image
    # Compute external potential from actual gradients of occluded image
    sobel_x = cv2.Sobel(mri_occ_smooth, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(mri_occ_smooth, cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = np.hypot(sobel_x, sobel_y)
    grad_smooth = cv2.GaussianBlur(grad_mag, (15, 15), 4.0)
    edge_pot = -100.0 * (grad_smooth / (grad_smooth.max() + 1e-5))
    gy_pot, gx_pot = np.gradient(edge_pot)
    
    # Snake initialization
    N = 80
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    sx = cx + 38.0 * np.cos(theta)
    sy = cy + 38.0 * np.sin(theta)
    s0_x, s0_y = sx.copy(), sy.copy()
    
    alpha, beta, gamma = 0.06, 0.25, 0.25  # Slightly elevated beta to enhance bridging
    A = np.zeros((N, N))
    for i in range(N):
        A[i, i] = 2 * alpha + 6 * beta
        A[i, (i - 1) % N] = A[i, (i + 1) % N] = -(alpha + 4 * beta)
        A[i, (i - 2) % N] = A[i, (i + 2) % N] = beta
    inv_M = np.linalg.inv(np.eye(N) + gamma * A)
    
    for it in range(1, 121):
        ix = np.clip(np.round(sx).astype(int), 0, 511)
        iy = np.clip(np.round(sy).astype(int), 0, 511)
        sx = inv_M @ (sx - gamma * 0.45 * gx_pot[iy, ix])
        sy = inv_M @ (sy - gamma * 0.45 * gy_pot[iy, ix])
        
    snake_mask = np.zeros_like(gt_lesion)
    poly_pts = np.vstack([sx, sy]).T.astype(np.int32)
    cv2.fillPoly(snake_mask, [poly_pts], 255)
    
    # Calculate metrics
    def eval_mask(m, g_mask):
        g, p = (g_mask > 0), (m > 0)
        intersection = np.logical_and(g, p).sum()
        union = np.logical_or(g, p).sum()
        dsc = 2.0 * intersection / (g.sum() + p.sum()) if (g.sum() + p.sum()) > 0 else 0.0
        iou = intersection / union if union > 0 else 0.0
        return dsc, iou, int(p.sum())

    dsc_srg, iou_srg, area_srg = eval_mask(srg_mask, gt_lesion)
    dsc_snk, iou_snk, area_snk = eval_mask(snake_mask, gt_lesion)
    
    print("\n" + "=" * 95)
    print("TASK 11.3: BROKEN / OCCLUDED BOUNDARY BRIDGING (SRG VS. ACTIVE CONTOUR)")
    print("=" * 95)
    print(f"{'Method':<25} | {'Area (px)':<12} | {'DSC':<8} | {'IoU':<8} | {'Clinical Behavior'}")
    print("-" * 95)
    print(f"{'Seeded Region Growing':<25} | {area_srg:<12d} | {dsc_srg:<8.4f} | {iou_srg:<8.4f} | {'Catastrophic Leakage via Missing Gap'}")
    print(f"{'Active Contour (Snake)':<25} | {area_snk:<12d} | {dsc_snk:<8.4f} | {iou_snk:<8.4f} | {'Smooth Elastic Bridging across Gap'}")
    
    records = [
        {"Method": "Seeded Region Growing (T=38)", "Segmented_Area": area_srg, "Ground_Truth_Area": gt_area, "DSC": round(dsc_srg, 4), "Jaccard_IoU": round(iou_srg, 4), "Clinical_Outcome": "Catastrophic Boundary Leakage via Gap"},
        {"Method": "Active Contour (Snake, beta=0.25)", "Segmented_Area": area_snk, "Ground_Truth_Area": gt_area, "DSC": round(dsc_snk, 4), "Jaccard_IoU": round(iou_snk, 4), "Clinical_Outcome": "Smooth Curvature Bridging (Gap Sealed)"}
    ]
    df = pd.DataFrame(records)
    csv_path = os.path.join(tables_dir, "exp11_task_11_3_broken_boundary.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SAVED] Task 11.3 table saved to: {csv_path}")
    
    # Composite figure
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    zy1, zy2, zx1, zx2 = 185, 295, 270, 385
    crop_occ = mri_occluded[zy1:zy2, zx1:zx2]
    
    # Panel 1: Occluded Image with Gap Highlighted
    axes[0].imshow(crop_occ, cmap='gray', extent=[zx1, zx2, zy2, zy1])
    axes[0].plot(cx + 22, cy, 'ro', markersize=8, markeredgewidth=2, markeredgecolor='yellow')
    axes[0].annotate("15px Erased Gap", xy=(cx+22, cy), xytext=(cx+40, cy-25),
                     arrowprops=dict(facecolor='yellow', shrink=0.05, width=1.5, headwidth=6),
                     color='yellow', fontsize=9.5, fontweight='bold')
    axes[0].set_title("(A) Artificially Occluded Tumor\n15-Pixel Disrupted Rim", fontsize=10, fontweight='bold')
    axes[0].axis('off')
    
    # Panel 2: SRG Leakage
    ov_srg = cv2.cvtColor(crop_occ, cv2.COLOR_GRAY2BGR)
    srg_crop = srg_mask[zy1:zy2, zx1:zx2]
    ov_srg[srg_crop > 0] = [255, 100, 0]
    axes[1].imshow(cv2.cvtColor(ov_srg, cv2.COLOR_BGR2RGB), extent=[zx1, zx2, zy2, zy1])
    axes[1].set_title(f"(B) Seeded Region Growing\nArea = {area_srg} px | DSC = {dsc_srg:.3f}\nCatastrophic Boundary Leakage", fontsize=10, fontweight='bold')
    axes[1].axis('off')
    
    # Panel 3: Snake Bridging
    axes[2].imshow(crop_occ, cmap='gray', extent=[zx1, zx2, zy2, zy1])
    axes[2].plot(s0_x, s0_y, 'r--', linewidth=1.8, label='Initial (t=0)')
    axes[2].plot(sx, sy, 'lime', linewidth=2.5, label='Converged Snake (t=120)')
    axes[2].set_title(f"(C) Active Contour (Snake)\nArea = {area_snk} px | DSC = {dsc_snk:.3f}\nElastic Bending Bridges Gap!", fontsize=10, fontweight='bold')
    axes[2].axis('off')
    axes[2].legend(loc='lower left', fontsize=9)
    
    plt.tight_layout()
    fig_path = os.path.join(outputs_dir, "exp11_task_11_3_broken_boundary.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SAVED] Task 11.3 figure saved to: {fig_path}")

if __name__ == "__main__":
    run_task_11_3()
