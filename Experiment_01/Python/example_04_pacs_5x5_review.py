"""
Experiment 01 - Section 8: Clinical PACS Workstation 5x5 (25-Panel) Volumetric Series Review
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University
"""

import os
import cv2
import pydicom
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("=" * 70)
    print("EXAMPLE 8: 5x5 (25-PANEL) CLINICAL PACS WORKSTATION SERIES REVIEW")
    print("=" * 70)

    # 1. Load 3D MRI volume (21 frames)
    mri_path = 'DICOM/IMG-0004-00001.dcm'
    if not os.path.exists(mri_path):
        mri_path = os.path.join('..', 'DICOM', 'IMG-0004-00001.dcm')
    
    ds_mri = pydicom.dcmread(mri_path)
    mri_frames = ds_mri.pixel_array # shape (21, 512, 512)
    print(f"Loaded 3D MRI Volume: {mri_frames.shape[0]} sequential frames ({mri_frames.shape[1]} x {mri_frames.shape[2]})")

    # 2. Load CT scan & PET scan
    ct_path = 'images/CT.jpg' if os.path.exists('images/CT.jpg') else '../images/CT.jpg'
    ct_img = cv2.imread(ct_path, cv2.IMREAD_GRAYSCALE)
    if ct_img is None:
        ct_img = np.zeros((512, 512), dtype=np.uint8)
    else:
        ct_img = cv2.resize(ct_img, (512, 512))

    pet_path = 'DICOM/IM-0001-0002.dcm' if os.path.exists('DICOM/IM-0001-0002.dcm') else '../DICOM/IM-0001-0002.dcm'
    ds_pet = pydicom.dcmread(pet_path)
    pet_raw = ds_pet.pixel_array.astype(np.float64) * float(getattr(ds_pet, 'RescaleSlope', 1.0))
    pet_img = cv2.resize(pet_raw, (512, 512))

    print("Loaded Multi-Modal CT & PET Scans: Resized and calibrated to 512 x 512 pixels")

    # 3. Assemble exactly 25 slices
    # Slices 01-21: MRI Sagittal Frames
    # Slices 22-23: CT Bone Window & CT Soft Tissue Window
    # Slices 24-25: PET 18F-FDG Metabolic Activity Maps
    slices = [mri_frames[i] for i in range(21)]
    # CT Bone (original) & CT Soft (contrast stretched)
    ct_soft = np.clip(ct_img.astype(float) * 1.4, 0, 255).astype(np.uint8)
    slices.extend([ct_img, ct_soft, pet_img, pet_img])

    cmaps = ['gray'] * 21 + ['bone', 'bone', 'hot', 'turbo']
    titles = [f"MR Sag S{i+1:02d}" for i in range(21)] + ["CT Bone", "CT Soft", "PET 18F-FDG", "PET Turbo"]

    print(f"Constructed 25-Slice Multi-Modal Patient Series (5x5 Grid):")
    print(f"    Slices 01-21: Sequential Brain Sagittal MRI Frames (Lateral -> Medial -> Lateral)")
    print(f"    Slices 22-23: CT Brain Bone Window & Soft Tissue Window (Bone Colormap)")
    print(f"    Slices 24-25: PET 18F-FDG Metabolic Activity Maps (Hot & Turbo Colormaps)")

    # 4. Create 5x5 Clinical PACS Workstation Grid
    os.makedirs('outputs', exist_ok=True)
    os.makedirs('scrat', exist_ok=True)
    fig, axes = plt.subplots(5, 5, figsize=(14, 14), facecolor='#0b1120')

    for idx, ax in enumerate(axes.flat):
        ax.imshow(slices[idx], cmap=cmaps[idx])
        ax.set_title(titles[idx], color='white', fontsize=8.5, fontweight='bold', pad=3)
        ax.axis('off')
        # Diagnostic workstation badge
        badge_color = '#fde047' if idx < 21 else ('#38bdf8' if idx < 23 else '#f43f5e')
        ax.text(12, 38, f"[{idx+1:02d}/25]", color=badge_color, fontsize=6.5, fontweight='bold',
                bbox=dict(boxstyle='square,pad=0.15', fc='#0f172a', ec=badge_color, lw=0.6, alpha=0.9))

    plt.suptitle("PACS Diagnostic Workstation: 5x5 Multi-Modal Series Review", color='#38bdf8', fontsize=14, fontweight='bold', y=0.99)
    plt.tight_layout()

    out_main = 'outputs/example_04_pacs_5x5_review_python.png'
    out_scrat = 'scrat/05_medical_report_output.png'
    plt.savefig(out_main, dpi=200, facecolor=fig.get_facecolor())
    plt.savefig(out_scrat, dpi=200, facecolor=fig.get_facecolor())
    plt.close()

    print(f"\n[SAVED] Output Figure Saved: {out_main}")
    print(f"[SAVED] Output Figure Saved: {out_scrat}")

if __name__ == '__main__':
    main()
