# Experiment No. 7: Image Sharpening of Medical Images Using High-Boost Filtering and Unsharp Masking: Implementation and Diagnostic Analysis

**Course:** Medical Image Processing (BME 7th Semester)  
**Institution:** Department of Biomedical Engineering, Riphah International University, Lahore Campus  
**Faculty / Lab Engineer:** Engr. Rana Talha Khalid  

---

## 1. Executive Summary & Lab Objectives

This laboratory investigates the spatial-domain sharpening of clinical radiographs using **Gaussian Unsharp Masking** and **High-Boost Filtering**. Using actual thoracic radiograph inputs (`Xray.jpg`, $466 \times 429$ pixels, uint8), the experiment models high-frequency boundary injection, analyzes mathematical edge physics (mean gradient magnitude, 1-D profile transects, Mach band halos), measures dynamic range clipping (underflow at 0, saturation at 255), evaluates quantum mottle amplification in low-dose imaging, and formulates modality-specific clinical decision rules.

---

## 2. Directory Architecture

```plaintext
Biomedical_Image_Processing_Lab/Experiment_07/
├── Documentation/
│   ├── README.md                          # Comprehensive user & developer manual
│   └── requirement_traceability.md        # Complete 20-point requirement traceability matrix
├── Figures/                               # High-resolution (300 DPI) publication figures
│   ├── exp07_example_01_benchmark_py.png  # Python: Baseline sharpening parameter sweep
│   ├── exp07_example_01_benchmark_m.png   # MATLAB: Baseline sharpening parameter sweep
│   ├── exp07_task_7_1_clipping_sweep_py.png # Python: Dynamic range clipping vs boost k
│   ├── exp07_task_7_1_clipping_sweep_m.png  # MATLAB: Dynamic range clipping vs boost k
│   ├── exp07_task_7_2_mask_bandwidth_py.png # Python: Blur kernel sigma sweep & mask bandwidth
│   ├── exp07_task_7_2_mask_bandwidth_m.png  # MATLAB: Blur kernel sigma sweep & mask bandwidth
│   ├── exp07_task_7_3_mach_band_profiles_py.png # Python: 1D transect & Mach band halos
│   ├── exp07_task_7_3_mach_band_profiles_m.png  # MATLAB: 1D transect & Mach band halos
│   ├── exp07_task_7_4_noise_tradeoff_py.png # Python: Quantum mottle noise amplification
│   ├── exp07_task_7_4_noise_tradeoff_m.png  # MATLAB: Quantum mottle noise amplification
│   ├── exp07_task_7_5_clinical_rois_py.png  # Python: Bone vs Lung ROI magnification
│   ├── exp07_task_7_5_clinical_rois_m.png   # MATLAB: Bone vs Lung ROI magnification
│   ├── exp07_task_7_5_diagnostic_report_py.png # Python: Master 2x3 clinical diagnostic report
│   └── exp07_task_7_5_diagnostic_report_m.png  # MATLAB: Master 2x3 clinical diagnostic report
├── Inputs/
│   └── images/
│       ├── Xray.jpg                       # Primary clinical radiograph (466x429)
│       ├── CT.jpg, MRI.jpg, PET.jpg       # Supporting modality references
├── MATLAB/
│   ├── example_01.m                       # Example 01: Baseline sharpening sweep
│   ├── task_7_1.m                         # Task 7.1: High-boost sweep & clipping
│   ├── task_7_2.m                         # Task 7.2: Kernel blur & mask bandwidth
│   ├── task_7_3.m                         # Task 7.3: 1D transect & Mach band quantification
│   ├── task_7_4.m                         # Task 7.4: Quantum mottle noise trade-off
│   ├── task_7_5.m                         # Task 7.5: Clinical ROIs & diagnostic report
│   ├── experiment_07.m                    # Master pipeline runner
│   └── run_all.m                          # Top-level script runner
├── Outputs/
│   ├── Python/                            # Processed output images & overlays
│   └── MATLAB/                            # Processed output images & overlays
├── Python/
│   ├── requirements.txt                   # Pip dependency declarations
│   ├── example_01.py                      # Example 01 implementation
│   ├── task_7_1.py                        # Task 7.1 implementation
│   ├── task_7_2.py                        # Task 7.2 implementation
│   ├── task_7_3.py                        # Task 7.3 implementation
│   ├── task_7_4.py                        # Task 7.4 implementation
│   ├── task_7_5.py                        # Task 7.5 implementation
│   ├── experiment_07.py                   # Master pipeline runner
│   └── run_all.py                         # Top-level runner
├── Report/
│   ├── Experiment_07_Report.docx          # Academic laboratory report (DOCX)
│   └── Experiment_07_Report.pdf           # Publication PDF report (compiled via Word COM)
├── Tables/
│   ├── exp07_benchmark_summary_py.csv     # Master benchmark metrics (Python)
│   ├── exp07_benchmark_summary_matlab.csv # Master benchmark metrics (MATLAB)
│   ├── exp07_task_7_1_clipping_metrics.csv
│   ├── exp07_task_7_1_clipping_metrics_matlab.csv
│   ├── exp07_task_7_2_bandwidth_metrics.csv
│   ├── exp07_task_7_2_bandwidth_metrics_matlab.csv
│   ├── exp07_task_7_3_mach_band_metrics.csv
│   ├── exp07_task_7_3_mach_band_metrics_matlab.csv
│   ├── exp07_task_7_4_noise_amplification_metrics.csv
│   ├── exp07_task_7_4_noise_amplification_metrics_matlab.csv
│   ├── exp07_task_7_5_clinical_roi_metrics.csv
│   └── exp07_task_7_5_clinical_roi_metrics_matlab.csv
└── Tests/
    ├── test_experiment_07.py              # Automated 9-suite verification framework
    └── test_results.txt                   # Automated test execution log (100% PASS)
```

