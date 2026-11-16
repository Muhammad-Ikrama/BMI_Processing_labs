"""
Experiment 05 - Example 01: Medical Edge Detection Benchmark
Sobel, Prewitt, and Canny Operators Implementation & Quantitative Comparison
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Riphah International University
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve


def run_example_01():
    print("=" * 70)
    print("EXPERIMENT 05 - EXAMPLE 01: MEDICAL EDGE DETECTION BENCHMARK")
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
    total_pixels = float(img.size)
    print(f"[INFO] Loaded CT Image: {W}x{H} pixels ({int(total_pixels):,} total pixels)")

    # 1. Prewitt Operator (Orthogonal finite difference)
    px = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
    py = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)
    img_f = img.astype(float)
    prew_x = convolve(img_f, px)
    prew_y = convolve(img_f, py)
    prew_mag = np.hypot(prew_x, prew_y)
    prew_thresh = 45.0
    prew_edge = (prew_mag > prew_thresh).astype(np.uint8) * 255

    # 2. Sobel Operator (Binomial weighted difference)
    sob_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    sob_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    sob_mag = np.hypot(sob_x, sob_y)
    sob_thresh = 60.0
    sob_edge = (sob_mag > sob_thresh).astype(np.uint8) * 255

    # 3. Canny Operator (Optimal NMS + Hysteresis)
    canny_edge = cv2.Canny(img, 50, 150)

    # 4. Quantitative Benchmarking
    operators = [
        ("Prewitt Operator", prew_edge, prew_mag),
        ("Sobel Operator", sob_edge, sob_mag),
        ("Canny Edge Detector", canny_edge, None)
    ]

    print("\n" + "-" * 65)
    print(f"{'Operator':<24} | {'Edge Pixels':<12} | {'Density (%)':<12}")
    print("-" * 65)
    results = {}
    for name, b_map, _ in operators:
        cnt = int(np.count_nonzero(b_map))
        pct = (cnt / total_pixels) * 100.0
        results[name] = {"count": cnt, "density": pct}
        print(f"{name:<24} | {cnt:<12,} | {pct:<12.2f}")
    print("-" * 65)
    
    thinning_ratio = (1.0 - (results["Canny Edge Detector"]["count"] / results["Sobel Operator"]["count"])) * 100.0
    print(f"[DECISION] Canny Operator achieves OPTIMAL 1-pixel skeletonization ({thinning_ratio:.1f}% thinner than Sobel).")

    # Save output edge maps
    out_dir = os.path.join(exp_dir, "Outputs", "Python")
    os.makedirs(out_dir, exist_ok=True)
    cv2.imwrite(os.path.join(out_dir, "exp05_example_01_prewitt.png"), prew_edge)
    cv2.imwrite(os.path.join(out_dir, "exp05_example_01_sobel.png"), sob_edge)
    cv2.imwrite(os.path.join(out_dir, "exp05_example_01_canny.png"), canny_edge)

    # 5. Publication-Grade Visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 11), dpi=300)
    
    # Original
    axes[0, 0].imshow(img, cmap="gray")
    axes[0, 0].set_title("Original Clinical Head CT Scan\n(Ground Truth Anatomy)", fontsize=11, fontweight="bold", pad=8)
    axes[0, 0].axis("off")

    # Prewitt
    p_cnt = results["Prewitt Operator"]["count"]
    p_pct = results["Prewitt Operator"]["density"]
    axes[0, 1].imshow(prew_edge, cmap="gray")
    axes[0, 1].set_title(f"Prewitt Operator (Threshold > {int(prew_thresh)})\nEdges: {p_cnt:,} | Density: {p_pct:.2f}% (Thick Ramps)", 
                         fontsize=11, fontweight="bold", pad=8)
    axes[0, 1].axis("off")

    # Sobel
    s_cnt = results["Sobel Operator"]["count"]
    s_pct = results["Sobel Operator"]["density"]
    axes[1, 0].imshow(sob_edge, cmap="gray")
    axes[1, 0].set_title(f"Sobel Operator (Threshold > {int(sob_thresh)})\nEdges: {s_cnt:,} | Density: {s_pct:.2f}% (Binomial Smoothing)", 
                         fontsize=11, fontweight="bold", pad=8)
    axes[1, 0].axis("off")

    # Canny
    c_cnt = results["Canny Edge Detector"]["count"]
    c_pct = results["Canny Edge Detector"]["density"]
    axes[1, 1].imshow(canny_edge, cmap="gray")
    axes[1, 1].set_title(f"Canny Edge Detector (T_low=50, T_high=150)\nEdges: {c_cnt:,} | Density: {c_pct:.2f}% (1-px Skeletons)", 
                         fontsize=11, fontweight="bold", pad=8)
    axes[1, 1].axis("off")

    plt.suptitle("Clinical Head CT Edge Detection Benchmark\nSpatial Gradient Operators (Sobel & Prewitt) vs. Multi-Stage Optimal Canny",
                 fontsize=13, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    fig_dir = os.path.join(exp_dir, "Figures")
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, "exp05_example_01_benchmark_py.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SUCCESS] Figure saved to {fig_path}")

    return results


if __name__ == "__main__":
    run_example_01()
