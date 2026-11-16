"""
Experiment 01 - Task 4: Calibrated Real-World Organ Measurement from Pixel Spacing
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

Task Requirement:
Using extracted DICOM PixelSpacing metadata [Sy, Sx] (in mm/pixel) from 'DICOM/IM-0001-0002.dcm'
or 'images/sample_brain_ct.dcm', write a function that takes two user-selected pixel coordinates
(x1, y1) and (x2, y2) across an anatomical structure or suspected lesion.
Calculate both the uncalibrated distance in pixels and the calibrated physical distance in absolute millimeters (mm).
Plot the DICOM image and draw the measurement caliper line with text annotations.
"""

import os
import math
import pydicom
import numpy as np
import matplotlib.pyplot as plt

def compute_calibrated_distance(dicom_path, p1, p2):
    """
    Compute pixel and metric millimeter distance between two coordinates in a DICOM scan.
    p1: (x1, y1) [Col, Row]
    p2: (x2, y2) [Col, Row]
    """
    if not os.path.exists(dicom_path):
        raise FileNotFoundError(f"DICOM file not found at: {dicom_path}")
    
    dcm = pydicom.dcmread(dicom_path)
    
    # Extract PixelSpacing [RowSpacing (dy), ColSpacing (dx)]
    pixel_spacing = getattr(dcm, 'PixelSpacing', None)
    if pixel_spacing is None:
        raise ValueError("DICOM file does not contain PixelSpacing (0028,0030) metadata!")
    
    dy, dx = float(pixel_spacing[0]), float(pixel_spacing[1])

    x1, y1 = p1
    x2, y2 = p2

    dx_pix = x2 - x1
    dy_pix = y2 - y1

    # Uncalibrated Euclidean pixel distance
    dist_pixels = math.sqrt(dx_pix**2 + dy_pix**2)

    # Calibrated physical distance in millimeters
    dist_mm = math.sqrt((dx_pix * dx)**2 + (dy_pix * dy)**2)

    # Calibrated image array (SUV or HU)
    slope = float(getattr(dcm, 'RescaleSlope', 1.0))
    intercept = float(getattr(dcm, 'RescaleIntercept', 0.0))
    img_calibrated = dcm.pixel_array.astype(np.float64) * slope + intercept

    return {
        'dcm': dcm,
        'image': img_calibrated,
        'dx': dx,
        'dy': dy,
        'p1': p1,
        'p2': p2,
        'dist_pixels': dist_pixels,
        'dist_mm': dist_mm,
        'modality': str(getattr(dcm, 'Modality', 'Unknown')),
        'patient_name': str(getattr(dcm, 'PatientName', 'Anonymized'))
    }

