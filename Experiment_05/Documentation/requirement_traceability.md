# Requirement Traceability Matrix (RTM) - Experiment 05
## Edge Detection in Medical Images Using Sobel, Prewitt, and Canny Operators: Implementation and Comparative Analysis

**Course**: Medical Image Processing | **Institution**: Riphah International University  
**Instructor**: Engr. Rana Talha Khalid | **Targeted CLO**: CLO 1 (Psychomotor - P2) | **Mapped PLO**: PLO 5 (Modern Tool Usage)  

---

| Req ID | Manual Requirement / Task Description | Target Metric / Deliverable | Python Implementation | MATLAB Implementation | Verification Test | Status |
|:---:|:---|:---|:---|:---|:---|:---:|
| **REQ-01** | Zero-Sum Kernel Mechanics | Prove $\sum w(s,t) = 0.0$ for edge kernels, canceling flat tissue to 0 and spiking at boundaries | `Python/example_01.py` | `MATLAB/example_01.m` | `test_02_zero_sum_kernels` | **VERIFIED** |
| **REQ-02** | Example 01: Multi-Operator Benchmark | Benchmark Prewitt, Sobel, and Canny on clinical CT; verify Canny 1-px skeletonization | `Python/example_01.py` | `MATLAB/example_01.m` | `test_03_example_01_execution` | **VERIFIED** |
| **REQ-03** | Task 5.1: Discrete Gradient Kernels | Convolve horizontal ($G_x$) and vertical ($G_y$) Sobel kernels independently | `Python/task_5_1.py` | `MATLAB/task_5_1.m` | `test_04_task_5_1_directional_sensitivity` | **VERIFIED** |
| **REQ-04** | Task 5.1: Directional Sensitivity | Identify anatomical features: $G_x$ vertical edges (sagittal suture) vs $G_y$ horizontal edges (cranial vault) | `Python/task_5_1.py` | `MATLAB/task_5_1.m` | `test_04_task_5_1_directional_sensitivity` | **VERIFIED** |
| **REQ-05** | Task 5.1: HSV Orientation Map | Compute $\theta = \arctan(G_y/G_x)$ mapped to $[0, 180^\circ)$, display HSV direction map | `Python/task_5_1.py` | `MATLAB/task_5_1.m` | `test_04_task_5_1_directional_sensitivity` | **VERIFIED** |
| **REQ-06** | Task 5.2: Noise Sensitivity Benchmark | Add Gaussian noise ($\sigma=15$), measure false edges in background air ROI | `Python/task_5_2.py` | `MATLAB/task_5_2.m` | `test_05_task_5_2_noise_sensitivity` | **VERIFIED** |
| **REQ-07** | Task 5.2: Binomial Smoothing Advantage | Explain mathematically why Sobel $[1, 2, 1]^T$ binomial filter rejects noise vs. Prewitt $[1, 1, 1]^T$ | `Python/task_5_2.py` | `MATLAB/task_5_2.m` | `test_05_task_5_2_noise_sensitivity` | **VERIFIED** |
| **REQ-08** | Task 5.3: Manual NMS Algorithm | Implement Stage 3 Canny from scratch: quantize $\theta$ into 4 sectors ($0^\circ, 45^\circ, 90^\circ, 135^\circ$) | `Python/task_5_3.py` | `MATLAB/task_5_3.m` | `test_06_task_5_3_manual_nms` | **VERIFIED** |
| **REQ-09** | Task 5.3: Ridge Thinning Verification | Suppress non-maximal pixels along normal, prove $>50\%$ data reduction with 1-pixel skeletons | `Python/task_5_3.py` | `MATLAB/task_5_3.m` | `test_06_task_5_3_manual_nms` | **VERIFIED** |
| **REQ-10** | Task 5.4: Hysteresis Threshold Tuning | Sweep $T_{\text{high}} \in [80, 150, 220]$ and $T_{\text{low}} \in [15, 50, 100]$ across 6 clinical cases | `Python/task_5_4.py` | `MATLAB/task_5_4.m` | `test_07_task_5_4_hysteresis_tuning` | **VERIFIED** |
| **REQ-11** | Task 5.4: Broken Contour Analysis | Analyze clinical tradeoffs: broken bone contours vs. spurious noise clutter in brain tissue | `Python/task_5_4.py` | `MATLAB/task_5_4.m` | `test_07_task_5_4_hysteresis_tuning` | **VERIFIED** |
| **REQ-12** | Task 5.5: Multi-Panel Diagnostic Report | Publication-grade $2\times 3$ panel: CT, Prewitt, Sobel, Canny, 1D Profile, Benchmark chart | `Python/task_5_5.py` | `MATLAB/task_5_5.m` | `test_08_task_5_5_diagnostic_benchmark` | **VERIFIED** |
| **REQ-13** | Task 5.5: 1D Anatomical Edge Profile | Extract row $H/2$ transect showing broad Sobel/Prewitt bell curve vs Canny razor spike | `Python/task_5_5.py` | `MATLAB/task_5_5.m` | `test_08_task_5_5_diagnostic_benchmark` | **VERIFIED** |
| **REQ-14** | Task 5.5: Pratt's Figure of Merit | Compute Pratt's FOM ($\ge 0.75$), skeleton width ($1.0$ px vs $3.8-4.2$ px), and export CSV | `Python/task_5_5.py` | `MATLAB/task_5_5.m` | `test_08_task_5_5_diagnostic_benchmark` | **VERIFIED** |
| **REQ-15** | Deliverable Figure Completeness | 12 high-resolution figures generated in `Figures/` (>200 KB each) | Both Pipelines | Both Pipelines | `test_09_all_figures_exist` | **VERIFIED** |
| **REQ-16** | University Report Compliance | 12 mandatory sections, no cover/TOC, top header opening, DOCX & PDF generation | `build_report.py` | Word COM | COM File Generation | **VERIFIED** |
