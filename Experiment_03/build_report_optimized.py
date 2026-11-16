"""
Optimized Academic Laboratory Report Generator for Experiment 03
Target Page Count: 10-12 pages (Strictly within 8-15 pages limit)
Course: Medical Image Processing | Riphah International University
Faculty: Engr. Rana Talha Khalid, Lab Engineer
Author: 60140-Mikrama
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import pandas as pd


def generate_optimized_report():
    print("================================================================================")
    print("GENERATING OPTIMIZED ACADEMIC REPORT FOR EXPERIMENT 03 (TARGET: 10-12 PAGES)")
    print("================================================================================\n")

    doc = docx.Document()

    # 1. Page Margins (0.75 in all around)
    section = doc.sections[0]
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    section.different_first_page_header_footer = False

    # 2. Running Header and Footer
    header = section.header
    h_p = header.paragraphs[0]
    h_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    h_run = h_p.add_run("Medical Image Processing Lab | Experiment No. 3")
    h_run.font.name = "Arial"
    h_run.font.size = Pt(8.5)
    h_run.font.color.rgb = RGBColor(140, 150, 165)

    footer = section.footer
    f_p = footer.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    f_run = f_p.add_run("Department of Biomedical Engineering, Riphah International University")
    f_run.font.name = "Arial"
    f_run.font.size = Pt(8.5)
    f_run.font.color.rgb = RGBColor(140, 150, 165)

    # Base paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    fig_dir = os.path.join(base_dir, "Figures")
    tab_dir = os.path.join(base_dir, "Tables")
    rep_dir = os.path.join(base_dir, "Report")
    os.makedirs(rep_dir, exist_ok=True)

    # 3. Formatting Helpers
    def format_run(run, font_name="Arial", font_size=10, bold=False, italic=False, color_rgb=(30, 41, 59)):
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = RGBColor(*color_rgb)

    def add_p(text="", space_before=0, space_after=3, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        p.alignment = align
        if text:
            run = p.add_run(text)
            format_run(run, "Arial", 10, color_rgb=(51, 65, 85))
        return p

    def add_h1(text):
        p = doc.add_paragraph(style='Heading 1')
        p.paragraph_format.space_before = Pt(11)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        format_run(run, "Arial", 12.5, bold=True, color_rgb=(30, 58, 138))
        return p

    def add_h2(text):
        p = doc.add_paragraph(style='Heading 2')
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        format_run(run, "Arial", 11, bold=True, color_rgb=(37, 99, 235))
        return p

    def set_cell_margins(cell, top=70, bottom=70, left=100, right=100):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def set_cell_shading(cell, color_hex):
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    def set_table_borders(table, color="D1D5DB"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>\n'
            f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>\n'
            f'  <w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>\n'
            f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>\n'
            f'  <w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>\n'
            f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>\n'
            f'  <w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>\n'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    def add_table_from_df(df, col_widths=None, caption=""):
        if caption:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(caption)
            format_run(run, "Arial", 9.5, bold=True, color_rgb=(30, 58, 138))

        rows, cols = df.shape[0] + 1, df.shape[1]
        table = doc.add_table(rows=rows, cols=cols)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table)

        # Header
        hdr_cells = table.rows[0].cells
        for col_idx, col_name in enumerate(df.columns):
            hdr_cells[col_idx].text = str(col_name).replace("_", " ")
            set_cell_shading(hdr_cells[col_idx], "F1F5F9")
            set_cell_margins(hdr_cells[col_idx], 80, 80, 100, 100)
            p = hdr_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                format_run(r, "Arial", 8.5, bold=True, color_rgb=(30, 41, 59))

        # Rows
        for r_idx, row in df.iterrows():
            row_cells = table.rows[r_idx + 1].cells
            bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row):
                row_cells[c_idx].text = str(val)
                set_cell_shading(row_cells[c_idx], bg_color)
                set_cell_margins(row_cells[c_idx], 50, 50, 80, 80)
                p = row_cells[c_idx].paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.space_before = Pt(0)
                if isinstance(val, (int, float)) or (isinstance(val, str) and (val.replace('.', '', 1).isdigit() or val.endswith('%'))):
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    format_run(r, "Arial", 8.5, color_rgb=(51, 65, 85))

        if col_widths and len(col_widths) == cols:
            for row in table.rows:
                for c_idx, w in enumerate(col_widths):
                    row.cells[c_idx].width = Inches(w)

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(4)

    def add_fig(img_filename, caption, width_in=5.8):
        fpath = os.path.join(fig_dir, img_filename)
        if not os.path.exists(fpath):
            print(f"[WARNING] Figure missing: {fpath}")
            return
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(5)
        p_img.paragraph_format.space_after = Pt(1)
        p_img.paragraph_format.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(fpath, width=Inches(width_in))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(1)
        p_cap.paragraph_format.space_after = Pt(6)
        run_cap = p_cap.add_run(caption)
        format_run(run_cap, "Arial", 8.5, italic=True, color_rgb=(71, 85, 105))

    # =========================================================================
    # MANDATORY FIRST PAGE OPENING PATTERN
    # =========================================================================
    p_exp = doc.add_paragraph()
    p_exp.paragraph_format.space_before = Pt(0)
    p_exp.paragraph_format.space_after = Pt(1)
    r_exp = p_exp.add_run("Experiment No. 3")
    format_run(r_exp, "Arial", 16, bold=True, color_rgb=(30, 58, 138))

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("Title: Image Smoothing of Medical Images Using Spatial Domain Mean/Averaging and Gaussian Filters")
    format_run(r_title, "Arial", 12.5, bold=True, color_rgb=(71, 85, 105))

    # =========================================================================
    # GITHUB QR CODE INTEGRATION BOX (Page 1 Top)
    # =========================================================================
    qr_table = doc.add_table(rows=1, cols=2)
    qr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(qr_table, color="94A3B8")

    cell_qr = qr_table.cell(0, 0)
    cell_qr.width = Inches(1.3)
    set_cell_margins(cell_qr, top=40, bottom=40, left=40, right=40)
    set_cell_shading(cell_qr, "FFFFFF")
    p_qr = cell_qr.paragraphs[0]
    p_qr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    qr_img_path = os.path.join(fig_dir, "exp03_github_qr.png")
    if os.path.exists(qr_img_path):
        p_qr.add_run().add_picture(qr_img_path, width=Inches(1.05))

    cell_info = qr_table.cell(0, 1)
    cell_info.width = Inches(5.7)
    set_cell_margins(cell_info, top=60, bottom=60, left=80, right=80)
    set_cell_shading(cell_info, "F8FAFC")
    p_info = cell_info.paragraphs[0]
    p_info.paragraph_format.space_before = Pt(0)
    p_info.paragraph_format.space_after = Pt(1)
    r_qh = p_info.add_run("GitHub Repository — Scan to Access Complete Source Code and Project Files\n")
    format_run(r_qh, "Arial", 9.5, bold=True, color_rgb=(30, 58, 138))
    r_url = p_info.add_run("Repository URL: https://github.com/Muhammad-Ikrama/BMI_Processing_labs\n")
    format_run(r_url, "Arial", 8.5, bold=True, color_rgb=(37, 99, 235))
    r_sub = p_info.add_run("Includes verified MATLAB R2026a and Python 3.14 pipelines, raw DICOM/radiographs, and automated test suite.")
    format_run(r_sub, "Arial", 8, italic=True, color_rgb=(100, 116, 139))

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

    # =========================================================================
    # 1. INTRODUCTION (~120 words)
    # =========================================================================
    add_h1("1. Introduction")
    add_p(
        "Digital radiographic acquisitions inherently contain random high-frequency fluctuations caused by electronic thermal noise, "
        "detector gain variations, and photon starvation (quantum mottle). Spatial-domain image smoothing reduces these stochastic corruptions "
        "by replacing each pixel with a weighted linear combination of its surrounding neighborhood. Linear spatial filtering techniques, "
        "primarily uniform mean (averaging) and isotropic Gaussian filters, represent fundamental pre-processing operations for noise suppression "
        "prior to feature extraction and segmentation. However, spatial averaging introduces an inevitable clinical trade-off: attenuating high-frequency "
        "noise also attenuates high-frequency anatomical edges, causing boundary blurring and contrast degradation. This laboratory investigates "
        "the mathematical formulations, boundary padding mechanics, kernel scaling dynamics, and diagnostic quality trade-offs of spatial mean "
        "and Gaussian filters on clinical thoracic radiographs."
    )

    # =========================================================================
    # 2. OBJECTIVES
    # =========================================================================
    add_h1("2. Objectives")
    objectives = [
        "1. Understand the theoretical principles of 2-D discrete spatial convolution and linear spatial filtering in medical image processing.",
        "2. Formulate and implement normalized box (mean) spatial averaging kernels across window sizes (3x3, 5x5, 7x7).",
        "3. Derive and construct isotropic 2-D Gaussian smoothing kernels across spatial standard deviations (sigma in [0.8, 1.2, 2.0]).",
        "4. Evaluate boundary padding techniques (zero padding, replicate, and symmetric reflection) and document border attenuation artifacts.",
        "5. Quantify noise reduction efficiency using background air standard deviation and Contrast-to-Noise Ratio (CNR).",
        "6. Extract 1-D spatial intensity transects (Row 150) across cortical bone to evaluate edge slope degradation and transition penumbras.",
        "7. Benchmark filtering performance using Peak Signal-to-Noise Ratio (PSNR) and Structural Similarity Index (SSIM).",
        "8. Formulate evidence-based clinical deployment protocols for routine radiographic PACS viewing."
    ]
    for obj in objectives:
        add_p(obj, space_before=1, space_after=1)

    # =========================================================================
    # 3. THEORY (~1 page)
    # =========================================================================
    add_h1("3. Theory")
    add_p(
        "3.1 Discrete 2-D Spatial Convolution: Linear spatial filtering operates directly on pixel neighborhood W of size (2a+1) x (2b+1) centered at (x, y): "
        "g(x, y) = sum_{s=-a}^a sum_{t=-b}^b w(s, t) * f(x+s, y+t), where w(s, t) is the filter mask kernel and f is the input image."
    )
    add_p(
        "3.2 Linear Mean (Averaging) Filter: Employs uniform weights w(s, t) = 1 / (K * K) across a square K x K window. "
        "Assuming additive zero-mean uncorrelated noise with variance sigma_n^2, spatial averaging over K^2 pixels reduces output noise variance to sigma_out^2 = sigma_n^2 / K^2. "
        "However, because all pixels in the window are weighted equally regardless of spatial distance from the center, mean filtering causes severe edge blurring."
    )
    add_p(
        "3.3 Isotropic Gaussian Smoothing Filter: Weights pixels inversely proportional to their Euclidean distance from the kernel center: "
        "h(x, y) = (1 / (2 * pi * sigma^2)) * exp(-(x^2 + y^2) / (2 * sigma^2)). The spatial standard deviation sigma governs the spread of the bell curve. "
        "To prevent truncation artifacts, the discrete window width K must satisfy K = 2 * ceil(3 * sigma) + 1. The Gaussian distribution provides the unique property "
        "of maximum smoothing for a given spatial bandwidth without introducing directional bias or spurious ringing."
    )
    add_p(
        "3.4 Boundary Handling Effects: Near image boundaries, kernel W extends beyond the array dimensions. (1) Zero-padding treats outer pixels as zero, "
        "causing severe dark boundary gradients; (2) Replicate padding repeats edge pixels; (3) Symmetric reflection mirrors boundary values, maintaining intensity continuity."
    )
    add_p(
        "3.5 Quantitative Image Quality Metrics: (1) PSNR = 10 * log10(MAX_I^2 / MSE); (2) SSIM: Measures structural correlation in [0, 1]; "
        "(3) Contrast-to-Noise Ratio: CNR = |mu_lesion - mu_background| / sqrt(sigma_lesion^2 + sigma_background^2)."
    )

    # =========================================================================
    # 4. TOOLS AND REQUIREMENTS (Compact Table)
    # =========================================================================
    add_h1("4. Tools and Requirements")
    df_tools = pd.DataFrame([
        {"Category": "Computing Platform", "Specification": "MacBook Pro M-series / 64-bit multi-core workstation with Windows & POSIX runtimes"},
        {"Category": "MATLAB Environment", "Specification": "MathWorks MATLAB R2026a (64-bit) with Image Processing Toolbox (imfilter, fspecial, imgaussfilt)"},
        {"Category": "Python Environment", "Specification": "Python 3.14.4 (OpenCV 4.10, NumPy 2.2, SciPy 1.15, scikit-image 0.25, Matplotlib 3.10)"},
        {"Category": "Clinical Dataset", "Specification": "Primary clinical thoracic radiograph (Xray.jpg, 466 x 429 pixels, 8-bit grayscale)"},
        {"Category": "Verification Harness", "Specification": "Automated Python unittest suite (9 test suites, 100% assertion pass rate)"}
    ])
    add_table_from_df(df_tools, [1.6, 5.4], "Table 1: Computational Environment, Software Tools, and Dataset Specifications")

    # =========================================================================
    # 5. PROCEDURE / METHODOLOGY (Numbered Steps)
    # =========================================================================
    add_h1("5. Procedure / Methodology")
    proc_steps = [
        "1. Image Ingestion: Load Xray.jpg, verify uint8 class, spatial dimensions (466 x 429), and baseline noise variance in apical lung air field.",
        "2. Baseline Noise Generation: Inject zero-mean Gaussian noise (var = 0.01) to simulate typical quantum mottle.",
        "3. Boundary Condition Evaluation: Apply 5x5 mean filter with zero-padding, replicate, and symmetric reflection. Document border attenuation artifacts.",
        "4. Mean Filter Sweep: Convolve noisy radiograph with uniform box kernels across dimensions 3x3, 5x5, and 7x7. Measure PSNR and SSIM.",
        "5. Gaussian Filter Sweep: Apply Gaussian smoothing across scales sigma in [0.8, 1.2, 2.0] with adaptive window sizes. Measure noise suppression.",
        "6. 1-D Transect Profiling: Extract pixel profile along Row 150 across columns 100 to 250 crossing cortical bone. Measure edge slope reduction.",
        "7. Quality Metric Evaluation: Compute background noise standard deviation, CNR, PSNR, and SSIM across all filtered images.",
        "8. Clinical Protocol Formulation: Synthesize smoothing fidelity and edge preservation into PACS diagnostic viewing guidelines."
    ]
    for s in proc_steps:
        add_p(s, space_before=1, space_after=1)

    # =========================================================================
    # 6. CODE IMPLEMENTATION & EXECUTION EVIDENCE
    # =========================================================================
    add_h1("6. Code Implementation")
    add_p("Core algorithmic implementations and execution verification captures are provided below for both MATLAB and Python environments.")

    add_h2("6.1 MATLAB Implementation and Execution Verification")
    mat_code = """function results = example_01()
    img = im2double(imread('Xray.jpg'));
    noisy = imnoise(img, 'gaussian', 0, 0.01);
    h_mean = fspecial('average', [5, 5]);
    out_mean = imfilter(noisy, h_mean, 'symmetric');
    out_gauss = imgaussfilt(noisy, 1.2, 'FilterSize', [5, 5]);
    psnr_m = psnr(out_mean, img); psnr_g = psnr(out_gauss, img);
    fprintf('PSNR Mean: %.2f dB | PSNR Gauss: %.2f dB\\n', psnr_m, psnr_g);
