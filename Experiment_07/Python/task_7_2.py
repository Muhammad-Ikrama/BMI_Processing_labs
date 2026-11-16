"""
Experiment 07 - Task 7.2: Influence of Smoothing Kernel Blur Parameter on Mask Bandwidth
Varies Gaussian blur standard deviation sigma across [0.8, 1.5, 3.0] with fixed k = 1.0,
evaluates high-frequency mask spatial bandwidth, mask dynamic range, and edge injection scale.
Course: Medical Image Processing | Riphah International University
Faculty: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

def run_task_7_2():
    print("==============================================================================")
    print("EXPERIMENT 07 - TASK 7.2: SMOOTHING KERNEL BLUR & MASK BANDWIDTH ANALYSIS")
    print("==============================================================================")

    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.abspath(os.path.join(script_dir, ".."))
    img_path = os.path.join(exp_dir, "Inputs", "images", "Xray.jpg")
    if not os.path.exists(img_path):
        img_path = os.path.join(exp_dir, "..", "..", "images", "Xray.jpg")

    out_py_dir = os.path.join(exp_dir, "Outputs", "Python")
    fig_dir = os.path.join(exp_dir, "Figures")
    tab_dir = os.path.join(exp_dir, "Tables")
    os.makedirs(out_py_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(tab_dir, exist_ok=True)

    # 1. Load Image
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Cannot load radiograph at {img_path}")
    H, W = img.shape
    img_f = img.astype(np.float64)

    def calc_mean_grad(im):
        gy, gx = np.gradient(im.astype(np.float64))
        return float(np.mean(np.hypot(gx, gy)))

    base_grad = calc_mean_grad(img)

    sigmas = [0.8, 1.5, 3.0]
    masks = {}
    sharpened_images = {}
    metrics_list = []

    for s in sigmas:
        win_size = int(2 * np.ceil(2 * s) + 1)
        blurred = gaussian_filter(img_f, sigma=s)
        mask = img_f - blurred
        raw_sharp = img_f + 1.0 * mask
        sharp_u8 = np.clip(raw_sharp, 0, 255).astype(np.uint8)

        masks[s] = mask
        sharpened_images[s] = sharp_u8

        # Save individual images
        bipolar_mask = np.clip(mask + 128.0, 0, 255).astype(np.uint8)
        cv2.imwrite(os.path.join(out_py_dir, f"exp07_task_7_2_mask_sigma_{str(s).replace('.', '_')}.png"), bipolar_mask)
        cv2.imwrite(os.path.join(out_py_dir, f"exp07_task_7_2_sharp_sigma_{str(s).replace('.', '_')}.png"), sharp_u8)

        mask_std = float(np.std(mask))
        mask_range = float(np.ptp(mask))
        mg = calc_mean_grad(raw_sharp)
        boost = ((mg - base_grad) / base_grad) * 100.0
        cutoff_freq = float(1.0 / (2.0 * np.pi * s))

        if s == 0.8:
            interp = "Microscopic Edge Mask (Fine textures, minimal halo risk)"
        elif s == 1.5:
            interp = "Balanced Diagnostic Mask (Cortical borders & trabeculae)"
        else:
            interp = "Macroscopic Boundary Mask (Thick structures, wide halos)"

        metrics_list.append({
            "Sigma_Pixels": s,
            "Equivalent_Window": f"{win_size}x{win_size}",
            "Cutoff_Freq_Cycles_Px": round(cutoff_freq, 4),
            "Mask_Std_Dev": round(mask_std, 2),
            "Mask_Dynamic_Range": round(mask_range, 2),
            "Sharpened_Mean_Grad": round(mg, 2),
            "Grad_Boost_Pct": round(boost, 2),
            "Bandwidth_Interpretation": interp
        })

    # Save CSV
    df_metrics = pd.DataFrame(metrics_list)
    csv_path = os.path.join(tab_dir, "exp07_task_7_2_bandwidth_metrics.csv")
    df_metrics.to_csv(csv_path, index=False)
    print(f"\n[INFO] Smoothing Kernel Blur & Bandwidth Metrics saved at: {csv_path}")
    print(df_metrics.to_string(index=False))

    # Visualization Figure (2x3)
    fig, axes = plt.subplots(2, 3, figsize=(16, 11), facecolor='white')
    plt.subplots_adjust(wspace=0.25, hspace=0.32)

    # Top Row: The 3 High-Frequency Masks (bipolar display)
    axes[0, 0].imshow(np.clip(masks[0.8] + 128.0, 0, 255).astype(np.uint8), cmap='gray')
    axes[0, 0].set_title(f"(a) High-Freq Mask ($\\sigma=0.8$, $5\\times 5$)\nMask Std: {metrics_list[0]['Mask_Std_Dev']} | Micro-Edges Only",
                          fontsize=10.5, fontweight='bold', color='#0284c7')
    axes[0, 0].axis('off')

    axes[0, 1].imshow(np.clip(masks[1.5] + 128.0, 0, 255).astype(np.uint8), cmap='gray')
    axes[0, 1].set_title(f"(b) High-Freq Mask ($\\sigma=1.5$, $7\\times 7$)\nMask Std: {metrics_list[1]['Mask_Std_Dev']} | Balanced Detail",
                          fontsize=10.5, fontweight='bold', color='#15803d')
    axes[0, 1].axis('off')

    axes[0, 2].imshow(np.clip(masks[3.0] + 128.0, 0, 255).astype(np.uint8), cmap='gray')
    axes[0, 2].set_title(f"(c) High-Freq Mask ($\\sigma=3.0$, $13\\times 13$)\nMask Std: {metrics_list[2]['Mask_Std_Dev']} | Broad Structures",
                          fontsize=10.5, fontweight='bold', color='#b45309')
    axes[0, 2].axis('off')

    # Bottom Row: Reconstructed Sharpened Outputs (k = 1.0)
    axes[1, 0].imshow(sharpened_images[0.8], cmap='gray')
    axes[1, 0].set_title(f"(d) Sharpened Image ($\\sigma=0.8$)\nBoost: {metrics_list[0]['Grad_Boost_Pct']:+.1f}% | Fine Trabeculae",
                          fontsize=10.5, fontweight='bold', color='#0284c7')
    axes[1, 0].axis('off')

    axes[1, 1].imshow(sharpened_images[1.5], cmap='gray')
    axes[1, 1].set_title(f"(e) Sharpened Image ($\\sigma=1.5$) [OPTIMUM]\nBoost: {metrics_list[1]['Grad_Boost_Pct']:+.1f}% | Clinical Standard",
                          fontsize=10.5, fontweight='bold', color='#15803d')
    axes[1, 1].axis('off')

    axes[1, 2].imshow(sharpened_images[3.0], cmap='gray')
    axes[1, 2].set_title(f"(f) Sharpened Image ($\\sigma=3.0$)\nBoost: {metrics_list[2]['Grad_Boost_Pct']:+.1f}% | Thick Bone Halos",
                          fontsize=10.5, fontweight='bold', color='#b45309')
    axes[1, 2].axis('off')

    plt.suptitle("Experiment 07 - Task 7.2: Influence of Smoothing Kernel Blur Parameter on Mask Bandwidth",
                 fontsize=13, fontweight='bold', color='#0f172a', y=0.98)

    fig_path = os.path.join(fig_dir, "exp07_task_7_2_mask_bandwidth_py.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Figure saved at: {fig_path}")

    return metrics_list

if __name__ == "__main__":
    run_task_7_2()
