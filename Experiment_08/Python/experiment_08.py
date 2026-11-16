"""
Experiment 08 - Master Pipeline Orchestrator (Python)
Coordinates execution of all benchmark scripts and student laboratory practice tasks.
"""
import os
import sys
import time

from example_01_global_adaptive_benchmark import run_benchmark
from task_8_1_custom_otsu import run_task_8_1
from task_8_2_isodata_convergence import run_task_8_2
from task_8_3_rf_bias_failure import run_task_8_3
from task_8_4_adaptive_param_sweep import run_task_8_4
from task_8_5_multi_otsu import run_task_8_5

def run_experiment_08():
    t_start = time.time()
    print("=" * 80)
    print("STARTING EXPERIMENT 08: GLOBAL AND ADAPTIVE THRESHOLDING PIPELINE")
    print("Department of Biomedical Engineering - Riphah International University")
    print("=" * 80)

    print("\n>>> STEP 1: Running Benchmark & Clinical Comparison...")
    df_bench = run_benchmark()

    print("\n>>> STEP 2: Running Task 8.1 (Custom First-Principles Otsu on Head CT)...")
    df_8_1 = run_task_8_1()

    print("\n>>> STEP 3: Running Task 8.2 (Iterative Isodata vs. Otsu Convergence)...")
    df_8_2 = run_task_8_2()

    print("\n>>> STEP 4: Running Task 8.3 (MRI RF Bias-Field Shading & Failure Analysis)...")
    df_8_3 = run_task_8_3()

    print("\n>>> STEP 5: Running Task 8.4 (Adaptive Window & Offset Sensitivity Sweep)...")
    df_8_4 = run_task_8_4()

    print("\n>>> STEP 6: Running Task 8.5 (Multi-Otsu 3-Class Tissue Classification)...")
    df_8_5 = run_task_8_5()

    elapsed = time.time() - t_start
    print("\n" + "=" * 80)
    print(f"EXPERIMENT 08 PIPELINE COMPLETED SUCCESSFULLY IN {elapsed:.2f} SECONDS")
    print("All CSV tables and PNG figures generated.")
    print("=" * 80)

if __name__ == "__main__":
    run_experiment_08()
