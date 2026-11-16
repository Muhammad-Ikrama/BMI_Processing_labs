"""
Experiment 03: Image Smoothing of Medical Images Using Spatial Domain Mean/Averaging and Gaussian Filters
Task 3.1: 2D Spatial Discrete Convolution & Boundary Padding Comparison (Zero vs Replicate)
Course: Medical Image Processing | Riphah International University
Instructor: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def custom_conv2d(image, kernel, padding_mode='replicate'):
    """
    Custom 2D spatial convolution implementing the discrete formula:
    g(x, y) = sum_s sum_t w(s, t) * f(x+s, y+t)
    
    Parameters:
        image: 2D numpy array (float or uint8)
        kernel: 2D odd-sized square numpy array
        padding_mode: 'zero' or 'replicate'
    """
    im_h, im_w = image.shape
    k_h, k_w = kernel.shape
    pad_y = k_h // 2
    pad_x = k_w // 2

    # Apply padding
    if padding_mode == 'zero':
        padded = np.pad(image, ((pad_y, pad_y), (pad_x, pad_x)), mode='constant', constant_values=0)
    elif padding_mode == 'replicate':
        padded = np.pad(image, ((pad_y, pad_y), (pad_x, pad_x)), mode='edge')
    elif padding_mode == 'reflect':
        padded = np.pad(image, ((pad_y, pad_y), (pad_x, pad_x)), mode='reflect')
    else:
        raise ValueError(f"Unsupported padding mode: {padding_mode}")

    # Flip kernel for true convolution (correlation vs convolution)
    k_flipped = np.flipud(np.fliplr(kernel))

    # Fast sliding window implementation via strided vectorization or optimized loop
    output = np.zeros((im_h, im_w), dtype=np.float64)
    for s in range(k_h):
        for t in range(k_w):
            output += padded[s:s+im_h, t:t+im_w] * k_flipped[s, t]

    return np.clip(output, 0, 255).astype(np.uint8)

def run_task_3_1():
    print("=" * 70)
    print("EXPERIMENT 03 - TASK 3.1: 2D CONVOLUTION & BOUNDARY PADDING COMPARISON")
    print("=" * 70)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.dirname(script_dir)
    img_path = os.path.join(exp_dir, "Inputs", "images", "MRI.jpg")

    if not os.path.exists(img_path):
        img_path = os.path.join(exp_dir, "..", "..", "images", "MRI.jpg")

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not load image from {img_path}")

    H, W = img.shape
    print(f"[INFO] Loaded MRI scan: {W} x {H} pixels")

    # Define 3x3 Mean averaging kernel: 1/9 everywhere
    k_size = 3
    kernel_3x3 = np.ones((k_size, k_size), dtype=np.float64) / (k_size * k_size)
    print(f"[INFO] 3x3 Averaging Kernel:\n{kernel_3x3}")

    # Perform custom convolution under two boundary conditions
    print("[INFO] Computing 2D discrete convolution with Zero-Padding...")
    filtered_zero = custom_conv2d(img, kernel_3x3, padding_mode='zero')

    print("[INFO] Computing 2D discrete convolution with Replicate-Padding...")
    filtered_replicate = custom_conv2d(img, kernel_3x3, padding_mode='replicate')

    # Quantify boundary distortion in outer 5-pixel perimeter band
    # Create mask of outer 5 pixels
    border_mask = np.zeros((H, W), dtype=bool)
    border_mask[:5, :] = True
    border_mask[-5:, :] = True
    border_mask[:, :5] = True
    border_mask[:, -5:] = True

    # Reference internal region vs border region
    diff_abs = np.abs(filtered_replicate.astype(float) - filtered_zero.astype(float))
    border_mae = np.mean(diff_abs[border_mask])
    border_rmse = np.sqrt(np.mean((diff_abs[border_mask]) ** 2))
    max_border_drop = np.max(diff_abs[border_mask])

    print("\n" + "-" * 65)
    print("BOUNDARY PADDING ERROR METRICS (5-Pixel Perimeter Region):")
    print(f"  * Mean Absolute Error (MAE):     {border_mae:.2f} intensity levels")
    print(f"  * Root Mean Squared Error (RMSE): {border_rmse:.2f} intensity levels")
    print(f"  * Maximum Intensity Drop:        {max_border_drop:.2f} intensity levels")
    print("-" * 65)
    print("Clinical Conclusion: Zero-padding introduces dark boundary decay (halo artifact),")
    print("whereas replicate/clamp padding maintains tissue continuity across image borders.")

    # Magnify the perimeter region (first 25 rows and 25 columns)
    mag_rows, mag_cols = 25, 25
    roi_zero = filtered_zero[:mag_rows, :mag_cols]
    roi_repl = filtered_replicate[:mag_rows, :mag_cols]
    roi_orig = img[:mag_rows, :mag_cols]

    # Visualization: 4-panel comparison
    fig, axes = plt.subplots(2, 2, figsize=(12, 10), dpi=300)
    plt.subplots_adjust(wspace=0.2, hspace=0.25)

    # Top-Left: Zero-Padded Full Image
    axes[0, 0].imshow(filtered_zero, cmap='gray', vmin=0, vmax=255)
    axes[0, 0].set_title("A: Zero-Padding (Constant 0 Border) Full Scan\n[Notice Dark Outer Perimeter Artifact]",
                          fontsize=10, fontweight='bold', color='#b91c1c')
    axes[0, 0].axis('off')
    rect1 = plt.Rectangle((0, 0), mag_cols, mag_rows, fill=False, edgecolor='#ef4444', linewidth=2, linestyle='--')
    axes[0, 0].add_patch(rect1)

    # Top-Right: Replicate-Padded Full Image
    axes[0, 1].imshow(filtered_replicate, cmap='gray', vmin=0, vmax=255)
    axes[0, 1].set_title("B: Replicate/Clamp Padding (Clinical Standard)\n[Continuous Border Intensities Preserved]",
                          fontsize=10, fontweight='bold', color='#15803d')
    axes[0, 1].axis('off')
    rect2 = plt.Rectangle((0, 0), mag_cols, mag_rows, fill=False, edgecolor='#22c55e', linewidth=2, linestyle='--')
    axes[0, 1].add_patch(rect2)

    # Bottom-Left: Magnified Top-Left Perimeter (Zero Padding)
    im3 = axes[1, 0].imshow(roi_zero, cmap='magma', vmin=0, vmax=255)
    axes[1, 0].set_title(f"C: Magnified Corner (Zero-Padding)\nOuter Row/Col Attenuated (MAE={border_mae:.1f})",
                          fontsize=10, fontweight='bold', color='#b91c1c')
    axes[1, 0].set_xlabel("Pixel Column Index (0 to 24)", fontsize=9)
    axes[1, 0].set_ylabel("Pixel Row Index (0 to 24)", fontsize=9)
    plt.colorbar(im3, ax=axes[1, 0], fraction=0.046, pad=0.04, label="Pixel Intensity [0-255]")

    # Bottom-Right: Magnified Top-Left Perimeter (Replicate Padding)
    im4 = axes[1, 1].imshow(roi_repl, cmap='magma', vmin=0, vmax=255)
    axes[1, 1].set_title("D: Magnified Corner (Replicate-Padding)\nUnbiased Uniform Boundary Continuity",
                          fontsize=10, fontweight='bold', color='#15803d')
    axes[1, 1].set_xlabel("Pixel Column Index (0 to 24)", fontsize=9)
    axes[1, 1].set_ylabel("Pixel Row Index (0 to 24)", fontsize=9)
    plt.colorbar(im4, ax=axes[1, 1], fraction=0.046, pad=0.04, label="Pixel Intensity [0-255]")

    fig.suptitle("Task 3.1: 2D Spatial Discrete Convolution & Boundary Padding Comparison (Brain MRI)",
                 fontsize=13, fontweight='bold', color='#0f172a', y=0.98)

    out_dir_py = os.path.join(exp_dir, "Outputs", "Python")
    fig_dir = os.path.join(exp_dir, "Figures")
    os.makedirs(out_dir_py, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    out_path_1 = os.path.join(out_dir_py, "exp03_task_3_1_boundary_padding_py.png")
    out_path_2 = os.path.join(fig_dir, "exp03_task_3_1_boundary_padding_py.png")

    plt.savefig(out_path_1, bbox_inches='tight', dpi=300)
    plt.savefig(out_path_2, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"[SUCCESS] Saved figure to:\n  {out_path_1}\n  {out_path_2}")

if __name__ == '__main__':
    run_task_3_1()
