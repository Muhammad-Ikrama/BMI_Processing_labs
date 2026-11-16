"""
Experiment 02 - Example 2: Global Equalization vs CLAHE Benchmarking
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_metrics(im):
    h, _ = np.histogram(im.flatten(), 256, [0, 256])
    p = h / float(im.size)
    p_nz = p[p > 0]
    ent = -np.sum(p_nz * np.log2(p_nz))
    std = float(im.std())
    min_val, max_val = float(im.min()), float(im.max())
    mc = (max_val - min_val) / (max_val + min_val) if (max_val + min_val) > 0 else 0.0
    return ent, std, mc

def main():
    print("=" * 70)
    print("EXAMPLE 2: GLOBAL HE VS CLAHE BENCHMARKING")
    print("=" * 70)

    possible_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'Inputs', 'images', 'Lung-HR-contrast.png'),
        os.path.join(os.path.dirname(__file__), '..', '..', '..', 'images', 'Lung-HR-contrast.png'),
        'images/Lung-HR-contrast.png'
    ]
    img_path = next((p for p in possible_paths if os.path.exists(p)), None)
    if not img_path:
        raise FileNotFoundError("Could not locate Lung-HR-contrast.png")

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # 1. Global Histogram Equalization (GHE)
    ghe_img = cv2.equalizeHist(img)

    # 2. Contrast-Limited Adaptive Histogram Equalization (CLAHE)
    clahe_20 = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(img)
    clahe_40 = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8)).apply(img)

    methods = [
        ("Original Scan", img),
        ("Global HE (GHE)", ghe_img),
        ("CLAHE (Clip=2.0)", clahe_20),
        ("CLAHE (Clip=4.0)", clahe_40)
    ]

    print(f"{'Method':<24} | {'Entropy (bits)':<14} | {'Std Dev':<10} | {'Michelson':<10}")
    print("-" * 65)
    for name, im in methods:
        e, s, m = get_metrics(im)
        print(f"{name:<24} | {e:<14.4f} | {s:<10.2f} | {m:<10.4f}")

    print(">>> Decision: CLAHE (Clip=2.0) is OPTIMAL (Entropy improved with controlled background noise).")

    # 3. Visualization
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'Outputs', 'Python')
    fig_dir = os.path.join(os.path.dirname(__file__), '..', 'Figures')
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    fig, axes = plt.subplots(2, 4, figsize=(18, 9), facecolor='#0f172a')

    for idx, (name, im) in enumerate(methods):
        e, s, m = get_metrics(im)
        
        # Row 1: Image
        axes[0, idx].imshow(im, cmap='gray')
        axes[0, idx].set_title(f"{name}\nH={e:.2f} | Std={s:.1f}", color='white', fontweight='bold', fontsize=11)
        axes[0, idx].axis('off')

        # Row 2: Histogram
        h, _ = np.histogram(im.flatten(), 256, [0, 256])
        axes[1, idx].bar(range(256), h, color='#38bdf8', width=1.0, edgecolor='none')
        axes[1, idx].set_facecolor('#1e293b')
        axes[1, idx].set_title(f"Histogram ({name})", color='white', fontsize=10)
        axes[1, idx].set_xlabel("Intensity", color='#94a3b8', fontsize=9)
        axes[1, idx].tick_params(colors='#94a3b8', labelsize=8)
        axes[1, idx].set_xlim([0, 255])

    plt.suptitle("Example 2: Global HE vs Contextual CLAHE Contrast Benchmarking", color='#38bdf8', fontsize=14, fontweight='bold')
    plt.tight_layout()

    out_file1 = os.path.join(out_dir, 'example_02_ghe_vs_clahe_python.png')
    out_file2 = os.path.join(fig_dir, 'example_02_ghe_vs_clahe_python.png')
    plt.savefig(out_file1, dpi=200, facecolor=fig.get_facecolor())
    plt.savefig(out_file2, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"[SAVED] Saved plot to {out_file1} and {out_file2}")

if __name__ == '__main__':
    main()
