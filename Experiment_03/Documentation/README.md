# Experiment 03: Image Smoothing of Medical Images Using Spatial Domain Mean/Averaging and Gaussian Filters

**Course**: Medical Image Processing (B.Sc. Biomedical Engineering, 6th Semester)  
**Institution**: Faculty of Engineering & Applied Sciences, Department of Biomedical Engineering, Riphah International University, Lahore  
**Course Instructor**: Engr. Rana Talha Khalid, Lab Engineer  
**Targeted CLO**: CLO 1 (Psychomotor - P2) | **Mapped PLO**: PLO 5 (Modern Tool Usage)  

---

## 1. Executive Summary and Clinical Rationale
In clinical imaging modalities (Magnetic Resonance Imaging, Computed Tomography, Ultrasound, Digital Radiography), physical sensor noise inevitably degrades diagnostic quality:
- **MRI**: Thermal Radiofrequency (RF) electronic noise in receiver coils, characterized by high-frequency Gaussian-distributed perturbations.
- **CT**: Quantum mottle arising from low-dose photon starvation in high-speed helical scans.
- **Ultrasound**: Speckle noise from coherent acoustic backscattering interference.

Prior to automated computer-aided detection (CADe), anatomical tissue segmentation, or 3D volume reconstruction, clinical images must undergo spatial domain smoothing to suppress stochastic noise while preserving critical diagnostic boundaries.

This laboratory experiment rigorously implements and benchmarks:
1. **2D Spatial Discrete Convolution Mechanics**: Sliding window Multiply-Accumulate (MAC) algorithms and boundary padding strategies (Zero-Padding vs. Replicate/Clamp-Padding).
2. **Spatial Mean (Box Averaging) Filtering**: Noise variance attenuation $\sigma^2 / K^2$ vs. isotropic boundary erosion across kernel dimensions $K \in [3, 5, 7, 9]$.
3. **2D Isotropic Gaussian Smoothing**: Discrete kernel construction from continuous bell-curve equations, spatial spread $\sigma \in [0.6, 1.2, 2.0]$, rotational symmetry, and separability advantage.
4. **Quantitative Quality Benchmarking**: Rigorous evaluation using Peak Signal-to-Noise Ratio (PSNR), Structural Similarity Index (SSIM), and Contrast-to-Noise Ratio (CNR).
5. **1D Anatomical Edge Gradient Profiles**: Objective measurement of the 10% to 90% intensity transition rise width ($W_{10-90}$) across cortical margins.

---

## 2. Directory Architecture
```
Biomedical_Image_Processing_Lab/
└── Experiment_03/
    ├── Documentation/
    │   ├── README.md
    │   └── requirement_traceability.md
    ├── Figures/
    │   ├── exp03_example_01_filtering_benchmark_py.png
    │   ├── exp03_example_01_filtering_benchmark_m.png
    │   ├── exp03_task_3_1_boundary_padding_py.png
    │   ├── exp03_task_3_1_boundary_padding_m.png
    │   ├── exp03_task_3_2_mean_kernel_sweep_py.png
    │   ├── exp03_task_3_2_mean_kernel_sweep_m.png
    │   ├── exp03_task_3_3_gaussian_kernel_sweep_py.png
    │   ├── exp03_task_3_3_gaussian_kernel_sweep_m.png
    │   ├── exp03_task_3_4_quality_benchmarking_py.png
    │   ├── exp03_task_3_4_quality_benchmarking_m.png
    │   ├── exp03_task_3_5_edge_profile_py.png
    │   └── exp03_task_3_5_edge_profile_m.png
    ├── Inputs/
    │   └── images/
    │       └── MRI.jpg
    ├── MATLAB/
    │   ├── example_01.m
    │   ├── task_3_1.m
    │   ├── task_3_2.m
    │   ├── task_3_3.m
    │   ├── task_3_4.m
    │   ├── task_3_5.m
    │   ├── experiment_03.m
    │   └── run_all.m
    ├── Outputs/
    │   ├── MATLAB/
    │   └── Python/
    ├── Python/
    │   ├── example_01.py
    │   ├── task_3_1.py
    │   ├── task_3_2.py
    │   ├── task_3_3.py
    │   ├── task_3_4.py
    │   ├── task_3_5.py
    │   ├── experiment_03.py
    │   ├── run_all.py
    │   └── requirements.txt
    ├── Report/
    │   ├── Experiment_03_Report.docx
    │   └── Experiment_03_Report.pdf
    ├── Tables/
    │   └── task_3_4_smoothing_benchmark_summary.csv
    ├── Tests/
    │   ├── test_experiment_03.py
    │   └── test_results.txt
    └── build_report.py
```

---

## 3. Mathematical Foundations

### 3.1 2D Discrete Spatial Convolution
$$g(x, y) = \sum_{s=-a}^{a} \sum_{t=-b}^{b} w(s, t) \cdot f(x + s, y + t)$$
For a kernel of size $K \times K$ with $a = b = \lfloor K/2 \rfloor$.

### 3.2 2D Continuous Isotropic Gaussian Formulation
$$G(x, y) = \frac{1}{2\pi\sigma^2} \exp\left(-\frac{x^2 + y^2}{2\sigma^2}\right)$$
Discrete coefficients are normalized over kernel window $\Omega$:
$$w(x, y) = \frac{G(x, y)}{\sum_{(u, v) \in \Omega} G(u, v)}$$
Ensuring $\sum w(x, y) = 1.000000$ to maintain photometric brightness equilibrium.

### 3.3 Contrast-to-Noise Ratio (CNR)
$$\text{CNR} = \frac{|\mu_{\text{signal}} - \mu_{\text{background}}|}{\sqrt{\sigma_{\text{signal}}^2 + \sigma_{\text{background}}^2}}$$

### 3.4 10% to 90% Edge Transition Width ($W_{10-90}$)
$$T_{10} = I_{\min} + 0.10 \cdot (I_{\max} - I_{\min}), \quad T_{90} = I_{\min} + 0.90 \cdot (I_{\max} - I_{\min})$$
$$W_{10-90} = |x_{90} - x_{10}| \quad [\text{pixels}]$$

---

## 4. Execution Commands

### Python Pipeline
```powershell
# Navigate to Python directory
cd "d:\BME\7th sem\biomedical Image Processing\labs\Biomedical_Image_Processing_Lab\Experiment_03\Python"

# Execute entire suite
python experiment_03.py
```

### MATLAB Pipeline
```powershell
# Execute entire MATLAB batch suite
& "C:\Program Files\MATLAB\R2026a\bin\matlab.exe" -batch "run('d:/BME/7th sem/biomedical Image Processing/labs/Biomedical_Image_Processing_Lab/Experiment_03/MATLAB/experiment_03.m');"
```

### Automated Testing & Validation
```powershell
cd "d:\BME\7th sem\biomedical Image Processing\labs\Biomedical_Image_Processing_Lab\Experiment_03\Tests"
python test_experiment_03.py
```

### Report Generation
```powershell
cd "d:\BME\7th sem\biomedical Image Processing\labs\Biomedical_Image_Processing_Lab\Experiment_03"
python build_report.py
```
