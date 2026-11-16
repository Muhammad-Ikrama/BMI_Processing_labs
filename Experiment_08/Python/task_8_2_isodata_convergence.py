"""
Experiment 08 - Task 8.2: Iterative Isodata vs. Otsu's Global Method Convergence Analysis
Evaluates convergence dynamics on Brain MRI and Chest X-ray across multiple starting guesses.
"""
import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_isodata(img, T0, tol=0.05, max_iter=50):
    """
    Executes Iterative Isodata algorithm, recording trajectory of threshold values.
    """
    T = float(T0)
    trajectory = [T]
    
    for i in range(1, max_iter + 1):
        bg = img[img <= T]
        fg = img[img > T]
        
        mu_bg = float(bg.mean()) if len(bg) > 0 else 0.0
        mu_fg = float(fg.mean()) if len(fg) > 0 else 255.0
        
        T_next = 0.5 * (mu_bg + mu_fg)
        trajectory.append(T_next)
        
        if abs(T_next - T) < tol:
            return T_next, i, trajectory
        T = T_next
        
    return T, max_iter, trajectory

def run_task_8_2():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_dir = os.path.join(base_dir, "Inputs", "images")
    out_dir = os.path.join(base_dir, "Outputs", "Python")
    tab_dir = os.path.join(base_dir, "Tables")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(tab_dir, exist_ok=True)

    modalities = [
        ("Brain MRI", os.path.join(img_dir, "Brain_MRI.png")),
        ("Chest X-ray", os.path.join(img_dir, "Chest_Xray.png"))
    ]

    t0_guesses = [20, 128, 230]
    records = []
    trajectories = {}

    print("=" * 80)
    print("TASK 8.2: ITERATIVE ISODATA VS. OTSU CONVERGENCE BENCHMARK")
    print("=" * 80)

    for mod_name, path in modalities:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(f"Image not found at {path}")
        if img.shape != (512, 512):
            img = cv2.resize(img, (512, 512))

        # Otsu reference
        t_otsu, mask_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        t_otsu = float(t_otsu)

        print(f"\n--- Modality: {mod_name} (Otsu Reference T* = {t_otsu:.1f}) ---")
        print(f"{'Initial T0':<12} | {'Final T_iso':<12} | {'Iterations':<11} | {'Diff vs Otsu':<13} | {'Dice (DSC)':<10}")
        print("-" * 65)

        for T0 in t0_guesses:
            T_final, iters, traj = run_isodata(img, T0)
            trajectories[(mod_name, T0)] = traj
            
            # Mask comparison
            mask_iso = (img > T_final).astype(np.uint8) * 255
            inter = np.logical_and(mask_iso > 0, mask_otsu > 0).sum()
            denom = (mask_iso > 0).sum() + (mask_otsu > 0).sum()
            dsc = (2.0 * inter / denom) if denom > 0 else 1.0
            diff = abs(T_final - t_otsu)

            records.append({
                "Modality": mod_name,
                "T0_Guess": T0,
                "Final_T_iso": round(T_final, 2),
                "Otsu_T_star": round(t_otsu, 2),
                "Iterations": iters,
                "Delta_T": round(diff, 2),
                "Dice_vs_Otsu": round(dsc, 4)
            })

            print(f"{T0:<12} | {T_final:<12.2f} | {iters:<11} | {diff:<13.2f} | {dsc:<10.4f}")

    df = pd.DataFrame(records)
    csv_path = os.path.join(tab_dir, "exp08_task_8_2_isodata_convergence.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[SAVED] Task 8.2 metrics to: {csv_path}")

    # Plot Convergence Trajectories & Visual Results
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.patch.set_facecolor("#FFFFFF")

    colors = {20: "#2563EB", 128: "#16A34A", 230: "#DC2626"}

    # Row 1: Brain MRI Trajectory, Input Image, Segmentation Mask
    ax_t1 = axes[0, 0]
    for T0 in t0_guesses:
        traj = trajectories[("Brain MRI", T0)]
        ax_t1.plot(range(len(traj)), traj, marker="o", markersize=4, label=f"T0 = {T0} (Converged in {len(traj)-1} iters)", color=colors[T0])
    otsu_val_mri = df[df["Modality"] == "Brain MRI"]["Otsu_T_star"].iloc[0]
    ax_t1.axhline(otsu_val_mri, color="#000000", linestyle="--", linewidth=1.8, label=f"Otsu T* = {otsu_val_mri:.1f}")
    ax_t1.set_title("Brain MRI: Isodata Convergence Dynamics", fontsize=11, fontweight="bold", pad=8)
    ax_t1.set_xlabel("Iteration Step $k$", fontsize=10, fontweight="bold")
    ax_t1.set_ylabel("Threshold Value $T_k$", fontsize=10, fontweight="bold")
    ax_t1.legend(fontsize=8.5, loc="best")
    ax_t1.grid(True, linestyle=":", alpha=0.6)

    mri_img = cv2.imread(modalities[0][1], cv2.IMREAD_GRAYSCALE)
    if mri_img.shape != (512, 512): mri_img = cv2.resize(mri_img, (512, 512))
    axes[0, 1].imshow(mri_img, cmap="gray")
    axes[0, 1].set_title("Brain MRI (Input)", fontsize=11, fontweight="bold", pad=8)
    axes[0, 1].axis("off")

    final_t_mri = df[df["Modality"] == "Brain MRI"]["Final_T_iso"].iloc[0]
    axes[0, 2].imshow(mri_img > final_t_mri, cmap="gray")
    axes[0, 2].set_title(f"Brain MRI Isodata Mask (T={final_t_mri:.1f})", fontsize=11, fontweight="bold", pad=8)
    axes[0, 2].axis("off")

    # Row 2: Chest X-ray Trajectory, Input Image, Segmentation Mask
    ax_t2 = axes[1, 0]
    for T0 in t0_guesses:
        traj = trajectories[("Chest X-ray", T0)]
        ax_t2.plot(range(len(traj)), traj, marker="s", markersize=4, label=f"T0 = {T0} (Converged in {len(traj)-1} iters)", color=colors[T0])
    otsu_val_xray = df[df["Modality"] == "Chest X-ray"]["Otsu_T_star"].iloc[0]
    ax_t2.axhline(otsu_val_xray, color="#000000", linestyle="--", linewidth=1.8, label=f"Otsu T* = {otsu_val_xray:.1f}")
    ax_t2.set_title("Chest X-ray: Isodata Convergence Dynamics", fontsize=11, fontweight="bold", pad=8)
    ax_t2.set_xlabel("Iteration Step $k$", fontsize=10, fontweight="bold")
    ax_t2.set_ylabel("Threshold Value $T_k$", fontsize=10, fontweight="bold")
    ax_t2.legend(fontsize=8.5, loc="best")
    ax_t2.grid(True, linestyle=":", alpha=0.6)

    xray_img = cv2.imread(modalities[1][1], cv2.IMREAD_GRAYSCALE)
    if xray_img.shape != (512, 512): xray_img = cv2.resize(xray_img, (512, 512))
    axes[1, 1].imshow(xray_img, cmap="gray")
    axes[1, 1].set_title("Chest X-ray (Input)", fontsize=11, fontweight="bold", pad=8)
    axes[1, 1].axis("off")

    final_t_xray = df[df["Modality"] == "Chest X-ray"]["Final_T_iso"].iloc[0]
    axes[1, 2].imshow(xray_img > final_t_xray, cmap="gray")
    axes[1, 2].set_title(f"Chest X-ray Isodata Mask (T={final_t_xray:.1f})", fontsize=11, fontweight="bold", pad=8)
    axes[1, 2].axis("off")

    plt.tight_layout()
    fig_path = os.path.join(out_dir, "exp08_task_8_2_isodata_convergence.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Task 8.2 figure to: {fig_path}")

    return df

if __name__ == "__main__":
    run_task_8_2()
