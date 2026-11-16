# Experiment 05: Edge Detection in Medical Images Using Sobel, Prewitt, and Canny Operators: Implementation and Comparative Analysis

**Course**: Medical Image Processing (B.Sc. Biomedical Engineering, 6th Semester)  
**Institution**: Faculty of Engineering & Applied Sciences, Department of Biomedical Engineering, Riphah International University, Lahore  
**Course Instructor**: Engr. Rana Talha Khalid, Lab Engineer  
**Targeted CLO**: CLO 1 (Psychomotor - P2) | **Mapped PLO**: PLO 5 (Modern Tool Usage)  

---

## 1. Executive Summary & Clinical Rationale
In clinical diagnostic imaging (CT, MRI, X-ray), an edge represents a localized spatial discontinuity in image brightness that correlates directly with physical anatomical boundaries: the interface between cortical bone and soft tissue, the border of a metastatic tumor, or the ventricular boundaries of the brain. Accurately extracting these boundaries is the indispensable first step for anatomical organ segmentation, volumetric measurement, radiation oncology planning, and computer-aided diagnosis.

### Edge Physics & Differential Calculus
- **1st-Order Spatial Derivative (Gradient Vector)**:
  $$\nabla f = \begin{bmatrix} G_x \\ G_y \end{bmatrix} = \begin{bmatrix} \frac{\partial f}{\partial x} \\ \frac{\partial f}{\partial y} \end{bmatrix}$$
- **Gradient Magnitude**: $|\nabla f| = \sqrt{G_x^2 + G_y^2} \approx |G_x| + |G_y|$
- **Gradient Orientation**: $\theta = \arctan\left(\frac{G_y}{G_x}\right)$ (points in direction of steepest ascent; anatomical edge runs orthogonal to gradient!)

### Zero-Sum Kernel Secret
All edge detection convolution kernels satisfy $\sum w(s, t) = 0.0$.
- In flat, homogeneous tissue (e.g. liver parenchyma or brain white matter), balanced positive and negative weights cancel out exactly: $(-1 \cdot 50) + (0 \cdot 50) + (+1 \cdot 50) = 0$ (pure black).
- At an anatomical attenuation boundary (e.g. soft tissue $20\text{ HU}$ to cortical bone $200\text{ HU}$), the output spikes to $+180$ (brilliant white line).

### Operator Mechanics Comparison
1. **Prewitt Operator**: Unweighted central finite difference with orthogonal moving average $[1, 1, 1]^T$. Highly sensitive to noise; produces wide ramps (3–5 pixels thick).
2. **Sobel Operator**: Discrete binomial filter $[1, 2, 1]^T$ in orthogonal direction. Doubles center tap weight for superior noise suppression; still produces multi-pixel ramps.
3. **Canny Operator**: Multi-stage optimal pipeline (Gaussian pre-smoothing, Sobel gradients, Non-Maximum Suppression (NMS), and Hysteresis Double Thresholding). Quantizes gradient normal vectors into 4 discrete sectors ($0^\circ, 45^\circ, 90^\circ, 135^\circ$) to thin ramps into crisp, continuous 1-pixel-wide skeletons.

---

## 2. Directory Architecture
```
Biomedical_Image_Processing_Lab/
└── Experiment_05/
    ├── Documentation/
    │   ├── README.md
    │   └── requirement_traceability.md
    ├── Figures/ (12 High-Resolution PNG Figures)
    ├── Inputs/
    │   └── images/ (CT.jpg, MRI.jpg, Xray.jpg, sample_brain_ct.dcm)
    ├── MATLAB/ (8 M-Scripts: example_01, tasks 5.1-5.5, experiment_05, run_all)
    ├── Outputs/ (MATLAB/ and Python/ subdirectories)
    ├── Python/ (8 Python scripts + requirements.txt)
    ├── Report/
    │   ├── Experiment_05_Report.docx
    │   └── Experiment_05_Report.pdf
    ├── Tables/
    │   └── task_5_5_edge_benchmark_summary.csv
    ├── Tests/
    │   ├── test_experiment_05.py
    │   └── test_results.txt (9/9 Passed, 100%)
    └── build_report.py
```

---

## 3. Mathematical Formulations & Evaluation Metrics

### 3.1 Pratt's Figure of Merit (FOM)
Measures edge localization accuracy relative to ground truth anatomy:
$$\text{FOM} = \frac{1}{\max(N_I, N_A)} \sum_{i=1}^{N_A} \frac{1}{1 + \alpha d_i^2}$$
where $\alpha = 1/9$, $N_I$ is ideal edge count, $N_A$ is actual edge count, and $d_i$ is distance to nearest true edge. Target: $\text{FOM} \ge 0.75$.

### 3.2 Non-Maximum Suppression (NMS) Quantization
- Sector 0 ($0^\circ$ normal): $[0^\circ, 22.5^\circ) \cup [157.5^\circ, 180^\circ) \implies$ compare left/right neighbors.
- Sector 1 ($45^\circ$ normal): $[22.5^\circ, 67.5^\circ) \implies$ compare top-right / bottom-left.
- Sector 2 ($90^\circ$ normal): $[67.5^\circ, 112.5^\circ) \implies$ compare top/bottom.
- Sector 3 ($135^\circ$ normal): $[112.5^\circ, 157.5^\circ) \implies$ compare top-left / bottom-right.

---

## 4. Execution Commands

### Python Pipeline
```powershell
cd "d:\BME\7th sem\biomedical Image Processing\labs\Biomedical_Image_Processing_Lab\Experiment_05\Python"
python experiment_05.py
```

### MATLAB Pipeline
```powershell
& "C:\Program Files\MATLAB\R2026a\bin\matlab.exe" -batch "run('d:/BME/7th sem/biomedical Image Processing/labs/Biomedical_Image_Processing_Lab/Experiment_05/MATLAB/experiment_05.m');"
```

### Automated Validation Test Suite
```powershell
python -m unittest "Biomedical_Image_Processing_Lab/Experiment_05/Tests/test_experiment_05.py"
```

### University Report Compilation
```powershell
python "Biomedical_Image_Processing_Lab/Experiment_05/build_report.py"
```
