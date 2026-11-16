"""
Automated 9-Tier Unit Test Suite: Experiment 10
Region-Based Segmentation Using Seeded Region Growing and Watershed Transform
Student: Muhammad Ikrama (Reg ID: 60140)
Department of Biomedical Engineering, Riphah International University, Lahore
"""

import os
import unittest
import cv2
import numpy as np
import pandas as pd

class TestExperiment10(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.inputs_dir = os.path.join(cls.base_dir, "Inputs", "images")
        cls.tables_dir = os.path.join(cls.base_dir, "Tables")
        cls.outputs_py = os.path.join(cls.base_dir, "Outputs", "Python")
        cls.outputs_m = os.path.join(cls.base_dir, "Outputs", "MATLAB")
        cls.figures_dir = os.path.join(cls.base_dir, "Figures")

    def test_suite_01_input_integrity(self):
        """Test Suite 1: Input image resolution, bit depth, and presence"""
        mri_path = os.path.join(self.inputs_dir, "Brain_MRI.png")
        self.assertTrue(os.path.exists(mri_path), "Brain_MRI.png missing")
        mri = cv2.imread(mri_path, cv2.IMREAD_GRAYSCALE)
        self.assertIsNotNone(mri, "Failed to load Brain_MRI.png")
        self.assertEqual(mri.shape, (512, 512), "Brain_MRI must be 512x512")
        self.assertEqual(mri.dtype, np.uint8, "Brain_MRI must be uint8")
        
        # Check seed location inside tumor
        seed_val = mri[242, 327]
        self.assertGreaterEqual(seed_val, 180, f"Seed intensity {seed_val} too low for tumor core")

    def test_suite_02_qr_code_integrity(self):
        """Test Suite 2: GitHub repository QR code validation"""
        qr_path = os.path.join(self.figures_dir, "exp10_github_qr.png")
        self.assertTrue(os.path.exists(qr_path), "exp10_github_qr.png missing")
        qr_img = cv2.imread(qr_path)
        self.assertIsNotNone(qr_img, "Failed to read QR image")
        detector = cv2.QRCodeDetector()
        val, pts, _ = detector.detectAndDecode(qr_img)
        expected_url = "https://github.com/Muhammad-Ikrama/BMI_Processing_labs"
        self.assertEqual(val, expected_url, f"QR code decoded '{val}' does not match '{expected_url}'")

    def test_suite_03_srg_tolerance_sweep(self):
        """Test Suite 3: Seeded region growing tolerance sweep & optimal DSC"""
        csv_py = os.path.join(self.tables_dir, "exp10_benchmark_summary_py.csv")
        self.assertTrue(os.path.exists(csv_py), "Python benchmark summary CSV missing")
        df = pd.read_csv(csv_py)
        
        # Verify tolerances
        expected_tols = [12, 22, 38, 60, 85, 110]
        self.assertListEqual(list(df["Tolerance_T"]), expected_tols, "Tolerance list mismatch")
        
        # T=38 must be optimal (DSC >= 0.94)
        opt_row = df[df["Tolerance_T"] == 38].iloc[0]
        self.assertGreaterEqual(opt_row["DSC"], 0.94, f"Optimal DSC {opt_row['DSC']} below 0.94")
        self.assertGreaterEqual(opt_row["Jaccard_IoU"], 0.88, f"Optimal IoU {opt_row['Jaccard_IoU']} below 0.88")
        
        # T=12 must be under-grown (Area < 1000)
        under_row = df[df["Tolerance_T"] == 12].iloc[0]
        self.assertLess(under_row["Region_Area_px"], 1000, "T=12 not under-grown")
        
        # T=110 must leak into parenchyma (Area > 50,000)
        leak_row = df[df["Tolerance_T"] == 110].iloc[0]
        self.assertGreater(leak_row["Region_Area_px"], 50000, "T=110 failed to leak into parenchyma")
        self.assertLess(leak_row["DSC"], 0.15, "T=110 DSC too high for leaked mask")

    def test_suite_04_watershed_marker_control(self):
        """Test Suite 4: Marker-controlled watershed eliminates noise over-segmentation"""
        csv_sweep = os.path.join(self.tables_dir, "exp10_task_10_4_distance_sweep.csv")
        self.assertTrue(os.path.exists(csv_sweep), "Task 10.4 table missing")
        df = pd.read_csv(csv_sweep)
        
        # Optimal alpha = 0.35 must yield exactly 6 clean anatomical structures
        opt_alpha_row = df[df["Alpha_Factor"] == 0.35].iloc[0]
        self.assertEqual(int(opt_alpha_row["Watershed_Regions"]), 6, "Optimal watershed regions must be 6")
        self.assertEqual(int(opt_alpha_row["FG_Marker_Count"]), 6, "Optimal markers count must be 6")

    def test_suite_05_task_10_1_connectivity(self):
        """Test Suite 5: 4-connected vs 8-connected neighborhood metrics"""
        csv_path = os.path.join(self.tables_dir, "exp10_task_10_1_connectivity.csv")
        self.assertTrue(os.path.exists(csv_path), "Task 10.1 table missing")
        df = pd.read_csv(csv_path)
        
        self.assertEqual(len(df), 2, "Task 10.1 must contain 2 rows (4-conn and 8-conn)")
        self.assertGreater(df.loc[0, "Area_px"], 1000, "4-conn area non-positive")
        self.assertGreater(df.loc[1, "Area_px"], 1000, "8-conn area non-positive")
        self.assertGreaterEqual(df.loc[0, "DSC"], 0.90, "4-conn DSC below 0.90")
        self.assertGreaterEqual(df.loc[1, "DSC"], 0.90, "8-conn DSC below 0.90")

    def test_suite_06_task_10_2_predicate_rules(self):
        """Test Suite 6: Fixed seed stability vs running mean drift & leakage"""
        csv_path = os.path.join(self.tables_dir, "exp10_task_10_2_fixed_vs_running_mean.csv")
        self.assertTrue(os.path.exists(csv_path), "Task 10.2 table missing")
        df = pd.read_csv(csv_path)
        
        # At T=50, running mean must trigger catastrophic leakage (>80,000 px)
        mean_t50 = df[(df["Tolerance_T"] == 50) & (df["Predicate_Rule"] == "Running Mean")].iloc[0]
        fixed_t50 = df[(df["Tolerance_T"] == 50) & (df["Predicate_Rule"] == "Fixed Seed")].iloc[0]
        
        self.assertGreater(mean_t50["Area_px"], 80000, "Running mean did not leak at T=50")
        self.assertLess(fixed_t50["Area_px"], 5000, "Fixed seed leaked prematurely at T=50")

    def test_suite_07_task_10_3_seed_perturbation(self):
        """Test Suite 7: Seed placement robustness across 5 coordinates"""
        csv_path = os.path.join(self.tables_dir, "exp10_task_10_3_seed_perturbation.csv")
        self.assertTrue(os.path.exists(csv_path), "Task 10.3 table missing")
        df = pd.read_csv(csv_path)
        
        self.assertEqual(len(df), 5, "Task 10.3 must test 5 seeds")
        # Centroid must have DSC >= 0.95
        centroid_row = df[df["Seed_Location"] == "Centroid"].iloc[0]
        self.assertGreaterEqual(centroid_row["DSC"], 0.95, "Centroid DSC below 0.95")
        
        # Marginal Rim 2 must exhibit rim degradation
        rim2_row = df[df["Seed_Location"] == "Peripheral Rim 2"].iloc[0]
        self.assertLess(rim2_row["DSC"], 0.50, "Rim 2 did not show expected degradation")

    def test_suite_08_task_10_4_distance_sweep(self):
        """Test Suite 8: Distance transform threshold monotonic decrease"""
        csv_path = os.path.join(self.tables_dir, "exp10_task_10_4_distance_sweep.csv")
        self.assertTrue(os.path.exists(csv_path), "Task 10.4 table missing")
        df = pd.read_csv(csv_path)
        
        markers = list(df["FG_Marker_Count"])
        # Should be monotonically non-increasing
        self.assertTrue(all(x >= y for x, y in zip(markers, markers[1:])), "Marker count not monotonic with alpha")
        self.assertGreater(markers[0], 20, "Alpha=0.15 marker count too low")
        self.assertLessEqual(markers[-1], 3, "Alpha=0.75 marker count too high")

    def test_suite_09_task_10_5_lung_watershed(self):
        """Test Suite 9: Chest X-ray bilateral lung watershed separation"""
        csv_path = os.path.join(self.tables_dir, "exp10_task_10_5_chest_xray_watershed.csv")
        self.assertTrue(os.path.exists(csv_path), "Task 10.5 table missing")
        df = pd.read_csv(csv_path)
        
        self.assertEqual(len(df), 3, "Task 10.5 table must contain 3 rows")
        right_area = df.loc[0, "Area_px"]
        left_area = df.loc[1, "Area_px"]
        total_area = df.loc[2, "Area_px"]
        
        self.assertGreater(right_area, 0, "Right lung area non-positive")
        self.assertGreater(left_area, 0, "Left lung area non-positive")
        self.assertEqual(right_area + left_area, total_area, "Lobe area sum mismatch")
        
        thoracic_pct = df.loc[2, "Image_Percentage"]
        self.assertGreaterEqual(thoracic_pct, 15.0, "Thoracic coverage below 15%")
        self.assertLessEqual(thoracic_pct, 40.0, "Thoracic coverage above 40%")

if __name__ == "__main__":
    unittest.main()
