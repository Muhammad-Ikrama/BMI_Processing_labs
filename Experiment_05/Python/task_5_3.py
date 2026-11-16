"""
Experiment 05 - Task 5.3: Manual Implementation of Non-Maximum Suppression (NMS)
Stage 3 of Canny Optimal Edge Detector: 4-Sector Geometric Quantization & Ridge Thinning
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Riphah International University
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve


def manual_non_maximum_suppression(magnitude, orientation_rad):
    """
    Manual implementation of Canny Stage 3: Non-Maximum Suppression.
    Quantizes gradient direction into 4 discrete sectors (0, 45, 90, 135 deg)
    and suppresses non-peak pixels along the gradient normal vector.
    """
    H, W = magnitude.shape
    nms_out = np.zeros((H, W), dtype=np.float64)
    sector_map = np.zeros((H, W), dtype=np.uint8)

    # Convert orientation from radians [-pi, pi] to degrees [0, 180)
    angle_deg = np.rad2deg(orientation_rad) % 180.0

    # Sector assignments:
    # Sector 0: 0 deg (Horizontal gradient, vertical edge) -> [0, 22.5) or [157.5, 180)
    # Sector 1: 45 deg (Diagonal) -> [22.5, 67.5)
    # Sector 2: 90 deg (Vertical gradient, horizontal edge) -> [67.5, 112.5)
    # Sector 3: 135 deg (Anti-diagonal) -> [112.5, 157.5)
    
    # Vectorized sector mapping
    s0_mask = (angle_deg < 22.5) | (angle_deg >= 157.5)
    s1_mask = (angle_deg >= 22.5) & (angle_deg < 67.5)
    s2_mask = (angle_deg >= 67.5) & (angle_deg < 112.5)
    s3_mask = (angle_deg >= 112.5) & (angle_deg < 157.5)

    sector_map[s0_mask] = 0
    sector_map[s1_mask] = 1
    sector_map[s2_mask] = 2
    sector_map[s3_mask] = 3

    # Pad magnitude by 1 pixel to handle borders safely
    pad_mag = np.pad(magnitude, ((1, 1), (1, 1)), mode="constant", constant_values=0)

    # Iterate over inner pixels
    for r in range(1, H + 1):
        for c in range(1, W + 1):
            sec = sector_map[r - 1, c - 1]
            curr_val = pad_mag[r, c]

            if curr_val <= 0:
                continue

            if sec == 0:
                # Gradient normal is horizontal: check left and right
                q = pad_mag[r, c + 1]
                p = pad_mag[r, c - 1]
            elif sec == 1:
                # Gradient normal is 45 deg: check top-right and bottom-left
                q = pad_mag[r - 1, c + 1]
                p = pad_mag[r + 1, c - 1]
            elif sec == 2:
                # Gradient normal is 90 deg: check top and bottom
                q = pad_mag[r - 1, c]
                p = pad_mag[r + 1, c]
            else:  # sec == 3
                # Gradient normal is 135 deg: check top-left and bottom-right
                q = pad_mag[r - 1, c - 1]
                p = pad_mag[r + 1, c + 1]

            # Suppress non-maximum
            if curr_val >= q and curr_val >= p:
                nms_out[r - 1, c - 1] = curr_val
            else:
                nms_out[r - 1, c - 1] = 0.0

    return nms_out, sector_map


def run_task_5_3():
    print("=" * 70)
    print("EXPERIMENT 05 - TASK 5.3: MANUAL NON-MAXIMUM SUPPRESSION (NMS)")
    print("=" * 70)

    # Path handling
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.dirname(script_dir)
    img_path = os.path.join(exp_dir, "Inputs", "images", "CT.jpg")
    if not os.path.exists(img_path):
        img_path = os.path.join(exp_dir, "..", "..", "images", "CT.jpg")
    
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not load image at {img_path}")

    # Gaussian pre-smoothing as per Canny Stage 1
    blurred = cv2.GaussianBlur(img, (5, 5), 1.2)

    # Stage 2: Sobel Gradients
    Gx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    Gy = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.hypot(Gx, Gy)
    theta = np.arctan2(Gy, Gx)

    print("[INFO] Executing custom manual Non-Maximum Suppression algorithm...")
    nms_out, sector_map = manual_non_maximum_suppression(mag, theta)

    # Threshold for binary demonstration
    thresh = 40.0
    unthinned_bin = (mag > thresh).astype(np.uint8) * 255
    thinned_bin = (nms_out > thresh).astype(np.uint8) * 255

    unthinned_cnt = int(np.count_nonzero(unthinned_bin))
    thinned_cnt = int(np.count_nonzero(thinned_bin))
    thin_pct = (1.0 - (thinned_cnt / max(unthinned_cnt, 1))) * 100.0

    print(f"[METRIC] Un-thinned Sobel Edges (Thresh > {thresh}): {unthinned_cnt:,} pixels")
    print(f"[METRIC] Manual NMS 1-px Skeletons:           {thinned_cnt:,} pixels")
    print(f"[DECISION] Ridge Thinning Efficiency: {thin_pct:.1f}% data reduction with 1-pixel skeletonization.")

    # Save outputs
    out_dir = os.path.join(exp_dir, "Outputs", "Python")
    os.makedirs(out_dir, exist_ok=True)
    cv2.imwrite(os.path.join(out_dir, "exp05_task_5_3_unthinned_sobel.png"), unthinned_bin)
    cv2.imwrite(os.path.join(out_dir, "exp05_task_5_3_nms_thinned.png"), thinned_bin)

    # Visualization
    fig, axes = plt.subplots(2, 2, figsize=(13, 11), dpi=300)

    # (a) Un-thinned Sobel Magnitude
    axes[0, 0].imshow(mag, cmap="hot")
    axes[0, 0].set_title(f"Un-Thinned Sobel Gradient Magnitude\n(Ramped 3-5 Pixel Bands: {unthinned_cnt:,} Pixels > {int(thresh)})",
                         fontsize=11, fontweight="bold", pad=8)
    axes[0, 0].axis("off")

    # (b) Quantized Direction Sectors Map
    cmap_sec = plt.cm.get_cmap("Set1", 4)
    im1 = axes[0, 1].imshow(sector_map, cmap=cmap_sec)
    cbar1 = plt.colorbar(im1, ax=axes[0, 1], ticks=[0.375, 1.125, 1.875, 2.625], fraction=0.046, pad=0.04)
    cbar1.ax.set_yticklabels(["0° (H)", "45° (Diag)", "90° (V)", "135° (Anti-D)"], fontweight="bold", fontsize=9)
    axes[0, 1].set_title("Quantized 4-Sector Gradient Direction Map\n[0°, 45°, 90°, 135° Discretization]",
                         fontsize=11, fontweight="bold", pad=8)
    axes[0, 1].axis("off")

    # (c) Manual NMS Output
    axes[1, 0].imshow(thinned_bin, cmap="gray")
    axes[1, 0].set_title(f"Manual Non-Maximum Suppression (NMS)\n(Crisp 1-Pixel Skeletons: {thinned_cnt:,} Pixels | {thin_pct:.1f}% Thinner)",
                         fontsize=11, fontweight="bold", pad=8)
    axes[1, 0].axis("off")

    # (d) Zoom Comparison Window on Skull Boundary
    # Extract zoom ROI around lateral skull table [180:260, 80:160]
    zr1, zr2, zc1, zc2 = 180, 260, 80, 160
    zoom_unthinned = unthinned_bin[zr1:zr2, zc1:zc2]
    zoom_thinned = thinned_bin[zr1:zr2, zc1:zc2]

    # Create composite side-by-side zoom
    zoom_composite = np.zeros((zr2 - zr1, (zc2 - zc1) * 2 + 10, 3), dtype=np.uint8)
    # Left: unthinned (reddish)
    zoom_composite[:, :zc2-zc1, 0] = zoom_unthinned
    zoom_composite[:, :zc2-zc1, 1] = zoom_unthinned // 2
    # Divider line
    zoom_composite[:, zc2-zc1:zc2-zc1+10, :] = 128
    # Right: thinned (cyan/green)
    zoom_composite[:, zc2-zc1+10:, 1] = zoom_thinned
    zoom_composite[:, zc2-zc1+10:, 2] = zoom_thinned

    axes[1, 1].imshow(zoom_composite)
    axes[1, 1].set_title(f"High-Res Zoom Window (Skull Boundary ROI)\nLeft: Un-thinned Sobel (3-5 px) | Right: NMS 1-px Skeleton",
                         fontsize=11, fontweight="bold", pad=8)
    axes[1, 1].axis("off")

    plt.suptitle("Task 5.3: Manual Non-Maximum Suppression (NMS) Algorithm Architecture\nDiscretized Normal-Vector Ridge Tracking and 1-Pixel Skeletonization",
                 fontsize=13, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    fig_dir = os.path.join(exp_dir, "Figures")
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, "exp05_task_5_3_manual_nms_py.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SUCCESS] Figure saved to {fig_path}")

    return {
        "unthinned_count": unthinned_cnt,
        "thinned_count": thinned_cnt,
        "thinning_percentage": thin_pct
    }


if __name__ == "__main__":
    run_task_5_3()
