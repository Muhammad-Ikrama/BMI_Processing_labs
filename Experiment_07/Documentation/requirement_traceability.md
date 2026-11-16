# Requirement Traceability Matrix: Experiment No. 7

**Experiment Title:** Image Sharpening of Medical Images Using High-Boost Filtering and Unsharp Masking: Implementation and Diagnostic Analysis  
**Course:** Medical Image Processing (BME 7th Semester)  
**Institution:** Riphah International University, Lahore Campus  
**Faculty / Lab Engineer:** Engr. Rana Talha Khalid  

---

## 1. Traceability Summary Table

| Requirement ID | Requirement Specification | Implementation Source | Verification & Evidence Files | Status |
| :--- | :--- | :--- | :--- | :--- |
| **REQ-01** | Full Ingestion & Analysis of Instructor Manual | Manual extraction | `pdf_exp07_text_extracted.txt` | **COMPLETE** |
| **REQ-02** | Baseline Unsharp Masking & High-Pass Mask Formation | `example_01.py`, `example_01.m` | `Outputs/Python/exp07_example_01_*.png`, `Outputs/MATLAB/` | **COMPLETE** |
| **REQ-03** | Boost Parameter Sweep ($k \in [0.5, 1.0, 1.8, 3.0]$) | `example_01.py`, `example_01.m` | `Figures/exp07_example_01_benchmark_py.png`, `_m.png` | **COMPLETE** |
| **REQ-04** | Mean Gradient Magnitude & Edge Metric Quantification | `example_01.py`, `task_7_1.py` | `Tables/exp07_benchmark_summary_py.csv`, `_matlab.csv` | **COMPLETE** |
| **REQ-05** | Dynamic Range Clipping & Saturation Analysis | `task_7_1.py`, `task_7_1.m` | `Tables/exp07_task_7_1_clipping_metrics.csv`, `_matlab.csv` | **COMPLETE** |
| **REQ-06** | Information Entropy Evaluation (Shannon Bits/Px) | `task_7_1.py`, `task_7_1.m` | `Figures/exp07_task_7_1_clipping_sweep_py.png`, `_m.png` | **COMPLETE** |
| **REQ-07** | Spatial Smoothing Kernel Blur Parameter Sweep ($\sigma \in [0.8, 1.5, 3.0]$) | `task_7_2.py`, `task_7_2.m` | `Figures/exp07_task_7_2_mask_bandwidth_py.png`, `_m.png` | **COMPLETE** |
| **REQ-08** | High-Frequency Mask Bandwidth & Cutoff Frequency ($f_c = 1/(2\pi\sigma)$) | `task_7_2.py`, `task_7_2.m` | `Tables/exp07_task_7_2_bandwidth_metrics.csv`, `_matlab.csv` | **COMPLETE** |
| **REQ-09** | 1-D Spatial Intensity Transect Profile Extraction (Row 150) | `task_7_3.py`, `task_7_3.m` | `Outputs/Python/exp07_task_7_3_transect_overlay.png` | **COMPLETE** |
| **REQ-10** | Edge Slope Steepening Quantification ($\max \|dI/dx\|$) | `task_7_3.py`, `task_7_3.m` | `Tables/exp07_task_7_3_mach_band_metrics.csv`, `_matlab.csv` | **COMPLETE** |
| **REQ-11** | Mach Band Overshoot & Peak Elevation Measurement | `task_7_3.py`, `task_7_3.m` | `Figures/exp07_task_7_3_mach_band_profiles_py.png`, `_m.png` | **COMPLETE** |
| **REQ-12** | Halo Width & Clinical Compliance ($\le 2.0$ px at $k=1.0$) | `task_7_3.py`, `task_7_3.m` | `Tables/exp07_task_7_3_mach_band_metrics.csv` | **COMPLETE** |
| **REQ-13** | Simulated Gaussian Quantum Mottle ($\sigma_{\text{noise}} \approx 13.97$) | `task_7_4.py`, `task_7_4.m` | `Outputs/Python/exp07_task_7_4_noisy_radiograph.png` | **COMPLETE** |
| **REQ-14** | Homogeneous Background ROI Noise Measurement | `task_7_4.py`, `task_7_4.m` | `Tables/exp07_task_7_4_noise_amplification_metrics.csv` | **COMPLETE** |
| **REQ-15** | Low-Dose Safety Threshold Evaluation ($>25\%$ noise limit) | `task_7_4.py`, `task_7_4.m` | `Figures/exp07_task_7_4_noise_tradeoff_py.png`, `_m.png` | **COMPLETE** |
| **REQ-16** | Anatomical ROI Segmentation (Cortical Bone vs. Lung Parenchyma) | `task_7_5.py`, `task_7_5.m` | `Figures/exp07_task_7_5_clinical_rois_py.png`, `_m.png` | **COMPLETE** |
| **REQ-17** | Michelson Contrast & Modality Decision Rules | `task_7_5.py`, `task_7_5.m` | `Tables/exp07_task_7_5_clinical_roi_metrics.csv` | **COMPLETE** |
| **REQ-18** | Multi-Environment Parity (Python 3.14 & MATLAB R2026a) | Python & MATLAB trees | All scripts in `Python/` and `MATLAB/` | **COMPLETE** |
| **REQ-19** | Comprehensive Automated Quality & Testing Suite | `Tests/test_experiment_07.py` | `Tests/test_results.txt` (9/9 suites passed) | **COMPLETE** |
| **REQ-20** | Academic Laboratory Report Generation (DOCX & PDF) | `build_report.py` | `Report/Experiment_07_Report.docx`, `.pdf` | **COMPLETE** |

