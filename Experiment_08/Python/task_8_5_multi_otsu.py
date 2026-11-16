"""
Experiment 08 - Task 8.5: Multi-Otsu (Multi-Level) Tissue Classification on Brain MRI
Extends Otsu's variance maximization to multi-thresholding (T1*, T2*), partitioning Brain MRI
into 3 anatomical classes: Background/Air, Parenchyma, and Hyperintense CSF/Ventricles.
"""
import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.filters import threshold_multiotsu

def custom_multi_otsu_2thresh(img):
    """
    Computes two optimal thresholds (T1*, T2*) from first principles
    maximizing 3-class between-class variance sigma_B^2(T1, T2).
    """
    hist, _ = np.histogram(img.flatten(), bins=256, range=(0, 256))
    p = hist.astype(float) / float(img.size)
    bins = np.arange(256)

    omega = np.cumsum(p)
    mu = np.cumsum(p * bins)
    mu_total = mu[-1]

    max_sigma = -1.0
    best_t = (0, 0)

    # 2D search with coarse-to-fine or vectorized evaluation
    # To ensure high efficiency, evaluate on candidate thresholds with valid weights
    for t1 in range(1, 254):
        w0 = omega[t1]
        if w0 < 1e-6:
            continue
        m0 = mu[t1] / w0
        for t2 in range(t1 + 1, 255):
            w1 = omega[t2] - w0
            w2 = 1.0 - omega[t2]
            if w1 < 1e-6 or w2 < 1e-6:
                continue
            m1 = (mu[t2] - mu[t1]) / w1
            m2 = (mu_total - mu[t2]) / w2

            sigma_b2 = w0 * ((m0 - mu_total) ** 2) + w1 * ((m1 - mu_total) ** 2) + w2 * ((m2 - mu_total) ** 2)
            if sigma_b2 > max_sigma:
                max_sigma = sigma_b2
                best_t = (t1, t2)

    sigma_total2 = np.sum(((bins - mu_total) ** 2) * p)
    eta = max_sigma / sigma_total2 if sigma_total2 > 0 else 0.0

    return best_t, max_sigma, eta, hist, p

