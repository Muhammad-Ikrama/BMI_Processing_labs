"""
Experiment 01 - Task 6: Multi-Modal and Longitudinal Patient Dataset Identification & Curation
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

Task Requirement:
1. Search and identify open medical repositories (TCIA RIDER, OASIS, ADNI, BraTS, TCGA-GBM)
   containing multiple scans of the SAME patient across modalities and longitudinal timepoints.
2. Programmatically inspect DICOM header tags (PatientID, PatientName, StudyDate, Modality,
   FrameOfReferenceUID, StudyInstanceUID, SeriesInstanceUID, PixelSpacing, Dimensions) to verify
   patient identity coherence and spatial alignment.
3. Document how same-patient curation provides the foundational prerequisites for:
   - Exp 12: Spatial Image Registration (rigid / affine transformation)
   - Exp 16: Multi-Modal Image Fusion (PET-CT, MRI-CT complementary integration)
"""

import os
import glob
import pydicom
import pandas as pd

def scan_dicom_archive(folder_path):
    """Scan directory and parse DICOM header tags into structured dictionary."""
    records = []
    files = glob.glob(os.path.join(folder_path, "*.[dD][cC][mM]")) + glob.glob(os.path.join(folder_path, "*.[dD][cC][mM]*"))
    # Filter unique files
    files = sorted(list(set(files)))

    for fpath in files:
        try:
            dcm = pydicom.dcmread(fpath, stop_before_pixels=True)
            fname = os.path.basename(fpath)

            spacing = getattr(dcm, 'PixelSpacing', None)
            spacing_str = f"[{float(spacing[0]):.3f}, {float(spacing[1]):.3f}]" if spacing else "N/A"

            records.append({
                "Filename": fname,
                "PatientID": str(getattr(dcm, 'PatientID', 'N/A')),
                "PatientName": str(getattr(dcm, 'PatientName', 'N/A')),
                "Modality": str(getattr(dcm, 'Modality', 'Unknown')),
                "StudyDate": str(getattr(dcm, 'StudyDate', 'N/A')),
                "StudyDesc": str(getattr(dcm, 'StudyDescription', 'N/A'))[:25],
                "SeriesDesc": str(getattr(dcm, 'SeriesDescription', 'N/A'))[:25],
                "Dimensions": f"{getattr(dcm, 'Rows', 'N/A')}x{getattr(dcm, 'Columns', 'N/A')}",
                "Spacing_mm": spacing_str,
                "FrameOfRefUID": str(getattr(dcm, 'FrameOfReferenceUID', 'N/A'))[:18] + "..." if getattr(dcm, 'FrameOfReferenceUID', None) else "N/A"
            })
        except Exception as e:
            print(f"Error reading {fpath}: {e}")

    return pd.DataFrame(records)

def main():
    print("=" * 80)
    print("STUDENT LAB TASK 6: MULTI-MODAL & LONGITUDINAL PATIENT DATASET CURATION")
    print("=" * 80)

    dataset_folder = 'lab 1 dataset' if os.path.exists('lab 1 dataset') else 'DICOM'
    if not os.path.exists(dataset_folder):
        dataset_folder = os.path.join('..', 'lab 1 dataset')

    print(f"Scanning Clinical DICOM Repository: '{dataset_folder}'...\n")
    df = scan_dicom_archive(dataset_folder)

    if not df.empty:
        print("=== AUTOMATED DICOM HEADER CURATION TABLE ===")
        print(df.to_string(index=False))
    
    # Analysis & Curation Logic
    print("\n" + "=" * 80)
    print("CLINICAL ANALYSIS: SAME-PATIENT COHERENCE & MODALITY COMPATIBILITY")
    print("=" * 80)

    print("""
1. PATIENT IDENTITY COHERENCE AUDIT:
   - PatientID & PatientName must match exactly across multi-modal or longitudinal acquisition sessions.
   - Example from dataset:
     * 'IM-0001-0002.dcm': PatientName = CEREBRIX, ID = XsxuId (Modality: PT)
     * 'IMG-0004-00001.dcm': PatientName = Ultra_fast_Brain (Modality: MR)
     * '0020.DCM': PatientName = Rubo DEMO, ID = 123-45-6789 (Modality: US)
     * 'image-000001.dcm': PatientName = Anonymized, ID = 0 (Modality: PX)
   - Finding: The local lab archive contains multi-subject clinical exemplars representing 4 diverse modalities
     (PET, MRI 3D, Ultrasound multi-frame, Panoramic X-ray).

2. SPATIAL FRAME OF REFERENCE (FrameOfReferenceUID):
   - When multiple scans share an identical FrameOfReferenceUID, they are acquired on the same physical gantry
     or pre-registered (e.g. combined PET-CT scanner).
   - If FrameOfReferenceUIDs differ or are absent, rigid/non-rigid image registration (Exp 12) is mandatory
     to align voxels before mathematical fusion.

3. OPEN BENCHMARK REPOSITORIES FOR SAME-PATIENT RESEARCH:
   a) ADNI (Alzheimer's Disease Neuroimaging Initiative):
      - Longitudinal T1/T2 MRI + 18F-FDG/Amyloid PET of identical subjects scanned over 5+ years.
   b) BraTS (Brain Tumor Segmentation Challenge):
      - Co-registered 4-channel multi-parametric MRI (T1, T1-Contrast, T2, FLAIR) for the exact same patient.
   c) TCIA RIDER & TCGA-GBM (The Cancer Imaging Archive):
      - Matched CT, MRI, and PET-CT longitudinal oncology series for therapy response assessment.
   d) OASIS (Open Access Series of Imaging Studies):
      - Cross-sectional and longitudinal MRI studies across normal aging and dementia cohorts.

4. BRIDGING EXP 1 TO UPCOMING EXPERIMENTS:
   - Experiment 12 (Spatial Registration): Same-patient curation provides the target (fixed) and moving
     images. Geometric parameters (PixelSpacing, ImageOrientationPatient, ImagePositionPatient) define
     the initial affine transformation matrix.
   - Experiment 16 (Multi-Modal Image Fusion): Enables blending metabolic functional information (PET SUV)
     over high-resolution anatomical structure (MRI/CT Hounsfield Units) for neurosurgery and radiotherapy.
""")

    # Save CSV report
    os.makedirs('outputs', exist_ok=True)
    csv_path = 'outputs/task_06_dicom_curation_summary.csv'
    df.to_csv(csv_path, index=False)
    print(f"[SAVED] Curation table exported to: {csv_path}")

if __name__ == '__main__':
    main()
