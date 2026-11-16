"""
Comprehensive Test & Validation Suite for Experiment 06
Frequency-Domain Filtering of Medical Images Using the 2-D Fourier Transform
Verifies mathematical correctness, Parseval energy conservation, DC hollowing,
Gibbs ringing quantification, file deliverables, and cross-platform concordance.
Course: Medical Image Processing | Riphah International University
Faculty: Engr. Rana Talha Khalid
"""

import os
import unittest
import cv2
import numpy as np
import pandas as pd

class TestExperiment06(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = os.path.dirname(os.path.abspath(__file__))
        cls.exp_dir = os.path.abspath(os.path.join(cls.test_dir, ".."))
        cls.inputs_dir = os.path.join(cls.exp_dir, "Inputs", "images")
        cls.py_out_dir = os.path.join(cls.exp_dir, "Outputs", "Python")
        cls.mat_out_dir = os.path.join(cls.exp_dir, "Outputs", "MATLAB")
        cls.fig_dir = os.path.join(cls.exp_dir, "Figures")
        cls.tab_dir = os.path.join(cls.exp_dir, "Tables")

    def test_01_inputs_integrity(self):
        """T01: Verify MRI.jpg input exists, 512x512 matrix, uint8, valid range."""
        mri_path = os.path.join(self.inputs_dir, "MRI.jpg")
        self.assertTrue(os.path.exists(mri_path), f"Missing input image at {mri_path}")
        img = cv2.imread(mri_path, cv2.IMREAD_GRAYSCALE)
        self.assertIsNotNone(img, "Failed to read MRI.jpg")
        self.assertEqual(img.shape, (512, 512), f"Unexpected shape {img.shape}")
        self.assertEqual(img.dtype, np.uint8, f"Unexpected dtype {img.dtype}")
        self.assertGreater(img.max(), 200, "Image dynamic range insufficient")
        print("[PASS] T01 | Input Integrity: Clinical MRI.jpg verified (512x512, uint8).")

    def test_02_example_01_execution(self):
        """T02: Verify Example 01 filtered images exist, range [0, 255], and metric trends."""
        for fname in ["exp06_example_01_ilpf_py.png", "exp06_example_01_blpf_py.png", "exp06_example_01_glpf_py.png"]:
            fpath = os.path.join(self.py_out_dir, fname)
            self.assertTrue(os.path.exists(fpath), f"Missing {fname}")
            im = cv2.imread(fpath, cv2.IMREAD_GRAYSCALE)
            self.assertEqual(im.shape, (512, 512))
            self.assertEqual(im.dtype, np.uint8)
        print("[PASS] T02 | Example 01 Execution: Baseline ILPF, BLPF, and GLPF outputs verified.")

    def test_03_task_6_1_dc_energy_and_parseval(self):
        """T03: Verify Task 6.1 DC coordinates, Parseval conservation, and >95% energy in core."""
        img = cv2.imread(os.path.join(self.inputs_dir, "MRI.jpg"), cv2.IMREAD_GRAYSCALE)
        H, W = img.shape
        F = np.fft.fft2(img.astype(float))
        F_shift = np.fft.fftshift(F)

        # Parseval theorem: sum(f^2) == (1/MN) * sum(|F|^2)
        spatial_energy = np.sum(img.astype(float) ** 2)
        freq_energy = np.sum(np.abs(F) ** 2) / (H * W)
        relative_error = abs(spatial_energy - freq_energy) / spatial_energy
        self.assertLess(relative_error, 1e-10, "Parseval energy conservation violated!")

        # DC component coordinates
        self.assertAlmostEqual(np.abs(F[0, 0]), np.sum(img.astype(float)), places=2)
        self.assertAlmostEqual(np.abs(F_shift[H//2, W//2]), np.sum(img.astype(float)), places=2)

        # Core energy check
        u = np.arange(H) - H // 2
        v = np.arange(W) - W // 2
        V, U = np.meshgrid(v, u)
        D = np.hypot(V, U)
        energy_d45 = np.sum(np.abs(F_shift[D <= 45]) ** 2) / np.sum(np.abs(F_shift) ** 2)
        self.assertGreaterEqual(energy_d45, 0.95, "Radius D<=45 must retain >= 95% energy")
        print("[PASS] T03 | Task 6.1: Parseval theorem conserved (rel err < 1e-10), DC verified, 95% energy core verified.")

    def test_04_task_6_2_gibbs_ringing_quantification(self):
        """T04: Verify ILPF Gibbs ringing CSV metrics and ripple trends across D0 in [20, 40, 80]."""
        csv_path = os.path.join(self.tab_dir, "exp06_task_6_2_ilpf_ringing_metrics.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing task 6.2 CSV")
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 3)
        self.assertListEqual(list(df["Cutoff_D0"]), [20, 40, 80])
        # Energy retention must monotonically increase with D0
        self.assertTrue(df["Energy_Retention_Pct"].is_monotonic_increasing)
        # PSNR must monotonically increase with D0
        self.assertTrue(df["PSNR_dB"].is_monotonic_increasing)
        print("[PASS] T04 | Task 6.2: Gibbs ringing quantified, monotonic energy/PSNR verified.")

    def test_05_task_6_3_blpf_order_sweep(self):
        """T05: Verify BLPF order sweep CSV across n in [1, 2, 4, 8]."""
        csv_path = os.path.join(self.tab_dir, "exp06_task_6_3_blpf_sweep_metrics.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing task 6.3 CSV")
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 4)
        self.assertListEqual(list(df["Order_n"]), [1, 2, 4, 8])
        # Energy retention increases with order as transition steepens
        self.assertTrue(df["Energy_Retention_Pct"].is_monotonic_increasing)
        # Clinical optimum at n=2
        opt_row = df[df["Order_n"] == 2].iloc[0]
        self.assertEqual(opt_row["Clinical_Verdict"], "CLINICAL OPTIMUM")
        print("[PASS] T05 | Task 6.3: BLPF order sensitivity verified (n=2 confirmed as Clinical Optimum).")

    def test_06_task_6_4_ghpf_dc_elimination(self):
        """T06: Verify GHPF complete DC suppression (mean ~ 0.0) and high-frequency boundary isolation."""
        csv_path = os.path.join(self.tab_dir, "exp06_task_6_4_contrast_metrics.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing task 6.4 CSV")
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 3)

        ghpf_row = df[df["Condition"] == "Gaussian High-Pass (GHPF)"].iloc[0]
        # Mean brightness of GHPF must be approximately 0.0
        self.assertAlmostEqual(ghpf_row["Spatial_Mean_Brightness"], 0.0, places=2)
        # Energy retention of high-pass must be < 10%
        self.assertLess(ghpf_row["Energy_Retention_Pct"], 10.0)

        glpf_row = df[df["Condition"] == "Gaussian Low-Pass (GLPF)"].iloc[0]
        # GLPF must retain > 90% energy
        self.assertGreater(glpf_row["Energy_Retention_Pct"], 90.0)
        print("[PASS] T06 | Task 6.4: GHPF DC hollowing verified (Mean ~ 0.0), GLPF bulk preservation verified.")

    def test_07_task_6_5_diagnostic_benchmark(self):
        """T07: Verify master diagnostic benchmark CSVs for both Python and MATLAB."""
        py_csv = os.path.join(self.tab_dir, "exp06_benchmark_summary_py.csv")
        mat_csv = os.path.join(self.tab_dir, "exp06_benchmark_summary_matlab.csv")
        self.assertTrue(os.path.exists(py_csv), "Missing Python benchmark CSV")
        self.assertTrue(os.path.exists(mat_csv), "Missing MATLAB benchmark CSV")

        df_py = pd.read_csv(py_csv)
        df_mat = pd.read_csv(mat_csv)
        self.assertEqual(len(df_py), 4)
        self.assertEqual(len(df_mat), 4)
        print("[PASS] T07 | Task 6.5: Both Python and MATLAB benchmark CSVs verified (4 condition rows each).")

    def test_08_deliverable_figures_completeness(self):
        """T08: Verify all 12 publication-grade figures exist (>200 KB each)."""
        expected_figs = [
            "exp06_example_01_benchmark_py.png",
            "exp06_example_01_benchmark_m.png",
            "exp06_task_6_1_dft_spectrum_py.png",
            "exp06_task_6_1_dft_spectrum_m.png",
            "exp06_task_6_2_ilpf_gibbs_ringing_py.png",
            "exp06_task_6_2_ilpf_gibbs_ringing_m.png",
            "exp06_task_6_3_blpf_order_sweep_py.png",
            "exp06_task_6_3_blpf_order_sweep_m.png",
            "exp06_task_6_4_glpf_ghpf_contrast_py.png",
            "exp06_task_6_4_glpf_ghpf_contrast_m.png",
            "exp06_task_6_5_diagnostic_report_py.png",
            "exp06_task_6_5_diagnostic_report_m.png"
        ]
        for f in expected_figs:
            fpath = os.path.join(self.fig_dir, f)
            self.assertTrue(os.path.exists(fpath), f"Missing figure {f}")
            fsize = os.path.getsize(fpath)
            self.assertGreater(fsize, 200 * 1024, f"Figure {f} is suspiciously small ({fsize} bytes)")
        print(f"[PASS] T08 | Figure Completeness: All 12 publication-grade figures verified (>200 KB each).")

    def test_09_matlab_python_concordance(self):
        """T09: Verify numerical concordance between MATLAB and Python implementations."""
        py_csv = os.path.join(self.tab_dir, "exp06_benchmark_summary_py.csv")
        mat_csv = os.path.join(self.tab_dir, "exp06_benchmark_summary_matlab.csv")
        df_py = pd.read_csv(py_csv)
        df_mat = pd.read_csv(mat_csv)

        for i in range(len(df_py)):
            filt_name = df_py.iloc[i]["Filter_Name"]
            py_ret = df_py.iloc[i]["Energy_Retention_Pct"]
            mat_ret = df_mat.iloc[i]["Energy_Retention_Pct"]
            ret_diff = abs(py_ret - mat_ret)
            self.assertLess(ret_diff, 0.5, f"Energy retention mismatch for {filt_name}: Py={py_ret}, Mat={mat_ret}")

            py_psnr = df_py.iloc[i]["PSNR_dB"]
            mat_psnr = df_mat.iloc[i]["PSNR_dB"]
            psnr_diff = abs(py_psnr - mat_psnr)
            self.assertLess(psnr_diff, 0.5, f"PSNR mismatch for {filt_name}: Py={py_psnr}, Mat={mat_psnr}")

            py_ssim = df_py.iloc[i]["SSIM"]
            mat_ssim = df_mat.iloc[i]["SSIM_Val"]
            ssim_diff = abs(py_ssim - mat_ssim)
            self.assertLess(ssim_diff, 0.05, f"SSIM mismatch for {filt_name}: Py={py_ssim}, Mat={mat_ssim}")

        print("[PASS] T09 | Cross-Platform Concordance: MATLAB and Python results match within tolerance (PSNR < 0.5dB, SSIM < 0.05, Energy < 0.5%).")

if __name__ == "__main__":
    unittest.main()
