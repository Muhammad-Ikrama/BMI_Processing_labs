"""
Master Orchestrator for Experiment 14:
Lossless and Lossy Compression of Medical Images and Quality Evaluation Using PSNR & CR
Author: Muhammad Ikrama (Reg ID: 60140)
Department of Biomedical Engineering, Riphah International University, Lahore
Instructor: Engr. Rana Talha Khalid
Course: Medical Image Processing (BMI-701)
"""

import os
import sys
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

import benchmark_compression
import task_14_1_rle_compression
import task_14_2_entropy_redundancy
import task_14_3_rate_distortion_curves
import task_14_4_blocking_artifacts
import task_14_5_downstream_impact

def main():
    print("*" * 80)
    print("   RIPHAH INTERNATIONAL UNIVERSITY - FACULTY OF ENGINEERING & APPLIED SCIENCES")
    print("   DEPARTMENT OF BIOMEDICAL ENGINEERING - MEDICAL IMAGE PROCESSING LAB (BMI-701)")
    print("   EXPERIMENT 14: LOSSLESS & LOSSY MEDICAL IMAGE COMPRESSION (PSNR & CR)")
    print("   Student: Muhammad Ikrama (Reg ID: 60140) | Instructor: Engr. Rana Talha Khalid")
    print("*" * 80)
    
    t0 = time.time()
    
    print("\n>>> Running Section 5 Clinical Compression Benchmark...")
    benchmark_compression.run_benchmark()
    
    print("\n>>> Running Task 14.1: Custom RLE Compressor...")
    task_14_1_rle_compression.run_task_14_1()
    
    print("\n>>> Running Task 14.2: Shannon Entropy & Redundancy Across Modalities...")
    task_14_2_entropy_redundancy.run_task_14_2()
    
    print("\n>>> Running Task 14.3: Multi-Modality Rate-Distortion Curves...")
    task_14_3_rate_distortion_curves.run_task_14_3()
    
    print("\n>>> Running Task 14.4: 8x8 DCT Blocking Artifact Visualization...")
    task_14_4_blocking_artifacts.run_task_14_4()
    
    print("\n>>> Running Task 14.5: Downstream Impact on Segmentation & GLCM...")
    task_14_5_downstream_impact.run_task_14_5()
    
    elapsed = time.time() - t0
    print("\n" + "=" * 80)
    print(f"EXPERIMENT 14 COMPLETE: All 5 Tasks & Benchmark Successfully Executed in {elapsed:.2f}s.")
    print("All figures saved to Figures/ and all tables exported to Tables/.")
    print("=" * 80)

if __name__ == "__main__":
    main()
