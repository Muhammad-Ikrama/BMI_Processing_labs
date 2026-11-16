"""
Master Execution Script for All Python Scripts in Experiment 02
Histogram Computation and Histogram Equalization Techniques for Contrast Enhancement of Medical Images
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University
"""

import os
import sys
import subprocess

def run_script(script_name):
    print("\n" + "=" * 80)
    print(f"= EXECUTING: {script_name}")
    print("=" * 80)
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    res = subprocess.run([sys.executable, script_path], cwd=os.path.dirname(__file__))
    if res.returncode != 0:
        print(f"[FAIL] Script {script_name} returned code {res.returncode}")
        return False
    print(f"[PASS] {script_name} completed cleanly.\n")
    return True

def main():
    print("#" * 80)
    print("# EXPERIMENT NO. 02: PYTHON AUTOMATED SUITE")
    print("# Histogram Computation and Histogram Equalization Techniques")
    print("#" * 80)

    scripts = [
        "example_01_histogram_cdf.py",
        "example_02_ghe_vs_clahe.py",
        "task_2_1_manual_histogram.py",
        "task_2_2_dual_axis_cdf.py",
        "task_2_3_global_histogram_equalization.py",
        "task_2_4_clahe_clip_sensitivity.py",
        "task_2_5_multipanel_contrast_report.py"
    ]

    all_passed = True
    for s in scripts:
        if not run_script(s):
            all_passed = False

    print("=" * 80)
    if all_passed:
        print("[ALL SCRIPTS COMPLETED SUCCESSFULLY] 100% of Experiment 02 tasks executed.")
    else:
        print("[WARNING] One or more tasks encountered an execution error.")
    print("=" * 80)

if __name__ == '__main__':
    main()
