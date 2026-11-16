"""
Runner script for Experiment 03 Python implementation
"""

import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import experiment_03

if __name__ == '__main__':
    experiment_03.main()
