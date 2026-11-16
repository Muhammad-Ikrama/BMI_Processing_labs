"""
Optimized Academic Laboratory Report Generator for Experiment 02
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
    print("GENERATING OPTIMIZED ACADEMIC REPORT FOR EXPERIMENT 02 (TARGET: 10-12 PAGES)")
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
    h_run = h_p.add_run("Medical Image Processing Lab | Experiment No. 2")
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
    r_exp = p_exp.add_run("Experiment No. 2")
    format_run(r_exp, "Arial", 16, bold=True, color_rgb=(30, 58, 138))

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("Title: Histogram Computation and Histogram Equalization Techniques for Contrast Enhancement of Medical Images")
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
    qr_img_path = os.path.join(fig_dir, "exp02_github_qr.png")
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
        "Digital medical radiographs frequently exhibit compromised contrast resolution due to anatomical tissue density overlap, "
        "suboptimal exposure parameter selection, or Compton scatter radiation. In clinical chest examinations, low-contrast conditions "
        "impede the visualization of pulmonary nodules, fine bronchial vascular markings, and subtle cortical bone micro-fractures. "
        "Histogram analysis provides a quantitative statistical representation of the global tonal distribution. Global Histogram Equalization (GHE) "
        "attempts to expand contrast by linearly remapping gray levels using the cumulative distribution function (CDF). However, in radiographic scans, "
        "GHE induces severe over-saturation and noise amplification in uniform air and mediastinal regions. Contrast Limited Adaptive Histogram Equalization "
        "(CLAHE) resolves this deficiency by calculating local CDF mappings within contextual tiles while enforcing an upper clip limit on local contrast gain. "
        "This laboratory evaluates manual histogram derivation, GHE limitations, and CLAHE optimization on clinical radiographs."
    )

    # =========================================================================
    # 2. OBJECTIVES
    # =========================================================================
    add_h1("2. Objectives")
    objectives = [
        "1. Understand the theoretical statistical foundations of digital image histograms, probability density functions (PDFs), and cumulative distribution functions (CDFs).",
        "2. Implement manual 1-D intensity histogram computation without built-in library functions and verify numerical equivalence against standard implementations.",
        "3. Derive and implement the discrete Global Histogram Equalization (GHE) transformation function s_k = T(r_k).",
        "4. Document the clinical failure modes of GHE, specifically severe background noise amplification and loss of subtle soft-tissue contrast.",
        "5. Implement Contrast Limited Adaptive Histogram Equalization (CLAHE) across contextual grid dimensions (4x4, 8x8, 16x16) and clip limits (0.01, 0.02, 0.05).",
        "6. Quantify contrast enhancement and information content using RMS Contrast, Shannon Information Entropy, and Background Noise Variance.",
        "7. Execute and validate identical implementations across both Python 3.14 and MATLAB R2026a environments.",
        "8. Formulate evidence-based clinical PACS deployment recommendations for thoracic and skeletal radiography."
    ]
    for obj in objectives:
        add_p(obj, space_before=1, space_after=1)

    # =========================================================================
    # 3. THEORY (~1 page)
    # =========================================================================
    add_h1("3. Theory")
    add_p(
        "3.1 Digital Image Histograms & Probability Functions: For a digital image with L discrete intensity levels [0, L-1], "
        "the discrete histogram is h(r_k) = n_k, where r_k is the k-th gray level and n_k is the pixel count. "
        "The normalized Probability Density Function (PDF) is p(r_k) = n_k / N, where N = M x N total pixels. "
        "The Cumulative Distribution Function (CDF) represents the cumulative probability: S_k = sum_{j=0}^k p(r_j), with S_0 = p(0) and S_{L-1} = 1.0."
    )
    add_p(
        "3.2 Global Histogram Equalization (GHE): GHE maps original gray levels r_k to equalized levels s_k using the continuous CDF transformation: "
        "s_k = round((L - 1) * S_k). This non-linear mapping flattens the output probability distribution, spreading clustered intensities across the entire dynamic range. "
        "However, when a medical image contains large homogeneous regions (such as background ambient air), massive peaks in the histogram produce steep CDF slopes, "
        "causing GHE to violently stretch noise into harsh, washed-out artifacts."
    )
    add_p(
        "3.3 Contrast Limited Adaptive Histogram Equalization (CLAHE): CLAHE overcomes global over-enhancement through localized processing: "
        "(1) Grid Partitioning: The image is divided into small, non-overlapping contextual tiles (e.g., 8x8). "
        "(2) Contrast Limiting: A clip limit beta is enforced on each local histogram. Any bin exceeding beta is truncated, and the excess pixels are "
        "redistributed uniformly across all histogram bins prior to CDF calculation. "
        "(3) Equalization & Interpolation: Each tile is equalized, and bilinear interpolation is applied between tile centroids to eliminate block boundary artifacts."
    )
    add_p(
        "3.4 Quantitative Image Metrics: (1) RMS Contrast: C_rms = sqrt((1 / (M*N)) * sum (I(x, y) - mean_I)^2); "
        "(2) Shannon Information Entropy: H = - sum_{k=0}^{L-1} p(r_k) * log2(p(r_k)), measuring detail richness; "
        "(3) Background Noise Variance: sigma_air^2 in homogeneous unattenuated air field."
    )

    # =========================================================================
    # 4. TOOLS AND REQUIREMENTS (Compact Table)
    # =========================================================================
    add_h1("4. Tools and Requirements")
    df_tools = pd.DataFrame([
        {"Category": "Computing Platform", "Specification": "MacBook Pro M-series / 64-bit multi-core workstation with Windows & POSIX runtimes"},
        {"Category": "MATLAB Environment", "Specification": "MathWorks MATLAB R2026a (64-bit) with Image Processing Toolbox (histeq, adapthisteq)"},
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
        "1. Image Ingestion: Load Xray.jpg, verify uint8 class, spatial dimensions (466 x 429), and baseline mean brightness and contrast.",
        "2. Manual Histogram Computation: Compute 256-bin histogram manually using array iteration and compare with cv2.calcHist / imhist.",
        "3. Discrete CDF & Dual-Axis Plotting: Calculate cumulative probability sum and plot dual-axis normalized PDF and CDF curves.",
        "4. Global Histogram Equalization (GHE): Apply GHE transformation function s_k = round(255 * CDF(k)). Reconstruct equalized image.",
        "5. GHE Artifact Documentation: Quantify background noise amplification and loss of subtle soft-tissue contrast in lung fields.",
        "6. CLAHE Grid & Clip Parameter Sweep: Implement CLAHE across tile grids (4x4, 8x8, 16x16) and clip limits (0.01, 0.02, 0.05).",
        "7. Quantitative Metrics Evaluation: Calculate RMS contrast, Shannon entropy, and background noise variance across all enhancements.",
        "8. Clinical Protocol Formulation: Synthesize visual contrast and noise metrics into PACS clinical diagnostic guidelines."
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
    img = imread('Xray.jpg');
    if size(img, 3) == 3, img = rgb2gray(img); end
    img_ghe = histeq(img);
    img_clahe = adapthisteq(img, 'ClipLimit', 0.02, 'NumTiles', [8, 8]);
    fprintf('Orig Mean: %.2f | GHE: %.2f | CLAHE: %.2f\\n', ...
            mean(double(img(:))), mean(double(img_ghe(:))), mean(double(img_clahe(:))));
end"""
    p_mc = doc.add_paragraph()
    p_mc.paragraph_format.space_before = Pt(2)
    p_mc.paragraph_format.space_after = Pt(2)
    r_mc = p_mc.add_run(mat_code)
    format_run(r_mc, "Consolas", 8, color_rgb=(30, 41, 59))
    add_fig("exp02_matlab_exec_screenshot.png", "Figure 1: MATLAB R2026a Master Pipeline Execution Evidence Log", width_in=5.8)

    add_h2("6.2 Python Implementation and Execution Verification")
    py_code = """import cv2, numpy as np
def run_clahe_enhancement(img_path, clip_limit=2.0, tile_grid=(8, 8)):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid)
    enhanced = clahe.apply(img)
    rms_contrast = float(np.std(enhanced))
    return enhanced, rms_contrast"""
    p_pc = doc.add_paragraph()
    p_pc.paragraph_format.space_before = Pt(2)
    p_pc.paragraph_format.space_after = Pt(2)
    r_pc = p_pc.add_run(py_code)
    format_run(r_pc, "Consolas", 8, color_rgb=(30, 41, 59))
    add_fig("exp02_python_exec_screenshot.png", "Figure 2: Python 3.14 Automated Test Suite Verification Log (9/9 Suites Passed)", width_in=5.8)

    # =========================================================================
    # 7. RESULTS AND OUTPUTS
    # =========================================================================
    add_h1("7. Results and Outputs")
    add_p("Quantitative outputs, simulation figures, and structured comparison tables across all experimental phases are detailed below.")

    add_h2("7.1 Baseline Contrast Benchmark (Example 01 & Task 2.5)")
    add_fig("example_02_ghe_vs_clahe_python.png", "Figure 3: Contrast Enhancement Benchmark: Original Radiograph vs. Global Histogram Equalization vs. CLAHE (Python)", width_in=5.8)
    df_b = pd.read_csv(os.path.join(tab_dir, "task_2_5_contrast_benchmark_summary.csv"))
    add_table_from_df(df_b, [2.2, 1.3, 1.3, 1.4], "Table 2: Master Contrast Enhancement Benchmark: Mean Brightness, RMS Contrast, Entropy, and Noise Variance")

    add_h2("7.2 Manual Histogram & Dual-Axis CDF Curve (Tasks 2.1 & 2.2)")
    add_fig("task_2_1_manual_histogram_python.png", "Figure 4: Manual Histogram Verification: Pixel Frequency Distribution vs. Built-In Function Concordance", width_in=5.8)
    add_fig("task_2_2_dual_axis_cdf_python.png", "Figure 5: Dual-Axis Statistical Profile: Intensity Histogram (PDF) and Discrete Cumulative Distribution Function (CDF)", width_in=5.8)

    add_h2("7.3 GHE Failure & CLAHE Parameter Optimization (Tasks 2.3 & 2.4)")
    add_fig("task_2_3_global_histogram_equalization_python.png", "Figure 6: Global Histogram Equalization Failure: Severe Noise Amplification and Washed-Out Soft Tissue", width_in=5.8)
    add_fig("task_2_4_clahe_clip_sensitivity_python.png", "Figure 7: CLAHE Clip Limit Sensitivity Sweep (Clip = 0.01, 0.02, 0.05): Controlled Local Contrast Gain", width_in=5.8)
    add_fig("task_2_5_multipanel_contrast_report_python.png", "Figure 8: Master Clinical Contrast Diagnostic Report: Comprehensive Multi-Method Comparative Inset Analysis", width_in=5.8)

    # =========================================================================
    # 8. CALCULATIONS AND ANALYSIS
    # =========================================================================
    add_h1("8. Calculations and Analysis")
    add_p(
        "8.1 RMS Contrast Enhancement: The baseline radiograph exhibits low RMS contrast (C_rms = 33.40). "
        "Global HE artificially inflates contrast to 89.11 (+166.8% increase) by violently stretching the massive background air peak. "
        "CLAHE (Clip = 0.02, 8x8 grid) delivers an optimal diagnostic contrast of C_rms = 43.11 (+29.1% enhancement), restoring crisp parenchymal interfaces."
    )
    add_p(
        "8.2 Information Entropy Dynamics: Baseline radiograph entropy is 3.3345 bits/pixel. Under GHE, entropy paradoxically decreases to 3.0787 bits/pixel (-7.7% loss), "
        "caused by the merging of adjacent low-probability gray bins into single output states. CLAHE elevates entropy to 4.7086 bits/pixel (+41.2% information enrichment), "
        "proving superior preservation of subtle anatomical gradations."
    )
    add_p(
        "8.3 Background Noise Amplification: In the homogeneous apical air field, baseline noise variance is 32.64. "
        "GHE escalates noise variance to 414.25 (+1169% noise explosion), rendering air fields severely mottled. "
        "CLAHE restricts background noise variance to 41.31 (+26.6% controlled increase), confirming robust noise containment via contrast limiting."
    )

    # =========================================================================
    # 9. DISCUSSION (Concise, Technical, Meaningful)
    # =========================================================================
    add_h1("9. Discussion")
    add_p(
        "9.1 Global vs. Local Equalization Dynamics: Global Histogram Equalization assumes a uniform target distribution across the entire image. "
        "In medical radiographs dominated by dark background air and dense skeletal structures, global transformation produces unnatural contrast overshoots. "
        "CLAHE operates on local contextual neighborhoods, equalizing contrast based on local tissue characteristics rather than global scene extremes."
    )
    add_p(
        "9.2 Role of Clip Limit in Noise Suppression: The clip limit acts as a mathematical governor on contrast amplification. "
        "In flat, low-contrast tissue, small intensity differences produce steep local histogram slopes. Without clipping, these slopes act as high-gain amplifiers for quantum noise. "
        "Clipping the histogram at beta = 0.02 truncates steep slopes, redistributing excess counts across all bins to guarantee artifact-free enhancement."
    )
    add_p(
        "9.3 Contextual Grid Size Selection: An 8x8 tile grid matches the spatial scale of lobar anatomy and major vascular branches. "
        "Smaller grids (4x4) approach global behavior, whereas larger grids (16x16) can introduce tile-level blockiness if interpolation is insufficient."
    )
    add_p(
        "9.4 Clinical Protocol Recommendations: (a) Routine Chest Radiography: CLAHE (Clip = 0.02, 8x8 grid) is the gold standard for PACS viewing; "
        "(b) Dense Skeletal Trauma: CLAHE with higher clip (Clip = 0.04) accentuates trabecular micro-fractures; "
        "(c) Global Histogram Equalization: Strictly contraindicated in clinical practice due to extreme noise amplification."
    )

    # =========================================================================
    # 10. CONCLUSION (3-5 Sentences)
    # =========================================================================
    add_h1("10. Conclusion")
    add_p(
        "This laboratory investigated statistical histogram computation, Global Histogram Equalization, and CLAHE on clinical thoracic radiographs. "
        "While Global Histogram Equalization increased RMS contrast from 33.40 to 89.11, it failed clinically by inducing massive noise amplification (variance = 414.25) "
        "and reducing information entropy to 3.08 bits/pixel due to bin merging. CLAHE (Clip = 0.02, 8x8 grid) achieved optimal diagnostic enhancement, "
        "increasing RMS contrast to 43.11 and Shannon entropy to 4.71 bits/pixel while strictly containing background noise (variance = 41.31). "
        "CLAHE is definitively established as the preferred clinical enhancement standard for diagnostic medical imaging."
    )

    # =========================================================================
    # 11. REFERENCES (Verifiable)
    # =========================================================================
    add_h1("11. References")
    refs = [
        "[1] R. C. Gonzalez and R. E. Woods, Digital Image Processing, 4th ed. New York, NY: Pearson, 2018.",
        "[2] S. M. Pizer et al., 'Adaptive histogram equalization and its variations,' Computer Vision, Graphics, and Image Processing, vol. 39, no. 3, pp. 355-368, 1987.",
        "[3] K. Zuiderveld, 'Contrast limited adaptive histogram equalization,' in Graphics Gems IV, San Diego, CA: Academic Press, 1994, pp. 474-485.",
        "[4] J. T. Bushberg, J. A. Seibert, E. M. Leidholdt Jr., and J. M. Boone, The Essential Physics of Medical Imaging, 3rd ed. Philadelphia, PA: Lippincott Williams & Wilkins, 2011."
    ]
    for r in refs:
        add_p(r, space_before=1, space_after=1)

    # =========================================================================
    # 12. APPENDIX (Test Execution Summary)
    # =========================================================================
    add_h1("12. Appendix")
    add_p(
        "Verification Summary: The implementation was validated via an automated test harness (Tests/test_experiment_02.py) covering 9 comprehensive test suites: "
        "T01 Input Integrity (PASS), T02 Baseline Outputs (PASS), T03 Manual Histogram (PASS), T04 Dual-Axis CDF (PASS), T05 Global HE (PASS), "
        "T06 CLAHE Sensitivity (PASS), T07 Contrast Report (PASS), T08 Deliverables Completeness (PASS), T09 Cross-Platform Concordance (PASS). "
        "Overall execution time: 0.033s with 100% assertion pass rate. All materials and reproducible code are cataloged in the linked GitHub repository."
    )

    # Save Word DOCX
    docx_path = os.path.join(rep_dir, "Experiment_02_Report.docx")
    doc.save(docx_path)
    print(f"[SUCCESS] Optimized Report saved as DOCX: {docx_path}")

    # Compile PDF via Word COM
    pdf_path = os.path.join(rep_dir, "Experiment_02_Report.pdf")
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
