"""
Experiment 11: Task 11.4 - Edge-Based Snake vs. Chan-Vese Region-Based Active Contour under Noise
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
from skimage.segmentation import morphological_chan_vese

def run_task_11_4():
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
    
    # 1. Add heavy Gaussian noise (sigma = 28)
    np.random.seed(42)
    noise = np.random.normal(0, 28, mri.shape)
    mri_noisy = np.clip(mri.astype(float) + noise, 0, 255).astype(np.uint8)
    
    # Initial circular mask & points
    N = 80
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    sx = cx + 38.0 * np.cos(theta)
    sy = cy + 38.0 * np.sin(theta)
    s0_x, s0_y = sx.copy(), sy.copy()
    
    # Model 1: Edge-based Snake on Noisy Image
    sobel_x = cv2.Sobel(mri_noisy, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(mri_noisy, cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = np.hypot(sobel_x, sobel_y)
    # Slight smooth of noisy gradient
    grad_smooth = cv2.GaussianBlur(grad_mag, (9, 9), 2.0)
    edge_pot = -100.0 * (grad_smooth / (grad_smooth.max() + 1e-5))
    gy_pot, gx_pot = np.gradient(edge_pot)
    
    alpha, beta, gamma = 0.06, 0.12, 0.25
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
        
    mask_edge = np.zeros_like(gt_lesion)
    poly_pts = np.vstack([sx, sy]).T.astype(np.int32)
    cv2.fillPoly(mask_edge, [poly_pts], 255)
    
    # Model 2: Chan-Vese Region-Based Active Contour
    init_cv_mask = np.zeros_like(gt_lesion, dtype=bool)
    Y, X = np.ogrid[:512, :512]
    init_cv_mask[(X - cx)**2 + (Y - cy)**2 <= 38.0**2] = True
    
    cv_res = morphological_chan_vese(mri_noisy, num_iter=35, init_level_set=init_cv_mask, smoothing=3)
    # Filter to main CC around center
    cv_uint8 = (cv_res.astype(np.uint8)) * 255
    num_cc_cv, labels_cv, stats_cv, centroids_cv = cv2.connectedComponentsWithStats(cv_uint8)
    
    mask_chan_vese = np.zeros_like(gt_lesion)
    if num_cc_cv > 1:
        # Pick component closest to cx, cy
        dists = [np.hypot(centroids_cv[i,0] - cx, centroids_cv[i,1] - cy) for i in range(1, num_cc_cv)]
        best_lbl = 1 + np.argmin(dists)
        mask_chan_vese = ndimage.binary_fill_holes(labels_cv == best_lbl).astype(np.uint8) * 255
    else:
        mask_chan_vese = cv_uint8
        
    # Evaluate metrics
    def eval_mask(m, g_mask):
        g, p = (g_mask > 0), (m > 0)
        intersection = np.logical_and(g, p).sum()
        union = np.logical_or(g, p).sum()
        dsc = 2.0 * intersection / (g.sum() + p.sum()) if (g.sum() + p.sum()) > 0 else 0.0
        iou = intersection / union if union > 0 else 0.0
        return dsc, iou, int(p.sum())

    dsc_edge, iou_edge, area_edge = eval_mask(mask_edge, gt_lesion)
    dsc_cv, iou_cv, area_cv = eval_mask(mask_chan_vese, gt_lesion)
    
    print("\n" + "=" * 95)
    print("TASK 11.4: EDGE-BASED SNAKE VS. CHAN-VESE REGION-BASED ACTIVE CONTOUR (NOISE sigma=28)")
    print("=" * 95)
    print(f"{'Method':<32} | {'Area (px)':<12} | {'DSC':<8} | {'IoU':<8} | {'Clinical Status'}")
    print("-" * 95)
    print(f"{'Edge-Based Snake (Local Gradient)':<32} | {area_edge:<12d} | {dsc_edge:<8.4f} | {iou_edge:<8.4f} | {'Snagged on Noise Spikes'}")
    print(f"{'Chan-Vese Region-Based Model':<32} | {area_cv:<12d} | {dsc_cv:<8.4f} | {iou_cv:<8.4f} | {'Robust Global Region Averaging'}")
    
    records = [
        {"Model_Type": "Edge-Based Snake", "Formulation": "Local Gradient Magnitude ||del I||^2", "Area_px": area_edge, "Ground_Truth_px": gt_area, "DSC": round(dsc_edge, 4), "Jaccard_IoU": round(iou_edge, 4), "Noise_Robustness": "Poor (Trapped in Local Noise Minima)"},
        {"Model_Type": "Chan-Vese Region Model", "Formulation": "Global Mean Intensity Variance (c1, c2)", "Area_px": area_cv, "Ground_Truth_px": gt_area, "DSC": round(dsc_cv, 4), "Jaccard_IoU": round(iou_cv, 4), "Noise_Robustness": "Superior (Integral Averages Out Thermal Noise)"}
    ]
    df = pd.DataFrame(records)
    csv_path = os.path.join(tables_dir, "exp11_task_11_4_edge_vs_chan_vese.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SAVED] Task 11.4 table saved to: {csv_path}")
    
    # Multi-panel plot
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    zy1, zy2, zx1, zx2 = 185, 295, 270, 385
    crop_noisy = mri_noisy[zy1:zy2, zx1:zx2]
    
    # Subplot 1: Noisy Image
    axes[0].imshow(crop_noisy, cmap='gray', extent=[zx1, zx2, zy2, zy1])
    axes[0].plot(s0_x, s0_y, 'r--', linewidth=2, label='Initial Circle')
    axes[0].set_title("(A) Corrupted Brain MRI\nGaussian Thermal Noise (sigma = 28)", fontsize=10, fontweight='bold')
    axes[0].axis('off')
    axes[0].legend(loc='lower left', fontsize=9)
    
    # Subplot 2: Edge Snake (Distorted)
    axes[1].imshow(crop_noisy, cmap='gray', extent=[zx1, zx2, zy2, zy1])
    axes[1].plot(sx, sy, 'magenta', linewidth=2.4, label='Edge Snake')
    axes[1].set_title(f"(B) Edge-Based Snake\nArea = {area_edge} px | DSC = {dsc_edge:.3f}\nTrapped on Noise Gradients", fontsize=10, fontweight='bold')
    axes[1].axis('off')
    axes[1].legend(loc='lower left', fontsize=9)
    
    # Subplot 3: Chan-Vese (Robust)
    axes[2].imshow(crop_noisy, cmap='gray', extent=[zx1, zx2, zy2, zy1])
    cv_cont, _ = cv2.findContours(mask_chan_vese[zy1:zy2, zx1:zx2], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cv_cont:
        axes[2].plot(c[:,0,0] + zx1, c[:,0,1] + zy1, 'lime', linewidth=2.5, label='Chan-Vese')
    axes[2].set_title(f"(C) Chan-Vese Region Model\nArea = {area_cv} px | DSC = {dsc_cv:.3f}\nGlobal Region Averaging Prevails!", fontsize=10, fontweight='bold')
    axes[2].axis('off')
    axes[2].legend(loc='lower left', fontsize=9)
    
    plt.tight_layout()
    fig_path = os.path.join(outputs_dir, "exp11_task_11_4_edge_vs_chan_vese.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SAVED] Task 11.4 figure saved to: {fig_path}")

if __name__ == "__main__":
    run_task_11_4()
