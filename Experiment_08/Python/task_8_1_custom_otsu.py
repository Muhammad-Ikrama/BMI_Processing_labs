"""
Experiment 08 - Task 8.1: Custom Otsu's Method Implementation from First Principles
Validates against OpenCV built-in Otsu, evaluates separability metric eta, and segments Head CT bone.
"""
import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def custom_otsu(img):
    """
    Computes optimal Otsu threshold T* and between-class variance curve
    from first principles using 256-bin normalized histogram.
    """
    # 1. 256-bin histogram and probabilities
    hist, _ = np.histogram(img.flatten(), bins=256, range=(0, 256))
    p = hist.astype(float) / float(img.size)

    # 2. Cumulative sums and means
    omega = np.cumsum(p)                  # omega_0(T)
    mu = np.cumsum(p * np.arange(256))    # cumulative mean
    mu_total = mu[-1]                     # overall mean

    # 3. Compute between-class variance sigma_B^2(T)
    # sigma_B^2(T) = [mu_total * omega_0(T) - mu(T)]^2 / [omega_0(T) * (1 - omega_0(T))]
    denom = omega * (1.0 - omega)
    # Avoid division by zero at boundary points
    valid = denom > 1e-12
    sigma_b2 = np.zeros(256, dtype=float)
    sigma_b2[valid] = ((mu_total * omega[valid] - mu[valid]) ** 2) / denom[valid]

    # Optimal threshold T* maximizes sigma_b2
    T_star = int(np.argmax(sigma_b2))
    max_sigma_b2 = sigma_b2[T_star]

    # Total variance sigma_total^2
    sigma_total2 = np.sum(((np.arange(256) - mu_total) ** 2) * p)

    # Otsu separability metric eta = sigma_B^2(T*) / sigma_total^2
    eta = max_sigma_b2 / sigma_total2 if sigma_total2 > 0 else 0.0

    return T_star, sigma_b2, eta, hist, p, sigma_total2

def run_task_8_1():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(base_dir, "Inputs", "images", "Head_CT.png")
    out_dir = os.path.join(base_dir, "Outputs", "Python")
    tab_dir = os.path.join(base_dir, "Tables")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(tab_dir, exist_ok=True)

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Head CT not found at {img_path}")
    if img.shape != (512, 512):
        img = cv2.resize(img, (512, 512))

    # 1. Custom First-Principles Otsu
    T_custom, sigma_b2, eta, hist, p, sigma_total2 = custom_otsu(img)

    # 2. Built-in OpenCV Otsu for verification
    t_cv2, mask_cv2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    T_cv2 = int(t_cv2)

    # Integer match assertion
    match_status = (T_custom == T_cv2)
    print("=" * 80)
    print("TASK 8.1: CUSTOM OTSU THRESHOLDING FROM FIRST PRINCIPLES (HEAD CT)")
    print("=" * 80)
    print(f"Custom First-Principles Optimal Threshold T* : {T_custom}")
    print(f"OpenCV Built-in cv2.THRESH_OTSU Cutoff       : {T_cv2}")
    print(f"Exact Integer Concordance Verified            : {match_status}")
    print(f"Maximum Between-Class Variance sigma_B^2(T*)  : {sigma_b2[T_custom]:.4f}")
    print(f"Total Histogram Variance sigma_Total^2        : {sigma_total2:.4f}")
    print(f"Otsu Separability Metric eta                  : {eta:.4f} ({eta*100:.2f}%)")
    print(f"Quality Check (eta >= 0.65 Target)            : {'EXCELLENT' if eta >= 0.65 else 'ACCEPTABLE'}")

    # Generate Binary Masks
    mask_custom = (img > T_custom).astype(np.uint8) * 255
    bone_pixels = np.sum(mask_custom > 0)
    bone_pct = (bone_pixels / img.size) * 100.0
    print(f"Segmented Calvarial Bone Area                 : {bone_pixels} px ({bone_pct:.2f}%)")

    # Save metrics table
    metrics = [{
        "Modality": "Head CT",
        "Image_Size": f"{img.shape[0]}x{img.shape[1]}",
        "Custom_T_star": T_custom,
        "OpenCV_T_star": T_cv2,
        "Exact_Match": match_status,
        "Between_Class_Var": round(sigma_b2[T_custom], 2),
        "Total_Var": round(sigma_total2, 2),
        "Separability_eta": round(eta, 4),
        "Bone_Area_Pct": round(bone_pct, 2)
    }]
    df = pd.DataFrame(metrics)
    csv_path = os.path.join(tab_dir, "exp08_task_8_1_otsu_metrics.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SAVED] Task 8.1 metrics to: {csv_path}")

    # Plot Visualizations
    fig = plt.figure(figsize=(15, 5))
    fig.patch.set_facecolor("#FFFFFF")

    # Subplot 1: Input Head CT
    ax1 = fig.add_subplot(1, 3, 1)
    ax1.imshow(img, cmap="gray")
    ax1.set_title("Input Head CT (512x512)", fontsize=11, fontweight="bold", pad=8)
    ax1.axis("off")

    # Subplot 2: Overlaid Histogram & Otsu Variance Curve
    ax2 = fig.add_subplot(1, 3, 2)
    bins = np.arange(256)
    ax2.bar(bins, hist / hist.max(), color="#2563EB", alpha=0.55, width=1.0, label="Normalized Intensity Histogram")
    ax2_twin = ax2.twinx()
    ax2_twin.plot(bins, sigma_b2, color="#DC2626", linewidth=2.2, label=r"Between-Class Variance $\sigma_B^2(T)$")
    ax2_twin.axvline(T_custom, color="#16A34A", linestyle="--", linewidth=2.0, label=f"Optimal $T^* = {T_custom}$ ($\eta={eta:.3f}$)")
    ax2.set_xlabel("Intensity Level $T$", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Normalized Pixel Count", fontsize=10, fontweight="bold", color="#1E3A8A")
    ax2_twin.set_ylabel(r"Variance $\sigma_B^2(T)$", fontsize=10, fontweight="bold", color="#991B1B")
    ax2.set_title(r"Histogram Overlaid with Otsu $\sigma_B^2(T)$", fontsize=11, fontweight="bold", pad=8)
    ax2.grid(True, linestyle=":", alpha=0.5)

    # Subplot 3: Segmented Calvarial Bone Mask
    ax3 = fig.add_subplot(1, 3, 3)
    ax3.imshow(mask_custom, cmap="gray")
    ax3.set_title(f"Segmented Bone Mask ($T^* = {T_custom}$)\nArea: {bone_pct:.2f}%", fontsize=11, fontweight="bold", pad=8)
    ax3.axis("off")

    plt.tight_layout()
    fig_path = os.path.join(out_dir, "exp08_task_8_1_custom_otsu.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Task 8.1 composite figure to: {fig_path}")

    return df

if __name__ == "__main__":
    run_task_8_1()
