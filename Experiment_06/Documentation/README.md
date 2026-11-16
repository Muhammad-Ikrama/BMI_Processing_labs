# Biomedical Image Processing Laboratory — Experiment 06
## Frequency-Domain Filtering of Medical Images Using the 2-D Fourier Transform: Low-Pass and High-Pass Filter Design and Analysis

**Institution**: Riphah International University, Lahore, Pakistan  
**Faculty**: Faculty of Engineering & Applied Sciences | Department of Biomedical Engineering  
**Course**: Medical Image Processing (B.Sc. Biomedical Engineering, 6th Semester)  
**Lab Engineer**: Engr. Rana Talha Khalid  

---

### 1. Experiment Overview
This laboratory experiment investigates the mathematical foundations, algorithm implementation, and clinical diagnostic applications of two-dimensional frequency-domain filtering on medical imaging datasets (specifically cranial magnetic resonance imaging, MRI). The experiment contrasts spatial-domain convolution with frequency-domain multiplication via the Fast Fourier Transform (FFT), establishes the 5-step frequency-filtering pipeline, analyzes Gibbs ringing phenomena in Ideal Low-Pass Filters (ILPF), systematically evaluates Butterworth Low-Pass Filter (BLPF) order sensitivity ($n \in [1, 2, 4, 8]$), and characterizes complementary Gaussian Low-Pass (GLPF) and High-Pass (GHPF) filters for organ parenchymal smoothing and micro-structural boundary isolation.

---

### 2. Project Directory Structure

```text
Experiment_06/
├── Documentation/
│   ├── README.md                           # Master execution guide & workflow overview
│   └── requirement_traceability.md         # Complete requirement traceability matrix (RTM)
├── Figures/                                # 12 high-resolution publication-grade figures
│   ├── exp06_example_01_benchmark_py.png   # Python baseline frequency filtering benchmark
│   ├── exp06_example_01_benchmark_m.png    # MATLAB baseline frequency filtering benchmark
│   ├── exp06_task_6_1_dft_spectrum_py.png  # Task 6.1: 2D-DFT & magnitude spectrum analysis (Py)
│   ├── exp06_task_6_1_dft_spectrum_m.png   # Task 6.1: 2D-DFT & magnitude spectrum analysis (MATLAB)
│   ├── exp06_task_6_2_ilpf_gibbs_ringing_py.png # Task 6.2: Gibbs ringing & ILPF sensitivity (Py)
│   ├── exp06_task_6_2_ilpf_gibbs_ringing_m.png  # Task 6.2: Gibbs ringing & ILPF sensitivity (MATLAB)
│   ├── exp06_task_6_3_blpf_order_sweep_py.png   # Task 6.3: BLPF order sensitivity sweep (Py)
│   ├── exp06_task_6_3_blpf_order_sweep_m.png    # Task 6.3: BLPF order sensitivity sweep (MATLAB)
│   ├── exp06_task_6_4_glpf_ghpf_contrast_py.png # Task 6.4: GLPF vs GHPF boundary isolation (Py)
│   ├── exp06_task_6_4_glpf_ghpf_contrast_m.png  # Task 6.4: GLPF vs GHPF boundary isolation (MATLAB)
│   ├── exp06_task_6_5_diagnostic_report_py.png  # Task 6.5: Master 2x3 diagnostic report (Py)
│   └── exp06_task_6_5_diagnostic_report_m.png   # Task 6.5: Master 2x3 diagnostic report (MATLAB)
├── Inputs/
│   └── images/                             # Verified clinical imaging inputs (MRI.jpg, CT.jpg, etc.)
├── MATLAB/                                 # Complete MATLAB R2026a implementations
│   ├── example_01.m                        # Baseline frequency filtering comparison
│   ├── task_6_1.m                          # 2D-DFT & centered magnitude spectrum
│   ├── task_6_2.m                          # Gibbs phenomenon & ILPF cutoff sweep
│   ├── task_6_3.m                          # Butterworth LP order sweep (n = 1, 2, 4, 8)
│   ├── task_6_4.m                          # Gaussian LP vs HP filtering & DC elimination
│   ├── task_6_5.m                          # Master multi-filter diagnostic report
│   ├── experiment_06.m                     # Master pipeline execution script
│   └── run_all.m                           # Master runner script
├── Outputs/
│   ├── MATLAB/                             # MATLAB generated filtered images (.png)
│   └── Python/                             # Python generated filtered images (.png)
├── Python/                                 # Complete Python 3.14 implementations
│   ├── example_01.py                       # Baseline frequency filtering comparison
│   ├── task_6_1.py                         # 2D-DFT & centered magnitude spectrum
│   ├── task_6_2.py                         # Gibbs phenomenon & ILPF cutoff sweep
│   ├── task_6_3.py                         # Butterworth LP order sweep (n = 1, 2, 4, 8)
│   ├── task_6_4.py                         # Gaussian LP vs HP filtering & DC elimination
│   ├── task_6_5.py                         # Master multi-filter diagnostic report
│   ├── experiment_06.py                     # Master pipeline execution script
│   ├── requirements.txt                    # Project dependency specification
│   └── run_all.py                          # Master runner script
├── Report/
│   ├── Experiment_06_Report.docx           # Publication-grade academic laboratory report
│   └── Experiment_06_Report.pdf            # Compiled authentic PDF laboratory report
├── Tables/                                 # Quantitative metric exports (CSV)
│   ├── exp06_benchmark_summary_py.csv      # Python master benchmarking summary
│   ├── exp06_benchmark_summary_matlab.csv  # MATLAB master benchmarking summary
│   ├── exp06_task_6_2_ilpf_ringing_metrics.csv # ILPF Gibbs ripple quantification
│   ├── exp06_task_6_3_blpf_sweep_metrics.csv   # BLPF order sweep metrics
│   └── exp06_task_6_4_contrast_metrics.csv # GLPF vs GHPF contrast & DC metrics
├── Tests/
│   ├── test_experiment_06.py               # Comprehensive 9-test validation suite
│   └── test_results.txt                    # Formatted test execution report (100% Pass)
└── build_report.py                         # Automated DOCX & PDF university report builder
```

