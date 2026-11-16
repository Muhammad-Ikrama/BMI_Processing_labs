"""
Master Orchestrator: Experiment 10 - Region-Based Segmentation Using Seeded Region Growing and Watershed Transform
Author: Muhammad Ikrama (Reg ID: 60140)
Department of Biomedical Engineering, Riphah International University, Lahore
Instructor: Engr. Rana Talha Khalid
"""

import os
import sys
import time

def run_all():
    print("=" * 80)
    print("STARTING COMPLETE MASTER EXECUTION: EXPERIMENT 10 (PYTHON)")
    print("=" * 80)
    start_total = time.time()
    
    # 1. Benchmark module
    import example_01_region_growing_watershed_benchmark as mod_bench
    mod_bench.run_benchmark()
    
    # 2. Task 10.1
    import task_10_1_connectivity_4_vs_8 as mod_10_1
    mod_10_1.run_task_10_1()
    
    # 3. Task 10.2
    import task_10_2_fixed_vs_running_mean as mod_10_2
    mod_10_2.run_task_10_2()
    
    # 4. Task 10.3
    import task_10_3_seed_perturbation as mod_10_3
    mod_10_3.run_task_10_3()
    
    # 5. Task 10.4
    import task_10_4_distance_transform_sweep as mod_10_4
    mod_10_4.run_task_10_4()
    
    # 6. Task 10.5
    import task_10_5_chest_xray_lung_watershed as mod_10_5
    mod_10_5.run_task_10_5()
    
    elapsed = time.time() - start_total
    print("\n" + "=" * 80)
    print(f"[SUCCESS] ALL EXPERIMENT 10 PYTHON MODULES COMPLETED IN {elapsed:.2f}s")
    print("=" * 80)

if __name__ == "__main__":
    run_all()
