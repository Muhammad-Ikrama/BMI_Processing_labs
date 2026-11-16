"""
Experiment No. 2 Master Runner: Histogram Computation and Histogram Equalization Techniques
Course: Medical Image Processing | Riphah International University
Faculty: Engr. Rana Talha Khalid
"""

import os
import sys
import subprocess

def main():
    print("#" * 80)
    print("# EXPERIMENT NO. 2 MASTER SUITE: CONTRAST ENHANCEMENT & HISTOGRAM EQUALIZATION")
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

    for s in scripts:
        print(f"\n>>> Running: {s} ...")
        path = os.path.join(os.path.dirname(__file__), s)
        res = subprocess.run([sys.executable, path], cwd=os.path.dirname(__file__))
        if res.returncode != 0:
            print(f"[ERROR] {s} failed with exit code {res.returncode}")
        else:
            print(f"[SUCCESS] {s} finished.")

if __name__ == '__main__':
    main()
