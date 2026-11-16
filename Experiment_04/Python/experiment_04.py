"""
Experiment 04 Master Orchestration Script: Noise Modeling & Adaptive Filtering Techniques
Course: Medical Image Processing | Riphah International University
Instructor: Engr. Rana Talha Khalid
"""

import os
import sys
import time

cur_dir = os.path.dirname(os.path.abspath(__file__))
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from example_01 import run_example_01
from task_4_1 import run_task_4_1
from task_4_2 import run_task_4_2
from task_4_3 import run_task_4_3
from task_4_4 import run_task_4_4
from task_4_5 import run_task_4_5

def main():
    t_start = time.time()
    print("=" * 80)
    print("RIPHAH INTERNATIONAL UNIVERSITY - DEPARTMENT OF BIOMEDICAL ENGINEERING")
    print("EXPERIMENT NO. 04: NOISE MODELING AND REMOVAL USING MEDIAN & ADAPTIVE FILTERING")
    print("Instructor: Engr. Rana Talha Khalid")
    print("=" * 80)

    print("\n>>> EXECUTING EXAMPLE 01: MEDICAL NOISE RESTORATION BENCHMARK...")
    run_example_01()

    print("\n>>> EXECUTING TASK 4.1: SYNTHETIC NOISE MODELING & PDF ANALYSIS...")
    run_task_4_1()

    print("\n>>> EXECUTING TASK 4.2: LINEAR FILTER FAILURE ANALYSIS ON IMPULSE NOISE...")
    run_task_4_2()

    print("\n>>> EXECUTING TASK 4.3: STANDARD MEDIAN FILTER KERNEL SWEEP [3x3, 5x5, 7x7]...")
    run_task_4_3()

    print("\n>>> EXECUTING TASK 4.4: ADAPTIVE MEDIAN (AMF) HIGH-DENSITY STRESS TEST...")
    run_task_4_4()

    print("\n>>> EXECUTING TASK 4.5: MULTI-PANEL DIAGNOSTIC RESTORATION REPORT...")
    run_task_4_5()

    t_elapsed = time.time() - t_start
    print("\n" + "=" * 80)
    print(f"[SUCCESS] ALL EXPERIMENT 04 PYTHON TASKS COMPLETED IN {t_elapsed:.2f} SECONDS!")
    print("All outputs saved to:")
    print(f"  * Figures: {os.path.join(os.path.dirname(cur_dir), 'Figures')}")
    print(f"  * Tables:  {os.path.join(os.path.dirname(cur_dir), 'Tables')}")
    print(f"  * Outputs: {os.path.join(os.path.dirname(cur_dir), 'Outputs', 'Python')}")
    print("=" * 80)

if __name__ == '__main__':
    main()