---

## 3. Mathematical Foundations

### 3.1 Unsharp Masking and High-Boost Filtering
Unsharp masking derives a high-frequency spatial mask $g_{\text{mask}}(x, y)$ by subtracting a smoothed version $f_{\text{LP}}(x, y)$ from original image $f(x, y)$:
$$g_{\text{mask}}(x, y) = f(x, y) - f_{\text{LP}}(x, y)$$

In high-boost filtering, the original image is multiplied by an amplification factor $A \ge 1$:
$$f_{\text{hb}}(x, y) = A \cdot f(x, y) - f_{\text{LP}}(x, y) = (A - 1) \cdot f(x, y) + [f(x, y) - f_{\text{LP}}(x, y)] = (A - 1) \cdot f(x, y) + g_{\text{mask}}(x, y)$$

Normalizing by $A$:
$$f_{\text{sharp}}(x, y) = f(x, y) + k \cdot g_{\text{mask}}(x, y), \quad \text{where } k = \frac{1}{A - 1}$$

- $k < 1.0$ ($A > 2.0$): De-emphasis / subtle sharpening
- $k = 1.0$ ($A = 2.0$): Standard unsharp masking
- $k > 1.0$ ($1.0 < A < 2.0$): High-boost filtering

### 3.2 Mean Gradient Magnitude
The local edge steepness is computed via 2D spatial gradients:
$$|\nabla f(x, y)| = \sqrt{\left(\frac{\partial f}{\partial x}\right)^2 + \left(\frac{\partial f}{\partial y}\right)^2}$$
$$\overline{|\nabla f|} = \frac{1}{M \cdot N} \sum_{x=1}^M \sum_{y=1}^N |\nabla f(x, y)|$$

### 3.3 Dynamic Range Clamping
Because $f_{\text{sharp}}$ can produce negative numbers or values exceeding 255:
$$f_{\text{display}}(x, y) = \min(\max(f_{\text{sharp}}(x, y), 0), 255)$$
When $k \ge 2.5$, severe overflow and underflow cause loss of subtle parenchymal textures.

---

## 4. Cross-Platform Execution Instructions

### macOS / Linux
```bash
# 1. Activate Python virtual environment & install requirements
python3 -m venv venv
source venv/bin/activate
pip install -r Biomedical_Image_Processing_Lab/Experiment_07/Python/requirements.txt

# 2. Run Python Master Pipeline
cd Biomedical_Image_Processing_Lab/Experiment_07/Python
python3 run_all.py

# 3. Run Automated Tests
cd ../Tests
python3 -m unittest -v test_experiment_07.py

# 4. Run MATLAB Pipeline (if MATLAB is installed)
cd ../MATLAB
matlab -nodisplay -nosplash -r "experiment_07; exit"
```

### Windows (PowerShell)
```powershell
# 1. Run Python Master Pipeline
Set-Location "Biomedical_Image_Processing_Lab\Experiment_07\Python"
python run_all.py

# 2. Run MATLAB Master Pipeline
$env:MATLAB_PREFDIR = "D:\BME\7th sem\biomedical Image Processing\labs\matlab_prefs"
Set-Location "..\MATLAB"
& "C:\Program Files\MATLAB\R2026a\bin\matlab.exe" -batch "experiment_07"

# 3. Run Automated Quality Tests
Set-Location "..\Tests"
python -m unittest -v test_experiment_07.py
```

---

## 5. Clinical Safety & Modality Guidelines

| Modality / Target Anatomy | Recommended $k$ | Optimal $\sigma$ | Clinical Justification & Safety Constraint |
| :--- | :--- | :--- | :--- |
| **Chest Radiography (Parenchyma)** | $k = 0.5 - 0.8$ | $\sigma = 1.0 - 1.5$ | Soft tissue is highly sensitive to noise amplification. Gentle boost prevents nodular pseudolesions. |
| **Chest Radiography (Skeletal / Ribs)** | $k = 1.0 - 1.2$ | $\sigma = 1.5$ | High bone mineral radiopacity provides sufficient contrast; sharpens cortical margins and trabeculae. |
| **Bariatric Pelvis / Spine X-Ray** | $k = 1.5 - 1.8$ | $\sigma = 1.5 - 2.0$ | Overcomes scatter radiation and photon starvation in thick tissue; restores trabecular sharpness. |
| **Low-Dose CT / Pediatric X-Ray** | **$k \le 0.5$** | $\sigma = 0.8$ | High quantum mottle. Boosting $k > 1.0$ causes $>25\%$ noise amplification, mimicking pathology. |
| **Extreme High-Boost ($k \ge 2.5$)** | **STRICTLY CONTRAINDICATED** | Any | Causes severe Mach band halos ($>2.0$ px) mimicking pneumothorax lines or pseudofractures, plus $>10\%$ pixel clipping. |
