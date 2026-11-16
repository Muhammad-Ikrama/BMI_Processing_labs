"""
Experiment 07 - Master Pipeline Execution Script (Python)
Image Sharpening of Medical Images Using High-Boost Filtering and Unsharp Masking
Course: Medical Image Processing | Riphah International University
Faculty: Engr. Rana Talha Khalid
"""

import time
import os
import sys

# Add script directory to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from example_01 import run_example_01
from task_7_1 import run_task_7_1
from task_7_2 import run_task_7_2
from task_7_3 import run_task_7_3
from task_7_4 import run_task_7_4
from task_7_5 import run_task_7_5

def run_experiment_07():
    start_time = time.time()
    print("================================================================================")
    print("STARTING EXPERIMENT 07: IMAGE SHARPENING & HIGH-BOOST MASTER PIPELINE")
    print("Riphah International University | Department of Biomedical Engineering")
    print("================================================================================\n")

    print(">>> STEP 1: Running Example 01 (Baseline Sharpening & Gradient Benchmark)...")
    t0 = time.time()
    run_example_01()
    print(f"    Completed in {time.time() - t0:.2f}s\n")

    print(">>> STEP 2: Running Task 7.1 (High-Boost Sweep & Clipping Analysis)...")
    t0 = time.time()
    run_task_7_1()
    print(f"    Completed in {time.time() - t0:.2f}s\n")

    print(">>> STEP 3: Running Task 7.2 (Smoothing Kernel Blur & Mask Bandwidth)...")
    t0 = time.time()
    run_task_7_2()
    print(f"    Completed in {time.time() - t0:.2f}s\n")

    print(">>> STEP 4: Running Task 7.3 (1D Transect & Mach Band Measurements)...")
    t0 = time.time()
    run_task_7_3()
    print(f"    Completed in {time.time() - t0:.2f}s\n")

    print(">>> STEP 5: Running Task 7.4 (Noise Amplification in Low-Dose Scans)...")
    t0 = time.time()
    run_task_7_4()
    print(f"    Completed in {time.time() - t0:.2f}s\n")

    print(">>> STEP 6: Running Task 7.5 (Clinical ROIs & Master Diagnostic Report)...")
    t0 = time.time()
    run_task_7_5()
    print(f"    Completed in {time.time() - t0:.2f}s\n")

    total_elapsed = time.time() - start_time
    print("================================================================================")
    print(f"EXPERIMENT 07 MASTER PYTHON PIPELINE COMPLETED SUCCESSFULLY IN {total_elapsed:.2f}s")
    print("All figures, tables, and sharpened outputs generated and verified.")
    print("================================================================================")

if __name__ == "__main__":
    run_experiment_07()
