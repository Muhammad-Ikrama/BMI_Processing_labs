# Requirement Traceability Matrix (RTM) - Experiment 04
## Noise Modeling and Removal in Medical Images Using Median and Adaptive Filtering Techniques

**Course**: Medical Image Processing | **Institution**: Riphah International University  
**Instructor**: Engr. Rana Talha Khalid | **Targeted CLO**: CLO 1 (P2) | **Mapped PLO**: PLO 5  

---

| Req ID | Manual Requirement / Task Description | Target Metric / Deliverable | Python Implementation | MATLAB Implementation | Verification Test | Status |
|:---:|:---|:---|:---|:---|:---|:---:|
| **REQ-01** | Medical Noise Modeling | Additive Gaussian ($\sigma=20$), 15% Salt & Pepper, Speckle ($\sigma^2=0.25$) | `Python/task_4_1.py` | `MATLAB/task_4_1.m` | `test_02_noise_residual_statistics` | **VERIFIED** |
| **REQ-02** | Residual Statistical Moments | Compute empirical histogram and PDF of $(g - f)$, verify zero-mean Gaussian | `Python/task_4_1.py` | `MATLAB/task_4_1.m` | `test_02_noise_residual_statistics` | **VERIFIED** |
| **REQ-03** | Task 4.2: Linear Filter Failure Analysis | Apply Mean 5x5 & Gaussian 5x5 on 10% impulse noise, prove smear mechanism | `Python/task_4_2.py` | `MATLAB/task_4_2.m` | `test_03_linear_filter_failure_on_impulses` | **VERIFIED** |
| **REQ-04** | Task 4.2: Uniform Region Magnification | Display 60x60 magnified patch, quantify 10.2 intensity level smear per impulse | `Python/task_4_2.py` | `MATLAB/task_4_2.m` | `test_03_linear_filter_failure_on_impulses` | **VERIFIED** |
| **REQ-05** | Task 4.3: Standard Median Filter Sweep | Sweep windows $[3\times 3, 5\times 5, 7\times 7]$ on 15% impulse noise | `Python/task_4_3.py` | `MATLAB/task_4_3.m` | `test_04_median_window_sensitivity` | **VERIFIED** |
| **REQ-06** | Task 4.3: Edge Preservation Index (EPI) | Calculate Laplacian correlation $\beta$, plot SSIM and EPI vs. window dimension | `Python/task_4_3.py` | `MATLAB/task_4_3.m` | `test_04_median_window_sensitivity` | **VERIFIED** |
| **REQ-07** | Task 4.4: Two-Stage AMF Implementation | Custom two-stage algorithm (Gonzalez & Woods), window expansion 3 to 9 | `Python/task_4_4.py` | `MATLAB/task_4_4.m` | `test_05_amf_high_density_superiority` | **VERIFIED** |
| **REQ-08** | Task 4.4: High-Density Stress Test | Test across $[10\%, 25\%, 40\%, 50\%]$ impulse noise, prove AMF > Standard Median | `Python/task_4_4.py` | `MATLAB/task_4_4.m` | `test_05_amf_high_density_superiority` | **VERIFIED** |
| **REQ-09** | Task 4.4: Corner Truncation Prevention | Prove AMF preserves uncorrupted pixels ($z_{\min} < z_{xy} < z_{\max}$) untouched | `Python/task_4_4.py` | `MATLAB/task_4_4.m` | `test_05_amf_high_density_superiority` | **VERIFIED** |
| **REQ-10** | Task 4.5: Multi-Panel Diagnostic Report | $2\times 3$ panel: Reference, Noisy, Mean 5x5, Median 3x3, AMF, 1D Edge Profile | `Python/task_4_5.py` | `MATLAB/task_4_5.m` | `test_07_all_figures_generated` | **VERIFIED** |
| **REQ-11** | Task 4.5: 1D Profile across Ventricle | Measure edge sharpness across Row 256, proving AMF follows true slope | `Python/task_4_5.py` | `MATLAB/task_4_5.m` | `test_07_all_figures_generated` | **VERIFIED** |
| **REQ-12** | Task 4.5: Summary Table Export | Export `task_4_5_restoration_benchmark_summary.csv` | `Python/task_4_5.py` | `MATLAB/task_4_5.m` | `test_06_benchmark_table_export` | **VERIFIED** |
| **REQ-13** | Deliverable Figure Completeness | All 12 figures generated in `Figures/` (>50 KB) | Both Pipelines | Both Pipelines | `test_07_all_figures_generated` | **VERIFIED** |
| **REQ-14** | University Report Compliance | 12 mandatory sections, no cover/TOC, DOCX & PDF generation | `build_report.py` | Word COM | COM File Generation | **VERIFIED** |
