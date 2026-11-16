"""
Experiment 08 - Benchmark Tutorial Code
Global (Fixed, Isodata, Otsu) & Adaptive (Mean-C, Gaussian-C, Sauvola) Thresholding Benchmark
"""
import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_benchmark():
    # Resolve paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(base_dir, "Inputs", "images", "Brain_MRI.png")
    out_dir = os.path.join(base_dir, "Outputs", "Python")
    tab_dir = os.path.join(base_dir, "Tables")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(tab_dir, exist_ok=True)

    # 1. Load reference 512x512 Brain MRI
    mri = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if mri is None:
        raise FileNotFoundError(f"Cannot load image at {img_path}")
    if mri.shape != (512, 512):
        mri = cv2.resize(mri, (512, 512))

    # Simulate RF Coil Bias Field shading (as specified in Lab Manual Section 5)
    Y, X = np.ogrid[:512, :512]
    bias_field = 0.45 + 0.95 * ((X / 512.0) * 0.7 + (Y / 512.0) * 0.3)
    mri_biased = np.clip(mri.astype(float) * bias_field, 0, 255).astype(np.uint8)

    # Reference anatomical structure ground truth from unbiased MRI
    m_clean = cv2.GaussianBlur(mri.astype(float), (35, 35), 6.0)
    gt_mask = ((mri > (m_clean + 4)) & (mri > 25)).astype(np.uint8) * 255

    # 2. Global Thresholding: Fixed (T=115), Iterative Isodata, and Otsu's Method
    _, th_fixed = cv2.threshold(mri_biased, 115, 255, cv2.THRESH_BINARY)
    
    # Iterative Isodata
    T_iso = float(mri_biased.mean())
    for _ in range(30):
        bg_mean = mri_biased[mri_biased <= T_iso].mean() if (mri_biased <= T_iso).any() else 0.0
        fg_mean = mri_biased[mri_biased > T_iso].mean() if (mri_biased > T_iso).any() else 255.0
        T_new = 0.5 * (bg_mean + fg_mean)
        if abs(T_new - T_iso) < 0.05:
            T_iso = T_new
            break
        T_iso = T_new
    _, th_isodata = cv2.threshold(mri_biased, int(round(T_iso)), 255, cv2.THRESH_BINARY)

    # Otsu's Global Method
    t_otsu, th_otsu = cv2.threshold(mri_biased, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 3. Local Adaptive Thresholding: Mean-C, Gaussian-C, and Sauvola
    th_mean = cv2.adaptiveThreshold(mri_biased, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 35, -5)
    th_gauss = cv2.adaptiveThreshold(mri_biased, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)

    # Sauvola Local (k=0.20, R=128)
    m_loc = cv2.boxFilter(mri_biased.astype(float), -1, (35, 35))
    s_loc = np.sqrt(np.maximum(cv2.boxFilter(mri_biased.astype(float)**2, -1, (35, 35)) - m_loc**2, 0))
    T_sauv = m_loc * (1.0 + 0.20 * ((s_loc / 128.0) - 1.0))
    th_sauv = ((mri_biased > T_sauv) & (mri_biased > 25)).astype(np.uint8) * 255

    # 4. Quantitative Evaluation (Dice, IoU, FG Area %)
    def eval_mask(gt, pr):
        g, p = (gt > 0), (pr > 0)
        inter = np.logical_and(g, p).sum()
        denom = g.sum() + p.sum()
        dsc = (2.0 * inter / denom) if denom > 0 else 0.0
        union = np.logical_or(g, p).sum()
        iou = (inter / union) if union > 0 else 0.0
        fg_pct = (p.sum() / p.size) * 100.0
        return dsc, iou, fg_pct

    methods = [
        ("Fixed Global (T=115)", th_fixed, 115.0),
        (f"Isodata Global (T={int(round(T_iso))})", th_isodata, T_iso),
        (f"Otsu Global (T*={int(t_otsu)})", th_otsu, t_otsu),
        ("Adaptive Mean (35x35)", th_mean, m_loc.mean() + 5),
        ("Adaptive Gaussian (35x35)", th_gauss, m_loc.mean() + 5),
        ("Sauvola Local (k=0.20)", th_sauv, T_sauv.mean())
    ]

    records = []
    print("=" * 80)
    print("EXPERIMENT 08 - GLOBAL & ADAPTIVE THRESHOLDING BENCHMARK (PYTHON)")
    print("=" * 80)
    print(f"{'Thresholding Method':<28} | {'Cutoff T':<9} | {'Dice (DSC)':<10} | {'Jaccard IoU':<11} | {'FG Area %':<9}")
    print("-" * 80)

    for name, mask, tval in methods:
        dsc, iou, fg = eval_mask(gt_mask, mask)
        records.append({
            "Method": name,
            "Cutoff_T": round(tval, 1),
            "Dice_DSC": round(dsc, 4),
            "Jaccard_IoU": round(iou, 4),
            "FG_Area_Pct": round(fg, 2)
        })
        print(f"{name:<28} | {tval:<9.1f} | {dsc:<10.4f} | {iou:<11.4f} | {fg:<8.2f}%")

    df = pd.DataFrame(records)
    csv_path = os.path.join(tab_dir, "exp08_benchmark_summary_py.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[SAVED] Benchmark metrics saved to: {csv_path}")

    # Save benchmark visualization (Figure 8.2 clinical comparison)
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    fig.patch.set_facecolor("#FFFFFF")

    panels = [
        ("1. Original Brain MRI", mri, "gray"),
        ("2. Biased MRI (RF Inhomogeneity)", mri_biased, "gray"),
        (f"3. Fixed Global (T=115)\nDSC={records[0]['Dice_DSC']}", th_fixed, "gray"),
        (f"4. Otsu Global (T*={int(t_otsu)})\nDSC={records[2]['Dice_DSC']}", th_otsu, "gray"),
        (f"5. Isodata (T={int(round(T_iso))})\nDSC={records[1]['Dice_DSC']}", th_isodata, "gray"),
        (f"6. Adaptive Mean (35x35)\nDSC={records[3]['Dice_DSC']}", th_mean, "gray"),
        (f"7. Adaptive Gauss (35x35)\nDSC={records[4]['Dice_DSC']}", th_gauss, "gray"),
        (f"8. Ground Truth Mask\nAnatomical Target", gt_mask, "gray")
    ]

    for ax, (title, img, cmap) in zip(axes.flatten(), panels):
        ax.imshow(img, cmap=cmap)
        ax.set_title(title, fontsize=10, fontweight="bold", pad=5)
        ax.axis("off")

    plt.tight_layout()
    bench_fig_path = os.path.join(out_dir, "exp08_benchmark_clinical_comparison.png")
    plt.savefig(bench_fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Clinical comparison figure: {bench_fig_path}")

    return df

if __name__ == "__main__":
    run_benchmark()
