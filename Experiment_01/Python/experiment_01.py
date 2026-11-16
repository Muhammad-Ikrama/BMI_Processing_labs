"""
Experiment No. 1 Master Runner: Digital Image Representation, Acquisition, and DICOM Data Handling
Course: Medical Image Processing | Department of Biomedical Engineering, Riphah International University
Faculty: Engr. Rana Talha Khalid

This master script runs all experiment tasks sequentially:
  - Task 1: Matrix Dimension, Data Type & Dynamic Range Analysis
  - Task 2: RGB Color Plane Extraction & Perceptual Luminance Computation
  - Task 3: Clinical DICOM Tag Extraction & Patient Anonymization Check
  - Task 4: Calibrated Real-World Organ Measurement from Pixel Spacing
  - Task 5: 5x5 (25-Panel) Volumetric & Multi-Modal Series Review Montage
  - Task 6: Multi-Modal and Longitudinal Patient Dataset Identification & Curation
"""

import os
import sys
import subprocess

def run_task(script_name):
    print("=" * 80)
    print(f"RUNNING: {script_name}")
    print("=" * 80)
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    result = subprocess.run([sys.executable, script_path], cwd=os.path.dirname(__file__))
    if result.returncode != 0:
        print(f"[FAIL] Task {script_name} returned exit code {result.returncode}")
        return False
    print(f"[PASS] Task {script_name} completed successfully.\n")
    return True

def main():
    print("#" * 80)
    print("# EXPERIMENT NO. 1: COMPLETE AUTOMATED TEST SUITE")
    print("# Digital Image Representation, Acquisition, and DICOM Data Handling")
    print("#" * 80 + "\n")

    tasks = [
        "task_01_matrix_analysis.py",
        "task_02_rgb_perceptual_luminance.py",
        "task_03_dicom_anonymization.py",
        "task_04_calibrated_measurement.py",
        "task_05_pacs_5x5_montage.py",
        "task_06_dataset_curation.py"
    ]

    all_passed = True
    for task in tasks:
        passed = run_task(task)
        if not passed:
            all_passed = False

    print("=" * 80)
    if all_passed:
        print("[ALL TASKS PASSED] All 6 experiment tasks executed with 100% success.")
    else:
        print("[WARNING] One or more tasks failed during execution.")
    print("=" * 80)

if __name__ == '__main__':
    main()
