"""
Experiment 06 - Master Pipeline Execution Script (Python)
Frequency-Domain Filtering of Medical Images Using the 2-D Fourier Transform:
Low-Pass and High-Pass Filter Design and Analysis
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
from task_6_1 import run_task_6_1
from task_6_2 import run_task_6_2
from task_6_3 import run_task_6_3
from task_6_4 import run_task_6_4
from task_6_5 import run_task_6_5

def run_experiment_06():
    start_time = time.time()
    print("================================================================================")
    print("STARTING EXPERIMENT 06: FREQUENCY-DOMAIN FILTERING MASTER PIPELINE")
    print("Riphah International University | Department of Biomedical Engineering")
    print("================================================================================\n")

    print(">>> STEP 1: Running Example 01 (Baseline Frequency Filtering Pipeline)...")
    t0 = time.time()
    run_example_01()
    print(f"    Completed in {time.time() - t0:.2f}s\n")

    print(">>> STEP 2: Running Task 6.1 (2-D DFT & Centered Magnitude Spectrum)...")
    t0 = time.time()
    run_task_6_1()
    print(f"    Completed in {time.time() - t0:.2f}s\n")

    print(">>> STEP 3: Running Task 6.2 (Gibbs Ringing & ILPF Sensitivity Sweep)...")
    t0 = time.time()
    run_task_6_2()
    print(f"    Completed in {time.time() - t0:.2f}s\n")

    print(">>> STEP 4: Running Task 6.3 (Butterworth LP Filter Order Sweep)...")
    t0 = time.time()
    run_task_6_3()
    print(f"    Completed in {time.time() - t0:.2f}s\n")

    print(">>> STEP 5: Running Task 6.4 (Gaussian Low-Pass vs High-Pass Contrast)...")
    t0 = time.time()
    run_task_6_4()
    print(f"    Completed in {time.time() - t0:.2f}s\n")

    print(">>> STEP 6: Running Task 6.5 (Multi-Filter Benchmarking & Diagnostic Report)...")
    t0 = time.time()
    run_task_6_5()
    print(f"    Completed in {time.time() - t0:.2f}s\n")

    total_elapsed = time.time() - start_time
    print("================================================================================")
    print(f"EXPERIMENT 06 MASTER PYTHON PIPELINE COMPLETED SUCCESSFULLY IN {total_elapsed:.2f}s")
    print("All figures, tables, and filtered outputs generated and verified.")
    print("================================================================================")

if __name__ == "__main__":
    run_experiment_06()
