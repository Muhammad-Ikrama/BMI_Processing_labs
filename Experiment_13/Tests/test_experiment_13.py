"""
Automated 9-Tier Verification Test Suite for Experiment 13:
Texture Feature Extraction from Medical Images Using the Gray-Level Co-occurrence Matrix (GLCM)
Author: Muhammad Ikrama (Reg ID: 60140)
Department of Biomedical Engineering, Riphah International University, Lahore
Instructor: Engr. Rana Talha Khalid
Course: Medical Image Processing (BMI-701)
"""

import os
import unittest
import numpy as np
import pandas as pd

class TestExperiment13(unittest.TestCase):
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
            
        required_images = ["Brain_MRI.png", "Chest_Xray.png"]
        for img in required_images:
            path = os.path.join(self.img_dir, img)
            self.assertTrue(os.path.isfile(path), f"Missing input image: {path}")

    # Tier 2: GLCM Matrix Normalization & Symmetry
    def test_tier_2_glcm_normalization_and_symmetry(self):
        norm_csv = os.path.join(self.tab_dir, "exp13_task_13_1_glcm_normalized.csv")
        self.assertTrue(os.path.isfile(norm_csv), "Missing normalized GLCM CSV")
        df_p = pd.read_csv(norm_csv, index_col=0)
        P = df_p.values
        
        prob_sum = float(np.sum(P))
        self.assertAlmostEqual(prob_sum, 1.0, places=5, msg=f"GLCM probability sum {prob_sum} != 1.000000")
        
        # Symmetry check: P == P.T
        diff = np.max(np.abs(P - P.T))
        self.assertAlmostEqual(diff, 0.0, places=6, msg=f"GLCM is not symmetric! max diff = {diff}")

    # Tier 3: Task 13.1 Hand-Verified 4x4 Synthetic Assertions
    def test_tier_3_task_13_1_hand_verification(self):
        counts_csv = os.path.join(self.tab_dir, "exp13_task_13_1_glcm_counts.csv")
        self.assertTrue(os.path.isfile(counts_csv), "Missing count GLCM CSV")
        df_counts = pd.read_csv(counts_csv, index_col=0)
        total_sym_pairs = int(df_counts.values.sum())
        self.assertEqual(total_sym_pairs, 24, f"Expected 24 symmetric pairs, got {total_sym_pairs}")
        
        summary_csv = os.path.join(self.tab_dir, "exp13_task_13_1_summary.csv")
        self.assertTrue(os.path.isfile(summary_csv), "Missing Task 13.1 summary CSV")
        df_sum = pd.read_csv(summary_csv)
        con_val = float(df_sum.loc[df_sum["Metric"] == "GLCM Contrast", "Value"].values[0])
        self.assertAlmostEqual(con_val, 0.5833, places=3, msg=f"Synthetic contrast {con_val} != 0.5833")

    # Tier 4: Haralick Feature Separation Assertions
    def test_tier_4_haralick_feature_separation(self):
        bm_csv = os.path.join(self.tab_dir, "exp13_benchmark_features.csv")
        self.assertTrue(os.path.isfile(bm_csv), "Missing benchmark features CSV")
        df_bm = pd.read_csv(bm_csv)
        
        c_norm = float(df_bm.loc[df_bm["Tissue_ROI"].str.contains("Normal"), "Contrast"].values[0])
        c_tumor = float(df_bm.loc[df_bm["Tissue_ROI"].str.contains("Tumor"), "Contrast"].values[0])
        ent_norm = float(df_bm.loc[df_bm["Tissue_ROI"].str.contains("Normal"), "Entropy_bits"].values[0])
        ent_tumor = float(df_bm.loc[df_bm["Tissue_ROI"].str.contains("Tumor"), "Entropy_bits"].values[0])
        h_norm = float(df_bm.loc[df_bm["Tissue_ROI"].str.contains("Normal"), "Homogeneity"].values[0])
        
        ratio = c_tumor / c_norm
        self.assertGreaterEqual(ratio, 3.0, f"Contrast ratio {ratio:.2f} is less than 3.0x")
        self.assertGreaterEqual(ent_tumor - ent_norm, 1.5, f"Entropy gap {ent_tumor - ent_norm:.2f} is less than 1.5 bits")
        self.assertGreaterEqual(h_norm, 0.75, f"Normal homogeneity {h_norm:.2f} is below 0.75")

    # Tier 5: Task 13.2 Inter-Pixel Distance Sensitivity Sweep
    def test_tier_5_distance_sweep_dynamics(self):
        dist_csv = os.path.join(self.tab_dir, "exp13_task_13_2_distance_sweep.csv")
        self.assertTrue(os.path.isfile(dist_csv), "Missing distance sweep CSV")
        df_d = pd.read_csv(dist_csv)
        
        df_norm = df_d[df_d["ROI"] == "Normal_White_Matter"].sort_values("Distance_d")
        c_vals = df_norm["Contrast"].values
        # Contrast should increase with distance
        self.assertTrue(all(c_vals[i] <= c_vals[i+1] for i in range(len(c_vals)-1)), "Contrast did not increase monotonically with d")
        
        corr_12 = df_norm.loc[df_norm["Distance_d"] == 12, "Correlation"].values[0]
        self.assertAlmostEqual(corr_12, 0.0, delta=0.15, msg=f"Correlation at d=12 {corr_12} did not decay toward 0.0")

    # Tier 6: Task 13.3 Directional Anisotropy Assertions
    def test_tier_6_directional_anisotropy(self):
        aniso_csv = os.path.join(self.tab_dir, "exp13_task_13_3_directional_anisotropy.csv")
        self.assertTrue(os.path.isfile(aniso_csv), "Missing directional anisotropy CSV")
        df_an = pd.read_csv(aniso_csv)
        
        rib_rows = df_an[df_an["Anatomical_ROI"].str.contains("Ribs")]
        ratio_rib = float(rib_rows["Anisotropy_Ratio_C90_over_C0"].values[0])
        self.assertGreaterEqual(ratio_rib, 5.0, f"Rib anisotropy ratio {ratio_rib:.2f} is less than 5.0x")

    # Tier 7: Task 13.4 Quantization Trade-Off Assertions
    def test_tier_7_quantization_tradeoff(self):
        q_csv = os.path.join(self.tab_dir, "exp13_task_13_4_quantization_tradeoff.csv")
        self.assertTrue(os.path.isfile(q_csv), "Missing quantization tradeoff CSV")
        df_q = pd.read_csv(q_csv)
        
        sp_256 = float(df_q.loc[df_q["Ng_Levels"] == 256, "Sparsity_Percent"].values[0])
        sp_16 = float(df_q.loc[df_q["Ng_Levels"] == 16, "Sparsity_Percent"].values[0])
        self.assertGreaterEqual(sp_256, 90.0, f"Ng=256 sparsity {sp_256}% is below 90%")
        self.assertLessEqual(sp_16, 80.0, f"Ng=16 sparsity {sp_16}% exceeds 80%")

    # Tier 8: Task 13.5 Sliding-Window Texture Feature Map Assertions
    def test_tier_8_texture_maps(self):
        map_csv = os.path.join(self.tab_dir, "exp13_task_13_5_texture_map_stats.csv")
        self.assertTrue(os.path.isfile(map_csv), "Missing texture map stats CSV")
        df_m = pd.read_csv(map_csv)
        
        c_max = float(df_m.loc[df_m["Feature_Map"] == "GLCM Contrast", "Max"].values[0])
        ent_max = float(df_m.loc[df_m["Feature_Map"] == "Shannon Entropy (bits)", "Max"].values[0])
        self.assertGreaterEqual(c_max, 5.0, f"Max contrast {c_max} is below 5.0")
        self.assertGreaterEqual(ent_max, 5.5, f"Max entropy {ent_max} is below 5.5 bits")

    # Tier 9: Report & Output Artifact Verification
    def test_tier_9_report_and_artifacts(self):
        # QR Code
        qr_path = os.path.join(self.fig_dir, "exp13_github_qr.png")
        self.assertTrue(os.path.isfile(qr_path), "Missing GitHub QR code PNG")
        self.assertGreater(os.path.getsize(qr_path), 500, "QR code file too small")
        
        # Terminal screenshots
        py_scr = os.path.join(self.fig_dir, "exp13_python_exec_screenshot.png")
        mat_scr = os.path.join(self.fig_dir, "exp13_matlab_exec_screenshot.png")
        self.assertTrue(os.path.isfile(py_scr), "Missing Python terminal screenshot")
        self.assertTrue(os.path.isfile(mat_scr), "Missing MATLAB terminal screenshot")
        
        # Figures
        fig_13_1 = os.path.join(self.fig_dir, "Figure_13_1_GLCM_Heatmaps.png")
        fig_13_2 = os.path.join(self.fig_dir, "Figure_13_2_Clinical_Characterization.png")
        self.assertTrue(os.path.isfile(fig_13_1), "Missing Figure 13.1")
        self.assertTrue(os.path.isfile(fig_13_2), "Missing Figure 13.2")
        
        # Check Report files if already compiled
        docx_path = os.path.join(self.rep_dir, "Experiment_13_Report.docx")
        pdf_path = os.path.join(self.rep_dir, "Experiment_13_Report.pdf")
        if os.path.isfile(pdf_path):
            import pypdf
            reader = pypdf.PdfReader(pdf_path)
            num_pages = len(reader.pages)
            self.assertTrue(8 <= num_pages <= 15, f"Report page count {num_pages} outside 8-15 budget!")

if __name__ == "__main__":
    unittest.main()
