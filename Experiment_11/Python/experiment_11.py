"""
Master Orchestrator: Experiment 11 - Active Contour (Snake) Based Segmentation of Anatomical Boundaries in Medical Images
Author: Muhammad Ikrama (Reg ID: 60140)
Department of Biomedical Engineering, Riphah International University, Lahore
Instructor: Engr. Rana Talha Khalid
"""

import os
import sys
import time

def run_all():
    print("=" * 80)
    print("STARTING COMPLETE MASTER EXECUTION: EXPERIMENT 11 (PYTHON)")
    print("=" * 80)
    start_total = time.time()
    
    # 1. Benchmark
    import example_01_snake_benchmark as mod_bench
    mod_bench.run_benchmark()
    
    # 2. Task 11.1
    import task_11_1_alpha_beta_sensitivity as mod_11_1
    mod_11_1.run_task_11_1()
    
    # 3. Task 11.2
    import task_11_2_capture_range_radius as mod_11_2
    mod_11_2.run_task_11_2()
    
    # 4. Task 11.3
    import task_11_3_broken_boundary_bridging as mod_11_3
    mod_11_3.run_task_11_3()
    
    # 5. Task 11.4
    import task_11_4_edge_vs_chan_vese_noise as mod_11_4
    mod_11_4.run_task_11_4()
    
    # 6. Task 11.5
    import task_11_5_head_ct_skull_extraction as mod_11_5
    mod_11_5.run_task_11_5()
    
    elapsed = time.time() - start_total
    print("\n" + "=" * 80)
    print(f"[SUCCESS] ALL EXPERIMENT 11 PYTHON MODULES COMPLETED IN {elapsed:.2f}s")
    print("=" * 80)

if __name__ == "__main__":
    run_all()
