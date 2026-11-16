"""
Experiment 09 - Master Pipeline Orchestrator (Python)
Coordinates execution of morphological benchmark and student practice tasks 9.1 to 9.5.
"""
import os
import sys
import time

from example_01_morphology_benchmark import run_benchmark
from task_9_1_se_geometry_comparison import run_task_9_1
from task_9_2_radius_sensitivity_sweep import run_task_9_2
from task_9_3_order_of_operations import run_task_9_3
from task_9_4_morphological_boundaries import run_task_9_4
from task_9_5_skull_stripping import run_task_9_5

def run_experiment_09():
    t_start = time.time()
    print("=" * 80)
    print("STARTING EXPERIMENT 09: MORPHOLOGICAL IMAGE PROCESSING PIPELINE")
    print("Department of Biomedical Engineering - Riphah International University")
    print("=" * 80)

    print("\n>>> STEP 1: Running Benchmark & Compound Morphological Operations...")
    df_bench = run_benchmark()

    print("\n>>> STEP 2: Running Task 9.1 (Structuring Element Geometry on Calvarium)...")
    df_9_1 = run_task_9_1()

    print("\n>>> STEP 3: Running Task 9.2 (SE Radius Sensitivity Sweep on Ventricles)...")
    df_9_2 = run_task_9_2()

    print("\n>>> STEP 4: Running Task 9.3 (Order of Operations: Open-Close vs. Close-Open)...")
    df_9_3 = run_task_9_3()

    print("\n>>> STEP 5: Running Task 9.4 (Morphological Boundary & Gradient Extraction)...")
    df_9_4 = run_task_9_4()

    print("\n>>> STEP 6: Running Task 9.5 (Automated Cortical Skull Stripping on Head CT)...")
    df_9_5 = run_task_9_5()

    elapsed = time.time() - t_start
    print("\n" + "=" * 80)
    print(f"EXPERIMENT 09 PIPELINE COMPLETED SUCCESSFULLY IN {elapsed:.2f} SECONDS")
    print("All CSV tables and PNG figures generated.")
    print("=" * 80)

if __name__ == "__main__":
    run_experiment_09()
