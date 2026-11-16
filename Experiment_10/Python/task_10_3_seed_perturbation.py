"""
Experiment 10: Task 10.3 - Seed Point Placement Perturbation & Robustness Test
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

def run_task_10_3():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.abspath(os.path.join(script_dir, ".."))
    inputs_dir = os.path.join(exp_dir, "Inputs", "images")
    outputs_dir = os.path.join(exp_dir, "Outputs", "Python")
    tables_dir = os.path.join(exp_dir, "Tables")
    os.makedirs(outputs_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)
    
    mri = cv2.imread(os.path.join(inputs_dir, "Brain_MRI.png"), cv2.IMREAD_GRAYSCALE)
    mri_smooth = cv2.GaussianBlur(mri, (3, 3), 0.8)
    tol = 38
    
    # Ground truth
    gt_lesion = np.zeros_like(mri)
    gt_lesion[205:280, 290:365] = (mri_smooth[205:280, 290:365] > 162).astype(np.uint8) * 255
    gt_lesion = ndimage.binary_fill_holes(gt_lesion > 0).astype(np.uint8) * 255
    gt_area = int((gt_lesion > 0).sum())
    
    def srg(img, sy, sx, tol_val):
        h, w = img.shape
        visited = np.zeros((h, w), dtype=bool)
        mask = np.zeros((h, w), dtype=np.uint8)
        stack = [(sy, sx)]
        visited[sy, sx] = True
        seed_val = float(img[sy, sx])
        neighbors = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        while stack:
            cy, cx = stack.pop()
            if abs(float(img[cy, cx]) - seed_val) <= tol_val:
                mask[cy, cx] = 255
                for dy, dx in neighbors:
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                        visited[ny, nx] = True
                        stack.append((ny, nx))
        return mask

    seed_definitions = [
        {"Name": "Centroid", "x": 327, "y": 242, "Type": "Center Core"},
        {"Name": "Interior Point 1", "x": 320, "y": 238, "Type": "Interior Paracentral"},
        {"Name": "Interior Point 2", "x": 332, "y": 248, "Type": "Interior Paracentral"},
        {"Name": "Peripheral Rim 1", "x": 305, "y": 228, "Type": "Marginal Boundary Rim"},
        {"Name": "Peripheral Rim 2", "x": 345, "y": 255, "Type": "Marginal Boundary Rim"}
    ]
    
    records = []
    masks = {}
    
    print("\n" + "=" * 95)
    print("TASK 10.3: SEED POINT PLACEMENT PERTURBATION & ROBUSTNESS TEST")
    print("=" * 95)
    print(f"{'Seed Location':<18} | {'(X, Y)':<10} | {'I_seed':<8} | {'Area (px)':<10} | {'DSC':<8} | {'IoU':<8} | {'Clinical Status'}")
    print("-" * 95)
    
    for s in seed_definitions:
        sx, sy = s['x'], s['y']
        seed_int = float(mri_smooth[sy, sx])
        raw_m = srg(mri_smooth, sy, sx, tol)
        eval_m = ndimage.binary_fill_holes(raw_m > 0).astype(np.uint8) * 255
        masks[s['Name']] = eval_m
        
        g, p = (gt_lesion > 0), (eval_m > 0)
        intersection = np.logical_and(g, p).sum()
        union = np.logical_or(g, p).sum()
        dsc = 2.0 * intersection / (g.sum() + p.sum()) if (g.sum() + p.sum()) > 0 else 0
        iou = intersection / union if union > 0 else 0
        area = int(p.sum())
        
        if dsc >= 0.95:
            status = "Optimal Capture"
        elif dsc >= 0.85:
            status = "Robust Interior"
        else:
            status = "Rim Degradation / Under-grown"
            
        records.append({
            "Seed_Location": s['Name'],
            "Seed_Type": s['Type'],
            "Coord_X": sx,
            "Coord_Y": sy,
            "Seed_Intensity": round(seed_int, 1),
            "Area_px": area,
            "Ground_Truth_px": gt_area,
            "Area_Ratio": round(area / gt_area, 4) if gt_area > 0 else 0.0,
            "DSC": round(dsc, 4),
            "Jaccard_IoU": round(iou, 4),
            "Status": status
        })
        print(f"{s['Name']:<18} | {f'({sx}, {sy})':<10} | {seed_int:<8.1f} | {area:<10d} | {dsc:<8.4f} | {iou:<8.4f} | {status}")
        
    df = pd.DataFrame(records)
    csv_path = os.path.join(tables_dir, "exp10_task_10_3_seed_perturbation.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SAVED] Task 10.3 table saved to: {csv_path}")
    
    # Plotting 5 seeds on tumor
    fig = plt.figure(figsize=(16, 7))
    
    # Left: MRI zoom with all 5 seeds marked
    ax_map = fig.add_subplot(1, 3, 1)
    zy1, zy2, zx1, zx2 = 190, 290, 280, 380
    zoom_mri = cv2.cvtColor(mri[zy1:zy2, zx1:zx2], cv2.COLOR_GRAY2BGR)
    colors = [(0, 255, 0), (0, 255, 255), (255, 255, 0), (0, 140, 255), (0, 0, 255)]
    for idx, s in enumerate(seed_definitions):
        rel_x = s['x'] - zx1
        rel_y = s['y'] - zy1
        cv2.circle(zoom_mri, (rel_x, rel_y), 3, colors[idx], -1)
        cv2.putText(zoom_mri, f"S{idx+1}", (rel_x + 4, rel_y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
    ax_map.imshow(cv2.cvtColor(zoom_mri, cv2.COLOR_BGR2RGB))
    ax_map.set_title("5 Tested Seed Coordinates\nInside & on Tumor Rim", fontsize=11, fontweight='bold')
    ax_map.axis('off')
    
    # Middle: Centroid (S1) vs Marginal Rim (S4)
    ax_mid = fig.add_subplot(1, 3, 2)
    s1_mask = masks["Centroid"][zy1:zy2, zx1:zx2]
    s4_mask = masks["Peripheral Rim 1"][zy1:zy2, zx1:zx2]
    comp_img = np.zeros((zy2 - zy1, zx2 - zx1, 3), dtype=np.uint8)
    comp_img[s1_mask > 0] = [0, 255, 0]      # Centroid = Green
    comp_img[s4_mask > 0] = [255, 120, 0]    # S4 = Orange
    ax_mid.imshow(comp_img)
    ax_mid.set_title("Centroid (Green) vs. Rim Seed S4 (Orange)\nRim Seed misses bright core!", fontsize=11, fontweight='bold')
    ax_mid.axis('off')
    
    # Right: Bar chart of DSC across seeds
    ax_bar = fig.add_subplot(1, 3, 3)
    bars = ax_bar.bar([f"S{i+1}: {s['Name']}" for i, s in enumerate(seed_definitions)], df['DSC'], color=['#2ca02c', '#1f77b4', '#17becf', '#ff7f0e', '#d62728'])
    ax_bar.axhline(0.90, color='red', linestyle='--', label='Clinical Goal (DSC >= 0.90)')
    ax_bar.set_ylabel("Dice Similarity Coefficient (DSC)", fontsize=10, fontweight='bold')
    ax_bar.set_title("Segmentation Fidelity vs. Seed Location", fontsize=11, fontweight='bold')
    ax_bar.set_ylim(0, 1.05)
    plt.xticks(rotation=25, ha='right', fontsize=9)
    ax_bar.legend(loc='lower left', fontsize=9)
    ax_bar.grid(True, linestyle=':', alpha=0.6)
    
    for bar in bars:
        h = bar.get_height()
        ax_bar.annotate(f"{h:.3f}", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 3),
                        textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')
                        
    plt.tight_layout()
    fig_path = os.path.join(outputs_dir, "exp10_task_10_3_seed_perturbation.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SAVED] Task 10.3 figure saved to: {fig_path}")

if __name__ == "__main__":
    run_task_10_3()
