"""
Automated 9-Tier Verification Test Suite for Experiment 14:
Lossless and Lossy Compression of Medical Images and Quality Evaluation Using PSNR & CR
Author: Muhammad Ikrama (Reg ID: 60140)
Department of Biomedical Engineering, Riphah International University, Lahore
Instructor: Engr. Rana Talha Khalid
Course: Medical Image Processing (BMI-701)
"""

import os
import unittest
import numpy as np
import pandas as pd

class TestExperiment14(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        cls.fig_dir = os.path.join(cls.base_dir, "Figures")
        cls.tab_dir = os.path.join(cls.base_dir, "Tables")
        cls.rep_dir = os.path.join(cls.base_dir, "Report")
        cls.out_matlab = os.path.join(cls.base_dir, "Outputs", "MATLAB")
        cls.out_python = os.path.join(cls.base_dir, "Outputs", "Python")
        cls.img_dir = os.path.join(cls.base_dir, "Inputs", "images")

    # Tier 1: Directory & Asset Integrity
    def test_tier_1_environment_and_assets(self):
        required_dirs = [self.fig_dir, self.tab_dir, self.rep_dir, self.out_matlab, self.out_python, self.img_dir]
        for d in required_dirs:
            self.assertTrue(os.path.isdir(d), f"Missing directory: {d}")
            
        required_images = ["Brain_MRI.png", "Head_CT.png", "Chest_Xray.png"]
        for img in required_images:
            path = os.path.join(self.img_dir, img)
            self.assertTrue(os.path.isfile(path), f"Missing input image: {path}")

    # Tier 2: Lossless Bit-Exact Verification
    def test_tier_2_lossless_bit_exactness(self):
        bm_csv = os.path.join(self.tab_dir, "exp14_benchmark_compression.csv")
        self.assertTrue(os.path.isfile(bm_csv), "Missing benchmark CSV")
        df_bm = pd.read_csv(bm_csv)
        
        row_png = df_bm[df_bm["Type"] == "Lossless"].iloc[0]
        self.assertEqual(row_png["MSE"], 0.0, "Lossless PNG has non-zero MSE!")
        self.assertEqual(row_png["SSIM"], 1.0, "Lossless PNG SSIM is not 1.0000!")

    # Tier 3: Task 14.1 Custom RLE Assertions
    def test_tier_3_rle_compression(self):
        rle_csv = os.path.join(self.tab_dir, "exp14_task_14_1_rle_summary.csv")
        self.assertTrue(os.path.isfile(rle_csv), "Missing Task 14.1 CSV")
        df_rle = pd.read_csv(rle_csv)
        
        cr_bin = float(df_rle.loc[df_rle["Input_Type"].str.contains("Binary"), "Compression_Ratio"].values[0])
        mse_bin = float(df_rle.loc[df_rle["Input_Type"].str.contains("Binary"), "MSE"].values[0])
        mse_gray = float(df_rle.loc[df_rle["Input_Type"].str.contains("Grayscale"), "MSE"].values[0])
        
        self.assertGreaterEqual(cr_bin, 10.0, f"Binary RLE CR {cr_bin:.2f} is below 10.0x")
        self.assertEqual(mse_bin, 0.0, "Binary RLE MSE != 0.0")
        self.assertEqual(mse_gray, 0.0, "Grayscale RLE MSE != 0.0")

    # Tier 4: Task 14.2 Shannon Entropy & Redundancy Assertions
    def test_tier_4_shannon_entropy(self):
        ent_csv = os.path.join(self.tab_dir, "exp14_task_14_2_entropy_comparison.csv")
        self.assertTrue(os.path.isfile(ent_csv), "Missing Task 14.2 CSV")
        df_ent = pd.read_csv(ent_csv)
        
        for _, row in df_ent.iterrows():
            h_val = float(row["Shannon_Entropy_bpp"])
            max_1st = float(row["Max_First_Order_CR"])
            actual_png = float(row["PNG_Compression_Ratio"])
            
            self.assertTrue(5.0 <= h_val <= 8.0, f"Entropy {h_val} outside expected range [5.0, 8.0]")
            self.assertGreater(actual_png, max_1st, f"PNG CR {actual_png} does not exceed first-order CR {max_1st}")

    # Tier 5: Task 14.3 Multi-Modality Rate-Distortion Assertions
    def test_tier_5_multimodal_rd_curves(self):
        rd_csv = os.path.join(self.tab_dir, "exp14_task_14_3_multimodal_rd.csv")
        self.assertTrue(os.path.isfile(rd_csv), "Missing Task 14.3 CSV")
        df_rd = pd.read_csv(rd_csv)
        
        # Test Brain MRI Q=85
        row_85 = df_rd[(df_rd["Modality"] == "Brain MRI") & (df_rd["Quality_Q"] == 85)].iloc[0]
        self.assertGreaterEqual(float(row_85["PSNR_dB"]), 40.0, f"Brain MRI Q=85 PSNR {row_85['PSNR_dB']} < 40 dB")
        self.assertGreaterEqual(float(row_85["SSIM"]), 0.980, f"Brain MRI Q=85 SSIM {row_85['SSIM']} < 0.980")

    # Tier 6: Task 14.4 8x8 DCT Blocking Artifact Assertions
    def test_tier_6_blocking_artifacts(self):
        err_csv = os.path.join(self.tab_dir, "exp14_task_14_4_error_stats.csv")
        self.assertTrue(os.path.isfile(err_csv), "Missing Task 14.4 CSV")
        df_err = pd.read_csv(err_csv)
        
        mae_85 = float(df_err.loc[df_err["Quality_Q"] == 85, "Mean_Absolute_Error"].values[0])
        mae_5  = float(df_err.loc[df_err["Quality_Q"] == 5, "Mean_Absolute_Error"].values[0])
        ratio = mae_5 / (mae_85 + 1e-12)
        self.assertGreaterEqual(ratio, 5.0, f"MAE ratio Q5/Q85 {ratio:.2f} is less than 5.0x")

    # Tier 7: Task 14.5 Downstream Radiomics Impact Assertions
    def test_tier_7_downstream_impact(self):
        down_csv = os.path.join(self.tab_dir, "exp14_task_14_5_downstream_impact.csv")
        self.assertTrue(os.path.isfile(down_csv), "Missing Task 14.5 CSV")
        df_down = pd.read_csv(down_csv)
        
        dsc_85 = float(df_down.loc[df_down["Quality_Q"] == 85, "Tumor_Dice_DSC"].values[0])
        err_con_5 = float(df_down.loc[df_down["Quality_Q"] == 5, "Contrast_Error_Pct"].values[0])
        
        self.assertGreaterEqual(dsc_85, 0.95, f"Tumor DSC at Q=85 {dsc_85} is below 0.95")
        self.assertGreaterEqual(err_con_5, 15.0, f"Contrast error at Q=5 {err_con_5}% is below 15.0%")

    # Tier 8: Dual-Platform Console Outputs Integrity
    def test_tier_8_console_outputs_integrity(self):
        py_log = os.path.join(self.out_python, "python_console_output.txt")
        mat_log = os.path.join(self.out_matlab, "matlab_console_output.txt")
        self.assertTrue(os.path.isfile(py_log), "Missing Python console log")
        self.assertTrue(os.path.isfile(mat_log), "Missing MATLAB console log")
        self.assertGreater(os.path.getsize(py_log), 500, "Python log too short")
        self.assertGreater(os.path.getsize(mat_log), 500, "MATLAB log too short")

    # Tier 9: Report & Output Artifact Verification
    def test_tier_9_report_and_artifacts(self):
        qr_path = os.path.join(self.fig_dir, "exp14_github_qr.png")
        self.assertTrue(os.path.isfile(qr_path), "Missing GitHub QR code PNG")
        self.assertGreater(os.path.getsize(qr_path), 500, "QR code too small")
        
        py_scr = os.path.join(self.fig_dir, "exp14_python_exec_screenshot.png")
        mat_scr = os.path.join(self.fig_dir, "exp14_matlab_exec_screenshot.png")
        self.assertTrue(os.path.isfile(py_scr), "Missing Python terminal screenshot")
        self.assertTrue(os.path.isfile(mat_scr), "Missing MATLAB terminal screenshot")
        
        pdf_path = os.path.join(self.rep_dir, "Experiment_14_Report.pdf")
        if os.path.isfile(pdf_path):
            import pypdf
            reader = pypdf.PdfReader(pdf_path)
            num_pages = len(reader.pages)
            self.assertTrue(8 <= num_pages <= 15, f"Report page count {num_pages} outside 8-15 budget!")

if __name__ == "__main__":
    unittest.main()
