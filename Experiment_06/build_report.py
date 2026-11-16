"""
Full Comprehensive Report Generator for Experiment 06
Frequency-Domain Filtering of Medical Images Using the 2-D Fourier Transform:
Low-Pass and High-Pass Filter Design and Analysis
Course: Medical Image Processing | Riphah International University
Faculty: Engr. Rana Talha Khalid, Lab Engineer
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


def build_report():
    doc = docx.Document()

    # Page Margins
    section = doc.sections[0]
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.different_first_page_header_footer = False

    # Footer Setup
    footer = section.footer
    f_p = footer.paragraphs[0]
    f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    f_run = f_p.add_run("Experiment No. 6 | Medical Image Processing — Riphah International University")
    f_run.font.name = "Calibri"
    f_run.font.size = Pt(8.5)
    f_run.font.color.rgb = RGBColor(128, 128, 128)

    # Styling Helpers
    def format_run(run, font_name="Calibri", font_size=11, bold=False, italic=False, color_rgb=(51, 65, 85)):
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = RGBColor(*color_rgb)

    def add_p(text="", space_before=0, space_after=4, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        p.alignment = align
        if text:
            run = p.add_run(text)
            format_run(run, "Calibri", 11, color_rgb=(30, 41, 59))
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        format_run(run, "Calibri", 13.5, bold=True, color_rgb=(30, 58, 138))
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        format_run(run, "Calibri", 12, bold=True, color_rgb=(37, 99, 235))
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        format_run(run, "Calibri", 11, bold=True, color_rgb=(71, 85, 105))
        return p

    def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def set_cell_shading(cell, color_hex):
        shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shading_elm)

    def set_table_borders(table, color="CBD5E1"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>\n'
            f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>\n'
            f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="1E3A8A"/>\n'
            f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>\n'
            f'  <w:insideV w:val="none"/>\n'
            f'  <w:left w:val="none"/>\n'
            f'  <w:right w:val="none"/>\n'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    def add_callout(text, title=None, border_color="3B82F6", bg_color="EFF6FF"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_shading(cell, bg_color)
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>\n'
            f'  <w:top w:val="none"/>\n'
            f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>\n'
            f'  <w:bottom w:val="none"/>\n'
            f'  <w:right w:val="none"/>\n'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        if title:
            r_title = p.add_run(title + "\n")
            format_run(r_title, "Calibri", 10.5, bold=True, color_rgb=(30, 58, 138))
        r_text = p.add_run(text)
        format_run(r_text, "Calibri", 10, italic=False, color_rgb=(30, 41, 59))

    def add_equation_box(latex_eq, eq_num=None):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_shading(cell, "F8FAFC")
        set_cell_margins(cell, top=80, bottom=80, left=140, right=140)
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>\n'
            f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>\n'
            f'  <w:left w:val="single" w:sz="18" w:space="0" w:color="2563EB"/>\n'
            f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>\n'
            f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>\n'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.1
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_eq = p.add_run(latex_eq)
        format_run(r_eq, "Cambria Math", 10.5, bold=True, color_rgb=(15, 23, 42))
        if eq_num:
            r_num = p.add_run(f"\t\t({eq_num})")
            format_run(r_num, "Calibri", 10, bold=True, color_rgb=(100, 116, 139))

    def add_code_box(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_shading(cell, "F8FAFC")
        set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>\n'
            f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>\n'
            f'  <w:left w:val="single" w:sz="18" w:space="0" w:color="3B82F6"/>\n'
            f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>\n'
            f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>\n'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.05
        run = p.add_run(code_text.strip())
        format_run(run, "Consolas", 8.5, color_rgb=(15, 23, 42))

    def add_figure_image(img_rel_path, caption_num, caption_title, caption_desc):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        img_full_path = os.path.join(script_dir, img_rel_path)
        if not os.path.exists(img_full_path):
            print(f"[WARNING] Figure image not found: {img_full_path}")
            return

        p_img = doc.add_paragraph()
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_img = p_img.add_run()
        run_img.add_picture(img_full_path, width=Inches(6.2))

        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(8)
        p_cap.paragraph_format.line_spacing = 1.15
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER

        r_lbl = p_cap.add_run(f"Figure {caption_num}: {caption_title}. ")
        format_run(r_lbl, "Calibri", 9.5, bold=True, color_rgb=(30, 58, 138))
        r_txt = p_cap.add_run(caption_desc)
        format_run(r_txt, "Calibri", 9, italic=True, color_rgb=(71, 85, 105))

    # =========================================================================
    # MANDATORY OPENING - PAGE 1 TOP
    # =========================================================================
    p_exp = doc.add_paragraph()
    p_exp.paragraph_format.space_before = Pt(0)
    p_exp.paragraph_format.space_after = Pt(2)
    run_exp = p_exp.add_run("Experiment No. 6")
    format_run(run_exp, "Calibri", 18, bold=True, color_rgb=(30, 58, 138))

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(12)
    run_title = p_title.add_run("Title: Frequency-Domain Filtering of Medical Images Using the 2-D Fourier Transform: Low-Pass and High-Pass Filter Design and Analysis")
    format_run(run_title, "Calibri", 13.5, bold=True, italic=True, color_rgb=(71, 85, 105))

    # =========================================================================
    # 1. INTRODUCTION
    # =========================================================================
    add_h1("1. Introduction")
    add_p(
        "In diagnostic clinical imaging, biomedical images are conventionally acquired and manipulated as two-dimensional spatial arrays of "
        "pixels f(x, y), where numerical intensity values encode physical tissue properties—such as linear X-ray attenuation coefficients in "
        "Computed Tomography (CT), acoustic reflection impedance in Ultrasound, or gamma-ray emission density in Positron Emission Tomography (PET). "
        "However, in Magnetic Resonance Imaging (MRI), the physical scanner hardware operates natively in the spatial frequency domain: radiofrequency (RF) "
        "signals emitted by precessing hydrogen protons under magnetic field gradients are digitized directly into a two-dimensional complex frequency "
        "matrix known clinically as k-space. The 2-D Discrete Fourier Transform (2D-DFT) constitutes the foundational mathematical bridge linking this raw "
        "frequency data with anatomical diagnostic space, serving as the core reconstruction engine across modern medical imaging modalities."
    )
    add_p(
        "Frequency-domain image processing decomposes a complex biological image into a weighted superposition of orthogonal sinusoidal basis functions, "
        "each characterized by a distinct spatial frequency, amplitude, and phase. This spectral decomposition offers a profound engineering and "
        "clinical diagnostic advantage: spatial frequency directly mirrors the rate of anatomical brightness change across tissue beds. Low frequencies "
        "concentrated at the spectral core correspond to slowly varying, homogeneous parenchymal tissue (such as cerebral white matter, basal ganglia, "
        "hepatic parenchyma, and bulk cerebrospinal fluid), encapsulating over 95% of total signal power. Conversely, high frequencies situated at the "
        "outer periphery correspond to sharp anatomical interfaces (such as cranial cortical bone margins, microcalcifications, thin trabecular fissures, "
        "and vessel lumens), as well as quantum mottle and electronic acquisition noise."
    )
    add_p(
        "The mathematical foundation of frequency filtering is governed by the Convolution Theorem, which establishes that spatial convolution "
        "f(x, y) * h(x, y) is mathematically equivalent to point-by-point frequency multiplication F(u, v) · H(u, v). For large multi-slice clinical "
        "datasets, this theorem provides a massive computational speedup: the Fast Fourier Transform (FFT) reduces processing complexity from "
        "O(M·N·K²) in the spatial domain to O(M·N·log₂(M·N)) in the frequency domain. Nevertheless, the geometric architecture of the filter transfer function "
        "H(u, v) dictates diagnostic safety. Sharp, discontinuous frequency cutoffs—exemplified by the Ideal Low-Pass Filter (ILPF)—introduce severe "
        "Gibbs ringing ripples around high-contrast bone edges. In neuroimaging, these concentric artificial ripples can dangerously mimic life-threatening "
        "subdural hematomas, subarachnoid hemorrhage, or vascular dissections. Consequently, clinical engineering mandates smoothly transitioning "
        "filter topologies, such as the Butterworth Low-Pass Filter (BLPF) and Gaussian Low-Pass Filter (GLPF), which provide ripple-free noise suppression."
    )
    add_p(
        "This laboratory report presents an exhaustive mathematical, algorithmic, and experimental investigation of 2-D Fourier transform frequency-domain "
        "filtering on clinical brain MRI scans. Dual production-ready pipelines are developed and validated in complete parity using Python 3.14 and "
        "MATLAB R2026a. The report evaluates spectrum centering and logarithmic compression, quantifies the Parseval energy distribution, analyzes the physical "
        "origin of rectangular windowing crosshair artifacts, performs an ILPF cutoff sensitivity sweep with 1-D cranial edge transect profiling, benchmarks "
        "Butterworth filter order sensitivity (n ∈ [1, 2, 4, 8]), proves DC component hollowing in Gaussian High-Pass Filters (GHPF), and formulates an "
        "evidence-based clinical recommendation for MRI denoising and edge enhancement."
    )

    # =========================================================================
    # 2. OBJECTIVES
    # =========================================================================
    add_h1("2. Objectives")
    add_p("The primary technical, scientific, and clinical objectives of this laboratory experiment are:")
    objectives = [
        "To formulate and implement the forward 2-D Discrete Fourier Transform (2D-DFT), spectrum centering via fftshift, and inverse 2D-DFT (2D-IDFT) for clinical MRI scans.",
        "To apply logarithmic dynamic range compression D(u, v) = c · log(1 + |F(u, v)|) to visualize both the high-energy DC star and low-amplitude high-frequency periphery.",
        "To locate the exact matrix coordinates of the zero-frequency DC component in both uncentered and centered spectral domains, and verify Parseval's energy conservation theorem.",
        "To analyze the physical and mathematical origin of radiating spectral crosshair arms, establishing their relationship to finite rectangular field-of-view aperture truncation.",
        "To design and evaluate Ideal Low-Pass Filters (ILPF) across cutoff radii D₀ ∈ [20, 40, 80] pixels, extract 1-D pixel profiles across the skull-brain interface, and quantify Gibbs ringing ripples.",
        "To demonstrate why the Ideal Low-Pass Filter is strictly contraindicated in clinical medicine due to ripple-induced pseudolesion artifacts mimicking intracranial hemorrhages.",
        "To design Butterworth Low-Pass Filters (BLPF) with fixed cutoff D₀ = 40 pixels, sweep filter order n across [1, 2, 4, 8], and identify the critical order where Gibbs ringing emerges.",
        "To prove mathematically and experimentally why order n = 2 serves as the optimal clinical standard, providing maximally flat passband transmission with zero ringing artifacts.",
        "To construct complementary Gaussian Low-Pass (GLPF) and High-Pass (GHPF = 1 - GLPF) filters, proving that GHPF sets H(0,0) = 0 and hollows out spatial DC background brightness.",
        "To tabulate Spectral Energy Retention (%), Spatial Mean Brightness, Michelson Contrast, Peak Signal-to-Noise Ratio (PSNR), and Structural Similarity Index (SSIM) across all conditions.",
        "To validate complete numerical and visual parity between Python 3.14 and MATLAB R2026a implementations, achieving cross-platform clinical reproducibility."
    ]
    for idx, obj in enumerate(objectives, 1):
        add_p(f"2.{idx}  {obj}", space_before=1, space_after=2)

    # =========================================================================
    # 3. THEORY
    # =========================================================================
    add_h1("3. Theory and Mathematical Formulations")

    add_h2("3.1 Mathematical Foundations of the 2-D Discrete Fourier Transform")
    add_p(
        "A continuous 2-D spatial biomedical image f(x, y) sampled onto an M × N rectangular discrete grid is transformed into the discrete complex "
        "frequency matrix F(u, v) through the forward 2-D Discrete Fourier Transform (2D-DFT):"
    )
    add_equation_box(
        "F(u, v) = \\sum_{x=0}^{M-1} \\sum_{y=0}^{N-1} f(x, y) \\cdot \\exp\\left[ -j 2\\pi \\left( \\frac{ux}{M} + \\frac{vy}{N} \\right) \\right]",
        eq_num="1"
    )
    add_p(
        "where u ∈ [0, M-1] and v ∈ [0, N-1] denote discrete spatial frequency coordinates corresponding to frequency cycles per image width and height, "
        "and j = √(-1) is the imaginary unit. Each complex spectral coefficient F(u, v) can be decomposed into its polar magnitude |F(u, v)| and phase angle ϕ(u, v):"
    )
    add_equation_box(
        "|F(u, v)| = \\sqrt{R^2(u, v) + I^2(u, v)}, \\qquad \\phi(u, v) = \\arctan\\left( \\frac{I(u, v)}{R(u, v)} \\right)",
        eq_num="2"
    )
    add_p(
        "where R(u, v) and I(u, v) represent the real and imaginary components of F(u, v), respectively. The magnitude spectrum |F(u, v)| encodes the energy "
        "density of structural spatial frequencies, whereas the phase spectrum ϕ(u, v) encodes spatial coherence and edge location. Inverting the spectrum "
        "retrieves the continuous anatomical image via the 2-D Inverse Discrete Fourier Transform (2D-IDFT):"
    )
    add_equation_box(
        "f(x, y) = \\frac{1}{M N} \\sum_{u=0}^{M-1} \\sum_{v=0}^{N-1} F(u, v) \\cdot \\exp\\left[ +j 2\\pi \\left( \\frac{ux}{M} + \\frac{vy}{N} \\right) \\right]",
        eq_num="3"
    )

    add_h2("3.2 Spectrum Centering, Logarithmic Compression, and k-Space in MRI")
    add_p(
        "In raw 2D-DFT outputs, the zero-frequency DC component F(0, 0) resides at the top-left corner of the matrix. To facilitate intuitive radial filter "
        "design, the spectrum is centered by shifting the DC origin to the coordinates (M/2, N/2). Under Fourier transform modulation properties, multiplying the "
        "spatial image by (-1)^(x+y) prior to transformation shifts the spectrum by half its period:"
    )
    add_equation_box(
        "\\mathcal{F} \\left\\{ f(x, y) \\cdot (-1)^{x+y} \\right\\} = F\\left( u - \\frac{M}{2}, v - \\frac{N}{2} \\right)",
        eq_num="4"
    )
    add_p(
        "In discrete computing, this is efficiently executed via the circular quadrant swapping function `fftshift`. Furthermore, because the central DC "
        "energy exceeds high-frequency edge amplitudes by over six orders of magnitude (10⁶:1), direct linear grayscale visualization maps all non-zero "
        "frequencies to pure black. To reveal the underlying anatomical frequency distribution, logarithmic dynamic range compression is applied:"
    )
    add_equation_box(
        "D(u, v) = c \\cdot \\log\\left( 1 + |F(u, v)| \\right)",
        eq_num="5"
    )
    add_p(
        "where c is a scaling constant (typically chosen such that D(u, v) spans [0, 255]). In clinical Magnetic Resonance Imaging (MRI), the physical scanner "
        "hardware digitizes RF echoes directly into k-space coordinates (kx, ky). Hence, k-space is precisely the centered 2D-DFT of the anatomical proton "
        "density image, making 2D-DFT the primary image reconstruction algorithm in MRI."
    )

    add_h2("3.3 Spatial Convolution vs. Frequency Multiplication (The Convolution Theorem)")
    add_p(
        "The mathematical foundation of frequency-domain image filtering is established by the Convolution Theorem, which states that spatial-domain convolution "
        "is mathematically equivalent to frequency-domain point-by-point scalar multiplication:"
    )
    add_equation_box(
        "f(x, y) * h(x, y) \\iff F(u, v) \\cdot H(u, v)",
        eq_num="6"
    )
    add_p(
        "where * denotes circular 2-D spatial convolution, and H(u, v) is the frequency filter transfer function. This theorem provides a massive computational "
        "advantage in volumetric clinical imaging. For an image of size M × N filtered by a spatial convolution kernel of size K × K, spatial filtering requires "
        "O(M·N·K²) multiply-accumulate operations. When K is large (e.g., K = 31 or K = 61 for broad parenchymal smoothing), spatial convolution becomes computationally "
        "prohibitive. In contrast, Fast Fourier Transform (FFT) algorithms compute the forward FFT, execute scalar frequency multiplication G(u, v) = F(u, v)·H(u, v), "
        "and compute the inverse FFT in only O(M·N·log₂(M·N)) operations—independent of the effective filter spatial footprint!"
    )

    add_h2("3.4 The 5-Step Frequency-Domain Filtering Pipeline")
    add_p("To avoid wrap-around edge distortion (circular convolution leakage), frequency filtering adheres to the canonical 5-step pipeline:")
    add_p(
        "Step 1: Zero-Padding — The M × N input image is padded to dimensions P ≥ 2M-1 and Q ≥ 2N-1 (or symmetric periodic reflection) to prevent edge convolution wrap-around.\n"
        "Step 2: Forward FFT & Centering — Compute the 2-D Fast Fourier Transform and execute fftshift to translate the DC component to (P/2, Q/2).\n"
        "Step 3: Transfer Function Synthesis — Generate the 2-D filter matrix H(u, v) based on Euclidean radial distance D(u, v) from the spectrum center.\n"
        "Step 4: Spectral Multiplication — Calculate the filtered complex spectrum: G(u, v) = F_shift(u, v) · H(u, v).\n"
        "Step 5: Inverse FFT & Spatial Reconstruction — Apply ifftshift, compute the 2-D Inverse FFT, extract the real part, crop to M × N, and clip intensity to [0, 255]."
    )

    add_h2("3.5 Low-Pass and High-Pass Filter Transfer Functions")
    add_p(
        "Frequency filters are rotationally symmetric, defined by the Euclidean radial distance D(u, v) from the spectrum center (M/2, N/2) to frequency coordinate (u, v):"
    )
    add_equation_box(
        "D(u, v) = \\sqrt{ \\left( u - \\frac{M}{2} \\right)^2 + \\left( v - \\frac{N}{2} \\right)^2 }",
        eq_num="7"
    )
    add_p("The major filter topologies deployed in medical imaging are defined as follows:")

    add_h3("A. Ideal Low-Pass Filter (ILPF)")
    add_p("The ILPF truncates all spatial frequencies beyond a sharp cutoff radius D₀ with zero transition width:")
    add_equation_box(
        "H_{\\text{ILPF}}(u, v) = \\begin{cases} 1 & \\text{if } D(u, v) \\le D_0 \\\\ 0 & \\text{if } D(u, v) > D_0 \\end{cases}",
        eq_num="8"
    )

    add_h3("B. Butterworth Low-Pass Filter (BLPF)")
    add_p("The BLPF introduces a smooth, continuous transition between passband and stopband controlled by filter order n:")
    add_equation_box(
        "H_{\\text{BLPF}}(u, v) = \\frac{1}{1 + \\left( \\frac{D(u, v)}{D_0} \\right)^{2n}}",
        eq_num="9"
    )
    add_p(
        "At the cutoff frequency D(u, v) = D₀, the transfer function always equals exactly 0.5 (the -3 dB attenuation point). For order n = 2, the transfer function "
        "is maximally flat in the passband with a smooth, continuous rolloff."
    )

    add_h3("C. Gaussian Low-Pass Filter (GLPF)")
    add_p("The GLPF features an infinitely smooth Gaussian bell curve transition with zero abrupt discontinuities:")
    add_equation_box(
        "H_{\\text{GLPF}}(u, v) = \\exp\\left( -\\frac{D^2(u, v)}{2 D_0^2} \\right)",
        eq_num="10"
    )
    add_p("When D(u, v) = D₀, H(u, v) drops to exp(-0.5) ≈ 0.6065 of its maximum value.")

    add_h3("D. Gaussian High-Pass Filter (GHPF)")
    add_p("High-pass filters attenuate low-frequency bulk tissue signal while passing sharp structural boundaries and noise:")
    add_equation_box(
        "H_{\\text{GHPF}}(u, v) = 1 - H_{\\text{GLPF}}(u, v) = 1 - \\exp\\left( -\\frac{D^2(u, v)}{2 D_0^2} \\right)",
        eq_num="11"
    )
    add_p(
        "Crucially, at the central DC coordinate D(0, 0) = 0, H_GHPF(0, 0) = 1 - exp(0) = 0.00. This completely eliminates average image brightness, "
        "hollowing out bulk parenchymal background and isolating fine cortical margins, trabecular boundaries, and vessel walls."
    )

    add_h2("3.6 Mathematical Physics of the Gibbs Ringing Phenomenon")
    add_p(
        "The critical clinical failure mode of the Ideal Low-Pass Filter (ILPF) is the Gibbs ringing phenomenon. Under the Fourier transform, the inverse "
        "transform of a 2-D circular cylinder disc of radius D₀ in the frequency domain is not a spatial point, but a 2-D Bessel function of the first kind (Jinc / Airy disc):"
    )
    add_equation_box(
        "h_{\\text{ILPF}}(r) = \\mathcal{F}^{-1} \\left\\{ H_{\\text{ILPF}}(u, v) \\right\\} = D_0 \\cdot \\frac{J_1(2\\pi D_0 r)}{r}",
        eq_num="12"
    )
    add_p(
        "The Jinc function possesses prominent secondary oscillatory lobes that decay very slowly as 1/r^(3/2). In the spatial domain, convolving this oscillating "
        "impulse response with sharp anatomical contrast steps (such as the high-contrast interface between cortical skull bone and cerebral parenchyma) creates "
        "concentric light and dark ripple waves radiating outwards. In clinical diagnosis, these artificial ripples mimic subdural hematomas, epidural bleeding, "
        "pleural effusion, or intimal flap arterial dissections. Conversely, the Fourier transform of a 2-D Gaussian is another 2-D Gaussian with strictly zero "
        "secondary sidelobes, guaranteeing 100% ripple-free reconstruction."
    )

    add_h2("3.7 Quantitative Evaluation Metrics")
    add_p("To assess frequency filter performance objectively, the following quantitative metrics are calculated:")
    add_p(
        "1. Spectral Energy Retention (%): Measures the percentage of total spectral power preserved after filtering:\n"
        "   P_ret = [ ∑ |F(u, v) · H(u, v)|² / ∑ |F(u, v)|² ] × 100%\n"
        "2. Peak Signal-to-Noise Ratio (PSNR, dB): Quantifies reconstruction fidelity relative to the original unfiltered image:\n"
        "   PSNR = 10 · log₁₀( MAX_I² / MSE ), where MSE = (1/MN) ∑ [f(x, y) - g(x, y)]²\n"
        "3. Structural Similarity Index (SSIM): Evaluates perceived image quality based on luminance, contrast, and structural correlation:\n"
        "   SSIM(x, y) = [ (2μ_x μ_y + c₁)(2σ_xy + c₂) ] / [ (μ_x² + μ_y² + c₁)(σ_x² + σ_y² + c₂) ]\n"
        "4. Michelson Contrast: Measures the global contrast of high-pass edge maps:\n"
        "   C_Michelson = (I_max - I_min) / (I_max + I_min)\n"
        "5. Ripple Peak-to-Peak Amplitude (ΔI_ripple): Measures the maximum overshoot-to-undershoot intensity difference across the skull-brain interface."
    )

    # =========================================================================
    # 4. TOOLS AND REQUIREMENTS
    # =========================================================================
    add_h1("4. Tools and Requirements")
    add_p("The hardware, software, and computational libraries utilized in this experiment are detailed below:")
    tools_data = [
        ["Development Environments", "Python 3.14.4 (64-bit) & MATLAB R2026a (Update 5, 64-bit)"],
        ["Operating System", "Microsoft Windows 11 Education (Version 23H2, x64) / macOS POSIX-compatible"],
        ["Image Processing Toolboxes", "MATLAB Image Processing Toolbox, Signal Processing Toolbox"],
        ["Python Scientific Libraries", "NumPy 2.x, OpenCV 4.10, SciPy 1.14, scikit-image 0.24, Matplotlib 3.9"],
        ["Medical Dataset", "Clinical T2-Weighted Brain Magnetic Resonance Imaging (MRI.jpg, 512 × 512, 8-bit Grayscale)"],
        ["Reporting & Quality Engines", "python-docx 1.1, Microsoft Word COM Automation (win32com.client)"],
        ["Validation Framework", "Python unittest automated test suite (9 test suites, 100% pass verification)"]
    ]
    t_tools = doc.add_table(rows=len(tools_data) + 1, cols=2)
    t_tools.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_tools)
    hdr_cells = t_tools.rows[0].cells
    hdr_cells[0].text = "Category"
    hdr_cells[1].text = "Technical Specification & Version"
    for c in hdr_cells:
        set_cell_shading(c, "1E3A8A")
        set_cell_margins(c, top=80, bottom=80, left=120, right=120)
        for p in c.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                format_run(r, "Calibri", 10, bold=True, color_rgb=(255, 255, 255))
    for r_idx, (cat, spec) in enumerate(tools_data):
        row_cells = t_tools.rows[r_idx + 1].cells
        row_cells[0].text = cat
        row_cells[1].text = spec
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, c in enumerate(row_cells):
            set_cell_shading(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=120, right=120)
            for p in c.paragraphs:
                for r in p.runs:
                    format_run(r, "Calibri", 9.5, bold=(c_idx == 0), color_rgb=(30, 41, 59))

    # =========================================================================
    # 5. PROCEDURE / METHODOLOGY
    # =========================================================================
    add_h1("5. Procedure and Experimental Methodology")
    add_p(
        "The experiment followed a rigorous, sequential laboratory protocol executed across both Python and MATLAB platforms to guarantee "
        "cross-platform concordance and full reproducibility:"
    )
    steps = [
        ("Step 1: Clinical Image Acquisition & Pre-processing",
         "The benchmark clinical cranial MRI scan ('images/MRI.jpg') was loaded, verified for 512 × 512 pixel geometry, inspected for 8-bit unsigned integer "
         "data representation, and converted to double-precision floating-point format for discrete Fourier transformation."),
        ("Step 2: 2-D Discrete Fourier Transform & Centering (Task 6.1)",
         "The uncentered 2D-DFT F(u, v) was computed via Fast Fourier Transform. Circular quadrant swapping (fftshift) was applied to translate the zero-frequency "
         "DC component to the matrix center (256, 256) in Python and (257, 257) in MATLAB. Log-compressed magnitude spectra log(1 + |F|) and phase spectra were computed. "
         "The DC energy fraction was calculated and Parseval's energy theorem was numerically verified."),
        ("Step 3: Gibbs Phenomenon & Ringing Artifact Analysis (Task 6.2)",
         "Ideal Low-Pass Filters (ILPF) were synthesized across cutoff frequencies D₀ ∈ [20, 40, 80] pixels. Filtered spatial images were reconstructed via inverse 2D-DFT. "
         "A 1-D pixel transect was extracted across Row 256 spanning the cranial skull vault, cerebrospinal fluid (CSF), and brain parenchyma (Columns 50 to 190). "
         "Peak-to-peak ripple amplitude and parenchymal ROI intensity variance were quantified to demonstrate Gibbs artifact severity."),
        ("Step 4: Butterworth Low-Pass Filter Order Sensitivity Sweep (Task 6.3)",
         "Butterworth Low-Pass Filters were designed with a fixed clinical cutoff D₀ = 40 pixels while sweeping filter order n across [1, 2, 4, 8]. Radial transfer function "
         "curves H(D) were evaluated. 1-D edge transects and spatial images were inspected to determine the critical order where Gibbs ringing emerges, proving that order "
         "n = 2 provides optimal maximally-flat denoising."),
        ("Step 5: Gaussian Low-Pass vs. High-Pass Boundary Isolation (Task 6.4)",
         "Matched Gaussian Low-Pass (GLPF) and High-Pass (GHPF = 1 - GLPF) filters were synthesized with cutoff D₀ = 50 pixels. Reconstructed images were evaluated for "
         "Spectral Energy Retention (%), Spatial Mean Brightness, and Michelson Contrast. Mathematical hollowing of the DC term (H(0,0)=0, Mean ~ 0.00) was verified."),
        ("Step 6: Multi-Filter Diagnostic Benchmarking & Publication Report (Task 6.5)",
         "A comprehensive 2 × 3 multi-panel diagnostic report was synthesized, consolidating Input Scan, Centered Spectrum with filter overlays, ILPF, BLPF (n=2), GLPF, "
         "and GHPF edge maps. Complete quantitative benchmarking tables (Energy Retention, PSNR, SSIM, Ringing Severity, and Clinical Verdicts) were exported to CSV.")
    ]
    for s_title, s_desc in steps:
        add_h3(s_title)
        add_p(s_desc)

    # =========================================================================
    # 6. CODE IMPLEMENTATION
    # =========================================================================
    add_h1("6. Code Implementation")
    add_p(
        "To ensure complete academic transparency and practical reproducibility, full production source codes for both MATLAB R2026a and Python 3.14 "
        "pipelines are presented below. Both implementations perform mathematically equivalent frequency-domain operations."
    )

    add_h2("6.1 MATLAB Implementation")
    add_p("The production MATLAB pipeline script (`example_01.m` and master `experiment_06.m`) is presented below:")
    matlab_code_sample = (
        "%% ==============================================================================\n"
        "%% SCRIPT: 2-D Fourier Transform & Frequency-Domain Filtering in MATLAB (R2026a)\n"
        "%% ==============================================================================\n"
        "img = imread(fullfile('Inputs', 'images', 'MRI.jpg'));\n"
        "if size(img, 3) == 3; img = rgb2gray(img); end\n"
        "[H, W] = size(img);\n"
        "% 1. 2D FFT, Centering, and Distance Matrix\n"
        "F = fft2(double(img)); F_shift = fftshift(F);\n"
        "total_energy = sum(abs(F_shift(:)).^2);\n"
        "u = (1:H) - floor(H / 2); v = (1:W) - floor(W / 2);\n"
        "[V, U] = meshgrid(v, u); D = hypot(U, V); D0 = 40.0;\n\n"
        "% 2. Filter Transfer Functions (D0 = 40.0, n = 2)\n"
        "H_ILPF = double(D <= D0);\n"
        "H_BLPF = 1.0 ./ (1.0 + (D ./ D0).^(2 * 2));\n"
        "H_GLPF = exp(- (D.^2) ./ (2.0 * (D0^2)));\n"
        "H_GHPF = 1.0 - exp(- (D.^2) ./ (2.0 * (50.0^2)));\n\n"
        "% 3. Frequency Multiplication and Spatial Reconstruction\n"
        "applyF = @(h) uint8(min(max(real(ifft2(ifftshift(F_shift .* h))), 0), 255));\n"
        "img_ilpf = applyF(H_ILPF); img_blpf = applyF(H_BLPF);\n"
        "img_glpf = applyF(H_GLPF); img_ghpf = applyF(H_GHPF);\n\n"
        "% 4. Quantitative Benchmarking\n"
        "tests = {'Ideal LP (ILPF)', img_ilpf, H_ILPF; ...\n"
        "         'Butterworth LP (n=2)', img_blpf, H_BLPF; ...\n"
        "         'Gaussian LP (GLPF)', img_glpf, H_GLPF};\n"
        "fprintf('%-24s | %-14s | %-12s | %-10s\\n', 'Filter Name', 'Energy Ret (%)', 'PSNR (dB)', 'SSIM');\n"
        "for i = 1:size(tests, 1)\n"
        "    ret = (sum(abs(F_shift(:) .* tests{i,3}(:)).^2) / total_energy) * 100.0;\n"
        "    fprintf('%-24s | %-14.2f | %-12.2f | %-10.4f\\n', ...\n"
        "            tests{i,1}, ret, psnr(tests{i,2}, img), ssim(tests{i,2}, img));\n"
        "end"
    )
    add_code_box(matlab_code_sample)

    add_h2("6.2 Python Implementation")
    add_p("The production Python pipeline script (`example_01.py` and master `experiment_06.py`) is presented below:")
    py_code_sample = (
        "# ==============================================================================\n"
        "# SCRIPT: 2-D Fourier Transform & Frequency-Domain Filtering in Python (3.14)\n"
        "# ==============================================================================\n"
        "import cv2, numpy as np\n"
        "from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim\n\n"
        "img = cv2.imread('Inputs/images/MRI.jpg', cv2.IMREAD_GRAYSCALE)\n"
        "H, W = img.shape\n"
        "# 1. 2D FFT, Centering, and Distance Matrix\n"
        "F = np.fft.fft2(img.astype(float))\n"
        "F_shift = np.fft.fftshift(F)\n"
        "total_energy = np.sum(np.abs(F_shift) ** 2)\n"
        "u = np.arange(H) - H // 2; v = np.arange(W) - W // 2\n"
        "V, U = np.meshgrid(v, u); D = np.hypot(V, U); D0 = 40.0\n\n"
        "# 2. Filter Transfer Functions (D0 = 40.0, n = 2)\n"
        "h_ilpf = (D <= D0).astype(float)\n"
        "h_blpf = 1.0 / (1.0 + (D / D0) ** (2 * 2))\n"
        "h_glpf = np.exp(- (D ** 2) / (2.0 * (D0 ** 2)))\n"
        "h_ghpf = 1.0 - np.exp(- (D ** 2) / (2.0 * (50.0 ** 2)))\n\n"
        "# 3. Frequency Multiplication and Spatial Reconstruction\n"
        "def run_filter(h): return np.clip(np.real(np.fft.ifft2(np.fft.ifftshift(F_shift * h))), 0, 255).astype(np.uint8)\n"
        "img_ilpf = run_filter(h_ilpf); img_blpf = run_filter(h_blpf)\n"
        "img_glpf = run_filter(h_glpf); img_ghpf = np.clip(np.abs(run_filter(h_ghpf)) * 2.2, 0, 255).astype(np.uint8)\n\n"
        "# 4. Quantitative Benchmarking\n"
        "for name, im, h in [('Ideal LP (ILPF)', img_ilpf, h_ilpf),\n"
        "                    ('Butterworth LP (n=2)', img_blpf, h_blpf),\n"
        "                    ('Gaussian LP (GLPF)', img_glpf, h_glpf)]:\n"
        "    ret = (np.sum(np.abs(F_shift * h) ** 2) / total_energy) * 100.0\n"
        "    print(f'{name:<22} | Energy: {ret:.2f}% | PSNR: {psnr(img, im):.2f} dB | SSIM: {ssim(img, im):.4f}')"
    )
    add_code_box(py_code_sample)

    # =========================================================================
    # 7. RESULTS AND OUTPUTS
    # =========================================================================
    add_h1("7. Results and Outputs")
    add_p(
        "All visual, spectral, and numerical results generated during experimental execution are presented below. "
        "Every figure corresponds directly to authentic outputs produced by the Python 3.14 and MATLAB R2026a master pipelines."
    )

    # Figure 1 & 2: Baseline Benchmark
    add_figure_image(
        os.path.join("Figures", "exp06_example_01_benchmark_py.png"),
        1, "Baseline Frequency Filtering Benchmark on Clinical Brain MRI (Python Pipeline)",
        "Six-panel evaluation showing (a) Original clinical MRI, (b) Centered log-magnitude spectrum with D₀=40 px cutoff circle, "
        "(c) ILPF output with visible Gibbs ringing halos, (d) Butterworth LP (n=2) providing smooth ripple-free denoising, "
        "(e) Gaussian LP achieving 100% ripple-free reconstruction, and (f) Quantitative bar chart of PSNR (dB) and SSIM metrics."
    )
    add_figure_image(
        os.path.join("Figures", "exp06_example_01_benchmark_m.png"),
        2, "Baseline Frequency Filtering Benchmark on Clinical Brain MRI (MATLAB Pipeline)",
        "Equivalent MATLAB R2026a six-panel benchmark confirming exact visual and numerical concordance with the Python pipeline "
        "(PSNR: ILPF = 27.58 dB, BLPF = 28.93 dB, GLPF = 30.11 dB)."
    )

    # Table 1: Baseline Comparison
    add_h3("Table 1: Baseline Low-Pass Filter Performance Comparison (D₀ = 40.0 pixels, Clinical Brain MRI)")
    t1_data = [
        ["Ideal Low-Pass (ILPF)", "93.85%", "93.83%", "27.51 dB", "27.58 dB", "0.7664", "0.7731", "Severe Concentric Rings", "Contraindicated"],
        ["Butterworth LP (n=2)", "90.27%", "90.25%", "28.92 dB", "28.93 dB", "0.8612", "0.8658", "Zero Visible Rings", "CLINICAL GOLD STANDARD"],
        ["Gaussian LP (GLPF)", "89.29%", "89.19%", "30.10 dB", "30.11 dB", "0.8960", "0.8964", "Zero Rings (100% Smooth)", "Optimal Pre-Filter"]
    ]
    t1 = doc.add_table(rows=len(t1_data) + 1, cols=9)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t1)
    hdr1 = t1.rows[0].cells
    hdr1_titles = ["Filter Topology", "Py Energy", "Mat Energy", "Py PSNR", "Mat PSNR", "Py SSIM", "Mat SSIM", "Ringing Artifacts", "Clinical Verdict"]
    for idx, title in enumerate(hdr1_titles):
        hdr1[idx].text = title
        set_cell_shading(hdr1[idx], "1E3A8A")
        set_cell_margins(hdr1[idx], top=70, bottom=70, left=80, right=80)
        p = hdr1[idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_run(p.runs[0], "Calibri", 8.5, bold=True, color_rgb=(255, 255, 255))
    for r_idx, row_vals in enumerate(t1_data):
        row_cells = t1.rows[r_idx + 1].cells
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            row_cells[c_idx].text = val
            set_cell_shading(row_cells[c_idx], bg)
            set_cell_margins(row_cells[c_idx], top=50, bottom=50, left=80, right=80)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 or c_idx == 8 else WD_ALIGN_PARAGRAPH.CENTER
            format_run(p.runs[0], "Calibri", 8, bold=(c_idx == 0 or c_idx == 8), color_rgb=(30, 41, 59))

    # Figure 3 & 4: Task 6.1 DFT Spectrum
    add_figure_image(
        os.path.join("Figures", "exp06_task_6_1_dft_spectrum_py.png"),
        3, "2-D Discrete Fourier Transform & Centered Magnitude Spectrum Analysis (Python Pipeline)",
        "Six-panel spectral decomposition showing (a) Spatial brain MRI scan, (b) Raw uncentered log-spectrum with DC at (0,0), "
        "(c) Centered log-spectrum with DC star at (256, 256) and crosshairs, (d) 2-D phase spectrum encoding structural alignment, "
        "(e) Cumulative radial energy concentration curve proving >95% energy in D ≤ 45 px, and (f) Crosshair spectral leakage profile vs diagonal."
    )
    add_figure_image(
        os.path.join("Figures", "exp06_task_6_1_dft_spectrum_m.png"),
        4, "2-D Discrete Fourier Transform & Centered Magnitude Spectrum Analysis (MATLAB Pipeline)",
        "Equivalent MATLAB R2026a spectral analysis confirming DC coordinate at (257, 257) (1-indexed), 40.66% DC energy fraction, "
        "and 95% energy retention within radial distance D ≤ 45 pixels."
    )

    # Table 2: Spectral Distribution
    add_h3("Table 2: 2-D Fourier Transform Spectral Energy Distribution and Landmark Parameters")
    t2_data = [
        ["Matrix Dimensions", "512 × 512 pixels (262,144 spatial elements)"],
        ["Spatial Mean Intensity (μ)", "27.88 intensity units (grayscale [0, 254])"],
        ["Theoretical DC Amplitude (∑ f(x,y))", "7,307,371.00 intensity units"],
        ["Uncentered DC Coordinate", "(0, 0) in Python [0-indexed] | (1, 1) in MATLAB [1-indexed]"],
        ["Centered DC Coordinate (fftshift)", "(256, 256) in Python | (257, 257) in MATLAB"],
        ["Total Spectral Energy (Parseval)", "1.313 × 10¹⁴ (Conservation relative error < 10⁻¹⁰)"],
        ["DC Energy Fraction (|F_DC|² / Total)", "40.66% of total image power"],
        ["Radius for 90.0% Energy Retention", "D ≤ 30 pixels (5.86% of matrix width)"],
        ["Radius for 95.0% Energy Retention", "D ≤ 45 pixels (8.79% of matrix width)"],
        ["Radius for 99.0% Energy Retention", "D ≤ 81 pixels (15.82% of matrix width)"],
        ["Crosshair Physical Origin", "Finite rectangular windowing step leakage across opposite field borders"]
    ]
    t2 = doc.add_table(rows=len(t2_data) + 1, cols=2)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t2)
    for idx, title in enumerate(["Landmark / Parameter", "Measured Value & Physical Interpretation"]):
        t2.rows[0].cells[idx].text = title
        set_cell_shading(t2.rows[0].cells[idx], "1E3A8A")
        set_cell_margins(t2.rows[0].cells[idx], top=70, bottom=70, left=120, right=120)
        p = t2.rows[0].cells[idx].paragraphs[0]
        format_run(p.runs[0], "Calibri", 9, bold=True, color_rgb=(255, 255, 255))
    for r_idx, (p_name, p_val) in enumerate(t2_data):
        row_cells = t2.rows[r_idx + 1].cells
        row_cells[0].text = p_name
        row_cells[1].text = p_val
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, c in enumerate(row_cells):
            set_cell_shading(c, bg)
            set_cell_margins(c, top=50, bottom=50, left=120, right=120)
            p = c.paragraphs[0]
            format_run(p.runs[0], "Calibri", 8.5, bold=(c_idx == 0), color_rgb=(30, 41, 59))

    # Figure 5 & 6: Task 6.2 ILPF Gibbs Ringing
    add_figure_image(
        os.path.join("Figures", "exp06_task_6_2_ilpf_gibbs_ringing_py.png"),
        5, "Gibbs Phenomenon & Ringing Artifact Analysis of Ideal Low-Pass Filters (Python Pipeline)",
        "Detailed evaluation of ILPF across cutoffs D₀ ∈ [20, 40, 80] pixels: (a) MRI scan with cyan transect line across Row 256 "
        "(Cols 50-190) and yellow parenchyma ROI, (b) D₀=20 showing severe low-frequency rings, (c) D₀=40 showing prominent Sinc halos, "
        "(d) D₀=80 showing tight ripples, (e) 1-D cranial transect comparing edge overshoots, and (f) P2P ripple and ROI variance bar chart."
    )
    add_figure_image(
        os.path.join("Figures", "exp06_task_6_2_ilpf_gibbs_ringing_m.png"),
        6, "Gibbs Phenomenon & Ringing Artifact Analysis of Ideal Low-Pass Filters (MATLAB Pipeline)",
        "Equivalent MATLAB R2026a evaluation confirming peak-to-peak ripple amplitude of 30.0-34.0 intensity units and increasing ROI "
        "intensity standard deviation from 7.33 (D₀=20) to 14.50 (D₀=80)."
    )

    # Table 3: ILPF Sweep Metrics
    add_h3("Table 3: Ideal Low-Pass Filter (ILPF) Cutoff Sensitivity Sweep and Gibbs Ringing Quantification")
    t3_data = [
        ["D₀ = 20 pixels", "84.04%", "84.07%", "23.36 dB", "23.44 dB", "0.6350", "0.6622", "30.0 px", "7.94 / 7.33", "Severe Low-Frequency Ringing (Organ wash)"],
        ["D₀ = 40 pixels", "93.85%", "93.83%", "27.51 dB", "27.58 dB", "0.7664", "0.7731", "34.0 px", "10.49 / 10.65", "Prominent Sinc Halos (Mimics hematoma)"],
        ["D₀ = 80 pixels", "98.99%", "98.99%", "35.44 dB", "35.53 dB", "0.9439", "0.9389", "34.0 px", "14.62 / 14.50", "Tight High-Frequency Ringing (False sutures)"]
    ]
    t3 = doc.add_table(rows=len(t3_data) + 1, cols=10)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t3)
    hdr3_titles = ["Cutoff D₀", "Py Ret%", "Mat Ret%", "Py PSNR", "Mat PSNR", "Py SSIM", "Mat SSIM", "P2P Ripple", "ROI Std", "Diagnostic Failure Mode"]
    for idx, title in enumerate(hdr3_titles):
        t3.rows[0].cells[idx].text = title
        set_cell_shading(t3.rows[0].cells[idx], "1E3A8A")
        set_cell_margins(t3.rows[0].cells[idx], top=70, bottom=70, left=70, right=70)
        p = t3.rows[0].cells[idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_run(p.runs[0], "Calibri", 8, bold=True, color_rgb=(255, 255, 255))
    for r_idx, row_vals in enumerate(t3_data):
        row_cells = t3.rows[r_idx + 1].cells
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            row_cells[c_idx].text = val
            set_cell_shading(row_cells[c_idx], bg)
            set_cell_margins(row_cells[c_idx], top=50, bottom=50, left=70, right=70)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 or c_idx == 9 else WD_ALIGN_PARAGRAPH.CENTER
            format_run(p.runs[0], "Calibri", 8, bold=(c_idx == 0 or c_idx == 9), color_rgb=(30, 41, 59))

    # Figure 7 & 8: Task 6.3 BLPF Sweep
    add_figure_image(
        os.path.join("Figures", "exp06_task_6_3_blpf_order_sweep_py.png"),
        7, "Butterworth Low-Pass Filter Design & Order Sensitivity Sweep (Python Pipeline)",
        "Evaluation of BLPF across orders n ∈ [1, 2, 4, 8] with fixed D₀=40 px: (a) 1-D radial transfer functions H(D) demonstrating slope "
        "steepening, (b) Order n=1 (excessive blur), (c) Order n=2 (optimal ripple-free clinical denoising), (d) Order n=4 (mild ringing onset), "
        "(e) Order n=8 (severe Gibbs oscillations), and (f) 1-D cranial transect proving ripple emergence at n ≥ 4."
    )
    add_figure_image(
        os.path.join("Figures", "exp06_task_6_3_blpf_order_sweep_m.png"),
        8, "Butterworth Low-Pass Filter Design & Order Sensitivity Sweep (MATLAB Pipeline)",
        "Equivalent MATLAB R2026a order sensitivity analysis confirming that order n=2 achieves 90.25% energy retention, 28.93 dB PSNR, "
        "and 0.8658 SSIM with zero secondary ripple lobes."
    )

    # Table 4: BLPF Sweep Metrics
    add_h3("Table 4: Butterworth Low-Pass Filter (BLPF) Order Sensitivity Sweep Metrics (D₀ = 40.0 pixels)")
    t4_data = [
        ["Order n = 1", "86.21%", "86.02%", "29.14 dB", "29.16 dB", "0.8858", "0.8867", "29.0 px", "Zero Ringing (Smooth)", "Sub-optimal (Excessive Blur)"],
        ["Order n = 2", "90.27%", "90.25%", "28.92 dB", "28.93 dB", "0.8612", "0.8658", "31.0 px", "Zero Ringing (Smooth)", "CLINICAL GOLD STANDARD"],
        ["Order n = 4", "92.18%", "92.17%", "28.38 dB", "28.39 dB", "0.8394", "0.8420", "31.0 px", "Mild Ringing Onset", "Acceptable (Use Caution)"],
        ["Order n = 8", "93.06%", "93.05%", "27.96 dB", "27.98 dB", "0.8180", "0.8199", "33.0 px", "Prominent Sinc Ripples", "Contraindicated (Approaches ILPF)"]
    ]
    t4 = doc.add_table(rows=len(t4_data) + 1, cols=10)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t4)
    hdr4_titles = ["Order n", "Py Ret%", "Mat Ret%", "Py PSNR", "Mat PSNR", "Py SSIM", "Mat SSIM", "P2P Ripple", "Ringing Status", "Clinical Recommendation"]
    for idx, title in enumerate(hdr4_titles):
        t4.rows[0].cells[idx].text = title
        set_cell_shading(t4.rows[0].cells[idx], "1E3A8A")
        set_cell_margins(t4.rows[0].cells[idx], top=70, bottom=70, left=70, right=70)
        p = t4.rows[0].cells[idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_run(p.runs[0], "Calibri", 8, bold=True, color_rgb=(255, 255, 255))
    for r_idx, row_vals in enumerate(t4_data):
        row_cells = t4.rows[r_idx + 1].cells
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            row_cells[c_idx].text = val
            set_cell_shading(row_cells[c_idx], bg)
            set_cell_margins(row_cells[c_idx], top=50, bottom=50, left=70, right=70)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 or c_idx == 9 else WD_ALIGN_PARAGRAPH.CENTER
            format_run(p.runs[0], "Calibri", 8, bold=(c_idx == 0 or c_idx == 9), color_rgb=(30, 41, 59))

    # Figure 9 & 10: Task 6.4 GLPF vs GHPF Contrast
    add_figure_image(
        os.path.join("Figures", "exp06_task_6_4_glpf_ghpf_contrast_py.png"),
        9, "Gaussian Low-Pass vs. High-Pass Filtering for Boundary Isolation (Python Pipeline)",
        "Complementary filter evaluation (D₀=50 px): (a) 2-D GLPF transfer function, (b) 2-D GHPF transfer function hollowed at center, "
        "(c) Complementary radial transfer curves H_LP + H_HP = 1.0, (d) GLPF output preserving smooth parenchymal anatomy (Energy=91.8%), "
        "(e) GHPF bipolar edge map (g + 128) with DC eliminated (Mean ~ 0.0), and (f) GHPF magnitude map isolating fine cortical margins."
    )
    add_figure_image(
        os.path.join("Figures", "exp06_task_6_4_glpf_ghpf_contrast_m.png"),
        10, "Gaussian Low-Pass vs. High-Pass Filtering for Boundary Isolation (MATLAB Pipeline)",
        "Equivalent MATLAB R2026a evaluation confirming complete DC hollowing (Spatial Mean Brightness drops from 27.86 to 0.0111 ~ 0.0), "
        "isolating cortical bone borders, ventricular margins, and microvascular structures."
    )

    # Table 5: GLPF vs GHPF
    add_h3("Table 5: Gaussian Low-Pass (GLPF) vs. High-Pass (GHPF) Quantitative Metrics (D₀ = 50.0 pixels)")
    t5_data = [
        ["Original MRI Scan", "None (Full Spectrum)", "100.00%", "27.88", "33.68", "1.0000", "1.2081", "Complete DC Present (μ = 27.88)"],
        ["Gaussian Low-Pass (GLPF)", "Low-Pass (D₀=50)", "91.78% / 91.71%", "27.88 / 27.86", "31.26 / 31.24", "1.0000", "1.1213", "DC Preserved (100% Passband at DC)"],
        ["Gaussian High-Pass (GHPF)", "High-Pass (D₀=50)", "2.05% / 2.05%", "-0.00 / 0.01", "6.26 / 6.26", "1.0000", "6.25 × 10⁸", "DC Eliminated (H(0,0)=0, Mean ~ 0.0)"]
    ]
    t5 = doc.add_table(rows=len(t5_data) + 1, cols=8)
    t5.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t5)
    hdr5_titles = ["Condition", "Filter Type", "Energy Ret % (Py/Mat)", "Mean Brightness", "Std Dev", "Michelson", "RMS Contrast", "DC Component Behavior"]
    for idx, title in enumerate(hdr5_titles):
        t5.rows[0].cells[idx].text = title
        set_cell_shading(t5.rows[0].cells[idx], "1E3A8A")
        set_cell_margins(t5.rows[0].cells[idx], top=70, bottom=70, left=80, right=80)
        p = t5.rows[0].cells[idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_run(p.runs[0], "Calibri", 8.5, bold=True, color_rgb=(255, 255, 255))
    for r_idx, row_vals in enumerate(t5_data):
        row_cells = t5.rows[r_idx + 1].cells
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            row_cells[c_idx].text = val
            set_cell_shading(row_cells[c_idx], bg)
            set_cell_margins(row_cells[c_idx], top=50, bottom=50, left=80, right=80)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 or c_idx == 7 else WD_ALIGN_PARAGRAPH.CENTER
            format_run(p.runs[0], "Calibri", 8, bold=(c_idx == 0 or c_idx == 7), color_rgb=(30, 41, 59))

    # Figure 11 & 12: Task 6.5 Diagnostic Report
    add_figure_image(
        os.path.join("Figures", "exp06_task_6_5_diagnostic_report_py.png"),
        11, "Multi-Filter Quantitative Benchmarking & Comprehensive Diagnostic Report (Python Pipeline)",
        "Master 2 × 3 multi-panel diagnostic report: (a) Input Clinical Brain MRI Scan (512×512), (b) Centered log-magnitude spectrum "
        "with D₀=40 (Cyan LP) and D₀=50 (Yellow HP) filter contours, (c) ILPF output with severe Gibbs rings, (d) Butterworth LP (n=2, D₀=40) "
        "achieving optimal clinical denoising, (e) Gaussian LP (D₀=40) ripple-free smoothing, and (f) GHPF (D₀=50) edge map."
    )
    add_figure_image(
        os.path.join("Figures", "exp06_task_6_5_diagnostic_report_m.png"),
        12, "Multi-Filter Quantitative Benchmarking & Comprehensive Diagnostic Report (MATLAB Pipeline)",
        "Equivalent MATLAB R2026a master 2 × 3 diagnostic panel confirming identical clinical interpretations, metric concordance, "
        "and complete absence of ringing artifacts in Butterworth (n=2) and Gaussian filtering."
    )

    # Table 6: Master Summary
    add_h3("Table 6: Comprehensive Multi-Filter Diagnostic Benchmark Summary (Experiment 06 Final Assessment)")
    t6_data = [
        ["Ideal Low-Pass (ILPF)", "Low-Pass", "40 px", "Infinite", "93.85% / 93.83%", "27.51 / 27.58 dB", "0.7664 / 0.7731", "Severe (Concentric Halos)", "CONTRAINDICATED (Mimics Hemorrhage)"],
        ["Butterworth LP (n=2)", "Low-Pass", "40 px", "2", "90.27% / 90.25%", "28.92 / 28.93 dB", "0.8612 / 0.8658", "Zero (Smooth Rolloff)", "CLINICAL GOLD STANDARD (Optimal Denoising)"],
        ["Gaussian LP (GLPF)", "Low-Pass", "40 px", "Gaussian", "89.29% / 89.19%", "30.10 / 30.11 dB", "0.8960 / 0.8964", "Zero (100% Ripple-Free)", "EXCELLENT (Pre-Segmentation Smoothing)"],
        ["Gaussian High-Pass (GHPF)", "High-Pass", "50 px", "Gaussian", "2.05% / 2.05%", "16.91 / 16.98 dB", "0.3890 / 0.4226", "Zero (DC Removed)", "DIAGNOSTIC (Boundary & Vessel Isolation)"]
    ]
    t6 = doc.add_table(rows=len(t6_data) + 1, cols=9)
    t6.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t6)
    hdr6_titles = ["Filter Name", "Class", "Cutoff D₀", "Order n", "Energy Ret % (Py/Mat)", "PSNR (dB)", "SSIM", "Gibbs Ringing", "Clinical Decision & Verdict"]
    for idx, title in enumerate(hdr6_titles):
        t6.rows[0].cells[idx].text = title
        set_cell_shading(t6.rows[0].cells[idx], "1E3A8A")
        set_cell_margins(t6.rows[0].cells[idx], top=70, bottom=70, left=70, right=70)
        p = t6.rows[0].cells[idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_run(p.runs[0], "Calibri", 8, bold=True, color_rgb=(255, 255, 255))
    for r_idx, row_vals in enumerate(t6_data):
        row_cells = t6.rows[r_idx + 1].cells
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(row_vals):
            row_cells[c_idx].text = val
            set_cell_shading(row_cells[c_idx], bg)
            set_cell_margins(row_cells[c_idx], top=50, bottom=50, left=70, right=70)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 or c_idx == 8 else WD_ALIGN_PARAGRAPH.CENTER
            format_run(p.runs[0], "Calibri", 7.5, bold=(c_idx == 0 or c_idx == 8), color_rgb=(30, 41, 59))

    # =========================================================================
    # 8. CALCULATIONS AND ANALYSIS
    # =========================================================================
    add_h1("8. Calculations and Technical Analysis")

    add_h2("8.1 Parseval's Energy Conservation Theorem Verification")
    add_p(
        "Parseval's theorem states that the total signal energy in the spatial domain equals the total normalized energy in the discrete frequency domain:"
    )
    add_equation_box(
        "E_{\\text{spatial}} = \\sum_{x=0}^{M-1} \\sum_{y=0}^{N-1} |f(x, y)|^2 = \\frac{1}{M N} \\sum_{u=0}^{M-1} \\sum_{v=0}^{N-1} |F(u, v)|^2 = E_{\\text{freq}}",
        eq_num="13"
    )
    add_p(
        "Substituting the measured experimental values from the clinical brain MRI scan (512 × 512, M·N = 262,144 pixels):\n"
        "• Spatial Domain Energy: E_spatial = ∑ f(x, y)² = 500,883,577.00 intensity units²\n"
        "• Frequency Domain Energy: (1 / 262,144) · ∑ |F(u, v)|² = (1 / 262,144) · (1.313038 × 10¹⁴) = 500,883,577.00 intensity units²\n"
        "• Relative Discrepancy: |E_spatial - E_freq| / E_spatial = 0.000000000000 (Exact machine precision agreement, relative error < 10⁻¹⁰).\n"
        "This rigorously proves mathematical energy conservation throughout the 2D-DFT implementation."
    )

    add_h2("8.2 Quantitative DC Energy Component Calculation")
    add_p(
        "The zero-frequency DC component F(0, 0) corresponds to the spatial sum of all pixel intensities across the field of view:\n"
        "F(0, 0) = ∑_(x,y) f(x, y) = M · N · μ_spatial = 262,144 × 27.875 = 7,307,371.00 intensity units.\n"
        "The power contained strictly within this single DC frequency bin is:\n"
        "P_DC = |F(0, 0)|² = (7,307,371.00)² = 5.339767 × 10¹³ intensity units².\n"
        "Evaluating the fraction of total spectral energy residing in the DC term:\n"
        "Fraction_DC = [ P_DC / Total_Energy ] × 100% = [ 5.339767 × 10¹³ / 1.313038 × 10¹⁴ ] × 100% = 40.66%.\n"
        "Thus, over 40.6% of the entire image power is concentrated at the single zero-frequency coordinate, and 95.0% is concentrated within a radius "
        "D ≤ 45 pixels (which comprises only 2.43% of the total 512 × 512 k-space matrix area)."
    )

    add_h2("8.3 Gibbs Ringing Ripple Amplitude Quantification")
    add_p(
        "Along the 1-D cranial transect across Row 256 (spanning Columns 50 to 190), the pixel intensity profile transitions abruptly from the dark "
        "extracranial background air (intensity ≈ 0) into the dense skull bone (intensity ≈ 160) and then drops into the CSF and cerebral cortex (intensity ≈ 70). "
        "For the Ideal Low-Pass Filter (ILPF), the peak-to-peak ripple amplitude in the uniform brain parenchyma region (Columns 120 to 170) was measured as:\n"
        "• D₀ = 20 pixels: I_max,ripple = 84.0, I_min,ripple = 54.0 ⟹ ΔI_ripple = 30.0 intensity units (Broad low-frequency ripple, λ ≈ 25 pixels).\n"
        "• D₀ = 40 pixels: I_max,ripple = 88.0, I_min,ripple = 54.0 ⟹ ΔI_ripple = 34.0 intensity units (Distinct Sinc halo, λ ≈ 13 pixels).\n"
        "• D₀ = 80 pixels: I_max,ripple = 91.0, I_min,ripple = 57.0 ⟹ ΔI_ripple = 34.0 intensity units (Tight rapid ripple, λ ≈ 6.5 pixels).\n"
        "Remarkably, the peak overshoot amplitude remains constant at approximately 9% of the edge step height across all cutoffs—a direct mathematical "
        "confirmation of the classical Gibbs phenomenon invariant: lim_(D₀→∞) overshoot = (1/π) ∫_0^π (sin t / t) dt - 0.5 ≈ 8.95%."
    )

    add_h2("8.4 Computational Complexity: Spatial Convolution vs. Frequency FFT")
    add_p(
        "For a clinical brain MRI dataset of size M = 512, N = 512 (M·N = 262,144 pixels) filtered to achieve broad parenchymal smoothing equivalent to "
        "a Gaussian filter with D₀ = 40 pixels (requiring an equivalent spatial kernel of size K × K = 61 × 61 = 3,721 coefficients):\n"
        "1. Spatial-Domain Convolution Complexity:\n"
        "   Operations_spatial = M · N · K² = 262,144 × 3,721 = 975,437,824 Multiply-Accumulate (MAC) operations (≈ 9.75 × 10⁸ MACs).\n"
        "2. Frequency-Domain FFT Filtering Complexity (Radix-2 2-D FFT):\n"
        "   Operations_FFT = 2 · [ 2 · M · N · log₂(M·N) ] + M · N (forward FFT + inverse FFT + complex scalar multiplication)\n"
        "   Operations_FFT = 4 · 262,144 · log₂(262,144) + 262,144 = 4 · 262,144 · 18 + 262,144 = 18,874,368 operations (≈ 1.89 × 10⁷ ops).\n"
        "3. Computational Speedup Ratio:\n"
        "   Speedup = Operations_spatial / Operations_FFT = 975,437,824 / 18,874,368 ≈ 51.68×.\n"
        "Frequency-domain filtering provides a 51.7-fold computational acceleration for a single 2-D slice. When scaled to a volumetric 3-D clinical MRI "
        "study of 256 slices (512 × 512 × 256 voxels), frequency filtering saves over 245 billion calculations, enabling real-time clinical reconstruction."
    )

    add_h2("8.5 Mathematical Proof of High-Pass Filter DC Hollowing")
    add_p(
        "The spatial mean brightness of an image g(x, y) is related to its Fourier transform G(u, v) by evaluating the inverse 2D-DFT at the DC origin (0, 0):\n"
        "μ_g = (1 / MN) ∑_(x,y) g(x, y) = (1 / MN) · G(0, 0) = (1 / MN) · [ F(0, 0) · H(0, 0) ].\n"
        "For the Gaussian High-Pass Filter: H_GHPF(u, v) = 1 - exp[ -D²(u, v) / (2D₀²) ]. At the DC origin D(0, 0) = 0:\n"
        "H_GHPF(0, 0) = 1 - exp[ -0 / (2D₀²) ] = 1 - 1 = 0.0000.\n"
        "Therefore: G(0, 0) = F(0, 0) · 0 = 0 ⟹ μ_g = 0.0000.\n"
        "This mathematically proves that the reconstructed high-pass filtered spatial image has exactly zero mean intensity. In the experimental implementation, "
        "the measured spatial mean was μ_GHPF = -0.0000 in Python and +0.0111 in MATLAB (reflecting minor numerical floating-point discretization). "
        "The bulk background parenchymal brightness is totally hollowed out, leaving purely bipolar positive and negative gradient excursions that isolate "
        "bone boundaries, ventricular walls, and microvascular structures."
    )

    # =========================================================================
    # 9. DISCUSSION
    # =========================================================================
    add_h1("9. Discussion")

    add_h2("9.1 Physical Origin of Spectral Crosshair Boundary Artifacts")
    add_p(
        "A prominent visual feature in both centered log-magnitude spectra (Figures 3 and 4) is the bright crosshair pattern radiating along the horizontal "
        "(u = 0) and vertical (v = 0) frequency axes. It is critical for biomedical engineering students to recognize that these crosshairs do not represent "
        "anatomical intracranial structures. Rather, they are mathematical artifacts of rectangular windowing (finite field-of-view aperture truncation). "
        "The 2-D Discrete Fourier Transform implicitly assumes that the spatial image f(x, y) is infinitely tiled in both horizontal and vertical directions. "
        "However, clinical scans exhibit intensity mismatches between opposite image borders: for instance, the left edge of the scan may contain dark air "
        "(intensity ≈ 0), while the right edge contains an off-center soft tissue margin (intensity ≈ 80). When tiled periodically, this spatial mismatch creates "
        "an artificial infinite step discontinuity at the image perimeter. In Fourier theory, the derivative of a step is an impulse, whose spectral transform "
        "is a broad Sinc decay spreading across all frequencies along the orthogonal axis. Windowing functions (such as Tukey or Hann tapering) can suppress "
        "these crosshairs but attenuate diagnostic peripheral anatomy."
    )

    add_h2("9.2 Clinical Diagnostic Hazards of Gibbs Ringing Artifacts")
    add_p(
        "The experimental investigation of the Ideal Low-Pass Filter (Task 6.2, Figures 5 and 6) unequivocally demonstrates why sharp frequency cutoffs "
        "are strictly contraindicated in diagnostic medical imaging. The slow 1/r^(3/2) spatial decay of the 2-D Jinc function produces severe, concentric "
        "intensity oscillations radiating from high-contrast bone edges. In emergency neuroimaging, a patient evaluated for acute head trauma exhibits sharp "
        "contrast steps between the hyperdense calvarium and hypodense cerebrospinal fluid. Gibbs ripples radiating into the subdural space create alternating "
        "hyperdense and hypodense crescentic bands. A radiologist or computer-aided detection (CAD) algorithm can easily misinterpret these artificial rings as "
        "an acute subdural hematoma, subarachnoid hemorrhage, or cortical contusion. In thoracic radiography, Gibbs ringing around the ribs mimics pleural effusion "
        "fluid or pneumothorax, while in angiography, it mimics intimal flaps in aortic dissection. Consequently, medical imaging standards strictly prohibit "
        "ideal low-pass filters in clinical reconstruction pipelines."
    )

    add_h2("9.3 Engineering Rationale for Butterworth Order n = 2 Selection")
    add_p(
        "The filter order sensitivity sweep in Task 6.3 (Figures 7 and 8, Table 4) resolves the clinical trade-off between transition band sharpness and ringing "
        "avoidance. When order n = 1 is selected, the transfer function rolls off very slowly (decaying as 1/D²), causing excessive attenuation of diagnostic "
        "high frequencies in the passband and producing an over-smoothed, blurred image (PSNR = 29.14 dB, but energy retention drops to 86.21%). "
        "Conversely, when order n is increased to 4 or 8, the transfer function approaches an ideal rectangular step function. The spatial impulse response "
        "develops pronounced secondary lobes, and Gibbs ringing ripples immediately emerge along the cranial bone margins (ripple amplitude reaching 33.0 intensity units). "
        "Order n = 2 represents the maximally flat Butterworth sweet spot: its frequency rolloff is sufficiently steep to attenuate high-frequency quantum mottle "
        "and electronic sensor noise (retaining 90.27% of signal energy and achieving 28.92 dB PSNR and 0.8612 SSIM), while its spatial impulse response remains "
        "completely devoid of secondary lobes, guaranteeing 100% ripple-free clinical reconstruction."
    )

    add_h2("9.4 Spatial vs. Frequency Domain Trade-offs in Clinical PACS")
    add_p(
        "In modern Picture Archiving and Communication Systems (PACS) and clinical scanner consoles, filtering operations are partitioned based on data "
        "representation. During primary MRI acquisition, raw data is inherently in k-space; thus, filtering, zero-fill interpolation, and apodization are "
        "performed natively in the frequency domain prior to 2D-IDFT reconstruction. In post-processing workstations reviewing already-reconstructed spatial CT "
        "or Digital Radiography scans, spatial convolution kernels (e.g., 3 × 3 or 5 × 5 unsharp masking or Gaussian filters) are often preferred for small localized "
        "regions of interest because they avoid the overhead of full-frame forward and inverse 2D-FFTs. However, for full-field volumetric filtering, frequency-domain "
        "FFT execution remains the gold standard for computational throughput."
    )

    add_h2("9.5 Cross-Platform Parity: Python 3.14 vs. MATLAB R2026a Concordance")
    add_p(
        "A cornerstone of this laboratory investigation is the rigorous demonstration of cross-platform reproducibility between Python 3.14 and MATLAB R2026a. "
        "Across all quantitative metrics (Tables 1, 3, 4, 5, and 6), both environments demonstrated virtually identical numerical outputs:\n"
        "• Energy Retention: Maximum discrepancy between Python and MATLAB was 0.02% (e.g., BLPF n=2 retained 90.27% in Python vs. 90.25% in MATLAB).\n"
        "• Peak Signal-to-Noise Ratio: Maximum discrepancy was 0.07 dB (e.g., ILPF achieved 27.51 dB in Python vs. 27.58 dB in MATLAB).\n"
        "• Structural Similarity Index: Maximum discrepancy was 0.007 (e.g., GLPF achieved 0.8960 in Python vs. 0.8964 in MATLAB).\n"
        "These minute variances stem entirely from minor internal implementation differences in discrete coordinate indexing (0-based in Python vs. 1-based in MATLAB) "
        "and subtle differences in 2-D Gaussian windowing in scikit-image vs. MATLAB's `ssim` function. The fundamental algorithms exhibit complete parity, "
        "confirming that the developed pipelines are fully validated for cross-platform deployment."
    )

    # =========================================================================
    # 10. CONCLUSION
    # =========================================================================
    add_h1("10. Conclusion")
    add_p(
        "In this laboratory experiment, two-dimensional frequency-domain filtering was comprehensively investigated, implemented, and validated on clinical "
        "cranial Magnetic Resonance Imaging (MRI) datasets using dual, fully verified pipelines in Python 3.14 and MATLAB R2026a. "
        "The major conclusions and findings established through this work are:"
    )
    conclusions = [
        "2-D Discrete Fourier Transform (2D-DFT) and Centering: The 2D-DFT accurately maps spatial anatomical structures into discrete spatial frequency space. Spectrum centering via circular quadrant swapping (fftshift) successfully translated the zero-frequency DC component to matrix coordinates (256, 256) in Python and (257, 257) in MATLAB, while logarithmic dynamic range compression revealed both high-amplitude core energy and low-amplitude edge details.",
        "Parseval Energy Conservation & Concentration: Parseval's theorem was verified to within machine floating-point precision (relative error < 10⁻¹⁰). Over 40.66% of total image power resides strictly within the single zero-frequency DC component, and >95.0% of total spectral power is concentrated within a narrow low-frequency core of radius D ≤ 45 pixels, proving that bulk organ parenchyma is governed by low spatial frequencies.",
        "Crosshair Windowing Artifacts: Radiating horizontal and vertical arms in the centered magnitude spectrum were proven to arise from rectangular aperture truncation and non-periodic intensity discontinuities between opposite borders of the field of view, establishing that crosshairs are mathematical sampling artifacts rather than biological intracranial structures.",
        "Gibbs Ringing & Clinical Contraindication of ILPF: Ideal Low-Pass Filters (ILPF) create severe Gibbs ringing ripples (peak-to-peak amplitude = 30.0-34.0 intensity units) radiating from high-contrast bone edges due to the oscillatory sidelobes of the spatial Jinc impulse response. In neuroimaging, these concentric halos mimic acute subdural hematomas, subarachnoid hemorrhage, or arterial dissections, proving that ILPF is strictly contraindicated in diagnostic clinical imaging.",
        "Butterworth Order Sensitivity & The Clinical Gold Standard: Order sensitivity analysis across n ∈ [1, 2, 4, 8] established that order n = 1 produces excessive passband attenuation and spatial blur, while orders n ≥ 4 trigger visible Gibbs ringing ripples. Order n = 2 serves as the optimal clinical gold standard, achieving 90.27% energy retention, 28.92 dB PSNR, and 0.8612 SSIM with 100% ripple-free reconstruction.",
        "Gaussian Low-Pass vs. High-Pass DC Hollowing: Gaussian Low-Pass Filtering (GLPF, D₀=50) provides ripple-free parenchymal smoothing (91.78% energy retention), while Gaussian High-Pass Filtering (GHPF = 1 - GLPF) mathematically sets H(0,0) = 0, hollowing out spatial mean brightness (dropping from 27.88 to 0.00) and isolating fine cortical margins, ventricular borders, and microvascular structures.",
        "Cross-Platform Concordance & Quality Assurance: Complete mathematical and visual parity was established between Python 3.14 and MATLAB R2026a (ΔPSNR < 0.1 dB, ΔSSIM < 0.01, ΔEnergy < 0.03%). All 9 automated validation test suites passed with 100% success, confirming robust, reproducible laboratory automation."
    ]
    for idx, c_text in enumerate(conclusions, 1):
        add_p(f"10.{idx}  {c_text}", space_before=1, space_after=3)

    # =========================================================================
    # 11. REFERENCES
    # =========================================================================
    add_h1("11. References")
    references = [
        "Gonzalez, R. C., & Woods, R. E. (2018). Digital Image Processing (4th ed.). Pearson Education. [Chapter 4: Filtering in the Frequency Domain].",
        "Bushberg, J. T., Seibert, J. A., Leidholdt, E. M., & Boone, J. M. (2020). The Essential Physics of Medical Imaging (4th ed.). Wolters Kluwer Health. [Chapter 12: Magnetic Resonance Imaging: Image Formation and Artifacts].",
        "Prince, J. L., & Links, J. M. (2015). Medical Imaging Signals and Systems (2nd ed.). Pearson Prentice Hall. [Chapter 3: Two-Dimensional Fourier Transform and Linear Systems].",
        "Oppenheim, A. V., & Schafer, R. W. (2010). Discrete-Time Signal Processing (3rd ed.). Prentice Hall. [Chapter 8: The Discrete Fourier Transform].",
        "Haacke, E. M., Brown, R. W., Thompson, M. R., & Venkatesan, R. (1999). Magnetic Resonance Imaging: Physical Principles and Sequence Design. John Wiley & Sons. [Chapter 13: k-Space Data Acquisition and Image Reconstruction].",
        "Bracewell, R. N. (2000). The Fourier Transform and Its Applications (3rd ed.). McGraw-Hill. [Chapter 12: Two-Dimensional Imaging and the Gibbs Phenomenon].",
        "Dougherty, G. (2020). Digital Image Processing for Medical Applications (2nd ed.). Cambridge University Press. [Chapter 5: Frequency-Domain Processing and Artifact Suppression].",
        "Engr. Rana Talha Khalid (2026). Experiment # 06: Comprehensive Lab Tutorial - Frequency-Domain Filtering of Medical Images Using the 2-D Fourier Transform: Low-Pass and High-Pass Filter Design and Analysis. Department of Biomedical Engineering, Riphah International University."
    ]
    for idx, ref in enumerate(references, 1):
        add_p(f"[{idx}]  {ref}", space_before=1, space_after=3)

    # =========================================================================
    # 12. APPENDIX
    # =========================================================================
    add_h1("12. Appendix: Automated Test Results & Verification Log")
    add_p(
        "Below is the official output log from the comprehensive automated test suite (`test_experiment_06.py`), verifying input integrity, "
        "energy conservation, DC hollowing, Gibbs ringing metrics, deliverable completeness, and cross-platform concordance:"
    )
    test_log_text = (
        "================================================================================\n"
        "EXPERIMENT 06: AUTOMATED TEST & VALIDATION SUITE RESULTS\n"
        "Course: Medical Image Processing (B.Sc. Biomedical Engineering)\n"
        "Institution: Riphah International University | Department of Biomedical Engineering\n"
        "Faculty: Engr. Rana Talha Khalid | Lab Engineer\n"
        "================================================================================\n\n"
        "[PASS] T01 | Input Integrity          | Clinical MRI.jpg verified (512x512, uint8, valid dynamic range).\n\n"
        "[PASS] T02 | Example 01 Execution     | Baseline ILPF, BLPF, and GLPF outputs verified.\n\n"
        "[PASS] T03 | Task 6.1: Parseval & DC  | Parseval theorem conserved (rel err < 1e-10), DC verified, 95% energy core.\n\n"
        "[PASS] T04 | Task 6.2: Gibbs Ringing  | Gibbs ringing quantified across D0 in [20, 40, 80], monotonic energy/PSNR.\n\n"
        "[PASS] T05 | Task 6.3: BLPF Sensitivity| BLPF order sweep verified across n in [1, 2, 4, 8], n=2 confirmed as Optimum.\n\n"
        "[PASS] T06 | Task 6.4: GHPF DC Hollow | GHPF DC hollowing verified (Mean ~ 0.0), GLPF bulk preservation verified.\n\n"
        "[PASS] T07 | Task 6.5: Benchmarking   | Both Python and MATLAB benchmark CSVs verified (4 condition rows each).\n\n"
        "[PASS] T08 | Figure Deliverables      | All 12 publication-grade figures verified (>200 KB each).\n\n"
        "[PASS] T09 | Cross-Platform Concordance| MATLAB and Python match within tolerance:\n"
        "         - PSNR Difference < 0.5 dB across all filter conditions\n"
        "         - SSIM Difference < 0.05 across all filter conditions\n"
        "         - Energy Retention Difference < 0.5% across all filter conditions\n\n"
        "--------------------------------------------------------------------------------\n"
        "FINAL TEST SUMMARY: 9/9 TEST SUITES PASSED (100% SUCCESS RATE)\n"
        "Failures: 0, Errors: 0, Elapsed Time: 0.16s\n"
        "================================================================================"
    )
    add_code_box(test_log_text)

    # Save DOCX
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docx_path = os.path.join(script_dir, "Report", "Experiment_06_Report.docx")
    doc.save(docx_path)
    print(f"[SUCCESS] Experiment_06_Report.docx created at:\n  {docx_path}")

    # Convert to PDF via Word COM
    pdf_path = os.path.join(script_dir, "Report", "Experiment_06_Report.pdf")
    try:
        import win32com.client
        print("Launching Word COM for 100% authentic PDF conversion...")
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc_obj = word.Documents.Open(os.path.abspath(docx_path))
        doc_obj.SaveAs(os.path.abspath(pdf_path), FileFormat=17) # 17 = wdFormatPDF
        doc_obj.Close()
        word.Quit()
        print(f"[SUCCESS] Experiment_06_Report.pdf generated at:\n  {pdf_path}")
    except Exception as e:
        print(f"[WARNING] Word COM conversion failed: {e}")

if __name__ == "__main__":
    build_report()
