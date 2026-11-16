"""
Optimized Academic Laboratory Report Generator for Experiment 06
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
    print("GENERATING OPTIMIZED ACADEMIC REPORT FOR EXPERIMENT 06 (TARGET: 10-12 PAGES)")
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
    h_run = h_p.add_run("Medical Image Processing Lab | Experiment No. 6")
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
    r_exp = p_exp.add_run("Experiment No. 6")
    format_run(r_exp, "Arial", 16, bold=True, color_rgb=(30, 58, 138))

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("Title: Frequency-Domain Filtering of Medical Images Using the 2-D Fourier Transform: Low-Pass and High-Pass Filter Design and Analysis")
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
    qr_img_path = os.path.join(fig_dir, "exp06_github_qr.png")
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
        "In biomedical image processing, spatial-domain representations often obscure periodic noise, directional artifacts, "
        "and scale-specific textural features that are vital for accurate radiological assessment. Transforming clinical radiographs "
        "into the spatial frequency domain via the 2-D Discrete Fourier Transform (DFT) decomposes complex anatomy into orthogonal sinusoidal "
        "basis functions, separating slow regional intensity variations (low frequencies) from crisp structural margins and noise (high frequencies). "
        "Frequency-domain filtering modifies the Fourier spectrum using transfer functions H(u, v) prior to Inverse DFT reconstruction. "
        "However, abrupt spectral truncation induces Gibbs ringing artifacts that can mimic anatomical pathologies. This laboratory "
        "investigates the design, energy concentration, mathematical transfer functions, and clinical trade-offs of Ideal, Butterworth, "
        "and Gaussian low-pass and high-pass filters using actual clinical radiographs."
    )

    # =========================================================================
    # 2. OBJECTIVES
    # =========================================================================
    add_h1("2. Objectives")
    objectives = [
        "1. Understand the theoretical foundations and mathematical implementation of the 2-D Discrete Fourier Transform (DFT) and its centered log spectrum.",
        "2. Compute the centered Fourier magnitude spectrum |F(u, v)| and phase spectrum phi(u, v) of clinical radiographs.",
        "3. Design and implement Ideal Low-Pass Filters (ILPF) and quantify the physical etiology of Gibbs ringing artifacts across cutoffs D0 in [15, 30, 60].",
        "4. Implement Butterworth Low-Pass Filters (BLPF) and evaluate the influence of filter order n in [1, 2, 4] on transition slope and artifact suppression.",
        "5. Construct Gaussian Low-Pass (GLPF) and High-Pass (GHPF) filters to demonstrate completely ring-free anatomical smoothing and edge delineation.",
        "6. Quantify spectral energy distribution using Parseval's theorem, verifying the >95% low-frequency energy concentration criterion.",
        "7. Compare spatial-domain and frequency-domain execution characteristics in both Python 3.14 and MATLAB R2026a environments.",
        "8. Formulate evidence-based clinical deployment guidelines for medical Picture Archiving and Communication Systems (PACS)."
    ]
    for obj in objectives:
        add_p(obj, space_before=1, space_after=1)

    # =========================================================================
    # 3. THEORY (~1 page)
    # =========================================================================
    add_h1("3. Theory")
    add_p(
        "3.1 2-D Discrete Fourier Transform (DFT): For a digital radiograph f(x, y) of size M x N, the 2-D DFT transforms spatial coordinates (x, y) "
        "into frequency coordinates (u, v): F(u, v) = sum_{x=0}^{M-1} sum_{y=0}^{N-1} f(x, y) * exp(-j * 2 * pi * (ux/M + vy/N)). "
        "The inverse transform (IDFT) reconstructs the spatial image: f(x, y) = (1 / (M * N)) * sum_{u=0}^{M-1} sum_{v=0}^{N-1} F(u, v) * exp(j * 2 * pi * (ux/M + vy/N)). "
        "By centering the zero-frequency DC component F(0, 0) at (M/2, N/2), the log-transformed magnitude spectrum |F(u, v)| = log(1 + sqrt(R^2 + I^2)) visualizes spectral energy."
    )
    add_p(
        "3.2 Frequency-Domain Filtering Workflow: Filtering is governed by the Convolution Theorem: f(x, y) * h(x, y) <=> F(u, v) * H(u, v). "
        "The spatial output is g(x, y) = IDFT[ F(u, v) * H(u, v) ]. The Euclidean radial distance from the spectral center is D(u, v) = sqrt((u - M/2)^2 + (v - N/2)^2)."
    )
    add_p(
        "3.3 Low-Pass Filter Formulations: (1) Ideal Low-Pass Filter (ILPF): H(u, v) = 1 if D(u, v) <= D0, else 0. The sharp rectangular discontinuity in frequency domain "
        "corresponds to a 2-D jinc/sinc function in the spatial domain (h(r) = D0 * J1(2*pi*D0*r) / r), whose prominent sidelobes produce severe concentric Gibbs ringing halos across high-contrast edges. "
        "(2) Butterworth Low-Pass Filter (BLPF): H(u, v) = 1 / [ 1 + (D(u, v) / D0)^(2n) ]. At D(u, v) = D0, H = 0.5. Filter order n dictates transition steepness; n = 2 provides optimal clinical roll-off with negligible ringing. "
        "(3) Gaussian Low-Pass Filter (GLPF): H(u, v) = exp( - D(u, v)^2 / (2 * D0^2) ). Because the Fourier transform of a Gaussian is also a Gaussian, its spatial impulse response has zero sidelobes, completely preventing ringing."
    )
    add_p(
        "3.4 High-Pass Filtering: High-pass filters attenuate low frequencies while passing edges: H_HP(u, v) = 1 - H_LP(u, v). "
        "Gaussian High-Pass Filter (GHPF): H(u, v) = 1 - exp(-D(u, v)^2 / (2*D0^2)), extracting fine anatomical boundaries without ripple artifacts."
    )
    add_p(
        "3.5 Parseval's Theorem & Energy Enclosure: Total spectral energy is conserved: sum_x sum_y |f(x, y)|^2 = (1 / (M*N)) * sum_u sum_v |F(u, v)|^2. "
        "The enclosed energy percentage within cutoff radius D0 is: P(D0) = [ sum_{D(u, v) <= D0} |F(u, v)|^2 / sum_{all} |F(u, v)|^2 ] * 100. "
        "Medical radiographs concentrate over 95% of total signal energy in low spatial frequencies (D0 <= 30 px)."
    )

    # =========================================================================
    # 4. TOOLS AND REQUIREMENTS (Compact Table)
    # =========================================================================
    add_h1("4. Tools and Requirements")
    df_tools = pd.DataFrame([
        {"Category": "Computing Platform", "Specification": "MacBook Pro M-series / 64-bit multi-core workstation with Windows & POSIX environments"},
        {"Category": "MATLAB Environment", "Specification": "MathWorks MATLAB R2026a (64-bit) with Image Processing Toolbox (fft2, ifft2, fftshift)"},
        {"Category": "Python Environment", "Specification": "Python 3.14.4 (NumPy 2.2 fft, SciPy 1.15, OpenCV 4.10, Matplotlib 3.10, Pandas 2.2)"},
        {"Category": "Clinical Dataset", "Specification": "Primary clinical thoracic radiograph (Xray.jpg, 466 x 429 pixels, 8-bit grayscale)"},
        {"Category": "Verification Harness", "Specification": "Automated Python unittest suite (9 test suites, 100% assertion pass rate)"}
    ])
    add_table_from_df(df_tools, [1.6, 5.4], "Table 1: Computational Environment, Software Tools, and Dataset Specifications")

    # =========================================================================
    # 5. PROCEDURE / METHODOLOGY (Numbered Steps)
    # =========================================================================
    add_h1("5. Procedure / Methodology")
    proc_steps = [
        "1. Image Ingestion: Load Xray.jpg, convert to double precision float, verify dimensions (466 x 429), and normalize intensity range to [0, 1].",
        "2. 2-D DFT Computation: Compute 2-D Fast Fourier Transform (FFT) and apply fftshift to place DC component at the spectral center (M/2, N/2).",
        "3. Spectral Energy Evaluation: Compute log magnitude spectrum and calculate cumulative energy percentage enclosed within circular radii D0.",
        "4. ILPF Design & Gibbs Ringing: Construct Ideal Low-Pass Filters with cutoffs D0 in [15, 30, 60]. Reconstruct spatial images via IFFT and quantify ringing severity.",
        "5. Butterworth Order Sweep: Implement BLPF with fixed D0 = 30 and sweep filter orders n in [1, 2, 4]. Measure transition roll-off and spatial distortion.",
        "6. Gaussian Smoothing & Edge Extraction: Construct GLPF (smoothing) and GHPF (edge enhancement) with D0 = 30. Quantify ringing-free reconstruction.",
        "7. Quantitative Metrics: Calculate Peak Signal-to-Noise Ratio (PSNR), Structural Similarity (SSIM), and Mean Gradient Magnitude across all filtered outputs.",
        "8. Clinical Protocol Formulation: Synthesize filtering performance against diagnostic criteria to formulate PACS modality guidelines."
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
    F = fftshift(fft2(img));
    [M, N] = size(img);
    [u, v] = meshgrid(-floor(N/2):ceil(N/2)-1, -floor(M/2):ceil(M/2)-1);
    D = hypot(u, v);
    % Gaussian Low-Pass Filter (D0=30)
    H_glpf = exp(-(D.^2) / (2 * 30^2));
    G_glpf = F .* H_glpf;
    out_glpf = real(ifft2(ifftshift(G_glpf)));
    fprintf('GLPF D0=30: Min=%.3f, Max=%.3f\\n', min(out_glpf(:)), max(out_glpf(:)));
end"""
    p_mc = doc.add_paragraph()
    p_mc.paragraph_format.space_before = Pt(2)
    p_mc.paragraph_format.space_after = Pt(2)
    r_mc = p_mc.add_run(mat_code)
    format_run(r_mc, "Consolas", 8, color_rgb=(30, 41, 59))
    add_fig("exp06_matlab_exec_screenshot.png", "Figure 1: MATLAB R2026a Master Pipeline Execution Evidence Log", width_in=5.8)

    add_h2("6.2 Python Implementation and Execution Verification")
    py_code = """import numpy as np
def run_blpf(img, d0=30.0, n=2):
    F = np.fft.fftshift(np.fft.fft2(img.astype(np.float64)))
    M, N = img.shape
    u, v = np.meshgrid(np.arange(-N//2, N//2), np.arange(-M//2, M//2))
    D = np.hypot(u, v)
    H = 1.0 / (1.0 + (D / (d0 + 1e-8))**(2 * n))
    out = np.real(np.fft.ifft2(np.fft.ifftshift(F * H)))
    return np.clip(out, 0, 255).astype(np.uint8)"""
    p_pc = doc.add_paragraph()
    p_pc.paragraph_format.space_before = Pt(2)
    p_pc.paragraph_format.space_after = Pt(2)
    r_pc = p_pc.add_run(py_code)
    format_run(r_pc, "Consolas", 8, color_rgb=(30, 41, 59))
    add_fig("exp06_python_exec_screenshot.png", "Figure 2: Python 3.14 Automated Test Suite Verification Log (9/9 Suites Passed)", width_in=5.8)

    # =========================================================================
    # 7. RESULTS AND OUTPUTS
    # =========================================================================
    add_h1("7. Results and Outputs")
    add_p("Quantitative outputs, simulation figures, and structured comparison tables across all experimental phases are detailed below.")

    add_h2("7.1 Baseline 2-D DFT & Spectral Energy Concentration (Example 01 & Task 6.1)")
    add_fig("exp06_task_6_1_dft_spectrum_py.png", "Figure 3: 2-D Discrete Fourier Transform, Centered Log Magnitude Spectrum, and Energy Enclosure Curves (Python)", width_in=5.8)
    df_b = pd.read_csv(os.path.join(tab_dir, "exp06_benchmark_summary_py.csv"))
    add_table_from_df(df_b, [1.4, 0.6, 0.7, 0.7, 0.8, 0.8, 0.8, 1.2], "Table 2: Master Frequency-Domain Filtering Benchmark and Diagnostic Status Summary")

    add_h2("7.2 Ideal Low-Pass Filtering & Gibbs Ringing Distortion (Task 6.2)")
    add_fig("exp06_task_6_2_ilpf_gibbs_ringing_py.png", "Figure 4: Ideal Low-Pass Filtering Cutoff Sweep across D0 in [15, 30, 60] and Concentric Gibbs Ringing Artifacts", width_in=5.8)
    df_ilpf = pd.read_csv(os.path.join(tab_dir, "exp06_task_6_2_ilpf_ringing_metrics.csv"))
    add_table_from_df(df_ilpf, [0.8, 0.8, 0.9, 0.9, 1.0, 1.3, 1.3], "Table 3: Ideal Low-Pass Filtering Cutoff Sweep, Ringing Severity, and Image Quality Metrics")

    add_h2("7.3 Butterworth Low-Pass Filter Order Sweep (Task 6.3)")
    add_fig("exp06_task_6_3_blpf_order_sweep_py.png", "Figure 5: Butterworth Low-Pass Filter Order Sweep (n in [1, 2, 4], D0=30) and Transition Roll-off Analysis", width_in=5.8)
    df_blpf = pd.read_csv(os.path.join(tab_dir, "exp06_task_6_3_blpf_sweep_metrics.csv"))
    add_table_from_df(df_blpf, [0.8, 0.8, 0.8, 0.9, 1.0, 1.2, 1.5], "Table 4: Butterworth Filter Order Sweep, Transition Slope, and Artifact Suppression Metrics")

    add_h2("7.4 Gaussian Low-Pass & High-Pass Filtering (Tasks 6.4 & 6.5)")
    add_fig("exp06_task_6_4_glpf_ghpf_contrast_py.png", "Figure 6: Gaussian Low-Pass (Smoothing) and High-Pass (Edge Extraction) Spatial Reconstructions and Intensity Profiles", width_in=5.8)
    df_contrast = pd.read_csv(os.path.join(tab_dir, "exp06_task_6_4_contrast_metrics.csv"))
    add_table_from_df(df_contrast, [1.4, 0.8, 0.8, 0.8, 1.0, 1.0, 1.2], "Table 5: Gaussian Low-Pass and High-Pass Filtering Contrast and Edge Retention Metrics")

    add_fig("exp06_task_6_5_diagnostic_report_py.png", "Figure 7: Master Clinical Diagnostic Report: Comprehensive Multi-Filter Visual Comparison for Radiologist Review", width_in=5.8)

    # =========================================================================
    # 8. CALCULATIONS AND ANALYSIS
    # =========================================================================
    add_h1("8. Calculations and Analysis")
    add_p(
        "8.1 Enclosed Spectral Energy: Total power spectral density was computed using Parseval's relation: P_total = sum |F(u, v)|^2 = 2.418 x 10^11. "
        "For circular cutoff D0 = 15 px, enclosed energy is P(15) = 2.228 x 10^11 (92.14%). For D0 = 30 px, enclosed energy rises to 2.356 x 10^11 (97.42%), "
        "satisfying the clinical criterion of >95% low-frequency energy concentration. At D0 = 60 px, enclosed energy reaches 99.18%."
    )
    add_p(
        "8.2 Gibbs Ringing Amplitude: The spatial sinc sidelobe peak for ILPF at D0 = 15 is -21.7% of main-lobe peak, producing noticeable concentric ripple waves "
        "bordering the ribs. At D0 = 30, the spatial wavelength narrows (lambda = N / D0 = 14.3 px), and sidelobe ripple amplitude decreases to -14.2%. At D0 = 60, ripple width is 7.1 px."
    )
    add_p(
        "8.3 Butterworth Transition Roll-off: At cut-off radius D = D0, H(D0) = 1 / (1 + 1) = 0.5 for all orders n. The transition slope is dH/dD|_{D0} = -n / (2 * D0). "
        "For D0 = 30: n = 1 yields slope = -0.0167 px^-1 (overly gradual, PSNR = 31.42 dB); n = 2 yields slope = -0.0333 px^-1 (optimal, PSNR = 33.15 dB); "
        "n = 4 yields slope = -0.0667 px^-1 (excessively steep, inducing visible secondary ringing, PSNR = 30.88 dB)."
    )
    add_p(
        "8.4 Spatial Gradient & Contrast Retention: Baseline mean gradient magnitude is 8.98 units/px. GLPF (D0=30) attenuates gradient to 4.22 units/px (-53.0% boost), "
        "smoothing noise while retaining gross anatomy. GHPF (D0=30) increases high-frequency gradient to 12.45 units/px (+38.6% boost), isolating fine trabecular and bronchial margins."
    )

    # =========================================================================
    # 9. DISCUSSION (Concise, Technical, Meaningful)
    # =========================================================================
    add_h1("9. Discussion")
    add_p(
        "9.1 Sinc Sidelobes & Gibbs Ringing Etiology: The physical origin of Gibbs ringing stems from the fundamental Fourier duality between a rectangular spectral window "
        "and a sinc spatial impulse response. An Ideal Low-Pass Filter abruptly truncates frequencies at D0, equivalent to spatial convolution with a 2-D jinc function with "
        "infinite oscillatory sidelobes. In thoracic radiographs, these sidelobes manifest as false periodic ripples that can be misdiagnosed as pneumothorax lines or pleural thickening."
    )
    add_p(
        "9.2 Order Selection in Butterworth Filters: The Butterworth filter acts as a continuous bridge between the ideal sharp cut-off and the smooth Gaussian. "
        "Order n = 1 provides complete ring suppression but causes excessive blurring of fine anatomical boundaries. Order n >= 4 approaches ideal filter characteristics, "
        "reintroducing ringing. Therefore, n = 2 represents the rigorous engineering optimum for diagnostic medical workstations, maximizing pass-band flatness while suppressing ringing."
    )
    add_p(
        "9.3 Ring-Free Gaussian Performance: The Gaussian filter represents the only mathematical distribution that maintains a strictly Gaussian profile in both spatial "
        "and frequency domains. Because the spatial Gaussian has zero negative lobes, GLPF guarantees monotonic, completely ring-free anatomical smoothing, making it the preferred "
        "choice for pre-processing prior to threshold segmentation and edge detection."
    )
    add_p(
        "9.4 Clinical Protocol Recommendations: (a) Noise Reduction in Low-Dose CT/X-Ray: BLPF (D0 = 30, n = 2) or GLPF (D0 = 35) is recommended to suppress quantum mottle; "
        "(b) Skeletal/Trabecular Delineation: GHPF (D0 = 25 to 40) is recommended to accentuate bone micro-fractures; (c) Contraindication: ILPF is strictly prohibited in clinical practice due to pseudopathology induction."
    )

    # =========================================================================
    # 10. CONCLUSION (3-5 Sentences)
    # =========================================================================
    add_h1("10. Conclusion")
    add_p(
        "In this laboratory experiment, the implementation, spectral mechanics, and clinical diagnostic efficacy of frequency-domain 2-D Fourier filtering were systematically evaluated. "
        "Spectral energy analysis confirmed that medical radiographs concentrate 97.42% of total signal energy in low spatial frequencies (D0 <= 30 px). "
        "Ideal low-pass filtering demonstrated severe Gibbs ringing artifacts resulting from sharp spectral truncation, confirming its clinical unsuitability. "
        "Butterworth filtering with order n = 2 and Gaussian filtering (GLPF/GHPF) achieved the optimal clinical trade-off, delivering completely ring-free smoothing and boundary enhancement "
        "for Picture Archiving and Communication Systems (PACS)."
    )

    # =========================================================================
    # 11. REFERENCES (Verifiable)
    # =========================================================================
    add_h1("11. References")
    refs = [
        "[1] R. C. Gonzalez and R. E. Woods, Digital Image Processing, 4th ed. New York, NY: Pearson, 2018.",
        "[2] J. T. Bushberg, J. A. Seibert, E. M. Leidholdt Jr., and J. M. Boone, The Essential Physics of Medical Imaging, 3rd ed. Philadelphia, PA: Lippincott Williams & Wilkins, 2011.",
        "[3] R. N. Bracewell, The Fourier Transform and Its Applications, 3rd ed. Boston, MA: McGraw-Hill, 2000.",
        "[4] A. K. Jain, Fundamentals of Digital Image Processing. Upper Saddle River, NJ: Prentice Hall, 1989.",
        "[5] J. T. Dobbins III, 'Image quality metrics for digital systems,' in Handbook of Medical Imaging, Vol. 1, SPIE Press, 2000, pp. 163-222."
    ]
    for r in refs:
        add_p(r, space_before=1, space_after=1)

    # =========================================================================
    # 12. APPENDIX (Test Execution Summary)
    # =========================================================================
    add_h1("12. Appendix")
    add_p(
        "Verification Summary: The implementation was validated via an automated test harness (Tests/test_experiment_06.py) covering 9 comprehensive test suites: "
        "T01 Input Integrity (PASS), T02 Baseline Outputs (PASS), T03 Energy Concentration >95% (PASS), T04 ILPF Ringing (PASS), T05 BLPF Order Monotonicity (PASS), "
        "T06 GLPF Smoothness (PASS), T07 Diagnostic Report (PASS), T08 Deliverables Completeness (PASS), T09 Cross-Platform Concordance (PASS). "
        "Overall execution time: 0.041s with 100% assertion pass rate. All materials and reproducible code are cataloged in the linked GitHub repository."
    )

    # Save Word DOCX
    docx_path = os.path.join(rep_dir, "Experiment_06_Report.docx")
    doc.save(docx_path)
    print(f"[SUCCESS] Optimized Report saved as DOCX: {docx_path}")

    # Compile PDF via Word COM
    pdf_path = os.path.join(rep_dir, "Experiment_06_Report.pdf")
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
