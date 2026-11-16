"""
Experiment 05 - Task 5.1: Discrete Gradient Kernel Construction & Directional Sensitivity
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Riphah International University
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve


def run_task_5_1():
    print("=" * 70)
    print("EXPERIMENT 05 - TASK 5.1: DIRECTIONAL GRADIENT SENSITIVITY & HSV MAPPING")
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

    H, W = img.shape
    img_f = img.astype(np.float64)

    # Sobel kernels
    # Gx detects vertical edges (horizontal intensity changes df/dx)
    Gx_kernel = np.array([[-1, 0, 1],
                          [-2, 0, 2],
                          [-1, 0, 1]], dtype=np.float64)
    # Gy detects horizontal edges (vertical intensity changes df/dy)
    Gy_kernel = np.array([[-1, -2, -1],
                          [ 0,  0,  0],
                          [ 1,  2,  1]], dtype=np.float64)

    Gx = convolve(img_f, Gx_kernel)
    Gy = convolve(img_f, Gy_kernel)

    # Gradient magnitude and orientation
    mag = np.hypot(Gx, Gy)
    # Angle in radians [-pi, pi], map to degrees [0, 180)
    theta = np.arctan2(Gy, Gx)
    theta_deg = np.rad2deg(theta) % 180.0

    # Build HSV Color-Coded Direction Map
    # Hue: angle [0, 180] -> OpenCV Hue is [0, 179]
    hsv = np.zeros((H, W, 3), dtype=np.uint8)
    hsv[..., 0] = (theta_deg / 180.0 * 179.0).astype(np.uint8)
    hsv[..., 1] = 255  # Full saturation

    # Value: normalized gradient magnitude, thresholded to avoid noise coloring
    norm_mag = np.clip(mag / np.percentile(mag, 98) * 255.0, 0, 255).astype(np.uint8)
    hsv[..., 2] = norm_mag

    # Convert HSV to RGB for display
    rgb_orientation = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

    # Save outputs
    out_dir = os.path.join(exp_dir, "Outputs", "Python")
    os.makedirs(out_dir, exist_ok=True)
    cv2.imwrite(os.path.join(out_dir, "exp05_task_5_1_Gx.png"), np.clip(np.abs(Gx), 0, 255).astype(np.uint8))
    cv2.imwrite(os.path.join(out_dir, "exp05_task_5_1_Gy.png"), np.clip(np.abs(Gy), 0, 255).astype(np.uint8))
    cv2.imwrite(os.path.join(out_dir, "exp05_task_5_1_magnitude.png"), np.clip(mag, 0, 255).astype(np.uint8))
    cv2.imwrite(os.path.join(out_dir, "exp05_task_5_1_hsv_orientation.png"), cv2.cvtColor(rgb_orientation, cv2.COLOR_RGB2BGR))

    # Print anatomical sensitivity insights
    print(f"[METRIC] Max Gx: {np.max(np.abs(Gx)):.2f} | Max Gy: {np.max(np.abs(Gy)):.2f} | Max Magnitude: {np.max(mag):.2f}")
    print("[CLINICAL ANATOMY INSIGHT]")
    print(" - Gx highlights VERTICAL edges: Lateral cranial bone table, sagittal suture, vertical sulci, falx cerebri.")
    print(" - Gy highlights HORIZONTAL edges: Superior cranial vault, tentorium cerebelli, transverse sinuses, horizontal ventricular horns.")
    print(" - HSV Map assigns unique hues to edge directions: Red (0 deg, horizontal), Green (60 deg), Blue (120 deg), etc.")

    # 4-Panel Visualization
    fig, axes = plt.subplots(2, 2, figsize=(13, 11), dpi=300)

    # Gx
    im0 = axes[0, 0].imshow(np.abs(Gx), cmap="hot")
    axes[0, 0].set_title("Horizontal Gradient |Gx|\n(Highlights Vertical Anatomical Edges)", fontsize=11, fontweight="bold", pad=8)
    axes[0, 0].axis("off")
    plt.colorbar(im0, ax=axes[0, 0], fraction=0.046, pad=0.04)

    # Gy
    im1 = axes[0, 1].imshow(np.abs(Gy), cmap="hot")
    axes[0, 1].set_title("Vertical Gradient |Gy|\n(Highlights Horizontal Anatomical Edges)", fontsize=11, fontweight="bold", pad=8)
    axes[0, 1].axis("off")
    plt.colorbar(im1, ax=axes[0, 1], fraction=0.046, pad=0.04)

    # Magnitude
    im2 = axes[1, 0].imshow(mag, cmap="viridis")
    axes[1, 0].set_title("Combined Gradient Magnitude |nabla f|\n|nabla f| = sqrt(Gx^2 + Gy^2)", fontsize=11, fontweight="bold", pad=8)
    axes[1, 0].axis("off")
    plt.colorbar(im2, ax=axes[1, 0], fraction=0.046, pad=0.04)

    # HSV Orientation Map
    axes[1, 1].imshow(rgb_orientation)
    axes[1, 1].set_title("HSV Color-Coded Gradient Orientation Map\nHue: Angle theta (0-180 deg) | Value: Magnitude", fontsize=11, fontweight="bold", pad=8)
    axes[1, 1].axis("off")

    plt.suptitle("Task 5.1: Directional Gradient Decomposition & Orientation Mapping in Head CT\nDifferential Spatial Calculus with Orthogonal Sobel Operators",
                 fontsize=13, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    fig_dir = os.path.join(exp_dir, "Figures")
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, "exp05_task_5_1_directional_gradients_py.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SUCCESS] Figure saved to {fig_path}")

    return {
        "max_Gx": float(np.max(np.abs(Gx))),
        "max_Gy": float(np.max(np.abs(Gy))),
        "max_mag": float(np.max(mag))
    }


if __name__ == "__main__":
    run_task_5_1()
