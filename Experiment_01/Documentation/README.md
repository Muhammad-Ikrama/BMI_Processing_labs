# Experiment No. 1: Digital Image Representation, Acquisition, and DICOM Data Handling
**Course**: Medical Image Processing (B.Sc. Biomedical Engineering)  
**Institution**: Faculty of Engineering & Applied Sciences, Riphah International University, Lahore  
**Instructor / Lab Engineer**: Engr. Rana Talha Khalid  

---

## 1. Overview
This laboratory experiment covers the foundational computational and physical concepts of medical imaging:
1. **Discrete Matrix Representation**: Converting continuous anatomical distributions $f(x, y)$ into digital matrices $I(i, j)$ via spatial sampling and intensity quantization.
2. **Color Models & Perceptual Luminance**: Decomposing 3-channel RGB medical images into 2D scalar planes and evaluating perceptual luminance preservation (ITU-R BT.601) against unweighted averaging.
3. **Clinical DICOM Standards & PHI Anonymization**: Parsing clinical DICOM headers (CT, MRI, PET, US), inspecting acquisition geometry, and executing programmatic Protected Health Information (PHI) sanitization.
4. **Geometric Calibration**: Converting pixel-based coordinate distances into real-world millimeters using metadata `PixelSpacing` $[S_y, S_x]$.
5. **PACS Workstation Montages**: Generating a $5 \times 5$ (25-panel) multi-modal volumetric series review montage (21 sagittal brain MRI slices + CT bone/soft windows + PET metabolic maps).
6. **Patient Cohort Curation**: Programmatic validation of identity coherence and frame of reference across multi-modal and longitudinal clinical scans.

---

## 2. Directory Structure

```text
Biomedical_Image_Processing_Lab/
└── Experiment_01/
    ├── Report/
    │   ├── Experiment_01_Report.docx       # Complete laboratory report (Word format)
    │   └── Experiment_01_Report.pdf        # Complete laboratory report (PDF format)
    ├── MATLAB/
    │   ├── task_01_matrix_analysis.m       # Task 1: Matrix analysis & 5x5 ROI
    │   ├── task_02_rgb_perceptual_luminance.m # Task 2: RGB planes & luminance
    │   ├── task_03_dicom_anonymization.m   # Task 3: DICOM header & PHI masking
    │   ├── task_04_calibrated_measurement.m # Task 4: Metric caliper in mm
    │   ├── task_05_pacs_5x5_montage.m      # Task 5: 5x5 PACS workstation montage
    │   ├── task_06_dataset_curation.m      # Task 6: DICOM cohort curation
    │   ├── example_01_matrix_properties.m  # Tutorial Example 7.1
    │   ├── example_02_rgb_luminance.m      # Tutorial Example 7.2
    │   ├── example_03_dicom_metadata.m     # Tutorial Example 7.3
    │   ├── example_04_pacs_5x5_review.m    # Tutorial Example 7.4
    │   ├── run_all.m                       # Batch runner
    │   └── experiment_01.m                 # Master experiment runner
    ├── Python/
    │   ├── task_01_matrix_analysis.py      # Task 1: Matrix analysis & 5x5 ROI
    │   ├── task_02_rgb_perceptual_luminance.py # Task 2: RGB planes & luminance
    │   ├── task_03_dicom_anonymization.py  # Task 3: DICOM header & PHI masking
    │   ├── task_04_calibrated_measurement.py # Task 4: Metric caliper in mm
    │   ├── task_05_pacs_5x5_montage.py     # Task 5: 5x5 PACS workstation montage
    │   ├── task_06_dataset_curation.py     # Task 6: DICOM cohort curation
    │   ├── example_01_matrix_properties.py # Tutorial Example 7.1
    │   ├── example_02_rgb_luminance.py     # Tutorial Example 7.2
    │   ├── example_03_dicom_metadata.py    # Tutorial Example 7.3
    │   ├── example_04_pacs_5x5_review.py   # Tutorial Example 7.4
    │   ├── run_all.py                      # Batch runner
    │   ├── experiment_01.py                # Master experiment runner
    │   └── requirements.txt                # Python package dependencies
    ├── Inputs/
    │   ├── images/                         # Source CT, MRI, PET, US images
    │   └── DICOM/                          # Clinical multi-modal DICOM files
    ├── Outputs/
    │   ├── MATLAB/                         # MATLAB output figures and DCMs
    │   └── Python/                         # Python output figures and DCMs
    ├── Figures/                            # Consolidated PNG figures for report
    ├── Tables/                             # Exported CSVs and metadata tables
    ├── Tests/
    │   └── test_results.txt                # Automated test execution log (100% PASS)
    └── Documentation/
        ├── README.md                       # This documentation guide
        └── requirement_traceability.md     # Requirement Traceability Matrix
```

---

## 3. Environment & Prerequisites

### Python Setup
* Python 3.10+ (tested on Python 3.14)
* Install dependencies:
  ```bash
  cd Python/
  pip install -r requirements.txt
  ```

### MATLAB Setup
* MATLAB R2022b or later (tested on MATLAB R2026a)
* Image Processing Toolbox

---

## 4. Execution Instructions

### Running Python Implementations
Execute the master runner to execute all tasks in sequence and generate figures:
```bash
cd Python/
python experiment_01.py
```
Or execute individual tasks:
```bash
python task_01_matrix_analysis.py
python task_02_rgb_perceptual_luminance.py
python task_03_dicom_anonymization.py
python task_04_calibrated_measurement.py
python task_05_pacs_5x5_montage.py
python task_06_dataset_curation.py
```

### Running MATLAB Implementations
Launch MATLAB, navigate to `MATLAB/`, and run:
```matlab
experiment_01
```
Or run individual task scripts (e.g., `task_01_matrix_analysis`).

---

## 5. Verification & Quality Assurance
Run the automated test suite to verify input data integrity, data types, mathematical calculations, and generated deliverables:
```bash
python -c "import subprocess; subprocess.run(['python', '../Tests/run_tests.py'])"
```
Audit logs are stored in `Tests/test_results.txt` confirming:
* 9/9 Test suites passed (100% success rate).
* Calibrated distance verified ($94.75\text{ px} \to 96.24\text{ mm}$).
* Difference metrics verified ($\Delta_{\text{max}} = 54$, $\text{MAD} = 29.55$).
* All 16 output figures generated and validated.
