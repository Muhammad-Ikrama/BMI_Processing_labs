"""
Automated 9-Tier Unit & Verification Test Suite: Experiment 12
Course: Medical Image Processing (BMI-701) | Riphah International University
Student: Muhammad Ikrama (Reg ID: 60140)
Instructor: Engr. Rana Talha Khalid
"""

import os
import unittest
import cv2
import numpy as np
import pandas as pd

class TestExperiment12(unittest.TestCase):
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
        """Tier 1: Verify all multi-modal input scans exist, correct dimensions, and dynamic ranges."""
        images = ["Brain_MRI.png", "Head_CT.png", "Brain_PET_Aligned.png", "Brain_PET_Moving.png"]
        for img_name in images:
            img_path = os.path.join(self.inputs_dir, img_name)
            self.assertTrue(os.path.exists(img_path), f"Input scan missing: {img_name}")
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            self.assertEqual(img.shape, (512, 512), f"Dimensions must be 512x512: {img_name}")
            self.assertGreater(img.max(), 180, f"Dynamic range must contain hyperintense structures: {img_name}")

    def test_02_qr_code_integrity(self):
        """Tier 2: Verify verified GitHub QR code exists and decodes correctly."""
        qr_path = os.path.join(self.fig_dir, "exp12_github_qr.png")
        self.assertTrue(os.path.exists(qr_path), "GitHub QR code image missing")
        qr_img = cv2.imread(qr_path)
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(qr_img)
        self.assertEqual(data.strip(), "https://github.com/Muhammad-Ikrama/BMI_Processing_labs",
                         "QR code must point to official course repository")

    def test_03_benchmark_mutual_information(self):
        """Tier 3: Verify multi-modal benchmark MI >= 1.40 bits and Tumor DSC >= 0.90."""
        py_csv = os.path.join(self.tables_dir, "exp12_benchmark_summary_py.csv")
        mat_csv = os.path.join(self.tables_dir, "exp12_benchmark_summary_matlab.csv")
        self.assertTrue(os.path.exists(py_csv), "Python benchmark summary CSV missing")
        self.assertTrue(os.path.exists(mat_csv), "MATLAB benchmark summary CSV missing")
        
        df_py = pd.read_csv(py_csv)
        df_mat = pd.read_csv(mat_csv)
        
        # Verify Registered MI and DSC
        reg_mi_py = float(df_py[df_py["Registration_Stage"].str.contains("Registered")]["Mutual_Information_MI"].values[0])
        reg_dsc_py = float(df_py[df_py["Registration_Stage"].str.contains("Registered")]["Tumor_Hotspot_DSC"].values[0])
        unreg_mi_py = float(df_py[df_py["Registration_Stage"].str.contains("Unaligned")]["Mutual_Information_MI"].values[0])
        
        reg_mi_mat = float(df_mat[df_mat["Registration_Stage"].str.contains("Registered")]["Mutual_Information_MI"].values[0])
        reg_dsc_mat = float(df_mat[df_mat["Registration_Stage"].str.contains("Registered")]["Tumor_Hotspot_DSC"].values[0])
        
        self.assertGreaterEqual(reg_mi_py, 1.40, "Python registered MI must exceed 1.40 bits")
        self.assertGreaterEqual(reg_dsc_py, 0.90, "Python registered Tumor DSC must exceed 0.90")
        self.assertGreater(reg_mi_py, unreg_mi_py * 2.0, "Registered MI must more than double unaligned baseline")
        
        self.assertGreaterEqual(reg_mi_mat, 1.40, "MATLAB registered MI must exceed 1.40 bits")
        self.assertGreaterEqual(reg_dsc_mat, 0.90, "MATLAB registered Tumor DSC must exceed 0.90")

    def test_04_homogeneous_matrix_inversion(self):
        """Tier 4: Verify homogeneous transformation matrix invertibility and numerical stability."""
        csv_path = os.path.join(self.tables_dir, "exp12_task_12_1_matrix_error.csv")
        self.assertTrue(os.path.exists(csv_path), "Task 12.1 matrix table missing")
        df = pd.read_csv(csv_path)
        
        det_val = float(df.iloc[0]["Matrix_Determinant"])
        dev_val = float(df.iloc[0]["Identity_Deviation"])
        psnr_val = float(df.iloc[0]["Parenchyma_PSNR_dB"])
        
        self.assertAlmostEqual(det_val, 1.0, places=4, msg="Rigid matrix determinant must equal 1.0 (isometry)")
        self.assertLess(dev_val, 1e-10, "Composite T_fwd @ T_inv deviation from identity must be negligible")
        self.assertGreater(psnr_val, 15.0, "Parenchyma reconstruction PSNR must exceed 15 dB")

    def test_05_interpolation_modes(self):
        """Tier 5: Verify interpolation quality ordering (Bicubic > Bilinear > Nearest)."""
        csv_path = os.path.join(self.tables_dir, "exp12_task_12_2_interpolation_metrics.csv")
        self.assertTrue(os.path.exists(csv_path), "Task 12.2 interpolation table missing")
        df = pd.read_csv(csv_path)
        
        psnr_nn = float(df[df["Interpolation_Method"].str.contains("Nearest")]["PSNR_dB"].values[0])
        psnr_lin = float(df[df["Interpolation_Method"].str.contains("Bilinear")]["PSNR_dB"].values[0])
        psnr_cub = float(df[df["Interpolation_Method"].str.contains("Bicubic")]["PSNR_dB"].values[0])
        
        self.assertGreater(psnr_cub, psnr_lin, "Bicubic PSNR must exceed Bilinear PSNR")
        self.assertGreater(psnr_lin, psnr_nn, "Bilinear PSNR must exceed Nearest-Neighbor PSNR")

    def test_06_rotation_sweep_global_peak(self):
        """Tier 6: Verify Mutual Information reaches strict global peak at Delta Theta = 0 deg."""
        csv_path = os.path.join(self.tables_dir, "exp12_task_12_3_rotation_sweep.csv")
        self.assertTrue(os.path.exists(csv_path), "Task 12.3 rotation sweep table missing")
        df = pd.read_csv(csv_path)
        
        max_mi_row = df.loc[df["Mutual_Information_MI"].idxmax()]
        min_ent_row = df.loc[df["Joint_Entropy"].idxmin()]
        
        self.assertEqual(int(max_mi_row["Delta_Theta_deg"]), 0,
                         "Mutual Information must peak strictly at Delta_Theta = 0 deg")
        self.assertEqual(int(min_ent_row["Delta_Theta_deg"]), 0,
                         "Joint Entropy must reach global minimum strictly at Delta_Theta = 0 deg")

    def test_07_mse_multimodal_failure(self):
        """Tier 7: Verify MSE failure on multi-modal scans (MSE is NOT minimized at tx = 0)."""
        csv_path = os.path.join(self.tables_dir, "exp12_task_12_4_mse_vs_mi.csv")
        self.assertTrue(os.path.exists(csv_path), "Task 12.4 MSE vs MI table missing")
        df = pd.read_csv(csv_path)
        
        best_tx_mi = int(df.loc[df["Mutual_Information_MI"].idxmax()]["Translation_tx_px"])
        best_tx_mse = int(df.loc[df["Mean_Squared_Error_MSE"].idxmin()]["Translation_tx_px"])
        
        self.assertEqual(best_tx_mi, 0, "Mutual Information must identify true anatomical alignment at tx = 0 px")
        self.assertNotEqual(best_tx_mse, 0, "Mean Squared Error must fail and not be minimized at tx = 0 px")

    def test_08_pet_mri_clinical_fusion_tre(self):
        """Tier 8: Verify clinical Target Registration Error (TRE <= 1.0 px)."""
        csv_path = os.path.join(self.tables_dir, "exp12_task_12_5_fusion_verification.csv")
        self.assertTrue(os.path.exists(csv_path), "Task 12.5 fusion table missing")
        df = pd.read_csv(csv_path)
        
        unreg_tre = float(df[df["Registration_State"].str.contains("Unaligned")]["Target_Registration_Error_TRE_px"].values[0])
        reg_tre = float(df[df["Registration_State"].str.contains("Registered")]["Target_Registration_Error_TRE_px"].values[0])
        
        self.assertGreater(unreg_tre, 25.0, "Unaligned state must exhibit gross displacement (TRE > 25 px)")
        self.assertLessEqual(reg_tre, 1.0, "Registered state must achieve sub-pixel accuracy (TRE <= 1.0 px)")

    def test_09_artifacts_and_figures_completeness(self):
        """Tier 9: Verify all execution screenshots, figures, and plots are generated and non-empty."""
        expected_figs = [
            os.path.join(self.fig_dir, "exp12_github_qr.png"),
            os.path.join(self.fig_dir, "exp12_python_exec_screenshot.png"),
            os.path.join(self.fig_dir, "exp12_matlab_exec_screenshot.png"),
            os.path.join(self.outputs_py, "exp12_benchmark_joint_histograms.png"),
            os.path.join(self.outputs_py, "exp12_benchmark_clinical_registration.png"),
            os.path.join(self.outputs_py, "exp12_task_12_1_homogeneous_matrix.png"),
            os.path.join(self.outputs_py, "exp12_task_12_2_interpolation_comparison.png"),
            os.path.join(self.outputs_py, "exp12_task_12_3_rotation_sweep.png"),
            os.path.join(self.outputs_py, "exp12_task_12_3_joint_histograms_panels.png"),
            os.path.join(self.outputs_py, "exp12_task_12_4_mse_vs_mi_failure.png"),
            os.path.join(self.outputs_py, "exp12_task_12_5_fusion_checkerboard.png"),
            os.path.join(self.outputs_mat, "exp12_matlab_benchmark_joint_histograms.png"),
            os.path.join(self.outputs_mat, "exp12_matlab_benchmark_clinical_registration.png"),
            os.path.join(self.outputs_mat, "exp12_matlab_task12_1_homogeneous_matrix.png"),
            os.path.join(self.outputs_mat, "exp12_matlab_task12_2_interpolation_comparison.png"),
            os.path.join(self.outputs_mat, "exp12_matlab_task12_3_rotation_sweep.png"),
            os.path.join(self.outputs_mat, "exp12_matlab_task12_3_joint_histograms_panels.png"),
            os.path.join(self.outputs_mat, "exp12_matlab_task12_4_mse_vs_mi_failure.png"),
            os.path.join(self.outputs_mat, "exp12_matlab_task12_5_fusion_checkerboard.png")
        ]
        for f in expected_figs:
            self.assertTrue(os.path.exists(f), f"Expected figure missing: {f}")
            self.assertGreater(os.path.getsize(f), 500, f"Figure file too small: {f}")

if __name__ == "__main__":
    unittest.main()
