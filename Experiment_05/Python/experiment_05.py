"""
Experiment 05: Master Execution Script (Python)
Edge Detection in Medical Images Using Sobel, Prewitt, and Canny Operators: Implementation and Comparative Analysis
Course: Medical Image Processing (B.Sc. Biomedical Engineering)
Faculty: Engr. Rana Talha Khalid | Riphah International University
"""

import sys
import os
import time

# Ensure Python directory is on path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from example_01 import run_example_01
from task_5_1 import run_task_5_1
from task_5_2 import run_task_5_2
from task_5_3 import run_task_5_3
from task_5_4 import run_task_5_4
from task_5_5 import run_task_5_5


def run_all_experiment_05():
    t_start = time.time()
    print("=" * 80)
    print("STARTING FULL EXECUTION: EXPERIMENT 05 (PYTHON PIPELINE)")
    print("Course: Medical Image Processing | Instructor: Engr. Rana Talha Khalid")
    print("=" * 80)

    # 1. Example 01
    print("\n>>> Running Example 01: Medical Edge Detection Benchmark...")
    res_ex01 = run_example_01()

    # 2. Task 5.1
    print("\n>>> Running Task 5.1: Discrete Gradient Kernel Construction & Directional Sensitivity...")
    res_t51 = run_task_5_1()

    # 3. Task 5.2
    print("\n>>> Running Task 5.2: Prewitt vs. Sobel Noise Sensitivity Benchmarking...")
    res_t52 = run_task_5_2()

    # 4. Task 5.3
    print("\n>>> Running Task 5.3: Manual Implementation of Non-Maximum Suppression (NMS)...")
    res_t53 = run_task_5_3()

    # 5. Task 5.4
    print("\n>>> Running Task 5.4: Canny Hysteresis Threshold Tuning & Broken Contour Analysis...")
    res_t54 = run_task_5_4()

    # 6. Task 5.5
    print("\n>>> Running Task 5.5: Multi-Operator Quantitative Diagnostic Evaluation Report...")
    res_t55 = run_task_5_5()

    elapsed = time.time() - t_start
    print("\n" + "=" * 80)
    print(f"[COMPLETE] All Experiment 05 Python tasks completed successfully in {elapsed:.2f} seconds.")
    print("Generated 6 publication figures in Figures/ and summary CSV in Tables/.")
    print("=" * 80)


if __name__ == "__main__":
    run_all_experiment_05()
