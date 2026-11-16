# Requirement Traceability Matrix (RTM) - Experiment 03
## Image Smoothing of Medical Images Using Spatial Domain Mean & Gaussian Filters

**Course**: Medical Image Processing | **Institution**: Riphah International University  
**Instructor**: Engr. Rana Talha Khalid | **Targeted CLO**: CLO 1 (P2) | **Mapped PLO**: PLO 5  

---

| Req ID | Manual Requirement / Task Description | Target Metric / Deliverable | Python Implementation | MATLAB Implementation | Verification Test | Status |
|:---:|:---|:---|:---|:---|:---|:---:|
| **REQ-01** | Reference scan acquisition & thermal noise simulation | Load `images/MRI.jpg` (512x512 uint8), simulate Gaussian noise ($\sigma=18.0$) | `Python/example_01.py` | `MATLAB/example_01.m` | `test_01_input_image_integrity` | **VERIFIED** |
| **REQ-02** | Baseline Filtering Benchmark | Mean 3x3, Mean 5x5, Gauss 3x3 ($\sigma=0.8$), Gauss 5x5 ($\sigma=1.2$) | `Python/example_01.py` | `MATLAB/example_01.m` | `test_05_gaussian_vs_mean_tradeoff` | **VERIFIED** |
| **REQ-03** | Task 3.1: 2D Spatial Discrete Convolution & Boundary Padding Comparison | Custom convolution under Zero vs. Replicate padding, boundary MAE/RMSE | `Python/task_3_1.py` | `MATLAB/task_3_1.m` | `test_02_custom_convolution_boundary_modes` | **VERIFIED** |
| **REQ-04** | Task 3.1: Perimeter Magnification & Halo Artifact Analysis | Magnify first 25 rows/cols, quantify dark perimeter decay | `Python/task_3_1.py` | `MATLAB/task_3_1.m` | `test_02_custom_convolution_boundary_modes` | **VERIFIED** |
| **REQ-05** | Task 3.2: Spatial Mean Averaging Filter Sweep | Kernels $[3\times 3, 5\times 5, 7\times 7, 9\times 9]$, PSNR & SSIM curves | `Python/task_3_2.py` | `MATLAB/task_3_2.m` | `test_03_mean_kernel_monotonicity` | **VERIFIED** |
| **REQ-06** | Task 3.2: Oversmoothing & Diagnostic Hazard Identification | Identify critical threshold where blurring destroys microcalcifications | `Python/task_3_2.py` | `MATLAB/task_3_2.m` | `test_03_mean_kernel_monotonicity` | **VERIFIED** |
| **REQ-07** | Task 3.3: 2D Gaussian Kernel Construction from Formula | Custom 7x7 kernel from $G(x,y)=\frac{1}{2\pi\sigma^2}e^{-(x^2+y^2)/(2\sigma^2)}$ | `Python/task_3_3.py` | `MATLAB/task_3_3.m` | `test_04_gaussian_kernel_normalization` | **VERIFIED** |
| **REQ-08** | Task 3.3: Discrete Normalization Verification | Verify sum of 49 kernel weights equals $1.000000 \pm 10^{-6}$ | `Python/task_3_3.py` | `MATLAB/task_3_3.m` | `test_04_gaussian_kernel_normalization` | **VERIFIED** |
| **REQ-09** | Task 3.3: Spread Parameter Sweep ($\sigma = 0.6, 1.2, 2.0$) | 2D heatmaps, 3D bell surfaces, filtered scans | `Python/task_3_3.py` | `MATLAB/task_3_3.m` | `test_04_gaussian_kernel_normalization` | **VERIFIED** |
| **REQ-10** | Task 3.4: Quantitative Benchmarking (PSNR, SSIM, CNR) | Signal ROI (Cortex) & Background Air ROI, evaluate PSNR, SSIM, CNR | `Python/task_3_4.py` | `MATLAB/task_3_4.m` | `test_05_gaussian_vs_mean_tradeoff` | **VERIFIED** |
| **REQ-11** | Task 3.4: 'Good to Go' Clinical Verification | Verify PSNR $\ge 28$ dB, SSIM $\ge 0.50$, CNR $\ge 1.0$ | `Python/task_3_4.py` | `MATLAB/task_3_4.m` | `test_05_gaussian_vs_mean_tradeoff` | **VERIFIED** |
| **REQ-12** | Task 3.4: Summary Table Export | Export `task_3_4_smoothing_benchmark_summary.csv` | `Python/task_3_4.py` | `MATLAB/task_3_4.m` | `test_06_benchmark_table_export` | **VERIFIED** |
| **REQ-13** | Task 3.5: 1D Anatomical Edge Gradient Profiles | Row 256 cross-section across cortical margin, cols 125-175 | `Python/task_3_5.py` | `MATLAB/task_3_5.m` | `test_07_all_figures_generated` | **VERIFIED** |
| **REQ-14** | Task 3.5: 10% to 90% Transition Width ($W_{10-90}$) | Quantify pixel rise width, prove Gaussian preserves steepness | `Python/task_3_5.py` | `MATLAB/task_3_5.m` | `test_07_all_figures_generated` | **VERIFIED** |
| **REQ-15** | Deliverable Figure Completeness | All 12 figures generated in `Figures/` (>50 KB) | Both Pipelines | Both Pipelines | `test_07_all_figures_generated` | **VERIFIED** |
| **REQ-16** | Academic Report Quality & Structure | 12 mandatory sections, no cover/TOC, DOCX & PDF generation | `build_report.py` | Word COM | COM File Generation | **VERIFIED** |
