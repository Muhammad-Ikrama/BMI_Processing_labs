"""
Master Orchestrator for Experiment 13:
Texture Feature Extraction from Medical Images Using the Gray-Level Co-occurrence Matrix (GLCM)
Author: Muhammad Ikrama (Reg ID: 60140)
Department of Biomedical Engineering, Riphah International University, Lahore
Instructor: Engr. Rana Talha Khalid
Course: Medical Image Processing (BMI-701)
"""

import os
import sys
import time

# Add current folder to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

import benchmark_glcm
import task_13_1_synthetic_glcm
import task_13_2_distance_sweep
import task_13_3_directional_anisotropy
import task_13_4_quantization_tradeoff
import task_13_5_texture_maps

def main():
    print("*" * 80)
    print("   RIPHAH INTERNATIONAL UNIVERSITY - FACULTY OF ENGINEERING & APPLIED SCIENCES")
    print("   DEPARTMENT OF BIOMEDICAL ENGINEERING - MEDICAL IMAGE PROCESSING LAB (BMI-701)")
    print("   EXPERIMENT 13: TEXTURE FEATURE EXTRACTION FROM MEDICAL IMAGES USING GLCM")
    print("   Student: Muhammad Ikrama (Reg ID: 60140) | Instructor: Engr. Rana Talha Khalid")
    print("*" * 80)
    
    t0 = time.time()
    
    # 1. Benchmark
    print("\n>>> Running Section 5 Clinical Benchmark Extraction...")
    benchmark_glcm.run_benchmark()
    
    # 2. Task 13.1
    print("\n>>> Running Task 13.1: Hand-Verified 4x4 GLCM Construction...")
    task_13_1_synthetic_glcm.run_task_13_1()
    
    # 3. Task 13.2
    print("\n>>> Running Task 13.2: Distance Sensitivity Sweep...")
    task_13_2_distance_sweep.run_task_13_2()
    
    # 4. Task 13.3
    print("\n>>> Running Task 13.3: Directional Anisotropy Analysis...")
    task_13_3_directional_anisotropy.run_task_13_3()
    
    # 5. Task 13.4
    print("\n>>> Running Task 13.4: Gray-Level Quantization Trade-Off...")
    task_13_4_quantization_tradeoff.run_task_13_4()
    
    # 6. Task 13.5
    print("\n>>> Running Task 13.5: Sliding-Window Texture Feature Maps...")
    task_13_5_texture_maps.run_task_13_5()
    
    total_time = time.time() - t0
    print("\n" + "=" * 80)
    print(f"EXPERIMENT 13 COMPLETE: All 5 Tasks & Benchmark Successfully Executed in {total_time:.2f}s.")
    print("All figures saved to Figures/ and all tables exported to Tables/.")
    print("=" * 80)

if __name__ == "__main__":
    main()
