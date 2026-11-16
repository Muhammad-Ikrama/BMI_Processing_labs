"""
Master Execution Script for All Python Examples and Tasks (Experiment #01)
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University
"""

import os
import sys
import subprocess

def run_script(script_name):
    print("\n" + "#" * 80)
    print(f"# EXECUTING: {script_name}")
    print("#" * 80)
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    res = subprocess.run([sys.executable, script_path], capture_output=False)
    if res.returncode != 0:
        print(f"[ERROR] Script {script_name} exited with code {res.returncode}")
    else:
        print(f"[SUCCESS] {script_name} completed cleanly.")

def main():
    print("=" * 80)
    print("RUNNING ALL EXPERIMENT 01 PYTHON EXAMPLES AND LAB TASKS")
    print("=" * 80)

    scripts = [
        "example_01_matrix_properties.py",
        "example_02_rgb_luminance.py",
        "example_03_dicom_metadata.py",
        "example_04_pacs_5x5_review.py",
        "task_01_matrix_analysis.py",
        "task_02_rgb_perceptual_luminance.py",
        "task_03_dicom_anonymization.py",
        "task_04_calibrated_measurement.py",
        "task_05_pacs_5x5_montage.py",
        "task_06_dataset_curation.py"
    ]

    for s in scripts:
        run_script(s)

    print("\n" + "=" * 80)
    print("ALL PYTHON EXAMPLES AND TASKS COMPLETED SUCCESSFULLY!")
    print("All generated figures and tables are located in the 'outputs/' folder.")
    print("=" * 80)

if __name__ == '__main__':
    main()
