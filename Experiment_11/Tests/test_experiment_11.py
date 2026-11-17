"""
Automated 9-Tier Unit & Verification Test Suite: Experiment 11
Course: Medical Image Processing (BMI-701) | Riphah International University
Student: Muhammad Ikrama (Reg ID: 60140)
Instructor: Engr. Rana Talha Khalid
"""

import os
import unittest
import cv2
import numpy as np
import pandas as pd

class TestExperiment11(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = os.path.dirname(os.path.abspath(__file__))
        cls.exp_dir = os.path.abspath(os.path.join(cls.test_dir, ".."))
        cls.inputs_dir = os.path.join(cls.exp_dir, "Inputs", "images")
        cls.outputs_py = os.path.join(cls.exp_dir, "Outputs", "Python")
        cls.outputs_mat = os.path.join(cls.exp_dir, "Outputs", "MATLAB")
        cls.tables_dir = os.path.join(cls.exp_dir, "Tables")
        cls.fig_dir = os.path.join(cls.exp_dir, "Figures")

    def test_01_inputs_integrity(self):
        """Tier 1: Verify input images exist, correct dimensions, and dynamic ranges."""
        mri_path = os.path.join(self.inputs_dir, "Brain_MRI.png")
        ct_path = os.path.join(self.inputs_dir, "Head_CT.png")
        self.assertTrue(os.path.exists(mri_path), "Brain_MRI.png missing from Inputs/images")
        self.assertTrue(os.path.exists(ct_path), "Head_CT.png missing from Inputs/images")
        
        mri = cv2.imread(mri_path, cv2.IMREAD_GRAYSCALE)
        ct = cv2.imread(ct_path, cv2.IMREAD_GRAYSCALE)
        self.assertEqual(mri.shape, (512, 512), "Brain_MRI dimensions must be 512x512")
        self.assertEqual(ct.shape, (512, 512), "Head_CT dimensions must be 512x512")
        self.assertGreater(mri.max(), 180, "Brain MRI must contain high-intensity focal lesion")
        self.assertGreater(ct.max(), 200, "Head CT must contain high-intensity cortical bone")

    def test_02_qr_code_integrity(self):
        """Tier 2: Verify verified GitHub QR code exists and decodes correctly."""
        qr_path = os.path.join(self.fig_dir, "exp11_github_qr.png")
        self.assertTrue(os.path.exists(qr_path), "GitHub QR code image missing")
        qr_img = cv2.imread(qr_path)
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(qr_img)
        self.assertEqual(data.strip(), "https://github.com/Muhammad-Ikrama/BMI_Processing_labs",
                         "QR code must point to official course repository")

    def test_03_benchmark_convergence(self):
        """Tier 3: Verify parametric active contour benchmark convergence and DSC >= 0.95."""
        py_csv = os.path.join(self.tables_dir, "exp11_benchmark_summary_py.csv")
        mat_csv = os.path.join(self.tables_dir, "exp11_benchmark_summary_matlab.csv")
        self.assertTrue(os.path.exists(py_csv), "Python benchmark summary CSV missing")
        self.assertTrue(os.path.exists(mat_csv), "MATLAB benchmark summary CSV missing")
        
        df_py = pd.read_csv(py_csv)
        df_mat = pd.read_csv(mat_csv)
        dsc_col_py = "DSC" if "DSC" in df_py.columns else "Dice_DSC"
        dsc_col_mat = "Dice_DSC" if "Dice_DSC" in df_mat.columns else "DSC"
        
        self.assertGreaterEqual(float(df_py.iloc[-1][dsc_col_py]), 0.95,
                                "Python final DSC must achieve >= 0.95")
        self.assertGreaterEqual(float(df_mat.iloc[-1][dsc_col_mat]), 0.95,
                                "MATLAB final DSC must achieve >= 0.95")
        self.assertLess(float(df_py.iloc[-1]["E_total"]), -90.0,
                        "Python total energy should settle in potential minimum")
        self.assertLess(float(df_mat.iloc[-1]["E_total"]), -90.0,
                        "MATLAB total energy should settle in potential minimum")

    def test_04_alpha_beta_sensitivity(self):
        """Tier 4: Verify elasticity and stiffness parameter sweep metrics."""
        csv_path = os.path.join(self.tables_dir, "exp11_task_11_1_alpha_beta.csv")
        self.assertTrue(os.path.exists(csv_path), "Task 11.1 table missing")
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 3, "Task 11.1 must evaluate exactly 3 regimes")
        
        area_col = "Segmented_Area" if "Segmented_Area" in df.columns else "Area_px"
        ht_area = float(df[df["Regime_Name"].str.contains("High Tension")][area_col].values[0])
        bal_area = float(df[df["Regime_Name"].str.contains("Balanced")][area_col].values[0])
        self.assertLess(ht_area, bal_area, "High tension (alpha=0.80) must produce over-shrinkage")

    def test_05_capture_range_behavior(self):
        """Tier 5: Verify capture range and initial contour radius evaluation."""
        csv_path = os.path.join(self.tables_dir, "exp11_task_11_2_capture_range.csv")
        self.assertTrue(os.path.exists(csv_path), "Task 11.2 table missing")
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 5, "Task 11.2 must evaluate 5 configurations")
        
        dsc_col = "DSC" if "DSC" in df.columns else "Final_DSC"
        r28_dsc = float(df[df["Configuration"].str.contains("r0=28")][dsc_col].values[0])
        r38_dsc = float(df[df["Configuration"].str.contains("r0=38")][dsc_col].values[0])
        self.assertGreaterEqual(r28_dsc, 0.95, "r0=28 px must converge with DSC >= 0.95")
        self.assertGreaterEqual(r38_dsc, 0.95, "r0=38 px must converge with DSC >= 0.95")
        
        r70_stall_dsc = float(df[df["Configuration"].str.contains("Outside Capture sigma=12")][dsc_col].values[0])
        self.assertLess(r70_stall_dsc, 0.35, "r0=70 with sigma=12 must stall outside capture range")

    def test_06_broken_boundary_bridging(self):
        """Tier 6: Verify broken boundary bridging demonstrates elastic bridging vs SRG leakage."""
        csv_path = os.path.join(self.tables_dir, "exp11_task_11_3_broken_boundary.csv")
        self.assertTrue(os.path.exists(csv_path), "Task 11.3 table missing")
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 2, "Task 11.3 must compare SRG and Snake")
        
        srg_row = df[df["Method"].str.contains("Seeded Region Growing")].iloc[0]
        snake_row = df[df["Method"].str.contains("Active Contour")].iloc[0]
        self.assertIn("Leakage", srg_row["Clinical_Outcome"], "SRG must exhibit boundary leakage")
        self.assertIn("Bridging", snake_row["Clinical_Outcome"], "Snake must exhibit elastic bridging")

    def test_07_edge_vs_chan_vese_noise(self):
        """Tier 7: Verify noise robustness comparison under thermal noise."""
        csv_path = os.path.join(self.tables_dir, "exp11_task_11_4_edge_vs_chan_vese.csv")
        self.assertTrue(os.path.exists(csv_path), "Task 11.4 table missing")
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 2, "Task 11.4 must compare Edge and Chan-Vese")
        
        cv_dsc = float(df[df["Model_Type"].str.contains("Chan-Vese")]["DSC"].values[0])
        edge_dsc = float(df[df["Model_Type"].str.contains("Edge-Based")]["DSC"].values[0])
        self.assertGreater(cv_dsc, edge_dsc, "Chan-Vese region model must outperform Edge snake under heavy noise")

    def test_08_head_ct_skull_extraction(self):
        """Tier 8: Verify Head CT calvarium contraction and locking."""
        csv_path = os.path.join(self.tables_dir, "exp11_task_11_5_head_ct_skull.csv")
        self.assertTrue(os.path.exists(csv_path), "Task 11.5 table missing")
        df = pd.read_csv(csv_path)
        self.assertEqual(len(df), 3, "Task 11.5 must evaluate iterations 30, 60, 100")
        
        final_area = float(df.iloc[-1]["Enclosed_Area_px"])
        self.assertGreater(final_area, 150000, "Final skull area must enclose intracranial vault")
        self.assertEqual(df.iloc[-1]["Status"].strip(), "Locked on Outer Skull",
                         "Final iteration status must be Locked on Outer Skull")

    def test_09_artifacts_and_figures_completeness(self):
        """Tier 9: Verify all execution screenshots, figures, and plots are generated and non-empty."""
        expected_figs = [
            os.path.join(self.fig_dir, "exp11_github_qr.png"),
            os.path.join(self.fig_dir, "exp11_python_exec_screenshot.png"),
            os.path.join(self.fig_dir, "exp11_matlab_exec_screenshot.png"),
            os.path.join(self.outputs_py, "exp11_potential_and_energy_curve.png"),
            os.path.join(self.outputs_py, "exp11_benchmark_clinical_comparison.png"),
            os.path.join(self.outputs_py, "exp11_task_11_1_alpha_beta.png"),
            os.path.join(self.outputs_py, "exp11_task_11_2_capture_range.png"),
            os.path.join(self.outputs_py, "exp11_task_11_3_broken_boundary.png"),
            os.path.join(self.outputs_py, "exp11_task_11_4_edge_vs_chan_vese.png"),
            os.path.join(self.outputs_py, "exp11_task_11_5_head_ct_skull.png"),
            os.path.join(self.outputs_mat, "exp11_matlab_benchmark_evolution.png"),
            os.path.join(self.outputs_mat, "exp11_matlab_task11_1_sensitivity.png"),
            os.path.join(self.outputs_mat, "exp11_matlab_task11_2_capture_range.png"),
            os.path.join(self.outputs_mat, "exp11_matlab_task11_3_bridging.png"),
            os.path.join(self.outputs_mat, "exp11_matlab_task11_4_noise_robustness.png"),
            os.path.join(self.outputs_mat, "exp11_matlab_task11_5_skull_extraction.png")
        ]
        for f in expected_figs:
            self.assertTrue(os.path.exists(f), f"Expected figure missing: {f}")
            self.assertGreater(os.path.getsize(f), 500, f"Figure file too small: {f}")

if __name__ == "__main__":
    unittest.main()