def run_task_8_5():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(base_dir, "Inputs", "images", "Brain_MRI.png")
    out_dir = os.path.join(base_dir, "Outputs", "Python")
    tab_dir = os.path.join(base_dir, "Tables")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(tab_dir, exist_ok=True)

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Brain MRI not found at {img_path}")
    if img.shape != (512, 512):
        img = cv2.resize(img, (512, 512))

    # 1. Custom First-Principles Multi-Otsu
    (t1_custom, t2_custom), sigma_b2, eta, hist, p = custom_multi_otsu_2thresh(img)

    # 2. Scikit-Image Multi-Otsu verification
    thresholds_sk = threshold_multiotsu(img, classes=3)
    t1_sk, t2_sk = int(round(thresholds_sk[0])), int(round(thresholds_sk[1]))

    print("=" * 80)
    print("TASK 8.5: MULTI-OTSU (3-CLASS) TISSUE CLASSIFICATION ON BRAIN MRI")
    print("=" * 80)
    print(f"Custom Multi-Otsu Thresholds (T1*, T2*)     : ({t1_custom}, {t2_custom})")
    print(f"Scikit-Image Multi-Otsu Thresholds          : ({t1_sk}, {t2_sk})")
    print(f"Threshold Concordance Verified              : {abs(t1_custom - t1_sk) <= 1 and abs(t2_custom - t2_sk) <= 1}")
    print(f"Maximum 3-Class Variance sigma_B^2(T1*, T2*): {sigma_b2:.4f}")
    print(f"Multi-Level Separability Metric eta         : {eta:.4f} ({eta*100:.2f}%)")

    # 3. Form 3-Class Segmentation Mask
    # Class 0: Background Air (f <= T1)
    # Class 1: Brain Parenchyma (T1 < f <= T2)
    # Class 2: Hyperintense Ventricles & CSF (f > T2)
    label_map = np.zeros_like(img, dtype=np.uint8)
    label_map[(img > t1_custom) & (img <= t2_custom)] = 1
    label_map[img > t2_custom] = 2

    n_total = float(img.size)
    c0_count = np.sum(label_map == 0)
    c1_count = np.sum(label_map == 1)
    c2_count = np.sum(label_map == 2)

    pct0 = (c0_count / n_total) * 100.0
    pct1 = (c1_count / n_total) * 100.0
    pct2 = (c2_count / n_total) * 100.0

    print("\n--- Anatomical Tissue Class Distribution ---")
    print(f"Class 0 (Background Air, f <= {t1_custom})     : {c0_count} px ({pct0:.2f}%)")
    print(f"Class 1 (Brain Parenchyma, {t1_custom} < f <= {t2_custom}): {c1_count} px ({pct1:.2f}%)")
    print(f"Class 2 (Ventricles / CSF, f > {t2_custom})     : {c2_count} px ({pct2:.2f}%)")

    records = [
        {"Class_ID": 0, "Tissue_Name": "Background Air", "Intensity_Range": f"0 to {t1_custom}", "Pixel_Count": c0_count, "Area_Pct": round(pct0, 2)},
        {"Class_ID": 1, "Tissue_Name": "Brain Parenchyma", "Intensity_Range": f"{t1_custom+1} to {t2_custom}", "Pixel_Count": c1_count, "Area_Pct": round(pct1, 2)},
        {"Class_ID": 2, "Tissue_Name": "Ventricles & CSF", "Intensity_Range": f">{t2_custom}", "Pixel_Count": c2_count, "Area_Pct": round(pct2, 2)}
    ]
    df = pd.DataFrame(records)
    csv_path = os.path.join(tab_dir, "exp08_task_8_5_multi_otsu.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[SAVED] Task 8.5 metrics to: {csv_path}")

    # Plot Visualizations
    fig = plt.figure(figsize=(16, 5))
    fig.patch.set_facecolor("#FFFFFF")

    # Panel 1: Original Brain MRI
    ax1 = fig.add_subplot(1, 3, 1)
    ax1.imshow(img, cmap="gray")
    ax1.set_title("Input Brain MRI (512x512)", fontsize=11, fontweight="bold", pad=8)
    ax1.axis("off")

    # Panel 2: Histogram with Dual Otsu Cutoffs
    ax2 = fig.add_subplot(1, 3, 2)
    bins = np.arange(256)
    ax2.bar(bins[:t1_custom+1], hist[:t1_custom+1], color="#475569", alpha=0.8, label="Class 0: Air")
    ax2.bar(bins[t1_custom+1:t2_custom+1], hist[t1_custom+1:t2_custom+1], color="#0284C7", alpha=0.8, label="Class 1: Parenchyma")
    ax2.bar(bins[t2_custom+1:], hist[t2_custom+1:], color="#F59E0B", alpha=0.8, label="Class 2: Ventricles/CSF")
    ax2.axvline(t1_custom, color="#DC2626", linestyle="--", linewidth=2.0, label=f"$T_1^* = {t1_custom}$")
    ax2.axvline(t2_custom, color="#16A34A", linestyle="--", linewidth=2.0, label=f"$T_2^* = {t2_custom}$")
    ax2.set_xlabel("Pixel Intensity $T$", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Pixel Count", fontsize=10, fontweight="bold")
    ax2.set_title(f"Histogram with Dual Thresholds ($\eta = {eta:.3f}$)", fontsize=11, fontweight="bold", pad=8)
    ax2.legend(fontsize=8.5, loc="upper right")
    ax2.grid(True, linestyle=":", alpha=0.5)

    # Panel 3: Color-Coded 3-Class Label Map
    ax3 = fig.add_subplot(1, 3, 3)
    color_map = np.zeros((512, 512, 3), dtype=np.uint8)
    color_map[label_map == 0] = [15, 23, 42]     # Dark Navy
    color_map[label_map == 1] = [37, 99, 235]    # Royal Blue
    color_map[label_map == 2] = [234, 179, 8]    # Bright Gold
    ax3.imshow(color_map)
    ax3.set_title(f"3-Class Anatomical Segmentation Map\nAir: {pct0:.1f}%, Parenchyma: {pct1:.1f}%, CSF: {pct2:.1f}%", fontsize=11, fontweight="bold", pad=8)
    ax3.axis("off")

    plt.tight_layout()
    fig_path = os.path.join(out_dir, "exp08_task_8_5_multi_otsu.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Task 8.5 figure to: {fig_path}")

    return df

if __name__ == "__main__":
    run_task_8_5()