---

## 2. Requirement Details & Technical Verification

### REQ-01: Instructor Manual Authority
- **Text Source:** `Experiment_07_Image_Sharpening_High_Boost_and_Unsharp_Masking.pdf` (6-page manual).
- **Extracted Content:** Theory of unsharp masking, high-boost equations $f_{\text{hb}} = A f - f_{\text{LP}} = (A-1)f + f_{\text{mask}} = f + k f_{\text{mask}}$, Mach band phenomena, dynamic range clipping hazards, and clinical radiograph analysis.

### REQ-02 to REQ-06: Filtering & Dynamic Range
- **Filter Formula:** $f_{\text{sharp}}(x, y) = f(x, y) + k \cdot [f(x, y) - f_{\text{smooth}}(x, y)]$.
- **Clipping Verification:** Clamped values at 0 and 255 increase monotonically with $k$:
  - $k=0.5$: $0.012\%$ total clipping
  - $k=1.0$: $0.087\%$ total clipping
  - $k=1.8$: $0.458\%$ total clipping
  - $k=3.0$: $2.140\%$ total clipping (severe saturation).

### REQ-07 to REQ-12: Spatial Bandwidth & Edge Physics
- **Spatial Scales:**
  - $\sigma = 0.8$ px ($5\times 5$ window): $f_c = 0.1989$ cyc/px, mask std dev = 3.65.
  - $\sigma = 1.5$ px ($7\times 7$ window): $f_c = 0.1061$ cyc/px, mask std dev = 6.42.
  - $\sigma = 3.0$ px ($13\times 13$ window): $f_c = 0.0531$ cyc/px, mask std dev = 9.87.
- **Mach Band Transect:** Row 150 across columns 100 to 250.
  - Baseline slope: $13.00$ units/px
  - $k=1.0$: $23.63$ units/px ($+81.8\%$), halo width $1.2$ px ($\le 2.0$ px compliance PASS).
  - $k=3.0$: $44.89$ units/px ($+245.3\%$), halo width $3.5$ px (FAIL: Thick pseudofracture halo).

### REQ-13 to REQ-15: Noise Amplification & Low-Dose Radiography
- Simulated quantum mottle with variance $0.003$ ($\sigma_{\text{noise}} \approx 13.97$).
- Background ROI noise std dev:
  - Clean baseline: $29.85$
  - Low-dose noisy: $33.05$
  - Unsharp masking ($k=1.0$): $41.72$ ($+26.2\%$ noise increase, acceptable with clinical justification)
  - High-boost ($k=2.0$): $51.99$ ($+57.3\%$ noise increase, STRICTLY CONTRAINDICATED).

### REQ-16 to REQ-17: Anatomical ROIs & Clinical Protocols
- **Dense Cortical Bone:** High intrinsic radiopacity tolerates high-boost ($k=1.2-1.8$) to expose fine trabeculae.
- **Lung Parenchyma:** Delicate alveolar architecture demands conservative boost ($k=0.5-0.8$) to prevent false nodular pseudolesions.
