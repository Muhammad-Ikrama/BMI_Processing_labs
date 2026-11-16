# Requirement Traceability Matrix (RTM) - Experiment 06
## Frequency-Domain Filtering of Medical Images Using the 2-D Fourier Transform: Low-Pass and High-Pass Filter Design and Analysis

**Course**: Medical Image Processing | **Institution**: Riphah International University  
**Department**: Biomedical Engineering | **Faculty**: Engr. Rana Talha Khalid, Lab Engineer  
**Semester**: 6th (B.Sc. Biomedical Engineering)  

---

| Req ID | Instructor Requirement / Task Description | Target Metric / Deliverable | Python Implementation | MATLAB Implementation | Evidence File / Test | Validation Status |
|:---:|:---|:---|:---|:---|:---|:---:|
| **REQ-01** | Mathematical 2D-DFT Formulation | Forward/inverse 2D-DFT, spectrum centering via $(-1)^{x+y}$ / `fftshift`, log dynamic range compression | `Python/task_6_1.py` | `MATLAB/task_6_1.m` | `test_03_task_6_1_dc_energy_and_parseval` | **COMPLETE** |
| **REQ-02** | Example 01: Baseline LP Benchmark | Benchmark ILPF, BLPF ($n=2$), and GLPF ($D_0=40$ px) on clinical MRI scan; evaluate Energy Retention, PSNR, and SSIM | `Python/example_01.py` | `MATLAB/example_01.m` | `exp06_example_01_benchmark_py.png`, `_m.png` | **COMPLETE** |
| **REQ-03** | Task 6.1: 2D-DFT Spectrum Computation | Compute uncentered and centered 2D-DFT; identify DC coordinate at $(0,0)$ / $(1,1)$ uncentered vs $(256,256)$ / $(257,257)$ centered | `Python/task_6_1.py` | `MATLAB/task_6_1.m` | `exp06_task_6_1_dft_spectrum_py.png`, `_m.png` | **COMPLETE** |
| **REQ-04** | Task 6.1: Energy Distribution Analysis | Verify Parseval theorem ($E_{\text{spatial}} = E_{\text{freq}}$); quantify DC energy fraction ($40.66\%$ of total power) | `Python/task_6_1.py` | `MATLAB/task_6_1.m` | `test_03_task_6_1_dc_energy_and_parseval` | **COMPLETE** |
| **REQ-05** | Task 6.1: Radial Energy Concentration | Prove $>95\%$ signal energy resides within low-frequency core radius $D \le 45$ pixels | `Python/task_6_1.py` | `MATLAB/task_6_1.m` | `test_03_task_6_1_dc_energy_and_parseval` | **COMPLETE** |
| **REQ-06** | Task 6.1: Crosshair Windowing Artifact | Analyze horizontal/vertical radiating arms as non-periodic boundary leakage from rectangular aperture truncation | `Python/task_6_1.py` | `MATLAB/task_6_1.m` | `exp06_task_6_1_dft_spectrum_py.png` | **COMPLETE** |
| **REQ-07** | Task 6.2: ILPF Cutoff Sensitivity Sweep | Sweep Ideal LP filter cutoff across $D_0 \in [20, 40, 80]$ pixels; reconstruct spatial outputs | `Python/task_6_2.py` | `MATLAB/task_6_2.m` | `exp06_task_6_2_ilpf_gibbs_ringing_py.png`, `_m.png` | **COMPLETE** |
| **REQ-08** | Task 6.2: Gibbs Ringing Edge Transect | Extract 1D intensity profile across cranial bone-brain interface (Row 256, Cols 50–190); measure ripple oscillations | `Python/task_6_2.py` | `MATLAB/task_6_2.m` | `exp06_task_6_2_ilpf_gibbs_ringing_py.png` | **COMPLETE** |
| **REQ-09** | Task 6.2: Clinical Contraindication | Quantify peak-to-peak ripple amplitude ($30-34$ px) and explain why ringing mimics subdural hematomas and dissection | `Python/task_6_2.py` | `MATLAB/task_6_2.m` | `exp06_task_6_2_ilpf_ringing_metrics.csv` | **COMPLETE** |
| **REQ-10** | Task 6.3: BLPF Order Sensitivity Sweep | Design Butterworth LP filter with $D_0=40$ px; sweep order $n \in [1, 2, 4, 8]$; reconstruct spatial scans | `Python/task_6_3.py` | `MATLAB/task_6_3.m` | `exp06_task_6_3_blpf_order_sweep_py.png`, `_m.png` | **COMPLETE** |
| **REQ-11** | Task 6.3: 1D Radial Transfer Functions | Plot radial curves $H(D)$ vs $D$, illustrating transition slope steepening towards ideal step as $n \to \infty$ | `Python/task_6_3.py` | `MATLAB/task_6_3.m` | `exp06_task_6_3_blpf_order_sweep_py.png` | **COMPLETE** |
| **REQ-12** | Task 6.3: Ringing Onset & Clinical Standard | Determine critical order $n=4$ where ripples emerge; establish $n=2$ as the maximally-flat clinical gold standard | `Python/task_6_3.py` | `MATLAB/task_6_3.m` | `exp06_task_6_3_blpf_sweep_metrics.csv` | **COMPLETE** |
| **REQ-13** | Task 6.4: Complementary GLPF & GHPF | Construct matched Gaussian LP and HP filters ($D_0=50$ px, $H_{\text{GHP}} = 1 - H_{\text{GLP}}$); reconstruct spatial scans | `Python/task_6_4.py` | `MATLAB/task_6_4.m` | `exp06_task_6_4_glpf_ghpf_contrast_py.png`, `_m.png` | **COMPLETE** |
| **REQ-14** | Task 6.4: Mathematical DC Hollowing | Prove $H_{\text{GHPF}}(0,0)=0$, zeroing spatial background brightness ($\mu \approx 0.00$) while isolating high frequencies | `Python/task_6_4.py` | `MATLAB/task_6_4.m` | `test_06_task_6_4_ghpf_dc_elimination` | **COMPLETE** |
| **REQ-15** | Task 6.4: Contrast & Boundary Metrics | Tabulate Spectral Energy Retention ($91.7\%$ vs $2.05\%$), Mean Brightness, and Michelson Contrast | `Python/task_6_4.py` | `MATLAB/task_6_4.m` | `exp06_task_6_4_contrast_metrics.csv` | **COMPLETE** |
| **REQ-16** | Task 6.5: Publication 2x3 Diagnostic Panel | Construct $2\times 3$ diagnostic panel: Input Scan, Centered Spectrum, ILPF, BLPF ($n=2$), GLPF, GHPF | `Python/task_6_5.py` | `MATLAB/task_6_5.m` | `exp06_task_6_5_diagnostic_report_py.png`, `_m.png` | **COMPLETE** |
| **REQ-17** | Task 6.5: Quantitative Benchmarking CSV | Export comprehensive metrics (Energy Retention, PSNR, SSIM, Ringing, Verdict) for Python and MATLAB | `Python/task_6_5.py` | `MATLAB/task_6_5.m` | `exp06_benchmark_summary_py.csv`, `_matlab.csv` | **COMPLETE** |
| **REQ-18** | Figure Completeness (>200 KB each) | Generate 12 high-resolution publication-grade figures in `Figures/` across both runtime environments | Both Pipelines | Both Pipelines | `test_08_deliverable_figures_completeness` | **COMPLETE** |
| **REQ-19** | Cross-Platform Concordance | Verify numerical agreement between MATLAB R2026a and Python 3.14 ($\Delta\text{PSNR} < 0.5$ dB, $\Delta\text{SSIM} < 0.05$) | Both Pipelines | Both Pipelines | `test_09_matlab_python_concordance` | **COMPLETE** |
| **REQ-20** | University Report Compliance | 12 mandatory sections, top header opening on Page 1, no cover/TOC/rubrics, DOCX & PDF generation via Word COM | `build_report.py` | Word COM | `Experiment_06_Report.docx`, `.pdf` | **COMPLETE** |
