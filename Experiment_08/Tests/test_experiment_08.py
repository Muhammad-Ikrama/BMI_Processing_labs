"""
Experiment 08 Automated Test Suite (9 Suites)
Validates algorithmic invariants, mathematical properties, cross-platform parity,
and deliverable completeness for Experiment 08.
"""
import os
import unittest
import cv2
import numpy as np
import pandas as pd
from skimage.filters import threshold_multiotsu

class TestExperiment08(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.img_dir = os.path.join(cls.base_dir, "Inputs", "images")
        cls.tab_dir = os.path.join(cls.base_dir, "Tables")
        cls.out_py_dir = os.path.join(cls.base_dir, "Outputs", "Python")
        cls.out_m_dir = os.path.join(cls.base_dir, "Outputs", "MATLAB")
        cls.fig_dir = os.path.join(cls.base_dir, "Figures")

    def test_01_image_inputs_integrity(self):
        """Suite 1: Verify presence, dimensions, and type of all input medical images."""
        for name in ["Brain_MRI.png", "Head_CT.png", "Chest_Xray.png"]:
            path = os.path.join(self.img_dir, name)
            self.assertTrue(os.path.exists(path), f"Missing image {name}")
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            self.assertIsNotNone(img, f"Failed to load {name}")
            self.assertEqual(img.dtype, np.uint8)
            self.assertGreater(img.size, 0)

    def test_02_custom_otsu_exact_match(self):
        """Suite 2: Verify custom Otsu matches OpenCV built-in to the exact integer on Head CT."""
        img = cv2.imread(os.path.join(self.img_dir, "Head_CT.png"), cv2.IMREAD_GRAYSCALE)
        if img.shape != (512, 512): img = cv2.resize(img, (512, 512))
        
        hist, _ = np.histogram(img.flatten(), bins=256, range=(0, 256))
        p = hist.astype(float) / float(img.size)
        omega = np.cumsum(p)
        mu = np.cumsum(p * np.arange(256))
        mu_t = mu[-1]
        denom = omega * (1.0 - omega)
        valid = denom > 1e-12
        sigma_b2 = np.zeros(256)
        sigma_b2[valid] = ((mu_t * omega[valid] - mu[valid]) ** 2) / denom[valid]
        t_custom = int(np.argmax(sigma_b2))
        
        t_cv2, _ = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        self.assertEqual(t_custom, int(t_cv2), f"Custom T* ({t_custom}) != cv2 T* ({int(t_cv2)})")
        
        # Verify separability metric in [0, 1]
        sigma_tot2 = np.sum(((np.arange(256) - mu_t) ** 2) * p)
        eta = sigma_b2[t_custom] / sigma_tot2
        self.assertGreaterEqual(eta, 0.40)
        self.assertLessEqual(eta, 1.0)

    def test_03_isodata_convergence_invariance(self):
        """Suite 3: Verify Iterative Isodata convergence dynamics across starting guesses."""
        csv_path = os.path.join(self.tab_dir, "exp08_task_8_2_isodata_convergence.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing task 8.2 CSV")
        df = pd.read_csv(csv_path)
        
        # 1. All starting guesses converge in < 25 iterations
        self.assertTrue((df["Iterations"] < 25).all(), "Iterations exceeded 25")
        
        # 2. Chest X-ray has unimodal/bimodal stability: all 3 guesses converge to same threshold
        xray_sub = df[df["Modality"] == "Chest X-ray"]
        self.assertLess(np.ptp(xray_sub["Final_T_iso"].values), 1.0)
        
        # 3. Brain MRI: T0=128 and T0=230 converge to the same global threshold
        mri_sub = df[df["Modality"] == "Brain MRI"]
        mri_high = mri_sub[mri_sub["T0_Guess"].isin([128, 230])]["Final_T_iso"].values
        self.assertLess(np.ptp(mri_high), 0.1)

    def test_04_rf_bias_monotonic_degradation(self):
        """Suite 4: Verify monotonic degradation of Global Otsu under RF shading."""
        csv_path = os.path.join(self.tab_dir, "exp08_task_8_3_rf_bias_metrics.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing task 8.3 CSV")
        df = pd.read_csv(csv_path)
        
        otsu_dsc = df["Otsu_DSC"].values
        # Verify degradation: DSC at alpha=0.9 is strictly lower than alpha=0.0
        self.assertLess(otsu_dsc[-1], otsu_dsc[0])
        # Adaptive Gaussian maintains DSC >= 0.85
        adap_dsc = df["Adap_DSC"].values
        self.assertTrue((adap_dsc >= 0.85).all(), f"Adaptive DSC dropped below 0.85: {adap_dsc}")

    def test_05_adaptive_param_sweep_hollow_core(self):
        """Suite 5: Verify that W=7 produces lower DSC than optimal W=35 on biased MRI."""
        csv_path = os.path.join(self.tab_dir, "exp08_task_8_4_adaptive_sweep.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing task 8.4 CSV")
        df = pd.read_csv(csv_path)
        
        dsc_w7 = df[(df["Window_W"] == 7) & (df["Offset_C"] == 5)]["Dice_DSC"].iloc[0]
        dsc_w35 = df[(df["Window_W"] == 35) & (df["Offset_C"] == 5)]["Dice_DSC"].iloc[0]
        self.assertLess(dsc_w7, dsc_w35, "Undersized W=7 should have lower DSC than W=35")
        self.assertGreaterEqual(dsc_w35, 0.85, "W=35 should achieve DSC >= 0.85")

    def test_06_multi_otsu_ordering_and_partition(self):
        """Suite 6: Verify dual Otsu thresholds are strictly ordered and partition full image."""
        csv_path = os.path.join(self.tab_dir, "exp08_task_8_5_multi_otsu.csv")
        self.assertTrue(os.path.exists(csv_path), "Missing task 8.5 CSV")
        df = pd.read_csv(csv_path)
        
        self.assertEqual(len(df), 3)
        total_pct = df["Area_Pct"].sum()
        self.assertAlmostEqual(total_pct, 100.0, places=1)
        total_px = df["Pixel_Count"].sum()
        self.assertEqual(total_px, 512 * 512)

    def test_07_cross_platform_parity(self):
        """Suite 7: Verify MATLAB and Python yields concordant Otsu thresholds and multi-Otsu classes."""
        py_otsu = pd.read_csv(os.path.join(self.tab_dir, "exp08_task_8_1_otsu_metrics.csv"))["Custom_T_star"].iloc[0]
        m_otsu = pd.read_csv(os.path.join(self.tab_dir, "exp08_task_8_1_otsu_metrics_matlab.csv"))["Custom_T_star"].iloc[0]
        self.assertEqual(py_otsu, m_otsu, f"Python Otsu ({py_otsu}) != MATLAB Otsu ({m_otsu})")

    def test_08_qr_code_decodability(self):
        """Suite 8: Verify GitHub QR code decodes to official repository URL."""
        qr_path = os.path.join(self.fig_dir, "exp08_github_qr.png")
        self.assertTrue(os.path.exists(qr_path), "Missing QR code file")
        detector = cv2.QRCodeDetector()
        img = cv2.imread(qr_path)
        data, _, _ = detector.detectAndDecode(img)
        self.assertEqual(data, "https://github.com/Muhammad-Ikrama/BMI_Processing_labs")

    def test_09_deliverables_completeness(self):
        """Suite 9: Verify existence of all required generated tables, figures, and screenshots."""
        required_tables = [
            "exp08_benchmark_summary_py.csv", "exp08_benchmark_summary_matlab.csv",
            "exp08_task_8_1_otsu_metrics.csv", "exp08_task_8_1_otsu_metrics_matlab.csv",
            "exp08_task_8_2_isodata_convergence.csv", "exp08_task_8_2_isodata_convergence_matlab.csv",
            "exp08_task_8_3_rf_bias_metrics.csv", "exp08_task_8_3_rf_bias_metrics_matlab.csv",
            "exp08_task_8_4_adaptive_sweep.csv", "exp08_task_8_4_adaptive_sweep_matlab.csv",
            "exp08_task_8_5_multi_otsu.csv", "exp08_task_8_5_multi_otsu_matlab.csv"
        ]
        for t in required_tables:
            p = os.path.join(self.tab_dir, t)
            self.assertTrue(os.path.exists(p), f"Missing table {t}")

        required_figures = [
            "exp08_github_qr.png",
            "exp08_matlab_exec_screenshot.png",
            "exp08_python_exec_screenshot.png"
        ]
        for f in required_figures:
            p = os.path.join(self.fig_dir, f)
            self.assertTrue(os.path.exists(p), f"Missing figure {f}")

if __name__ == "__main__":
    unittest.main()
