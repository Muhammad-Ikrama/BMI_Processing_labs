"""
Master Orchestrator: Experiment 12 - Rigid Registration of Multi-Modal Medical Images (PET-CT and PET-MRI)
Course: Medical Image Processing (BMI-701) | Riphah International University
Student: Muhammad Ikrama (Reg ID: 60140)
Instructor: Engr. Rana Talha Khalid
"""

import os
import sys
import time

def run_all():
    print("=" * 80)
    print("STARTING COMPLETE MASTER EXECUTION: EXPERIMENT 12 (PYTHON)")
    print("=" * 80)
    start_total = time.time()
    
    # 1. Benchmark
    import example_01_rigid_registration_benchmark as mod_bench
    mod_bench.run_benchmark()
    
    # 2. Task 12.1
    import task_12_1_matrix_construction as mod_12_1
    mod_12_1.run_task_12_1()
    
    # 3. Task 12.2
    import task_12_2_interpolation_modes as mod_12_2
    mod_12_2.run_task_12_2()
    
    # 4. Task 12.3
    import task_12_3_joint_histogram_rotation_sweep as mod_12_3
    mod_12_3.run_task_12_3()
    
    # 5. Task 12.4
    import task_12_4_why_mse_fails_multimodal as mod_12_4
    mod_12_4.run_task_12_4()
    
    # 6. Task 12.5
    import task_12_5_pet_mri_fusion_checkerboard as mod_12_5
    mod_12_5.run_task_12_5()
    
    elapsed = time.time() - start_total
    print("\n" + "=" * 80)
    print(f"[SUCCESS] ALL EXPERIMENT 12 PYTHON MODULES COMPLETED IN {elapsed:.2f}s")
    print("=" * 80)

if __name__ == "__main__":
    run_all()
