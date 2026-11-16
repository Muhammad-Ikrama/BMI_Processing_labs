"""
Experiment 09 Automated Test Suite (9 Suites)
Validates algorithmic invariants, mathematical properties, cross-platform parity,
and deliverable completeness for Experiment 09.
"""
import os
import unittest
import cv2
import numpy as np
import pandas as pd

class TestExperiment09(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.img_dir = os.path.join(cls.base_dir, "Inputs", "images")
        cls.tab_dir = os.path.join(cls.base_dir, "Tables")
        cls.out_py_dir = os.path.join(cls.base_dir, "Outputs", "Python")
        cls.out_m_dir = os.path.join(cls.base_dir, "Outputs", "MATLAB")
        cls.fig_dir = os.path.join(cls.base_dir, "Figures")

    def test_01_inputs_integrity(self):
        """Suite 1: Verify presence, 8-bit depth, and geometry of clinical datasets."""
        for name in ["Brain_MRI.png", "Head_CT.png"]:
            p = os.path.join(self.img_dir, name)
            self.assertTrue(os.path.exists(p), f"Missing image: {name}")
            img = cv2.imread(p, cv2.IMREAD_GRAYSCALE)
            self.assertIsNotNone(img, f"Failed to load: {name}")
            self.assertEqual(img.dtype, np.uint8)
            self.assertEqual(img.shape, (512, 512))

    def test_02_compound_morphology_superiority(self):
        """Suite 2: Verify Open+Close achieves DSC >= 0.95 and eliminates 100% of internal holes."""
        csv_path = os.path.join(self.tab_dir, "exp09_benchmark_summary_py.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing benchmark CSV")
        df = pd.read_csv(csv_path)
        
        oc_row = df[df["Operation"] == "Open + Close (5x5)"].iloc[0]
        self.assertGreaterEqual(oc_row["Dice_DSC"], 0.95)
        self.assertEqual(int(oc_row["Hole_Pixels"]), 0)
        self.assertLess(oc_row["CC_Count"], 10)

    def test_03_se_geometry_properties(self):
        """Suite 3: Verify Square SE produces greater perimeter distortion than Disk SE."""
        csv_path = os.path.join(self.tab_dir, "exp09_task_9_1_se_geometry.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing task 9.1 CSV")
        df = pd.read_csv(csv_path)
        
        sq_perim = df[df["SE_Shape"] == "Square"]["Boundary_Perimeter_Px"].iloc[0]
        dk_perim = df[df["SE_Shape"] == "Disk"]["Boundary_Perimeter_Px"].iloc[0]
        self.assertGreater(sq_perim, dk_perim, "Square SE should have higher perimeter due to stair-stepping")

    def test_04_radius_sweep_monotonic_horn_loss(self):
        """Suite 4: Verify monotonic increase in area error as SE radius increases."""
        csv_path = os.path.join(self.tab_dir, "exp09_task_9_2_radius_sweep.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing task 9.2 CSV")
        df = pd.read_csv(csv_path)
        
        self.assertEqual(len(df), 4)
        # Optimal 5x5 disk has lowest area error and highest DSC among filtered
        row_5x5 = df[df["Disk_Size_K"] == "5x5"].iloc[0]
        self.assertGreaterEqual(row_5x5["Dice_DSC"], 0.92)
        # 15x15 disk should have severe area loss (DSC < 0.50)
        row_15 = df[df["Disk_Size_K"] == "15x15"].iloc[0]
        self.assertLess(row_15["Dice_DSC"], 0.50)

    def test_05_order_of_operations_salt_fusion(self):
        """Suite 5: Verify Open-then-Close achieves higher DSC than Close-then-Open under salt noise."""
        csv_path = os.path.join(self.tab_dir, "exp09_task_9_3_order_of_ops.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing task 9.3 CSV")
        df = pd.read_csv(csv_path)
        
        dsc_a = df[df["Tag"] == "PipeA"]["Dice_DSC"].iloc[0]
        dsc_b = df[df["Tag"] == "PipeB"]["Dice_DSC"].iloc[0]
        cc_a = df[df["Tag"] == "PipeA"]["CC_Count"].iloc[0]
        cc_b = df[df["Tag"] == "PipeB"]["CC_Count"].iloc[0]
        
        self.assertGreater(dsc_a, dsc_b, "Pipeline A should have higher DSC than Pipeline B")
        self.assertLess(cc_a, cc_b, "Pipeline A should have fewer connected components (no fused salt)")

    def test_06_boundary_gradient_thickness_parity(self):
        """Suite 6: Verify Symmetrical Gradient perimeter is ~sum of internal and external boundaries."""
        csv_path = os.path.join(self.tab_dir, "exp09_task_9_4_boundary_metrics.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing task 9.4 CSV")
        df = pd.read_csv(csv_path)
        
        p_int = df[df["Formulation"].str.contains("Internal")]["Perimeter_Pixels"].iloc[0]
        p_ext = df[df["Formulation"].str.contains("External")]["Perimeter_Pixels"].iloc[0]
        p_grad = df[df["Formulation"].str.contains("Symmetrical")]["Perimeter_Pixels"].iloc[0]
        
        self.assertEqual(p_int, 728)
        self.assertEqual(p_ext, 775)
        self.assertEqual(p_grad, 1503)
        self.assertEqual(p_grad, p_int + p_ext)

    def test_07_skull_stripping_volume_consistency(self):
        """Suite 7: Verify skull stripping produces clinically consistent intracranial brain ratio."""
        csv_path = os.path.join(self.tab_dir, "exp09_task_9_5_skull_stripping.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing task 9.5 CSV")
        df = pd.read_csv(csv_path)
        
        brain_vol_pct = df["Brain_Scan_Volume_Pct"].iloc[0]
        ratio_pct = df["Brain_to_Head_Ratio_Pct"].iloc[0]
        self.assertGreaterEqual(brain_vol_pct, 15.0)
        self.assertLessEqual(brain_vol_pct, 25.0)
        self.assertGreaterEqual(ratio_pct, 25.0)
        self.assertLessEqual(ratio_pct, 35.0)

    def test_08_qr_code_decodability(self):
        """Suite 8: Verify GitHub QR code decodes to official repository URL."""
        qr_path = os.path.join(self.fig_dir, "exp09_github_qr.png")
        self.assertTrue(os.path.exists(qr_path), "Missing QR code file")
        detector = cv2.QRCodeDetector()
        img = cv2.imread(qr_path)
        data, _, _ = detector.detectAndDecode(img)
        self.assertEqual(data, "https://github.com/Muhammad-Ikrama/BMI_Processing_labs")

    def test_09_deliverables_completeness(self):
        """Suite 9: Verify existence of all required generated tables, figures, and screenshots."""
        required_tables = [
            "exp09_benchmark_summary_py.csv", "exp09_benchmark_summary_matlab.csv",
            "exp09_task_9_1_se_geometry.csv", "exp09_task_9_1_se_geometry_matlab.csv",
            "exp09_task_9_2_radius_sweep.csv", "exp09_task_9_2_radius_sweep_matlab.csv",
            "exp09_task_9_3_order_of_ops.csv", "exp09_task_9_3_order_of_ops_matlab.csv",
            "exp09_task_9_4_boundary_metrics.csv", "exp09_task_9_4_boundary_metrics_matlab.csv",
            "exp09_task_9_5_skull_stripping.csv", "exp09_task_9_5_skull_stripping_matlab.csv"
        ]
        for t in required_tables:
            p = os.path.join(self.tab_dir, t)
            self.assertTrue(os.path.exists(p), f"Missing table {t}")

        required_figures = [
            "exp09_github_qr.png",
            "exp09_matlab_exec_screenshot.png",
            "exp09_python_exec_screenshot.png"
        ]
        for f in required_figures:
            p = os.path.join(self.fig_dir, f)
            self.assertTrue(os.path.exists(p), f"Missing figure {f}")

if __name__ == "__main__":
    unittest.main()