---

### 3. Execution Instructions

#### 3.1 Python Execution (Compatible with macOS, Linux, and Windows)
1. Install dependencies:
   ```bash
   pip install -r Python/requirements.txt
   ```
2. Execute the master pipeline:
   ```bash
   python Python/run_all.py
   ```
3. Run the automated test suite:
   ```bash
   python Tests/test_experiment_06.py
   ```

#### 3.2 MATLAB Execution (R2026a or compatible)
Open MATLAB and run:
```matlab
cd('MATLAB');
run_all;
```
Or execute from terminal/CLI:
```bash
matlab -batch "cd('MATLAB'); run_all;"
```

#### 3.3 Report Generation
To regenerate the university laboratory report (`Experiment_06_Report.docx` and `Experiment_06_Report.pdf`):
```bash
python build_report.py
```

---

### 4. Key Quantitative Results Summary

| Filter Name | Type | Cutoff $D_0$ | Order $n$ | Energy Ret (%) | PSNR (dB) | SSIM | Ringing Artifacts | Clinical Verdict |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **Ideal LP (ILPF)** | Low-Pass | 40 px | $\infty$ | 93.85% | 27.51 dB | 0.7664 | Severe (Sinc Ripples) | **Contraindicated** |
| **Butterworth LP** | Low-Pass | 40 px | 2 | 90.27% | 28.92 dB | 0.8612 | Zero (Smooth Rolloff) | **CLINICAL GOLD STANDARD** |
| **Gaussian LP (GLPF)** | Low-Pass | 40 px | Gauss | 89.29% | 30.10 dB | 0.8960 | Zero (100% Ripple-Free) | **Optimal Pre-Segmentation** |
| **Gaussian HP (GHPF)** | High-Pass | 50 px | Gauss | 2.05% | 16.91 dB | 0.3890 | Zero (DC Hallowed) | **Micro-Structure Isolation** |

- **Parseval Conservation**: Energy error between spatial domain and frequency domain $< 10^{-10}$.
- **Core Concentration**: $>95\%$ of total anatomical power concentrated in low frequencies ($D \le 45$ px).
- **DC Elimination**: Gaussian High-Pass filter successfully reduces spatial mean brightness from $27.88$ to $0.00$, demonstrating complete removal of bulk parenchymal background.
