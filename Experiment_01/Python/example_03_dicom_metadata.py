"""
Experiment 01 - Example 7.3: DICOM Metadata Extraction & Real Metric mm Measurement
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University
"""

import os
import math
import pydicom
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("=" * 70)
    print("EXAMPLE 7.3: DICOM METADATA EXTRACTION & PHYSICAL CALIBRATION")
    print("=" * 70)

    dicom_path = 'DICOM/IM-0001-0002.dcm'
    if not os.path.exists(dicom_path):
        dicom_path = os.path.join('..', 'DICOM', 'IM-0001-0002.dcm')
    
    # 1. Read clinical DICOM file
    dcm = pydicom.dcmread(dicom_path)
    print(f"Loaded DICOM File: {dicom_path}")

    # 2. Extract Patient & Study Metadata
    patient_name = str(getattr(dcm, 'PatientName', 'Anonymous'))
    patient_id = str(getattr(dcm, 'PatientID', 'Unknown'))
    patient_sex = str(getattr(dcm, 'PatientSex', 'N/A'))
    patient_age = str(getattr(dcm, 'PatientAge', 'N/A'))
    modality = str(getattr(dcm, 'Modality', 'Unknown'))
    study_desc = str(getattr(dcm, 'StudyDescription', 'N/A'))
    series_desc = str(getattr(dcm, 'SeriesDescription', 'N/A'))

    print(f"Patient Demographics: Name = {patient_name} | ID = {patient_id} | Sex = {patient_sex} | Age = {patient_age}")
    print(f"Modality: {modality} (Positron Emission Tomography) | Study: {study_desc}")
    print(f"Series Description: {series_desc}")

    # 3. Geometric & Radiometric Tags
    rows = dcm.Rows
    cols = dcm.Columns
    bits_alloc = getattr(dcm, 'BitsAllocated', 16)
    bits_stored = getattr(dcm, 'BitsStored', 16)
    slice_thick = float(getattr(dcm, 'SliceThickness', 0.0))

    pixel_spacing = getattr(dcm, 'PixelSpacing', [1.0, 1.0])
    dy, dx = float(pixel_spacing[0]), float(pixel_spacing[1])
    rescale_slope = float(getattr(dcm, 'RescaleSlope', 1.0))
    rescale_intercept = float(getattr(dcm, 'RescaleIntercept', 0.0))

    print(f"Matrix Dimensions: {rows} Rows x {cols} Columns | Bits Allocated/Stored: {bits_alloc}/{bits_stored}")
    print(f"Pixel Spacing (dy, dx): [{dy:.4f} mm, {dx:.4f} mm] | Slice Thickness: {slice_thick:.2f} mm")
    print(f"Radiometric Scaling: Rescale Slope = {rescale_slope:.5f} | Rescale Intercept = {rescale_intercept:.1f}")

    # 4. Extract pixel array and calibrate
    raw_pixels = dcm.pixel_array
    calibrated_pixels = raw_pixels.astype(np.float64) * rescale_slope + rescale_intercept

    print(f"Raw Integer Pixel Range: Min = {raw_pixels.min()}, Max = {raw_pixels.max()}")
    print(f"Calibrated Activity Range: Min = {calibrated_pixels.min():.2f}, Max = {calibrated_pixels.max():.2f} SUV")

    # 5. Metric Caliper Test between 2 anatomical points
    p1 = (134, 134) # (y1, x1) or (row, col)
    p2 = (201, 201) # (y2, x2)
    dist_pixels = math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)
    dist_mm = math.sqrt(((p2[1] - p1[1]) * dx)**2 + ((p2[0] - p1[0]) * dy)**2)

    print(f"\nMetric Caliper Test (p1={p1} to p2={p2}):")
    print(f"  Pixel Distance      : {dist_pixels:.2f} pixels")
    print(f"  Calibrated Distance : {dist_mm:.2f} millimeters (mm)")

    # 6. Visualization
    os.makedirs('outputs', exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5), facecolor='#0f172a')

    # Image with caliper
    cax = axes[0].imshow(calibrated_pixels, cmap='magma')
    axes[0].set_title(f"Brain PET Scan (Calibrated SUV)\nModality: {modality} | Spacing: {dx:.3f} mm/px", color='white', fontweight='bold', fontsize=11)
    axes[0].axis('off')

    # Draw Caliper line
    axes[0].plot([p1[1], p2[1]], [p1[0], p2[0]], color='#38bdf8', lw=2.5, linestyle='-', marker='o', markersize=6, markerfacecolor='#fde047', markeredgecolor='#0f172a')
    mid_x, mid_y = (p1[1] + p2[1]) / 2.0, (p1[0] + p2[0]) / 2.0
    axes[0].text(mid_x + 8, mid_y - 8, f"{dist_mm:.2f} mm\n({dist_pixels:.1f} px)", color='#fde047', fontsize=9.5, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.3', fc='#0f172a', ec='#fde047', lw=1.2, alpha=0.9))

    cbar = fig.colorbar(cax, ax=axes[0], fraction=0.046, pad=0.04)
    cbar.set_label('Activity / SUV', color='white', fontsize=9)
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

    # Intensity distribution histogram
    non_zero_vals = calibrated_pixels[calibrated_pixels > 0]
    axes[1].set_facecolor('#1e293b')
    axes[1].hist(non_zero_vals.flatten(), bins=60, color='#38bdf8', edgecolor='#0f172a', alpha=0.85)
    axes[1].axvline(calibrated_pixels.mean(), color='#ef4444', linestyle='--', lw=2, label=f"Mean: {calibrated_pixels.mean():.1f} SUV")
    axes[1].axvline(np.median(non_zero_vals), color='#fde047', linestyle=':', lw=2, label=f"Median Non-zero: {np.median(non_zero_vals):.1f}")
    axes[1].set_title("Calibrated Radiometric Intensity Distribution", color='white', fontweight='bold', fontsize=11)
    axes[1].set_xlabel("Calibrated Tracer Uptake (SUV)", color='white', fontsize=10)
    axes[1].set_ylabel("Pixel Frequency Count", color='white', fontsize=10)
    axes[1].tick_params(colors='white')
    axes[1].legend(facecolor='#0f172a', edgecolor='#475569', labelcolor='white')
    axes[1].grid(True, color='#334155', linestyle='--', alpha=0.6)

    plt.tight_layout()
    output_path = 'outputs/example_03_dicom_metadata_python.png'
    plt.savefig(output_path, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"\n[SAVED] Visualization saved to: {output_path}")

if __name__ == '__main__':
    main()
