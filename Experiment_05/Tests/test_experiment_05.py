"""
Comprehensive Automated Test Suite for Experiment 05
Edge Detection in Medical Images Using Sobel, Prewitt, and Canny Operators
Course: Medical Image Processing | Instructor: Engr. Rana Talha Khalid
"""

import os
import sys
import unittest
import numpy as np
import cv2

# Add Python directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
exp_dir = os.path.dirname(script_dir)
python_dir = os.path.join(exp_dir, "Python")
if python_dir not in sys.path:
    sys.path.insert(0, python_dir)

from example_01 import run_example_01
from task_5_1 import run_task_5_1
from task_5_2 import run_task_5_2
from task_5_3 import run_task_5_3, manual_non_maximum_suppression
from task_5_4 import run_task_5_4
from task_5_5 import run_task_5_5, compute_pratt_fom


class TestExperiment05(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.img_path = os.path.join(exp_dir, "Inputs", "images", "CT.jpg")
        cls.img = cv2.imread(cls.img_path, cv2.IMREAD_GRAYSCALE)

    def test_01_input_image_loading(self):
        """Verify CT image exists, is readable, and has 512x512 resolution."""
        self.assertIsNotNone(self.img, "CT.jpg failed to load.")
        self.assertEqual(self.img.shape, (512, 512), "CT image must be 512x512.")
        self.assertTrue(self.img.dtype == np.uint8, "CT image must be 8-bit unsigned.")

    def test_02_zero_sum_kernels(self):
        """Verify that Prewitt and Sobel kernels sum to exactly 0.0."""
        # Prewitt
        px = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=float)
        py = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=float)
        self.assertAlmostEqual(np.sum(px), 0.0, places=7, msg="Prewitt Px kernel must sum to 0.0")
        self.assertAlmostEqual(np.sum(py), 0.0, places=7, msg="Prewitt Py kernel must sum to 0.0")

        # Sobel
        sx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
        sy = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float)
        self.assertAlmostEqual(np.sum(sx), 0.0, places=7, msg="Sobel Sx kernel must sum to 0.0")
        self.assertAlmostEqual(np.sum(sy), 0.0, places=7, msg="Sobel Sy kernel must sum to 0.0")

    def test_03_example_01_execution(self):
        """Verify Example 01 execution, edge counts, and thinning decision."""
        res = run_example_01()
        self.assertIn("Prewitt Operator", res)
        self.assertIn("Sobel Operator", res)
        self.assertIn("Canny Edge Detector", res)
        self.assertGreater(res["Prewitt Operator"]["count"], 0)
        self.assertGreater(res["Sobel Operator"]["count"], 0)
        self.assertGreater(res["Canny Edge Detector"]["count"], 0)
        # Canny must have fewer pixels than Sobel due to 1-pixel skeletonization
        self.assertLess(res["Canny Edge Detector"]["count"], res["Sobel Operator"]["count"])

    def test_04_task_5_1_directional_sensitivity(self):
        """Verify Task 5.1 directional gradient values and HSV map output."""
        res = run_task_5_1()
        self.assertGreater(res["max_Gx"], 500.0)
        self.assertGreater(res["max_Gy"], 500.0)
        self.assertGreater(res["max_mag"], 500.0)
        hsv_path = os.path.join(exp_dir, "Outputs", "Python", "exp05_task_5_1_hsv_orientation.png")
        self.assertTrue(os.path.exists(hsv_path), "HSV orientation output must exist.")

    def test_05_task_5_2_noise_sensitivity(self):
        """Verify Task 5.2 noise sensitivity benchmarking."""
        res = run_task_5_2()
        self.assertEqual(len(res["eval_thresholds"]), 4)
        self.assertEqual(len(res["prewitt_roi_rates"]), 4)
        self.assertEqual(len(res["sobel_roi_rates"]), 4)
        # Higher threshold should strictly decrease false edge rate
        for i in range(3):
            self.assertGreaterEqual(res["prewitt_roi_rates"][i], res["prewitt_roi_rates"][i+1])
            self.assertGreaterEqual(res["sobel_roi_rates"][i], res["sobel_roi_rates"][i+1])

    def test_06_task_5_3_manual_nms(self):
        """Verify Task 5.3 manual Non-Maximum Suppression algorithm."""
        # Test synthetic step ramp
        synth_mag = np.zeros((7, 7), dtype=float)
        synth_mag[:, 2] = 50.0
        synth_mag[:, 3] = 100.0  # Peak
        synth_mag[:, 4] = 50.0
        synth_theta = np.zeros((7, 7), dtype=float)  # Sector 0 (horizontal gradient)

        nms_synth, sec_synth = manual_non_maximum_suppression(synth_mag, synth_theta)
        # Peak at col 3 should be preserved, neighbors suppressed
        self.assertEqual(nms_synth[3, 3], 100.0)
        self.assertEqual(nms_synth[3, 2], 0.0)
        self.assertEqual(nms_synth[3, 4], 0.0)

        # Run real task
        res = run_task_5_3()
        self.assertGreater(res["thinning_percentage"], 50.0, "NMS must achieve >50% data reduction.")

    def test_07_task_5_4_hysteresis_tuning(self):
        """Verify Task 5.4 Canny hysteresis sweeps and sensitivity monotonic behavior."""
        res = run_task_5_4()
        self.assertEqual(len(res), 6)
        # Case A1 -> A3: increasing T_high with fixed T_low should decrease edge pixels
        self.assertGreater(res[0]["count"], res[1]["count"])
        self.assertGreater(res[1]["count"], res[2]["count"])

    def test_08_task_5_5_diagnostic_benchmark(self):
        """Verify Task 5.5 Pratt FOM and benchmark table export."""
        res = run_task_5_5()
        self.assertEqual(len(res), 3)
        # Check Canny has FOM >= 0.75
        canny_metrics = next(m for m in res if "Canny" in m["Operator"])
        self.assertGreaterEqual(canny_metrics["Pratts_FOM"], 0.75, "Canny FOM must meet 'Good to Go' >= 0.75")
        self.assertEqual(canny_metrics["Mean_Skeleton_Width_px"], 1.0)
        csv_path = os.path.join(exp_dir, "Tables", "task_5_5_edge_benchmark_summary.csv")
        self.assertTrue(os.path.exists(csv_path), "Summary CSV must exist.")

    def test_09_all_figures_exist(self):
        """Verify that all 12 publication-grade figures (6 Python, 6 MATLAB) exist and are non-empty."""
        fig_dir = os.path.join(exp_dir, "Figures")
        expected_figs = [
            "exp05_example_01_benchmark_py.png",
            "exp05_example_01_benchmark_m.png",
            "exp05_task_5_1_directional_gradients_py.png",
            "exp05_task_5_1_directional_gradients_m.png",
            "exp05_task_5_2_noise_sensitivity_py.png",
            "exp05_task_5_2_noise_sensitivity_m.png",
            "exp05_task_5_3_manual_nms_py.png",
            "exp05_task_5_3_manual_nms_m.png",
            "exp05_task_5_4_hysteresis_tuning_py.png",
            "exp05_task_5_4_hysteresis_tuning_m.png",
            "exp05_task_5_5_diagnostic_report_py.png",
            "exp05_task_5_5_diagnostic_report_m.png"
        ]
        for fig_name in expected_figs:
            p = os.path.join(fig_dir, fig_name)
            self.assertTrue(os.path.exists(p), f"Missing figure: {fig_name}")
            self.assertGreater(os.path.getsize(p), 10000, f"Figure too small / empty: {fig_name}")


if __name__ == "__main__":
    unittest.main()
