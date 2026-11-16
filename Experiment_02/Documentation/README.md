# Experiment No. 2: Histogram Computation and Histogram Equalization Techniques for Contrast Enhancement of Medical Images
**Course**: Medical Image Processing (B.Sc. Biomedical Engineering)  
**Institution**: Faculty of Engineering & Applied Sciences, Riphah International University, Lahore  
**Instructor / Lab Engineer**: Engr. Rana Talha Khalid  

---

## 1. Overview
This laboratory experiment investigates the mathematical, computational, and clinical principles of image contrast enhancement across biomedical diagnostic modalities:
1. **Discrete Histograms & Empirical PDFs**: Formulating frequency distributions $h(r_k) = n_k$ and normalized empirical probability density functions $p(r_k) = n_k / (M \times N)$ from raw medical pixel arrays.
2. **Cumulative Distribution Functions (CDF)**: Constructing empirical cumulative distribution curves $P(r_k) = \sum_{j=0}^k p(r_j)$ and correlating steep derivative segments with anatomical tissue volumes.
3. **Global Histogram Equalization (GHE)**: Implementing monotonic transformation functions $s_k = \text{round}[(L - 1) \cdot \text{CDF}(r_k)]$ and analyzing clinical failure modes (background air noise over-amplification, comb-gap quantization artifacts, and trabecular bone saturation).
4. **Contextual CLAHE Optimization**: Implementing Contrast-Limited Adaptive Histogram Equalization (8x8 tile grid, local histogram clipping, uniform redistribution, and bilinear interpolation) and performing parameter sensitivity sweeps across clip limits ($1.0, 2.0, 3.0, 4.0, 8.0$).
5. **Clinical Quantitative Decision Framework**: Evaluating contrast improvements using objective metrics: Shannon Information Entropy ($H \ge 4.75$ bits/pixel), Background Noise Floor Variance ($\sigma_{\text{bg}}^2 \le 15.0$), Boundary Saturation ($< 1.5\%$), and RMS Contrast ($55 \le C_{\text{RMS}} \le 75$).
6. **Multi-Panel Diagnostic Benchmarking**: Assembling a 2x3 clinical radiograph report featuring highlighted Regions of Interest (ROI 1 = Lung Parenchyma, ROI 2 = Background Air) and structured performance tables.

---

## 2. Directory Structure

```text
Biomedical_Image_Processing_Lab/
└── Experiment_02/
    ├── Report/
    │   ├── Experiment_02_Report.docx       # Complete laboratory report (Word format)
    │   └── Experiment_02_Report.pdf        # Complete laboratory report (PDF format)
    ├── MATLAB/
    │   ├── task_2_1_manual_histogram.m     # Task 2.1: Manual histogram & PDF
    │   ├── task_2_2_dual_axis_cdf.m        # Task 2.2: Dual-axis histogram & CDF
    │   ├── task_2_3_global_histogram_equalization.m # Task 2.3: Global HE & saturation
    │   ├── task_2_4_clahe_clip_sensitivity.m # Task 2.4: CLAHE clip limit sensitivity
    │   ├── task_2_5_multipanel_contrast_report.m # Task 2.5: Multi-panel contrast report
    │   ├── example_01_histogram_cdf.m      # Tutorial Example 1
    │   ├── example_02_ghe_vs_clahe.m       # Tutorial Example 2
    │   ├── run_all.m                       # Batch runner
    │   └── experiment_02.m                 # Master experiment runner
    ├── Python/
    │   ├── task_2_1_manual_histogram.py     # Task 2.1: Manual histogram & PDF
    │   ├── task_2_2_dual_axis_cdf.py        # Task 2.2: Dual-axis histogram & CDF
    │   ├── task_2_3_global_histogram_equalization.py # Task 2.3: Global HE & saturation
    │   ├── task_2_4_clahe_clip_sensitivity.py # Task 2.4: CLAHE clip limit sensitivity
    │   ├── task_2_5_multipanel_contrast_report.py # Task 2.5: Multi-panel contrast report
    │   ├── example_01_histogram_cdf.py      # Tutorial Example 1
    │   ├── example_02_ghe_vs_clahe.py       # Tutorial Example 2
    │   ├── run_all.py                      # Batch runner
    │   ├── experiment_02.py                # Master experiment runner
    │   └── requirements.txt                # Environment dependencies
    ├── Inputs/
    │   └── images/
    │       ├── Xray.jpg                    # Clinical chest radiograph (429 x 466)
    │       └── Lung-HR-contrast.png        # Low-contrast lung radiograph (2060 x 1240)
    ├── Outputs/
    │   ├── MATLAB/                         # MATLAB output figures
    │   └── Python/                         # Python output figures
    ├── Figures/                            # Consolidated PNG figures for report
    ├── Tables/                             # Exported CSV tables
    ├── Tests/
    │   └── test_results.txt                # Automated test execution log (100% PASS)
    └── Documentation/
        ├── README.md                       # This documentation guide
        └── requirement_traceability.md     # Requirement Traceability Matrix
```

---

## 3. Environment & Prerequisites

### Python Setup
* Python 3.10+ (tested on Python 3.14)
* Install dependencies:
  ```bash
  cd Python/
  pip install -r requirements.txt
  ```

### MATLAB Setup
* MATLAB R2022b or later (tested on MATLAB R2026a)
* Image Processing Toolbox

---

## 4. Execution Instructions

### Running Python Implementations
Execute the master runner to execute all tasks in sequence and generate figures:
```bash
cd Python/
python experiment_02.py
```

### Running MATLAB Implementations
Launch MATLAB, navigate to `MATLAB/`, and run:
```matlab
experiment_02
```

---

## 5. Verification & Quality Assurance
Run the automated test suite:
```bash
python -c "import subprocess; subprocess.run(['python', '../Tests/run_tests.py'])"
```
Audit logs in `Tests/test_results.txt` confirm:
* 8/8 Test suites passed (100% success rate).
* Manual histogram verified without high-level library functions ($\sum h(r_k) = M \times N$, $\sum p(r_k) = 1.000000$).
* Steepest CDF derivative peak verified at $r_k = 249$ ($n_k = 61,744$).
* Optimal clinical operating point confirmed at $\text{ClipLimit} = 2.0$.
* All 14 figures (7 Python, 7 MATLAB) generated and verified.