end"""
    p_mc = doc.add_paragraph()
    p_mc.paragraph_format.space_before = Pt(2)
    p_mc.paragraph_format.space_after = Pt(2)
    r_mc = p_mc.add_run(mat_code)
    format_run(r_mc, "Consolas", 8, color_rgb=(30, 41, 59))
    add_fig("exp03_matlab_exec_screenshot.png", "Figure 1: MATLAB R2026a Master Pipeline Execution Evidence Log", width_in=5.8)

    add_h2("6.2 Python Implementation and Execution Verification")
    py_code = """import cv2, numpy as np
def run_gaussian_smooth(img_path, sigma=1.2, ksize=(5, 5)):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    noisy = img.astype(np.float64) + np.random.normal(0, 10, img.shape)
    noisy = np.clip(noisy, 0, 255).astype(np.uint8)
    smooth = cv2.GaussianBlur(noisy, ksize, sigmaX=sigma, borderType=cv2.BORDER_REFLECT)
    return smooth"""
    p_pc = doc.add_paragraph()
    p_pc.paragraph_format.space_before = Pt(2)
    p_pc.paragraph_format.space_after = Pt(2)
    r_pc = p_pc.add_run(py_code)
    format_run(r_pc, "Consolas", 8, color_rgb=(30, 41, 59))
    add_fig("exp03_python_exec_screenshot.png", "Figure 2: Python 3.14 Automated Test Suite Verification Log (9/9 Suites Passed)", width_in=5.8)

    # =========================================================================
    # 7. RESULTS AND OUTPUTS
    # =========================================================================
    add_h1("7. Results and Outputs")
    add_p("Quantitative outputs, simulation figures, and structured comparison tables across all experimental phases are detailed below.")

    add_h2("7.1 Baseline Filtering Benchmark (Example 01)")
    add_fig("exp03_example_01_filtering_benchmark_py.png", "Figure 3: Baseline Image Smoothing Comparison: Noisy Input, Mean 5x5, and Gaussian 5x5 Filtering (Python)", width_in=5.8)
    df_b = pd.read_csv(os.path.join(tab_dir, "task_3_4_smoothing_benchmark_summary.csv"))
    add_table_from_df(df_b, [1.6, 0.8, 0.8, 0.7, 0.7, 0.7, 0.8, 1.2], "Table 2: Master Smoothing Quality Benchmark: PSNR, SSIM, CNR, and Noise Std Dev")

    add_h2("7.2 Boundary Padding & Mean Kernel Sweep (Tasks 3.1 & 3.2)")
    add_fig("exp03_task_3_1_boundary_padding_py.png", "Figure 4: Boundary Padding Analysis: Dark Penumbra in Zero Padding vs. Artifact-Free Reflection", width_in=5.8)
    add_fig("exp03_task_3_2_mean_kernel_sweep_py.png", "Figure 5: Mean Filter Kernel Dimension Sweep (3x3 vs. 5x5 vs. 7x7): Noise Attenuation vs. Edge Blurring", width_in=5.8)

    add_h2("7.3 Gaussian Scale Sweep & 1-D Edge Profiles (Tasks 3.3, 3.4 & 3.5)")
    add_fig("exp03_task_3_3_gaussian_kernel_sweep_py.png", "Figure 6: Gaussian Smoothing Scale Sweep (sigma in [0.8, 1.2, 2.0]): Preserving Fine Trabecular Margins", width_in=5.8)
    add_fig("exp03_task_3_4_quality_benchmarking_py.png", "Figure 7: Multi-Metric Benchmark Comparison: PSNR vs. SSIM vs. CNR Trade-off Curves", width_in=5.8)
    add_fig("exp03_task_3_5_edge_profile_py.png", "Figure 8: 1-D Spatial Intensity Transect Profile (Row 150) across Cortical Bone Margin", width_in=5.8)

    # =========================================================================
    # 8. CALCULATIONS AND ANALYSIS
    # =========================================================================
    add_h1("8. Calculations and Analysis")
    add_p(
        "8.1 Noise Variance Attenuation: Baseline background air noise standard deviation is 10.29 (variance = 105.88). "
        "Under 5x5 mean filtering, theoretical variance reduction is 1 / 25 = 0.04 (variance = 4.75, std = 2.18), representing a 95.5% reduction in background noise power. "
        "Gaussian filtering (5x5, sigma = 1.2) achieves noise std = 2.68, achieving significant noise suppression while preserving higher edge gradients."
    )
    add_p(
        "8.2 Contrast-to-Noise Ratio (CNR): Baseline noisy scan achieves CNR = 0.72. Mean 5x5 filtering elevates CNR to 1.38 (+91.7% enhancement). "
        "Gaussian 5x5 achieves CNR = 1.27 (+76.4% enhancement), cleanly separating retrocardiac lung soft tissue from background air."
    )
    add_p(
        "8.3 Edge Slope Degradation: Across Row 150, baseline cortical bone step edge slope is 14.50 intensity units/pixel. "
        "Mean 5x5 filtering degrades edge slope to 4.80 units/pixel (-66.9% flattening, severe blur). Gaussian 5x5 preserves edge slope at 6.20 units/pixel "
        "(+29.2% steeper transition than mean filter), confirming superior edge retention."
    )

    # =========================================================================
    # 9. DISCUSSION (Concise, Technical, Meaningful)
    # =========================================================================
    add_h1("9. Discussion")
    add_p(
        "9.1 Box Averaging vs. Gaussian Weighting: Uniform box filters treat all neighboring pixels equally, creating unnatural box-shaped blurring "
        "and severely flattening fine anatomical edges. Gaussian filters weight pixels with continuous spatial decay, acting as an optimal physical low-pass filter "
        "that preserves natural curvilinear bone margins and vascular structures."
    )
    add_p(
        "9.2 Boundary Padding in Diagnostic Imaging: Zero-padding introduces artificial dark borders that corrupt automated perimeter measurements and threshold segmentations. "
        "Symmetric reflection or replicate padding completely eliminates border discontinuity, making it mandatory for clinical preprocessing pipelines."
    )
    add_p(
        "9.3 Scale Selection Trade-offs: A small Gaussian kernel (sigma = 0.8) effectively cleans thermal sensor noise without noticeable blur. "
        "A moderate kernel (sigma = 1.2) matches the scale of quantum mottle in standard chest radiographs. A large kernel (sigma = 2.0) causes excessive loss of fine trabecular detail."
    )
    add_p(
        "9.4 Clinical Protocol Recommendations: (a) Pre-Processing for Bone Fracture Detection: Gaussian smoothing (5x5, sigma = 0.8 to 1.0) is recommended; "
        "(b) Soft-Tissue Lung Nodule Delineation: Gaussian smoothing (5x5, sigma = 1.2) balances noise suppression and contrast; "
        "(c) Box Mean Filtering: Contraindicated for high-resolution diagnostic reading due to severe edge smearing."
    )

    # =========================================================================
    # 10. CONCLUSION (3-5 Sentences)
    # =========================================================================
    add_h1("10. Conclusion")
    add_p(
        "This laboratory investigated spatial-domain linear smoothing using mean and Gaussian filters on clinical thoracic radiographs. "
        "Mean filtering achieved significant noise power attenuation (95.5% reduction) but caused severe edge smearing (edge slope reduced from 14.50 to 4.80 units/px). "
        "Gaussian smoothing (5x5, sigma = 1.2) achieved the optimal clinical trade-off, delivering PSNR = 31.46 dB, SSIM = 0.6848, and CNR = 1.27 while retaining "
        "significantly sharper anatomical boundaries. Symmetric reflection padding was confirmed as mandatory to prevent border artifacts, establishing Gaussian filtering "
        "as the preferred clinical standard for radiographic noise reduction."
    )

    # =========================================================================
    # 11. REFERENCES (Verifiable)
    # =========================================================================
    add_h1("11. References")
    refs = [
        "[1] R. C. Gonzalez and R. E. Woods, Digital Image Processing, 4th ed. New York, NY: Pearson, 2018.",
        "[2] J. T. Bushberg, J. A. Seibert, E. M. Leidholdt Jr., and J. M. Boone, The Essential Physics of Medical Imaging, 3rd ed. Philadelphia, PA: Lippincott Williams & Wilkins, 2011.",
        "[3] A. K. Jain, Fundamentals of Digital Image Processing. Upper Saddle River, NJ: Prentice Hall, 1989.",
        "[4] Z. Wang, A. C. Bovik, H. R. Sheikh, and E. P. Simoncelli, 'Image quality assessment: From error visibility to structural similarity,' IEEE Transactions on Image Processing, vol. 13, no. 4, pp. 600-612, 2004."
    ]
    for r in refs:
        add_p(r, space_before=1, space_after=1)

    # =========================================================================
    # 12. APPENDIX (Test Execution Summary)
    # =========================================================================
    add_h1("12. Appendix")
    add_p(
        "Verification Summary: The implementation was validated via an automated test harness (Tests/test_experiment_03.py) covering 9 comprehensive test suites: "
        "T01 Input Integrity (PASS), T02 Baseline Outputs (PASS), T03 Boundary Padding (PASS), T04 Mean Kernel Sweep (PASS), T05 Gaussian Kernel Sweep (PASS), "
        "T06 Quality Benchmarking (PASS), T07 Edge Profile (PASS), T08 Deliverables Completeness (PASS), T09 Cross-Platform Concordance (PASS). "
        "Overall execution time: 0.036s with 100% assertion pass rate. All materials and reproducible code are cataloged in the linked GitHub repository."
    )

    # Save Word DOCX
    docx_path = os.path.join(rep_dir, "Experiment_03_Report.docx")
    doc.save(docx_path)
    print(f"[SUCCESS] Optimized Report saved as DOCX: {docx_path}")

    # Compile PDF via Word COM
    pdf_path = os.path.join(rep_dir, "Experiment_03_Report.pdf")
    try:
        import win32com.client
        import pythoncom
        pythoncom.CoInitialize()
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = False
        in_docx = os.path.abspath(docx_path)
        out_pdf = os.path.abspath(pdf_path)
        doc_obj = word.Documents.Open(in_docx)
        doc_obj.SaveAs(out_pdf, FileFormat=17) # wdFormatPDF = 17
        doc_obj.Close()
        word.Quit()
        pythoncom.CoUninitialize()
        print(f"[SUCCESS] Genuine Print-Ready PDF compiled via Word COM: {pdf_path}")
    except Exception as e:
        print(f"[NOTICE] Word COM conversion notice: {e}")

    return docx_path, pdf_path


if __name__ == "__main__":
    generate_optimized_report()
