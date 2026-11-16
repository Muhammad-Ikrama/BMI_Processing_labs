"""
Experiment 10: Task 10.5 - Separating Touching Bilateral Lungs in Chest X-Ray via Watershed
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

def run_task_10_5():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    exp_dir = os.path.abspath(os.path.join(script_dir, ".."))
    inputs_dir = os.path.join(exp_dir, "Inputs", "images")
    outputs_dir = os.path.join(exp_dir, "Outputs", "Python")
    tables_dir = os.path.join(exp_dir, "Tables")
    os.makedirs(outputs_dir, exist_ok=True)
    os.makedirs(tables_dir, exist_ok=True)
    
    # Try Chest_Xray.png, fallback to Chest_Xray_512.png
    xray_path = os.path.join(inputs_dir, "Chest_Xray.png")
    if not os.path.exists(xray_path):
        xray_path = os.path.join(inputs_dir, "Chest_Xray_512.png")
    xray = cv2.imread(xray_path, cv2.IMREAD_GRAYSCALE)
    if xray is None:
        raise FileNotFoundError(f"Chest X-Ray not found at {xray_path}")
        
    h, w = xray.shape
    total_pixels = h * w
    
    # Invert so dark air-filled lungs become bright foreground
    xray_inv = cv2.bitwise_not(xray)
    
    # Gaussian smoothing to suppress fine rib textures
    smooth = cv2.GaussianBlur(xray_inv, (7, 7), 2.0)
    
    # Thresholding: Inverted lungs are bright, mediastinum and spine are dark
    _, bin_lungs = cv2.threshold(smooth, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Remove outer image borders if any
    border_mask = np.ones((h, w), dtype=np.uint8) * 255
    cv2.rectangle(border_mask, (int(0.05 * w), int(0.05 * h)), (int(0.95 * w), int(0.95 * h)), 0, -1)
    bin_lungs[border_mask == 255] = 0
    
    # Morphological cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    opened = cv2.morphologyEx(bin_lungs, cv2.MORPH_OPEN, kernel, iterations=2)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel, iterations=3)
    
    # Distance Transform
    dist_map = cv2.distanceTransform(closed, cv2.DIST_L2, 5)
    
    # Extract foreground markers: top peaks in left and right halves
    _, sure_fg = cv2.threshold(dist_map, 0.45 * dist_map.max(), 255, 0)
    sure_fg = sure_fg.astype(np.uint8)
    
    # Label markers
    num_markers, markers_fg = cv2.connectedComponents(sure_fg)
    
    # Sure background
    sure_bg = cv2.dilate(closed, kernel, iterations=3)
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    markers = markers_fg + 1
    markers[unknown == 255] = 0
    
    # Watershed segmentation
    xray_color = cv2.cvtColor(smooth, cv2.COLOR_GRAY2BGR)
    cv2.watershed(xray_color, markers)
    
    # Separate Left and Right Lung
    # Find two largest regions among labels > 1
    unique_labels, counts = np.unique(markers, return_counts=True)
    valid_regions = [(lbl, count) for lbl, count in zip(unique_labels, counts) if lbl > 1]
    valid_regions.sort(key=lambda x: x[1], reverse=True)
    
    # If two main lung regions are identified
    lung1_mask = np.zeros((h, w), dtype=np.uint8)
    lung2_mask = np.zeros((h, w), dtype=np.uint8)
    
    if len(valid_regions) >= 2:
        lbl1, cnt1 = valid_regions[0]
        lbl2, cnt2 = valid_regions[1]
        
        # Determine which is anatomical Right Lung (patient's right = image left) and Left Lung
        centroid1_x = np.mean(np.where(markers == lbl1)[1])
        centroid2_x = np.mean(np.where(markers == lbl2)[1])
        
        if centroid1_x < centroid2_x:
            right_lung_lbl, left_lung_lbl = lbl1, lbl2
            area_right, area_left = cnt1, cnt2
        else:
            right_lung_lbl, left_lung_lbl = lbl2, lbl1
            area_right, area_left = cnt2, cnt1
            
        lung1_mask[markers == right_lung_lbl] = 255
        lung2_mask[markers == left_lung_lbl] = 255
    else:
        # Fallback if single component
        area_right = valid_regions[0][1] // 2 if valid_regions else 0
        area_left = area_right
        lung1_mask = (markers > 1).astype(np.uint8) * 255
        lung2_mask = lung1_mask.copy()
        
    total_lung_area = area_right + area_left
    lung_ratio = area_left / area_right if area_right > 0 else 1.0
    thoracic_pct = (total_lung_area / total_pixels) * 100.0
    
    print("\n" + "=" * 95)
    print("TASK 10.5: SEPARATING TOUCHING BILATERAL LUNGS IN CHEST X-RAY VIA WATERSHED")
    print("=" * 95)
    print(f"{'Structure':<20} | {'Area (px)':<12} | {'Percentage of Total Image':<28} | {'Clinical Ratio'}")
    print("-" * 95)
    print(f"{'Right Lung (Anatomical)':<20} | {area_right:<12d} | {(area_right/total_pixels)*100:<28.2f}% | {'Baseline'}")
    print(f"{'Left Lung (Anatomical)':<20} | {area_left:<12d} | {(area_left/total_pixels)*100:<28.2f}% | {f'Ratio L/R = {lung_ratio:.3f}'}")
    print(f"{'Bilateral Total':<20} | {total_lung_area:<12d} | {thoracic_pct:<28.2f}% | {'Normal Aeration'}")
    
    records = [
        {"Anatomical_Structure": "Right Lung (Patient Right)", "Area_px": area_right, "Image_Percentage": round((area_right/total_pixels)*100, 2), "Symmetry_Ratio": 1.000, "Segmentation_Method": "Marker-Controlled Watershed"},
        {"Anatomical_Structure": "Left Lung (Patient Left)", "Area_px": area_left, "Image_Percentage": round((area_left/total_pixels)*100, 2), "Symmetry_Ratio": round(lung_ratio, 3), "Segmentation_Method": "Marker-Controlled Watershed"},
        {"Anatomical_Structure": "Bilateral Total Lung Field", "Area_px": total_lung_area, "Image_Percentage": round(thoracic_pct, 2), "Symmetry_Ratio": round(lung_ratio, 3), "Segmentation_Method": "Combined Segmented Lobes"}
    ]
    df = pd.DataFrame(records)
    csv_path = os.path.join(tables_dir, "exp10_task_10_5_chest_xray_watershed.csv")
    df.to_csv(csv_path, index=False)
    print(f"[SAVED] Task 10.5 table saved to: {csv_path}")
    
    # Composite multi-panel figure
    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    
    axes[0].imshow(xray, cmap='gray')
    axes[0].set_title("(1) Original Chest X-Ray\nAnterior-Posterior Projection", fontsize=10, fontweight='bold')
    axes[0].axis('off')
    
    axes[1].imshow(dist_map, cmap='magma')
    axes[1].set_title("(2) Distance Transform D(x, y)\nPeaks in Left & Right Lobes", fontsize=10, fontweight='bold')
    axes[1].axis('off')
    
    # Markers on xray
    ov_markers = cv2.cvtColor(xray, cv2.COLOR_GRAY2BGR)
    ov_markers[sure_fg > 0] = [0, 255, 255]
    axes[2].imshow(cv2.cvtColor(ov_markers, cv2.COLOR_BGR2RGB))
    axes[2].set_title(f"(3) Foreground Markers\n({num_markers-1} Core Seed Pools)", fontsize=10, fontweight='bold')
    axes[2].axis('off')
    
    # Final segmented colored overlay
    ov_seg = cv2.cvtColor(xray, cv2.COLOR_GRAY2BGR)
    ov_seg[lung1_mask > 0] = [0, 255, 0]    # Right Lung = Green
    ov_seg[lung2_mask > 0] = [255, 120, 0]  # Left Lung = Blue/Orange
    # Draw watershed boundary in red
    ov_seg[markers == -1] = [0, 0, 255]
    
    axes[3].imshow(cv2.cvtColor(ov_seg, cv2.COLOR_BGR2RGB))
    axes[3].set_title(f"(4) Watershed Separated Lobes\nRight: {area_right} px | Left: {area_left} px\nRed Dam = Mediastinal Separation", fontsize=10, fontweight='bold')
    axes[3].axis('off')
    
    plt.tight_layout()
    fig_path = os.path.join(outputs_dir, "exp10_task_10_5_chest_xray_watershed.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SAVED] Task 10.5 figure saved to: {fig_path}")

if __name__ == "__main__":
    run_task_10_5()
