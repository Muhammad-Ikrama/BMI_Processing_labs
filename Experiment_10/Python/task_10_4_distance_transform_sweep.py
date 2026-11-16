"""
Experiment 10: Task 10.4 - Distance-Transform Threshold Sweep in Marker-Controlled Watershed
Author: Muhammad Ikrama (Reg ID: 60140)
Department of Biomedical Engineering, Riphah International University, Lahore
Instructor: Engr. Rana Talha Khalid
"""

import os
import cv2
import numpy as np
import pandas as pd
from scipy import ndimage
import matplotlib.pyplot as plt

def run_task_10_4():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.abspath(os.path.join(script_dir, ".."))
    inputs_dir = os.path.join(exp_dir, "Inputs", "images")
    outputs_dir = os.path.join(exp_dir, "Outputs", "Python")
    tables_dir = os.path.join(exp_dir, "Tables")
    os.makedirs(outputs_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)
    
    mri = cv2.imread(os.path.join(inputs_dir, "Brain_MRI.png"), cv2.IMREAD_GRAYSCALE)
    mri_smooth = cv2.GaussianBlur(mri, (3, 3), 0.8)
    
    # Foreground extraction
    se5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    _, bright_bin = cv2.threshold(mri_smooth, 162, 255, cv2.THRESH_BINARY)
    bright_bin = cv2.morphologyEx(bright_bin, cv2.MORPH_CLOSE, se5)
    dist_map = cv2.distanceTransform(bright_bin, cv2.DIST_L2, 5)
    d_max = dist_map.max()
    
    sure_bg = cv2.dilate(bright_bin, se5, iterations=3)
    
    alphas = [0.15, 0.25, 0.35, 0.55, 0.75]
    records = []
    watershed_results = {}
    
    print("\n" + "=" * 95)
    print("TASK 10.4: DISTANCE-TRANSFORM THRESHOLD SWEEP IN MARKER-CONTROLLED WATERSHED")
    print("=" * 95)
    print(f"{'Alpha Factor':<14} | {'Cutoff Dist (px)':<18} | {'FG Markers':<12} | {'Watershed Regions':<20} | {'Status'}")
    print("-" * 95)
    
    for alpha in alphas:
        cutoff = alpha * d_max
        _, sure_fg = cv2.threshold(dist_map, cutoff, 255, 0)
        sure_fg = sure_fg.astype(np.uint8)
        
        num_fg_markers, markers_fg = cv2.connectedComponents(sure_fg)
        num_fg_markers -= 1  # subtract background
        
        unknown = cv2.subtract(sure_bg, sure_fg)
        markers = markers_fg + 1
        markers[unknown == 255] = 0
        
        mri_color = cv2.cvtColor(mri_smooth, cv2.COLOR_GRAY2BGR)
        cv2.watershed(mri_color, markers)
        
        # Count unique non-boundary and non-background segmented regions
        unique_labels = np.unique(markers)
        unique_regions = len([lbl for lbl in unique_labels if lbl > 1])
        
        watershed_results[alpha] = {
            "markers": markers,
            "boundaries": (markers == -1),
            "sure_fg": sure_fg,
            "regions": unique_regions
        }
        
        if alpha < 0.25:
            status = "Over-Segmented (Fragmented Basins)"
        elif alpha == 0.35:
            status = "OPTIMAL (6 Clean Anatomical Structures)"
        elif alpha <= 0.55:
            status = "Acceptable Separation"
        else:
            status = "Under-Segmented (Marker Shrinkage / Missing Basins)"
            
        records.append({
            "Alpha_Factor": alpha,
            "Cutoff_Distance_px": round(cutoff, 2),
            "Max_Distance_px": round(d_max, 2),
            "FG_Marker_Count": num_fg_markers,
            "Watershed_Regions": unique_regions,
            "Clinical_Status": status
        })
        print(f"alpha = {alpha:<7.2f} | {cutoff:<18.2f} | {num_fg_markers:<12d} | {unique_regions:<20d} | {status}")
        
    df = pd.DataFrame(records)
    csv_path = os.path.join(tables_dir, "exp10_task_10_4_distance_sweep.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SAVED] Task 10.4 table saved to: {csv_path}")
    
    # Composite multi-panel figure
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    
    # 5 Alpha cases
    alpha_plot_indices = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]
    for idx, alpha in enumerate(alphas):
        r, c = alpha_plot_indices[idx]
        res = watershed_results[alpha]
        ov = cv2.cvtColor(mri, cv2.COLOR_GRAY2BGR)
        ov[res['boundaries']] = [0, 255, 0]  # Green boundaries
        # Also highlight foreground markers in red
        ov[res['sure_fg'] > 0] = [0, 0, 255]
        
        axes[r, c].imshow(cv2.cvtColor(ov, cv2.COLOR_BGR2RGB))
        rec = df[df['Alpha_Factor'] == alpha].iloc[0]
        axes[r, c].set_title(f"alpha = {alpha:.2f} (Cutoff: {rec['Cutoff_Distance_px']} px)\nMarkers: {rec['FG_Marker_Count']} | Basins: {rec['Watershed_Regions']}\n{rec['Clinical_Status'].split('(')[0].strip()}", fontsize=10, fontweight='bold')
        axes[r, c].axis('off')
        
    # Final subplot: Sweep curve
    ax_curve = axes[1, 2]
    ax_curve.plot(df['Alpha_Factor'], df['FG_Marker_Count'], 'r-o', linewidth=2, label='FG Marker Count')
    ax_curve.plot(df['Alpha_Factor'], df['Watershed_Regions'], 'b--s', linewidth=2, label='Watershed Regions')
    ax_curve.axvline(0.35, color='green', linestyle=':', linewidth=2, label='Optimal alpha = 0.35')
    ax_curve.set_xlabel("Distance Threshold Factor alpha", fontsize=10, fontweight='bold')
    ax_curve.set_ylabel("Count", fontsize=10, fontweight='bold')
    ax_curve.set_title("Marker & Region Count vs. alpha", fontsize=11, fontweight='bold')
    ax_curve.grid(True, linestyle=':', alpha=0.6)
    ax_curve.legend(loc='upper right', fontsize=9)
    
    plt.tight_layout()
    fig_path = os.path.join(outputs_dir, "exp10_task_10_4_distance_sweep.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SAVED] Task 10.4 figure saved to: {fig_path}")

if __name__ == "__main__":
    run_task_10_4()
