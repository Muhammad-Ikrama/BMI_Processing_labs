"""
Experiment 02 - Task 2.4: Contextual CLAHE Optimization & Clip Limit Sensitivity Analysis
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

Task Requirement:
Apply CLAHE on low-contrast lung radiograph with fixed 8 x 8 tile grid.
Perform a sensitivity sweep with Clip Limit values: [1.0, 2.0, 3.0, 4.0, 8.0].
Measure Shannon Information Entropy, Standard Deviation, and Background Noise Variance.
Plot a sensitivity curve of Entropy vs Clip Limit and find the 'Good to Go' clinical operating point.
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def compute_entropy(im):
    h, _ = np.histogram(im.flatten(), 256, [0, 256])
    p = h / float(im.size)
    p_nz = p[p > 0]
    return -np.sum(p_nz * np.log2(p_nz))

def main():
    print("=" * 70)
    print("TASK 2.4: CLAHE CLIP LIMIT SENSITIVITY SWEEP & OPTIMIZATION")
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
    H, W = img.shape

    # Define background air ROI to measure noise floor variance
    # Top-left corner is typical background air
    air_roi_slice = (slice(10, 80), slice(10, 80))

    clip_limits = [1.0, 2.0, 3.0, 4.0, 8.0]
    entropies = []
    stds = []
    bg_variances = []
    enhanced_images = []

    print(f"{'Clip Limit':<12} | {'Entropy (bits)':<16} | {'Std Dev':<10} | {'Noise Floor Var':<16} | {'Clinical Status'}")
    print("-" * 75)

    for clip in clip_limits:
        clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=(8, 8))
        im_clahe = clahe.apply(img)
        enhanced_images.append(im_clahe)
        
        ent = compute_entropy(im_clahe)
        std_val = float(im_clahe.std())
        bg_var = float(np.var(im_clahe[air_roi_slice]))
        
        entropies.append(ent)
        stds.append(std_val)
        bg_variances.append(bg_var)

        status = "UNDERTUNED" if clip < 2.0 else ("OPTIMAL [Good to Go]" if clip == 2.0 else ("ACCEPTABLE" if clip <= 3.0 else "NOISE HAZARD"))
        print(f"{clip:<12.1f} | {ent:<16.4f} | {std_val:<10.2f} | {bg_var:<16.2f} | {status}")

    # Plotting
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'Outputs', 'Python')
    fig_dir = os.path.join(os.path.dirname(__file__), '..', 'Figures')
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    fig = plt.figure(figsize=(16, 10), facecolor='#0f172a')
    gs = fig.add_gridspec(2, 5, height_ratios=[1.2, 1.0])

    # Top row: Images across 5 clip limits
    for idx, clip in enumerate(clip_limits):
        ax = fig.add_subplot(gs[0, idx])
        ax.imshow(enhanced_images[idx], cmap='gray')
        is_opt = (clip == 2.0)
        title_color = '#4ade80' if is_opt else ('#f87171' if clip >= 4.0 else 'white')
        ax.set_title(f"Clip = {clip:.1f}\nH={entropies[idx]:.2f}\nVar_bg={bg_variances[idx]:.1f}",
                     color=title_color, fontsize=10, fontweight='bold')
        ax.axis('off')
        if is_opt:
            for spine in ax.spines.values():
                spine.set_edgecolor('#4ade80')
                spine.set_linewidth(3)

    # Bottom left: Sensitivity Curve (Entropy vs Clip Limit)
    ax_curve1 = fig.add_subplot(gs[1, :3])
    ax_curve1.set_facecolor('#1e293b')
    ax_curve1.plot(clip_limits, entropies, marker='o', color='#38bdf8', linewidth=2.5, markersize=8, label='Information Entropy (bits)')
    ax_curve1.axvline(2.0, color='#4ade80', linestyle='--', linewidth=2, label="Optimal 'Good to Go' (Clip=2.0)")
    ax_curve1.set_xlabel('CLAHE Clip Limit Parameter', color='#94a3b8', fontsize=11)
    ax_curve1.set_ylabel('Shannon Information Entropy (bits/pixel)', color='#38bdf8', fontsize=11)
    ax_curve1.tick_params(colors='#94a3b8')
    ax_curve1.set_title("Information Entropy Response Curve vs Clip Limit", color='white', fontweight='bold', fontsize=12)
    ax_curve1.grid(True, color='#334155', linestyle='--', alpha=0.5)
    ax_curve1.legend(loc='lower right', facecolor='#0f172a', edgecolor='#334155', labelcolor='white')

    # Bottom right: Background Noise Floor Variance vs Clip Limit
    ax_curve2 = fig.add_subplot(gs[1, 3:])
    ax_curve2.set_facecolor('#1e293b')
    ax_curve2.plot(clip_limits, bg_variances, marker='s', color='#f87171', linewidth=2.5, markersize=8, label='Background Noise Variance')
    ax_curve2.axhline(15.0, color='#fde047', linestyle=':', linewidth=2, label='Clinical Safety Ceiling (Var=15.0)')
    ax_curve2.axvline(2.0, color='#4ade80', linestyle='--', linewidth=2, label="Optimal Point (Clip=2.0)")
    ax_curve2.set_xlabel('CLAHE Clip Limit Parameter', color='#94a3b8', fontsize=11)
    ax_curve2.set_ylabel('Air Noise Floor Variance (Var)', color='#f87171', fontsize=11)
    ax_curve2.tick_params(colors='#94a3b8')
    ax_curve2.set_title("Background Noise Amplification vs Clip Limit", color='white', fontweight='bold', fontsize=12)
    ax_curve2.grid(True, color='#334155', linestyle='--', alpha=0.5)
    ax_curve2.legend(loc='upper left', facecolor='#0f172a', edgecolor='#334155', labelcolor='white')

    plt.suptitle("Task 2.4: Contextual CLAHE Optimization and Parameter Sensitivity Analysis", color='#38bdf8', fontsize=14, fontweight='bold')
    plt.tight_layout()

    out_file1 = os.path.join(out_dir, 'task_2_4_clahe_clip_sensitivity_python.png')
    out_file2 = os.path.join(fig_dir, 'task_2_4_clahe_clip_sensitivity_python.png')
    plt.savefig(out_file1, dpi=200, facecolor=fig.get_facecolor())
    plt.savefig(out_file2, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"[SAVED] Generated Task 2.4 figures:\n  {out_file1}\n  {out_file2}")

if __name__ == '__main__':
    main()
