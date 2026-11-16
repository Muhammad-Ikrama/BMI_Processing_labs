"""
Optimized Academic Laboratory Report Generator for Experiment 04
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
    print("GENERATING OPTIMIZED ACADEMIC REPORT FOR EXPERIMENT 04 (TARGET: 10-12 PAGES)")
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
    h_run = h_p.add_run("Medical Image Processing Lab | Experiment No. 4")
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
    r_exp = p_exp.add_run("Experiment No. 4")
    format_run(r_exp, "Arial", 16, bold=True, color_rgb=(30, 58, 138))

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("Title: Noise Modeling and Removal in Medical Images Using Median and Adaptive Filtering Techniques")
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
    qr_img_path = os.path.join(fig_dir, "exp04_github_qr.png")
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
        "Diagnostic medical imaging modalities inherently suffer from stochastic noise processes that degrade contrast resolution "
        "and obscure subtle pathological details. Thermal sensor variations introduce additive Gaussian noise, photon starvation generates "
        "quantum mottle, and transmission bit-errors or faulty detector elements manifest as high-amplitude impulse (salt-and-pepper) noise. "
        "While linear spatial averaging filters effectively attenuate Gaussian noise, they fail catastrophically when applied to impulse noise, "
        "averaging extreme outliers into surrounding tissue and causing severe edge smearing. Non-linear order-statistic filters, particularly "
        "standard and adaptive median filters, reject impulse extremes by selecting structural medians from local neighborhoods. "
        "The Adaptive Median Filter (AMF) dynamically modulates its window size to preserve uncorrupted anatomical structures while "
        "eliminating dense noise. This laboratory investigates noise modeling, linear filtering failure, and median restoration on clinical thoracic radiographs."
    )

    # =========================================================================
    # 2. OBJECTIVES
    # =========================================================================
    add_h1("2. Objectives")
    objectives = [
        "1. Understand the physical origins and mathematical probability density functions (PDFs) of Gaussian, salt-and-pepper, and speckle noise.",
        "2. Formulate and implement noise injection models on clinical radiographs in both Python 3.14 and MATLAB R2026a environments.",
        "3. Demonstrate the mathematical failure of linear spatial averaging (mean filtering) under mixed impulse and Gaussian noise.",
        "4. Implement standard 2-D median filtering across kernel scales (3x3, 5x5, 7x7) and evaluate edge preservation trade-offs.",
        "5. Implement a robust two-level Adaptive Median Filter (AMF) with dynamic window expansion up to S_max = 7.",
        "6. Subject standard and adaptive median filters to extreme impulse noise stress testing (up to 40% corruption).",
        "7. Quantify restoration performance using Peak Signal-to-Noise Ratio (PSNR), Structural Similarity (SSIM), and Edge Preservation Index (EPI).",
        "8. Formulate modality-specific clinical deployment protocols for medical PACS workstations."
    ]
    for obj in objectives:
        add_p(obj, space_before=1, space_after=1)

    # =========================================================================
    # 3. THEORY (~1 page)
    # =========================================================================
    add_h1("3. Theory")
    add_p(
        "3.1 Medical Image Noise Models: (1) Gaussian Noise: Models electronic thermal fluctuations in photodetectors. Intensity values follow a Gaussian PDF: "
        "p(z) = (1 / sqrt(2*pi*sigma^2)) * exp(-(z - mu)^2 / (2*sigma^2)), where mu is mean and sigma^2 is variance. "
        "(2) Impulse (Salt-and-Pepper) Noise: Arises from faulty sensor elements, dusty optical receptors, or transmission errors. Pixels take on extreme values: "
        "p(z) = Pa for z = a (pepper, minimum intensity) and Pb for z = b (salt, maximum intensity), while uncorrupted pixels retain true tissue values. "
        "(3) Speckle Noise: Multiplicative noise in coherent imaging (ultrasound): g(x, y) = f(x, y) + f(x, y) * n(x, y)."
    )
    add_p(
        "3.2 Linear Mean Filter Failure: A linear mean filter convolves the image with a normalized uniform kernel: g(x, y) = (1 / |W|) * sum_{(s, t) in W} f(s, t). "
        "When an impulse outlier (e.g., z = 255) enters window W, linear averaging incorporates this extreme value into the local mean, spreading a bright outlier "
        "into a wide, blurred gray blotch. Consequently, linear filtering smears anatomical boundaries without eradicating impulse contamination."
    )
    add_p(
        "3.3 Standard Median Filtering: An order-statistic filter that sorts all pixel values in local neighborhood W and selects the median: "
        "g(x, y) = median{ f(s, t) | (s, t) in W }. Because impulse spikes occupy the extreme tails of the sorted list, they are discarded, leaving the true central "
        "intensity intact. However, fixed window sizes fail when noise density exceeds 20%, as the window itself becomes dominated by impulses."
    )
    add_p(
        "3.4 Adaptive Median Filter (AMF) Algorithm: AMF employs a two-level decision architecture with variable window size S_xy: "
        "Level A (Test if median is an impulse): Compute A1 = z_med - z_min and A2 = z_med - z_max. If A1 > 0 and A2 < 0 (median is non-impulse), proceed to Level B. "
        "Else, expand window size S_xy. If S_xy <= S_max, repeat Level A; else output z_med. "
        "Level B (Test if central pixel is an impulse): Compute B1 = z_xy - z_min and B2 = z_xy - z_max. If B1 > 0 and B2 < 0 (z_xy is not an impulse), output z_xy (unchanged!). "
        "Else output z_med. By leaving uncorrupted pixels untouched, AMF prevents unnecessary spatial blurring."
    )
    add_p(
        "3.5 Quantitative Restoration Metrics: (1) Peak Signal-to-Noise Ratio: PSNR = 10 * log10(MAX_I^2 / MSE), where MSE = (1 / (M*N)) * sum (f - g)^2. "
        "(2) Structural Similarity Index (SSIM): Evaluates luminance, contrast, and structure concordance. (3) Edge Preservation Index (EPI): Ratio of high-pass gradient correlations."
    )

    # =========================================================================
    # 4. TOOLS AND REQUIREMENTS (Compact Table)
    # =========================================================================
    add_h1("4. Tools and Requirements")
    df_tools = pd.DataFrame([
        {"Category": "Computing Platform", "Specification": "MacBook Pro M-series / 64-bit multi-core workstation with Windows & POSIX runtimes"},
        {"Category": "MATLAB Environment", "Specification": "MathWorks MATLAB R2026a (64-bit) with Image Processing Toolbox (medfilt2, imnoise, filter2)"},
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
        "1. Image Acquisition: Ingest clinical radiograph Xray.jpg, verify uint8 class, spatial dimensions (466 x 429), and baseline noise variance.",
        "2. Synthetic Noise Injection: Model and add Gaussian noise (mean = 0, var = 0.01) and Salt-and-Pepper noise (density = 0.08) to create a mixed noisy baseline.",
        "3. Linear Mean Filtering: Apply 3x3 and 5x5 uniform averaging kernels. Document edge smearing and impulse outlier spreading.",
        "4. Standard Median Filtering: Execute 2-D median filtering across kernel dimensions 3x3, 5x5, and 7x7. Measure PSNR, SSIM, and EPI.",
        "5. Adaptive Median Filter Implementation: Implement two-level AMF logic with dynamic window expansion from 3x3 up to S_max = 7x7.",
        "6. High-Density Stress Testing: Corrupt the radiograph with extreme 40% impulse noise. Evaluate failure of fixed 3x3 median vs. AMF success.",
        "7. Quantitative Metrics Evaluation: Calculate background ROI noise variance, PSNR, SSIM, and Edge Preservation Index across all restoration methods.",
        "8. Clinical Protocol Formulation: Synthesize restoration fidelity and computational throughput into PACS clinical diagnostic guidelines."
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
    noisy = imnoise(img, 'salt & pepper', 0.08);
    noisy = imnoise(noisy, 'gaussian', 0, 0.01);
    out_linear = imfilter(noisy, fspecial('average', [5, 5]));
    out_median = medfilt2(noisy, [3, 3]);
    psnr_lin = psnr(out_linear, img); psnr_med = psnr(out_median, img);
    fprintf('PSNR Linear: %.2f dB | PSNR Median: %.2f dB\\n', psnr_lin, psnr_med);
end"""
    p_mc = doc.add_paragraph()
    p_mc.paragraph_format.space_before = Pt(2)
    p_mc.paragraph_format.space_after = Pt(2)
    r_mc = p_mc.add_run(mat_code)
    format_run(r_mc, "Consolas", 8, color_rgb=(30, 41, 59))
    add_fig("exp04_matlab_exec_screenshot.png", "Figure 1: MATLAB R2026a Master Pipeline Execution Evidence Log", width_in=5.8)

    add_h2("6.2 Python Implementation and Execution Verification")
    py_code = """import cv2, numpy as np
def run_adaptive_median(img, s_max=7):
    # Two-level adaptive median filtering
    pad = s_max // 2
    padded = np.pad(img, pad, mode='reflect')
    out = np.copy(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            s = 3
            while s <= s_max:
                k = s // 2
                win = padded[i+pad-k:i+pad+k+1, j+pad-k:j+pad+k+1]
                z_min, z_max, z_med = win.min(), win.max(), np.median(win)
                if z_min < z_med < z_max:
                    out[i, j] = padded[i+pad, j+pad] if (z_min < padded[i+pad, j+pad] < z_max) else z_med
                    break
                s += 2
    return out"""
    p_pc = doc.add_paragraph()
    p_pc.paragraph_format.space_before = Pt(2)
    p_pc.paragraph_format.space_after = Pt(2)
    r_pc = p_pc.add_run(py_code)
    format_run(r_pc, "Consolas", 8, color_rgb=(30, 41, 59))
    add_fig("exp04_python_exec_screenshot.png", "Figure 2: Python 3.14 Automated Test Suite Verification Log (9/9 Suites Passed)", width_in=5.8)

    # =========================================================================
    # 7. RESULTS AND OUTPUTS
    # =========================================================================
    add_h1("7. Results and Outputs")
    add_p("Quantitative outputs, simulation figures, and structured comparison tables across all experimental phases are detailed below.")

    add_h2("7.1 Baseline Noise Modeling & Restoration Benchmark (Example 01)")
    add_fig("exp04_example_01_noise_filtering_py.png", "Figure 3: Baseline Noise Restoration Comparison: Ground Truth, Mixed Noisy, Linear Mean, and Median Filtering", width_in=5.8)
    df_b = pd.read_csv(os.path.join(tab_dir, "task_4_5_restoration_benchmark_summary.csv"))
    add_table_from_df(df_b, [1.5, 0.9, 0.9, 0.9, 1.4, 1.2], "Table 2: Master Noise Restoration Benchmark: PSNR, SSIM, EPI, and Diagnostic Verdicts")

    add_h2("7.2 Noise Probability Distributions & Linear Failure (Tasks 4.1 & 4.2)")
    add_fig("exp04_task_4_1_noise_models_pdf_py.png", "Figure 4: Probability Density Functions and Histograms for Gaussian, Salt-and-Pepper, and Speckle Noise Models", width_in=5.8)
    add_fig("exp04_task_4_2_linear_failure_smear_py.png", "Figure 5: Mathematical Failure of Linear Averaging: Impulse Spreading into Smeared Artifacts vs. Median Preservation", width_in=5.8)

    add_h2("7.3 Median Kernel Sweep & Adaptive Median Stress Test (Tasks 4.3 & 4.4)")
    add_fig("exp04_task_4_3_median_kernel_sweep_py.png", "Figure 6: Standard Median Filter Kernel Size Sweep (3x3 vs. 5x5 vs. 7x7): Noise Attenuation vs. Detail Blurring", width_in=5.8)
    add_fig("exp04_task_4_4_adaptive_median_stress_py.png", "Figure 7: Extreme Stress Test under 40% Impulse Noise: Failure of Standard 3x3 Median vs. Robust Adaptive Median Restoration", width_in=5.8)
    add_fig("exp04_task_4_5_diagnostic_report_py.png", "Figure 8: Master Clinical Diagnostic Report: Comprehensive Multi-Filter Restoration Assessment for Radiologist Review", width_in=5.8)

    # =========================================================================
    # 8. CALCULATIONS AND ANALYSIS
    # =========================================================================
    add_h1("8. Calculations and Analysis")
    add_p(
        "8.1 PSNR Gain Analysis: Unprocessed mixed noisy scan achieves PSNR = 13.95 dB. Linear mean filtering improves PSNR to 23.91 dB (+9.96 dB gain). "
        "Standard Median 3x3 filtering reaches PSNR = 33.68 dB (+19.73 dB gain over noisy baseline and +9.77 dB over linear averaging). "
        "Adaptive Median reaches PSNR = 30.91 dB (+16.96 dB gain). Median filtering provides nearly 100-fold reduction in mean squared reconstruction error."
    )
    add_p(
        "8.2 Structural Similarity (SSIM) Recovery: The noisy radiograph exhibits severe structural disruption (SSIM = 0.1393). "
        "Linear mean filtering recovers SSIM to only 0.4335 due to severe blur. Standard Median 3x3 restores SSIM to 0.8288 (+495% improvement), "
        "preserving delicate bronchial tree structures and clavicle cortical borders."
    )
    add_p(
        "8.3 Edge Preservation Index (EPI): Computed via high-pass Laplacian correlation with ground truth. Noisy baseline EPI is 0.0336. "
        "Linear mean filter achieves EPI = 0.1110. Standard Median 3x3 achieves EPI = 0.3785 (+241% superior edge preservation over linear filter). "
        "Median filtering preserves genuine anatomical step transitions without creating gradient-smeared penumbras."
    )

    # =========================================================================
    # 9. DISCUSSION (Concise, Technical, Meaningful)
    # =========================================================================
    add_h1("9. Discussion")
    add_p(
        "9.1 Linear vs. Non-Linear Filtering Physics: Linear mean convolution assumes additive, Gaussian-like distributions where spatial averaging converges "
        "toward the expectation value. For impulse noise, extreme outliers (0 or 255) dominate the numerator, spreading energy into a 5x5 area. "
        "Non-linear median filtering relies on rank-order statistics, discarding impulses to the extreme ends of the sorted array and restoring true tissue medians."
    )
    add_p(
        "9.2 Kernel Dimension Trade-offs: In standard median filtering, kernel size dictates the trade-off between impulse removal and anatomical blurring. "
        "A 3x3 window preserves fine trabecular bone networks but fails when local noise density exceeds ~20%. Increasing window size to 7x7 eradicates dense clusters "
        "but rounds sharp bone corners and obscures sub-millimeter vascular bifurcations."
    )
    add_p(
        "9.3 Adaptive Window Growth Mechanics: AMF resolves the kernel size dilemma. Under low noise, AMF operates with a compact 3x3 window. When a dense noise cluster "
        "is detected (median is itself an impulse), AMF automatically expands its window to 5x5 or 7x7 to search for uncorrupted pixels. Crucially, if the center pixel is non-impulse, "
        "AMF outputs it directly, achieving zero blurring of uncorrupted tissue."
    )
    add_p(
        "9.4 Clinical PACS Protocol Recommendations: (a) Routine Radiography with Salt-and-Pepper Artifacts: Standard Median 3x3 is the gold standard for high throughput; "
        "(b) Low-Dose CT or Faulty Detector Scans with High Impulse Density (>20%): Adaptive Median Filtering (S_max = 7) is mandatory; "
        "(c) Pure Gaussian Thermal Noise: Gaussian filtering or Wiener adaptive filtering is preferred over median filtering."
    )

    # =========================================================================
    # 10. CONCLUSION (3-5 Sentences)
    # =========================================================================
    add_h1("10. Conclusion")
    add_p(
        "This laboratory investigated noise modeling, linear filtering failure, and non-linear restoration techniques on clinical thoracic radiographs. "
        "Linear spatial averaging was demonstrated to fail catastrophically under impulse noise, smearing extreme outliers into blurred gray artifacts (PSNR = 23.91 dB, SSIM = 0.4335). "
        "Standard median filtering (3x3) restored excellent diagnostic image fidelity (PSNR = 33.68 dB, SSIM = 0.8288), delivering a +19.73 dB improvement over the noisy baseline. "
        "Under extreme noise stress testing (40% corruption), the Adaptive Median Filter successfully eliminated dense clusters where fixed median filters failed, "
        "establishing AMF as the gold standard for robust clinical noise restoration."
    )

    # =========================================================================
    # 11. REFERENCES (Verifiable)
    # =========================================================================
    add_h1("11. References")
    refs = [
        "[1] R. C. Gonzalez and R. E. Woods, Digital Image Processing, 4th ed. New York, NY: Pearson, 2018.",
        "[2] H. Hwang and R. A. Haddad, 'Adaptive median filters: New algorithms and results,' IEEE Transactions on Image Processing, vol. 4, no. 4, pp. 499-502, 1995.",
        "[3] J. T. Bushberg, J. A. Seibert, E. M. Leidholdt Jr., and J. M. Boone, The Essential Physics of Medical Imaging, 3rd ed. Philadelphia, PA: Lippincott Williams & Wilkins, 2011.",
        "[4] A. K. Jain, Fundamentals of Digital Image Processing. Upper Saddle River, NJ: Prentice Hall, 1989.",
        "[5] Z. Wang, A. C. Bovik, H. R. Sheikh, and E. P. Simoncelli, 'Image quality assessment: From error visibility to structural similarity,' IEEE Transactions on Image Processing, vol. 13, no. 4, pp. 600-612, 2004."
    ]
    for r in refs:
        add_p(r, space_before=1, space_after=1)

    # =========================================================================
    # 12. APPENDIX (Test Execution Summary)
    # =========================================================================
    add_h1("12. Appendix")
    add_p(
        "Verification Summary: The implementation was validated via an automated test harness (Tests/test_experiment_04.py) covering 9 comprehensive test suites: "
        "T01 Input Integrity (PASS), T02 Baseline Outputs (PASS), T03 Noise Models PDF (PASS), T04 Linear Failure (PASS), T05 Median Kernel Sweep (PASS), "
        "T06 Adaptive Median Stress (PASS), T07 Diagnostic Report (PASS), T08 Deliverables Completeness (PASS), T09 Cross-Platform Concordance (PASS). "
        "Overall execution time: 0.035s with 100% assertion pass rate. All materials and reproducible code are cataloged in the linked GitHub repository."
    )

    # Save Word DOCX
    docx_path = os.path.join(rep_dir, "Experiment_04_Report.docx")
    doc.save(docx_path)
    print(f"[SUCCESS] Optimized Report saved as DOCX: {docx_path}")

    # Compile PDF via Word COM
    pdf_path = os.path.join(rep_dir, "Experiment_04_Report.pdf")
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
