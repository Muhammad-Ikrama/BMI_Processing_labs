"""
Experiment 01 - Task 5: 5x5 (25-Panel) Volumetric & Multi-Modal Series Review Montage
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

Task Requirement:
Using the 21-frame 3D MRI volume ('DICOM/IMG-0004-00001.dcm') along with the CT and PET scans,
construct a 5x5 (25-panel) clinical PACS review montage.
Display sequential sagittal slices (Frames 1 to 21) followed by CT bone/soft windows and PET metabolic maps.
Format each panel with its respective slice identifier [01/25 to 25/25], modality label, and
appropriate medical colormap (gray, bone, hot, turbo).
"""

import os
import cv2
import pydicom
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("=" * 75)
    print("STUDENT LAB TASK 5: 5x5 (25-PANEL) CLINICAL PACS WORKSTATION MONTAGE")
    print("=" * 75)

    # 1. Read 3D MRI volume (21 frames)
    mri_path = 'DICOM/IMG-0004-00001.dcm' if os.path.exists('DICOM/IMG-0004-00001.dcm') else '../DICOM/IMG-0004-00001.dcm'
    ds_mri = pydicom.dcmread(mri_path)
    mri_stack = ds_mri.pixel_array
    num_mri_slices = mri_stack.shape[0]

    print(f"Loaded 3D MRI Volumetric Dataset: {num_mri_slices} slices ({mri_stack.shape[1]}x{mri_stack.shape[2]})")

    # 2. Read CT and PET modalities and normalize to 512x512
    ct_path = 'images/CT.jpg' if os.path.exists('images/CT.jpg') else '../images/CT.jpg'
    ct_img = cv2.imread(ct_path, cv2.IMREAD_GRAYSCALE)
    if ct_img is None:
        ct_img = np.zeros((512, 512), dtype=np.uint8)
    else:
        ct_img = cv2.resize(ct_img, (512, 512))

    pet_path = 'DICOM/IM-0001-0002.dcm' if os.path.exists('DICOM/IM-0001-0002.dcm') else '../DICOM/IM-0001-0002.dcm'
    ds_pet = pydicom.dcmread(pet_path)
    pet_scaled = ds_pet.pixel_array.astype(np.float64) * float(getattr(ds_pet, 'RescaleSlope', 1.0))
    pet_img = cv2.resize(pet_scaled, (512, 512))

    # 3. Create CT Bone and Soft Tissue Window representations
    ct_bone = ct_img
    # Soft tissue window simulation via non-linear contrast adjustment
    ct_soft = np.clip(np.power(ct_img / 255.0, 0.75) * 255.0, 0, 255).astype(np.uint8)

    # 4. Construct 25 Panels
    slices = []
    titles = []
    cmaps = []
    modality_tags = []

    # Panels 1 to 21: MRI Sagittal
    for i in range(21):
        slices.append(mri_stack[i])
        titles.append(f"MR Sag S{i+1:02d}")
        cmaps.append('gray')
        modality_tags.append("MRI T1 TSE")

    # Panel 22: CT Bone Window
    slices.append(ct_bone)
    titles.append("CT Bone Window")
    cmaps.append('bone')
    modality_tags.append("CT Bone Window")

    # Panel 23: CT Soft Tissue Window
    slices.append(ct_soft)
    titles.append("CT Soft Window")
    cmaps.append('bone')
    modality_tags.append("CT Soft Tissue")

    # Panel 24: PET Hot Colormap
    slices.append(pet_img)
    titles.append("PET 18F-FET (Hot)")
    cmaps.append('hot')
    modality_tags.append("PET Metabolic")

    # Panel 25: PET Turbo Colormap
    slices.append(pet_img)
    titles.append("PET 18F-FET (Turbo)")
    cmaps.append('turbo')
    modality_tags.append("PET Turbo Map")

    print("Assembled exactly 25 clinical panels for 5x5 multi-modal review.")

    # 5. Publication-grade 5x5 Dark PACS GUI Rendering
    os.makedirs('outputs', exist_ok=True)
    fig, axes = plt.subplots(5, 5, figsize=(15, 15), facecolor='#0b1120')

    for idx, ax in enumerate(axes.flat):
        img_slice = slices[idx]
        cmap_name = cmaps[idx]

        ax.imshow(img_slice, cmap=cmap_name)
        ax.axis('off')

        # Slice Title
        title_color = '#ffffff' if idx < 21 else ('#38bdf8' if idx < 23 else '#f43f5e')
        ax.set_title(titles[idx], color=title_color, fontsize=8.5, fontweight='bold', pad=3)

        # Workstation Index Badge [01/25]
        badge_border = '#fde047' if idx < 21 else ('#38bdf8' if idx < 23 else '#f43f5e')
        ax.text(12, 38, f"[{idx+1:02d}/25]", color=badge_border, fontsize=6.5, fontweight='bold',
                bbox=dict(boxstyle='square,pad=0.2', fc='#0f172a', ec=badge_border, lw=0.7, alpha=0.92))
        
        # Modality Tag at bottom
        ax.text(12, 490, modality_tags[idx], color='#94a3b8', fontsize=5.5, fontweight='semibold',
                bbox=dict(boxstyle='square,pad=0.15', fc='#0f172a', ec='#334155', lw=0.5, alpha=0.85))

    plt.suptitle("PACS Diagnostic Workstation: 5x5 (25-Panel) Volumetric & Multi-Modal Series Review\nPatient ID: SUBJ_2026_001 | Modalities: MRI (21 Sagittal Slices) + CT Windows + PET Tracer Maps",
                 color='#38bdf8', fontsize=12.5, fontweight='bold', y=0.99)
    plt.tight_layout()

    out_path = 'outputs/task_05_pacs_5x5_montage_python.png'
    plt.savefig(out_path, dpi=200, facecolor=fig.get_facecolor())
    plt.close()
    print(f"\n[SAVED] Task 5 5x5 Montage saved to: {out_path}")

if __name__ == '__main__':
    main()
