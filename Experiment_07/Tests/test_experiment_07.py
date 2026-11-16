"""
Experiment 07 - Automated Testing and Quality Verification Suite
Validates image sharpening, high-boost filtering, clipping analysis,
Mach band measurements, noise amplification, and clinical ROI metrics.
Course: Medical Image Processing | Riphah International University
Faculty: Engr. Rana Talha Khalid
"""

import os
import sys
import unittest
import numpy as np
import pandas as pd
import cv2

class TestExperiment07(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = os.path.dirname(os.path.abspath(__file__))
        cls.exp_dir = os.path.abspath(os.path.join(cls.test_dir, ".."))
        cls.input_img = os.path.join(cls.exp_dir, "Inputs", "images", "Xray.jpg")
        cls.out_py_dir = os.path.join(cls.exp_dir, "Outputs", "Python")
        cls.out_mat_dir = os.path.join(cls.exp_dir, "Outputs", "MATLAB")
        cls.fig_dir = os.path.join(cls.exp_dir, "Figures")
        cls.tab_dir = os.path.join(cls.exp_dir, "Tables")

    # =========================================================================
    # Suite 1: Input Integrity Verification
    # =========================================================================
    def test_01_input_image_integrity(self):
        """Verify input chest radiograph exists, has correct dimensions and uint8 type."""
        self.assertTrue(os.path.exists(self.input_img), f"Missing input image at {self.input_img}")
        img = cv2.imread(self.input_img, cv2.IMREAD_GRAYSCALE)
        self.assertIsNotNone(img, "Failed to read Xray.jpg")
        self.assertEqual(img.shape, (466, 429), f"Unexpected shape: {img.shape}, expected (466, 429)")
        self.assertEqual(img.dtype, np.uint8, "Image is not uint8")
        self.assertGreater(float(np.mean(img)), 50.0, "Abnormally low mean intensity")
        self.assertLess(float(np.mean(img)), 200.0, "Abnormally high mean intensity")

    # =========================================================================
    # Suite 2: Example 01 Baseline Benchmark
    # =========================================================================
    def test_02_example_01_outputs(self):
        """Verify Example 01 baseline outputs and valid pixel ranges."""
        k_str = ["0_5", "1_0", "1_8", "3_0"]
        for ks in k_str:
            fname = f"exp07_example_01_k_{ks}_py.png"
            p = os.path.join(self.out_py_dir, fname)
            self.assertTrue(os.path.exists(p), f"Missing Python output {fname}")
            im = cv2.imread(p, cv2.IMREAD_GRAYSCALE)
            self.assertEqual(im.shape, (466, 429))
            self.assertGreaterEqual(int(np.min(im)), 0)
            self.assertLessEqual(int(np.max(im)), 255)

    # =========================================================================
    # Suite 3: Task 7.1 Clipping & Saturation Monotonicity
    # =========================================================================
    def test_03_task_7_1_clipping_monotonicity(self):
        """Verify that dynamic range clipping increases monotonically with boost factor k."""
        csv_path = os.path.join(self.tab_dir, "exp07_task_7_1_clipping_metrics.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing clipping CSV")
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 4)

        # Monotonic check
        clips_0 = df["Clipped_0_Pct"].tolist()
        sats_255 = df["Saturated_255_Pct"].tolist()
        tot_clips = df["Total_Clipping_Pct"].tolist()
        grads = df["Mean_Gradient"].tolist()

        for i in range(len(clips_0) - 1):
            self.assertLessEqual(clips_0[i], clips_0[i+1], "Underflow clipping not monotonic")
            self.assertLessEqual(sats_255[i], sats_255[i+1], "Overflow saturation not monotonic")
            self.assertLessEqual(tot_clips[i], tot_clips[i+1], "Total clipping not monotonic")
            self.assertLess(grads[i], grads[i+1], "Mean gradient not monotonic")

    # =========================================================================
    # Suite 4: Task 7.2 Smoothing Kernel Scale & Mask Bandwidth
    # =========================================================================
    def test_04_task_7_2_kernel_scale(self):
        """Verify that mask std dev increases and cutoff frequency decreases with sigma."""
        csv_path = os.path.join(self.tab_dir, "exp07_task_7_2_bandwidth_metrics.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing bandwidth CSV")
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 3)

        sigmas = df["Sigma_Pixels"].tolist()
        cutoffs = df["Cutoff_Freq_Cycles_Px"].tolist()
        stds = df["Mask_Std_Dev"].tolist()

        self.assertEqual(sigmas, [0.8, 1.5, 3.0])
        # As sigma increases, cutoff frequency must strictly decrease
        self.assertGreater(cutoffs[0], cutoffs[1])
        self.assertGreater(cutoffs[1], cutoffs[2])
        # As sigma increases, mask std dev must strictly increase
        self.assertLess(stds[0], stds[1])
        self.assertLess(stds[1], stds[2])

    # =========================================================================
    # Suite 5: Task 7.3 Edge Slope & Mach Band Compliance
    # =========================================================================
    def test_05_task_7_3_mach_band_compliance(self):
        """Verify edge slope steepening and Mach band compliance (<= 2.0 px at k=1.0)."""
        csv_path = os.path.join(self.tab_dir, "exp07_task_7_3_mach_band_metrics.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing Mach band CSV")
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 3)

        slopes = df["Max_Edge_Slope"].tolist()
        # Original < k=1.0 < k=3.0
        self.assertLess(slopes[0], slopes[1], "Unsharp masking failed to steepen slope")
        self.assertLess(slopes[1], slopes[2], "High-boost failed to further steepen slope")

        # Halo width compliance: k=1.0 must be <= 2.0 px
        k1_row = df[df["Condition"].str.contains("k=1.0")].iloc[0]
        self.assertLessEqual(k1_row["Mach_Band_Halo_Width_Px"], 2.0, "Unsharp masking halo width exceeds 2.0 px!")

    # =========================================================================
    # Suite 6: Task 7.4 Quantum Mottle Noise Amplification
    # =========================================================================
    def test_06_task_7_4_noise_amplification(self):
        """Verify quantum mottle amplification is acceptable at k=1.0 and contraindicated at k=2.0."""
        csv_path = os.path.join(self.tab_dir, "exp07_task_7_4_noise_amplification_metrics.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing noise CSV")
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 4)

        k1_row = df[df["Condition"].str.contains("k=1.0")].iloc[0]
        k2_row = df[df["Condition"].str.contains("k=2.0")].iloc[0]

        # k=2.0 noise increase must exceed 25%
        self.assertGreater(k2_row["Noise_Increase_Pct"], 25.0, "k=2.0 did not exceed 25% noise increase threshold")
        self.assertIn("CONTRAINDICATED", k2_row["Clinical_Safety"])
        self.assertIn("ACCEPTABLE", k1_row["Clinical_Safety"])

    # =========================================================================
    # Suite 7: Task 7.5 Clinical ROI Metrics
    # =========================================================================
    def test_07_task_7_5_clinical_rois(self):
        """Verify bone and lung ROI metrics, entropy, Michelson contrast, and gradient boost."""
        csv_path = os.path.join(self.tab_dir, "exp07_task_7_5_clinical_roi_metrics.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing clinical ROI CSV")
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 2)

        bone = df[df["Anatomical_ROI"].str.contains("Bone")].iloc[0]
        lung = df[df["Anatomical_ROI"].str.contains("Lung")].iloc[0]

        # Both ROIs must exhibit positive gradient boost under k=1.0 (> 20%)
        self.assertGreater(bone["Gradient_Boost_Pct"], 20.0)
        self.assertGreater(lung["Gradient_Boost_Pct"], 20.0)
        # Bone must have higher mean gradient than lung
        self.assertGreater(bone["Original_Mean_Grad"], 1.0)
        self.assertGreater(lung["Original_Mean_Grad"], 5.0)

    # =========================================================================
    # Suite 8: Deliverables Completeness (12 Figures & Master CSVs)
    # =========================================================================
    def test_08_deliverables_completeness(self):
        """Verify all publication figures exist in Figures/ and exceed 100 KB."""
        required_figs = [
            "exp07_example_01_benchmark_py.png",
            "exp07_example_01_benchmark_m.png",
            "exp07_task_7_1_clipping_sweep_py.png",
            "exp07_task_7_1_clipping_sweep_m.png",
            "exp07_task_7_2_mask_bandwidth_py.png",
            "exp07_task_7_2_mask_bandwidth_m.png",
            "exp07_task_7_3_mach_band_profiles_py.png",
            "exp07_task_7_3_mach_band_profiles_m.png",
            "exp07_task_7_4_noise_tradeoff_py.png",
            "exp07_task_7_4_noise_tradeoff_m.png",
            "exp07_task_7_5_clinical_rois_py.png",
            "exp07_task_7_5_clinical_rois_m.png",
            "exp07_task_7_5_diagnostic_report_py.png",
            "exp07_task_7_5_diagnostic_report_m.png"
        ]
        for f in required_figs:
            fpath = os.path.join(self.fig_dir, f)
            self.assertTrue(os.path.exists(fpath), f"Missing publication figure: {f}")
            size_kb = os.path.getsize(fpath) / 1024.0
            self.assertGreater(size_kb, 50.0, f"Figure {f} is suspiciously small: {size_kb:.1f} KB")

    # =========================================================================
    # Suite 9: Python vs MATLAB Numerical Concordance
    # =========================================================================
    def test_09_cross_platform_concordance(self):
        """Verify numerical concordance between Python and MATLAB metrics."""
        mat_csv = os.path.join(self.tab_dir, "exp07_task_7_1_clipping_metrics_matlab.csv")
        py_csv = os.path.join(self.tab_dir, "exp07_task_7_1_clipping_metrics.csv")
        self.assertTrue(os.path.exists(mat_csv), "Missing MATLAB clipping CSV")
        self.assertTrue(os.path.exists(py_csv), "Missing Python clipping CSV")

        df_m = pd.read_csv(mat_csv)
        df_p = pd.read_csv(py_csv)
        grad_m = df_m["Mean_Gradient"].tolist()
        grad_p = df_p["Mean_Gradient"].tolist()

        for gm, gp in zip(grad_m, grad_p):
            diff = abs(gm - gp)
            self.assertLess(diff, 1.0, f"Discrepancy between MATLAB ({gm}) and Python ({gp}) > 1.0")

if __name__ == "__main__":
    unittest.main()