def main():
    print("=" * 75)
    print("STUDENT LAB TASK 4: CALIBRATED REAL-WORLD ORGAN & LESION MEASUREMENT")
    print("=" * 75)

    dicom_file = 'DICOM/IM-0001-0002.dcm' if os.path.exists('DICOM/IM-0001-0002.dcm') else '../DICOM/IM-0001-0002.dcm'
    
    # Define clinical anatomical calipers:
    # Measurement A: Brain Transverse Width (Lesion to Contralateral Cortex)
    # Measurement B: Anteroposterior Dimension
    measurements = [
        {"name": "Anatomical Span A (Brain Diameter)", "p1": (110, 168), "p2": (226, 168), "color": "#38bdf8"},
        {"name": "Anatomical Span B (Hypermetabolic Lesion Core)", "p1": (134, 134), "p2": (201, 201), "color": "#fde047"}
    ]

    print(f"Loading Clinical DICOM: {dicom_file}")

    results = []
    for meas in measurements:
        res = compute_calibrated_distance(dicom_file, meas['p1'], meas['p2'])
        res['label'] = meas['name']
        res['color'] = meas['color']
        results.append(res)

        print(f"\n--- {meas['name']} ---")
        print(f"  Point 1 Coordinate (x1, y1) : {meas['p1']}")
        print(f"  Point 2 Coordinate (x2, y2) : {meas['p2']}")
        print(f"  Pixel Spacing (dx, dy)      : {res['dx']:.4f} mm/px, {res['dy']:.4f} mm/px")
        print(f"  Uncalibrated Pixel Distance : {res['dist_pixels']:.2f} pixels")
        print(f"  Calibrated Metric Distance  : {res['dist_mm']:.2f} mm ({res['dist_mm']/10.0:.2f} cm)")

    # Visualization
    os.makedirs('outputs', exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.5), facecolor='#0f172a')

    # Panel 1: PET Scan with caliper annotations
    ax1 = axes[0]
    cax1 = ax1.imshow(results[0]['image'], cmap='magma')
    ax1.set_title(f"Clinical Brain PET ({results[0]['modality']})\nCalibrated Physical Measurement Workstation",
                  color='white', fontweight='bold', fontsize=11)
    ax1.axis('off')

    for res in results:
        p1, p2 = res['p1'], res['p2']
        col = res['color']
        
        # Caliper line
        ax1.plot([p1[0], p2[0]], [p1[1], p2[1]], color=col, lw=2.5, linestyle='-', marker='o', markersize=6, markerfacecolor='#0f172a', markeredgecolor=col)
        
        # Midpoint text badge
        mx, my = (p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0
        offset_y = -15 if p1[1] == p2[1] else 12
        ax1.text(mx, my + offset_y, f"{res['dist_mm']:.2f} mm\n({res['dist_pixels']:.1f} px)",
                 color='white', fontsize=8.5, fontweight='bold', ha='center', va='center',
                 bbox=dict(boxstyle='round,pad=0.3', fc='#0f172a', ec=col, lw=1.5, alpha=0.95))

    cbar1 = fig.colorbar(cax1, ax=ax1, fraction=0.046, pad=0.04)
    cbar1.set_label('Calibrated Activity (SUV)', color='white', fontsize=9)
    cbar1.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar1.ax.axes, 'yticklabels'), color='white')

    # Panel 2: Caliper Calibration Comparison Chart
    ax2 = axes[1]
    ax2.set_facecolor('#1e293b')
    
    labels = [r['label'] for r in results]
    pix_dists = [r['dist_pixels'] for r in results]
    mm_dists = [r['dist_mm'] for r in results]

    x = np.arange(len(labels))
    width = 0.35

    rects1 = ax2.bar(x - width/2, pix_dists, width, label='Uncalibrated (Pixels)', color='#64748b', edgecolor='white', lw=0.5)
    rects2 = ax2.bar(x + width/2, mm_dists, width, label='Calibrated (Millimeters mm)', color='#38bdf8', edgecolor='white', lw=0.5)

    ax2.set_ylabel('Distance Value', color='white', fontsize=10)
    ax2.set_title('Pixel Space vs. Metric Physical Space Calibration', color='white', fontweight='bold', fontsize=11)
    ax2.set_xticks(x)
    ax2.set_xticklabels(['Span A\n(Brain Width)', 'Span B\n(Lesion Core)'], color='white', fontsize=9.5)
    ax2.tick_params(colors='white')
    ax2.legend(facecolor='#0f172a', edgecolor='#475569', labelcolor='white')
    ax2.grid(True, color='#334155', linestyle='--', alpha=0.6, axis='y')

    # Add bar values
    for rect in rects1:
        h = rect.get_height()
        ax2.annotate(f'{h:.1f} px', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                     textcoords="offset points", ha='center', va='bottom', color='white', fontsize=8.5, fontweight='bold')
    for rect in rects2:
        h = rect.get_height()
        ax2.annotate(f'{h:.2f} mm', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                     textcoords="offset points", ha='center', va='bottom', color='#38bdf8', fontsize=8.5, fontweight='bold')

    plt.suptitle("Task 4: DICOM Geometric Spacing and Real-World Metric Caliper Calibration",
                 color='#e2e8f0', fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout()

    output_path = 'outputs/task_04_calibrated_measurement_python.png'
    plt.savefig(output_path, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"\n[SAVED] Task 4 Output saved to: {output_path}")

if __name__ == '__main__':
    main()
