# Experiment 04: Noise Modeling and Removal in Medical Images Using Median and Adaptive Filtering Techniques

**Course**: Medical Image Processing (B.Sc. Biomedical Engineering, 6th Semester)  
**Institution**: Faculty of Engineering & Applied Sciences, Department of Biomedical Engineering, Riphah International University, Lahore  
**Course Instructor**: Engr. Rana Talha Khalid, Lab Engineer  
**Targeted CLO**: CLO 1 (Psychomotor - P2) | **Mapped PLO**: PLO 5 (Modern Tool Usage)  

---

## 1. Executive Summary & Clinical Rationale
Medical imaging systems are susceptible to distinct physical noise mechanisms:
- **Thermal RF Gaussian Noise**: Thermal agitation of electrons in MRI receiver coils and preamplifiers.
- **Salt-and-Pepper Impulse Noise**: Faulty detector elements in solid-state CT detector rings, digital radiography plates, and telemetry bit drops.
- **Speckle Noise**: Multiplicative interference from sub-resolution acoustic scatterers in B-mode Ultrasound and Optical Coherence Tomography (OCT).
- **Poisson Quantum Mottle**: Low-dose photon counting statistics in PET, SPECT, and low-dose CT protocols.

### Linear Filter Failure on Impulse Noise
Linear smoothing filters (Mean and Gaussian) compute arithmetic weighted averages. When an extreme outlier (pepper = 0 or salt = 255) enters a $K \times K$ window, it arithmetically contaminates all $K^2 - 1$ neighboring pixels. A single salt impulse adds $+255 / K^2$ intensity units ($+10.2$ levels for $5 \times 5$) to all neighbors, converting isolated sharp dots into broad, low-contrast gray smudge blotches.

### Non-Linear Order-Statistics & Adaptive Filtering Solution
1. **Standard Median Filter**: Sorts pixels $\{z_1 \le z_2 \le \dots \le z_N\}$ and outputs the numerical median $z_{(N+1)/2}$. Extreme outliers are pushed to the sorted tails and completely discarded.
2. **Two-Stage Adaptive Median Filter (AMF)**: Dynamically expands window from $S_{\min}=3$ to $S_{\max}=9$.
   - **Stage A**: Checks if median $z_{\text{med}}$ is clean ($z_{\min} < z_{\text{med}} < z_{\max}$). If not, expands window.
   - **Stage B**: Checks if central pixel $z_{xy}$ is clean. If clean, preserves it with 100% fidelity. If corrupted, replaces it with $z_{\text{med}}$.
   - **Advantage**: Uncorrupted pixels are untouched, eliminating the corner rounding and fine line truncation inherent to standard median filtering.

---

## 2. Directory Architecture
```
Biomedical_Image_Processing_Lab/
└── Experiment_04/
    ├── Documentation/
    │   ├── README.md
    │   └── requirement_traceability.md
    ├── Figures/ (12 High-Resolution PNG Figures)
    ├── Inputs/
    │   └── images/ (MRI.jpg, CT.jpg)
    ├── MATLAB/ (8 M-Scripts)
    ├── Outputs/ (MATLAB/ and Python/ subdirectories)
    ├── Python/ (8 Python scripts + requirements.txt)
    ├── Report/
    │   ├── Experiment_04_Report.docx
    │   └── Experiment_04_Report.pdf
    ├── Tables/
    │   └── task_4_5_restoration_benchmark_summary.csv
    ├── Tests/
    │   ├── test_experiment_04.py
    │   └── test_results.txt (7/7 Passed, 100%)
    └── build_report.py
```

---

## 3. Mathematical Formulations

### 3.1 Noise Probability Density Functions (PDFs)
- **Gaussian Noise**:
  $$p(z) = \frac{1}{\sqrt{2\pi}\sigma} \exp\left(-\frac{(z - \mu)^2}{2\sigma^2}\right)$$
- **Bipolar Salt-and-Pepper Impulse Noise**:
  $$p(z) = \begin{cases} P_a & \text{for } z = a \quad (\text{Pepper} = 0) \\ P_b & \text{for } z = b \quad (\text{Salt} = 255) \\ 0 & \text{otherwise} \end{cases}$$
- **Multiplicative Speckle Noise**:
  $$g(x, y) = f(x, y) + f(x, y) \cdot \eta(x, y), \quad \eta \sim \mathcal{N}(0, \sigma^2)$$

### 3.2 Two-Stage Adaptive Median Filtering (AMF)
- **Stage A**:
  $$A_1 = z_{\text{med}} - z_{\min}, \quad A_2 = z_{\text{med}} - z_{\max}$$
  If $A_1 > 0$ and $A_2 < 0 \implies$ Go to Stage B; Else $S_{xy} \leftarrow S_{xy} + 2$. If $S_{xy} \le S_{\max}$, Repeat Stage A; Else Output $z_{\text{med}}$.
- **Stage B**:
  $$B_1 = z_{xy} - z_{\min}, \quad B_2 = z_{xy} - z_{\max}$$
  If $B_1 > 0$ and $B_2 < 0 \implies$ Output $z_{xy}$ (clean pixel untouched); Else Output $z_{\text{med}}$.

### 3.3 Edge Preservation Index (EPI / $\beta$)
$$\beta = \frac{\sum (\Delta f - \overline{\Delta f})(\Delta g - \overline{\Delta g})}{\sqrt{\sum (\Delta f - \overline{\Delta f})^2 \sum (\Delta g - \overline{\Delta g})^2}}$$

---

## 4. Execution Commands

### Python Pipeline
```powershell
cd "d:\BME\7th sem\biomedical Image Processing\labs\Biomedical_Image_Processing_Lab\Experiment_04\Python"
python experiment_04.py
```

### MATLAB Pipeline
```powershell
& "C:\Program Files\MATLAB\R2026a\bin\matlab.exe" -batch "run('d:/BME/7th sem/biomedical Image Processing/labs/Biomedical_Image_Processing_Lab/Experiment_04/MATLAB/experiment_04.m');"
```

### Automated Validation Test Suite
```powershell
cd "d:\BME\7th sem\biomedical Image Processing\labs\Biomedical_Image_Processing_Lab\Experiment_04\Tests"
python test_experiment_04.py
```

### University Report Compilation
```powershell
cd "d:\BME\7th sem\biomedical Image Processing\labs\Biomedical_Image_Processing_Lab\Experiment_04"
python build_report.py
```
