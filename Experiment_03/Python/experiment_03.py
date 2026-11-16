"""
Experiment 03 Master Orchestration Script: Image Smoothing of Medical Images Using Spatial Domain Mean/Averaging and Gaussian Filters
Course: Medical Image Processing | Riphah International University
Instructor: Engr. Rana Talha Khalid
"""

import os
import sys
import time

# Ensure current directory is on python path
cur_dir = os.path.dirname(os.path.abspath(__file__))
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from example_01 import run_example_01
from task_3_1 import run_task_3_1
from task_3_2 import run_task_3_2
from task_3_3 import run_task_3_3
from task_3_4 import run_task_3_4
from task_3_5 import run_task_3_5

def main():
    t_start = time.time()
    print("=" * 80)
    print("RIPHAH INTERNATIONAL UNIVERSITY - DEPARTMENT OF BIOMEDICAL ENGINEERING")
    print("EXPERIMENT NO. 03: IMAGE SMOOTHING USING SPATIAL DOMAIN MEAN & GAUSSIAN FILTERS")
    print("Instructor: Engr. Rana Talha Khalid")
    print("=" * 80)

    print("\n>>> EXECUTING EXAMPLE 01: FILTERING BENCHMARK (MEAN VS GAUSSIAN)...")
    run_example_01()

    print("\n>>> EXECUTING TASK 3.1: 2D DISCRETE CONVOLUTION & BOUNDARY PADDING COMPARISON...")
    run_task_3_1()

    print("\n>>> EXECUTING TASK 3.2: MEAN FILTER KERNEL SWEEP [3x3 to 9x9]...")
    run_task_3_2()

    print("\n>>> EXECUTING TASK 3.3: 2D GAUSSIAN KERNEL GENERATION & SIGMA SWEEP...")
    run_task_3_3()

    print("\n>>> EXECUTING TASK 3.4: QUANTITATIVE BENCHMARKING (PSNR, SSIM, CNR)...")
    run_task_3_4()

    print("\n>>> EXECUTING TASK 3.5: 1D ANATOMICAL EDGE GRADIENT PROFILE ANALYSIS...")
    run_task_3_5()

    t_elapsed = time.time() - t_start
    print("\n" + "=" * 80)
    print(f"[SUCCESS] ALL EXPERIMENT 03 PYTHON TASKS COMPLETED IN {t_elapsed:.2f} SECONDS!")
    print("All outputs saved to:")
    print(f"  * Figures: {os.path.join(os.path.dirname(cur_dir), 'Figures')}")
    print(f"  * Tables:  {os.path.join(os.path.dirname(cur_dir), 'Tables')}")
    print(f"  * Outputs: {os.path.join(os.path.dirname(cur_dir), 'Outputs', 'Python')}")
    print("=" * 80)

if __name__ == '__main__':
    main()
