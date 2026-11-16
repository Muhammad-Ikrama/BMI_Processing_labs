"""
Experiment 05 - Task 5.4: Canny Hysteresis Threshold Tuning & Broken Contour Analysis
Investigating Hysteresis Dual-Threshold Dynamics on Clinical Anatomical Continuity
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Riphah International University
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def run_task_5_4():
    print("=" * 70)
    print("EXPERIMENT 05 - TASK 5.4: CANNY HYSTERESIS TUNING & CONTOUR ANALYSIS")
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

    # Parameter Sweep A: Fixed T_low = 30, varying T_high in [80, 150, 220]
    sweep_A = [
        (30, 80, "Case A1: Low T_high (30/80)\nExcessive Clutter & Spurious Loops"),
        (30, 150, "Case A2: Balanced T_high (30/150)\nGood Boundary Connectivity"),
        (30, 220, "Case A3: High T_high (30/220)\nBroken Skull & Ventricle Boundaries")
    ]

    # Parameter Sweep B: Fixed T_high = 150, varying T_low in [15, 50, 100]
    sweep_B = [
        (15, 150, "Case B1: Low T_low (15/150)\nNoise Breakthrough in Background"),
        (50, 150, "Case B2: Recommended (50/150)\nOptimal Clinical Trade-off"),
        (100, 150, "Case B3: High T_low (100/150)\nSevere Boundary Fragmentation")
    ]

    all_configs = sweep_A + sweep_B

    print("\n" + "-" * 80)
    print(f"{'Configuration':<22} | {'T_low':<6} | {'T_high':<6} | {'Ratio':<6} | {'Edge Pixels':<12} | {'Density (%)':<10}")
    print("-" * 80)

    results = []
    out_dir = os.path.join(exp_dir, "Outputs", "Python")
    os.makedirs(out_dir, exist_ok=True)

    edge_maps = []
    for t_low, t_high, label in all_configs:
        edges = cv2.Canny(img, t_low, t_high)
        cnt = int(np.count_nonzero(edges))
        density = (cnt / total_pixels) * 100.0
        ratio = t_high / float(t_low)
        results.append({
            "t_low": t_low, "t_high": t_high, "ratio": ratio,
            "count": cnt, "density": density, "label": label
        })
        print(f"{label.split(':')[0]:<22} | {t_low:<6} | {t_high:<6} | {ratio:<6.2f} | {cnt:<12,} | {density:<10.2f}")
        
        # Save edge map
        cfg_name = f"exp05_task_5_4_canny_tlow{t_low}_thigh{t_high}.png"
        cv2.imwrite(os.path.join(out_dir, cfg_name), edges)
        edge_maps.append(edges)

    print("-" * 80)
    print("[CLINICAL HYSTERESIS RULE OF THUMB]")
    print(" - Recommended ratio Thigh / Tlow is between 2.0 and 3.0 (e.g. 50 / 150).")
    print(" - Ratio < 1.5 allows random thermal noise to break through weak threshold.")
    print(" - Ratio > 4.0 or excessive Thigh causes severe contour dropouts in low-contrast lesions.")

    # Visualization: 2x3 Grid
    fig, axes = plt.subplots(2, 3, figsize=(16, 11), dpi=300)

    # Row 1: Sweep A (Varying T_high)
    for col in range(3):
        res = results[col]
        ax = axes[0, col]
        ax.imshow(edge_maps[col], cmap="gray")
        ax.set_title(f"{res['label']}\nEdges: {res['count']:,} | Density: {res['density']:.2f}% (Ratio: {res['ratio']:.1f})",
                     fontsize=10, fontweight="bold", pad=8)
        ax.axis("off")

    # Row 2: Sweep B (Varying T_low)
    for col in range(3):
        res = results[3 + col]
        ax = axes[1, col]
        ax.imshow(edge_maps[3 + col], cmap="gray")
        ax.set_title(f"{res['label']}\nEdges: {res['count']:,} | Density: {res['density']:.2f}% (Ratio: {res['ratio']:.1f})",
                     fontsize=10, fontweight="bold", pad=8)
        ax.axis("off")

    plt.suptitle("Task 5.4: Canny Hysteresis Dual-Threshold Sensitivity Analysis\nBalancing Boundary Continuity vs. Spurious Noise Breakthrough in Clinical Scans",
                 fontsize=14, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    fig_dir = os.path.join(exp_dir, "Figures")
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, "exp05_task_5_4_hysteresis_tuning_py.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SUCCESS] Figure saved to {fig_path}")

    return results


if __name__ == "__main__":
    run_task_5_4()
