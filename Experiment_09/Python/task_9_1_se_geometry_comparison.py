"""
Experiment 09 - Task 9.1: Structuring Element Geometry Comparison (Square vs. Cross vs. Disk)
Evaluates morphological boundary distortion on curved cranial calvarium in Head CT.
"""
import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run_task_9_1():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(base_dir, "Inputs", "images", "Head_CT.png")
    out_dir = os.path.join(base_dir, "Outputs", "Python")
    tab_dir = os.path.join(base_dir, "Tables")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(tab_dir, exist_ok=True)

    ct = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if ct is None:
        raise FileNotFoundError(f"Head CT not found at {img_path}")
    if ct.shape != (512, 512):
        ct = cv2.resize(ct, (512, 512))

    # Binary cortical calvarium mask via Otsu thresholding (T=118)
    _, skull_raw = cv2.threshold(ct, 118, 255, cv2.THRESH_BINARY)

    # 1. Define 7x7 Structuring Elements
    se_square = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    se_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (7, 7))
    se_disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

    elements = [
        ("Square (8-connected Box)", se_square, "Square"),
        ("Cross (4-connected Diamond)", se_cross, "Cross"),
        ("Disk (Isotropic Ellipse)", se_disk, "Disk")
    ]

    records = []
    results = {}

    print("=" * 80)
    print("TASK 9.1: STRUCTURING ELEMENT GEOMETRY COMPARISON (7x7)")
    print("=" * 80)
    print(f"{'SE Geometry':<28} | {'Active Px':<9} | {'Opened Area':<11} | {'Closed Area':<11} | {'Perimeter Px'}")
    print("-" * 80)

    for name, se, tag in elements:
        opened = cv2.morphologyEx(skull_raw, cv2.MORPH_OPEN, se)
        closed = cv2.morphologyEx(skull_raw, cv2.MORPH_CLOSE, se)
        results[tag] = (opened, closed, se)

        # Boundary perimeter
        grad = cv2.morphologyEx(opened, cv2.MORPH_GRADIENT, se)
        perim_px = int((grad > 0).sum())

        active_px = int(se.sum())
        op_area = int((opened > 0).sum())
        cl_area = int((closed > 0).sum())

        records.append({
            "SE_Geometry": name,
            "SE_Shape": tag,
            "Active_Pixels_KxK": active_px,
            "Opened_Area_Px": op_area,
            "Closed_Area_Px": cl_area,
            "Boundary_Perimeter_Px": perim_px
        })
        print(f"{name:<28} | {active_px:<9d} | {op_area:<11d} | {cl_area:<11d} | {perim_px}")

    df = pd.DataFrame(records)
    csv_path = os.path.join(tab_dir, "exp09_task_9_1_se_geometry.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n[SAVED] Task 9.1 metrics to: {csv_path}")

    # Visual Comparison with 80x80 curved cranial boundary zoom
    r_crop = slice(70, 150)
    c_crop = slice(360, 440)

    fig = plt.figure(figsize=(15, 8))
    fig.patch.set_facecolor("#FFFFFF")

    # Row 1: Full Opened Skull Masks
    ax1 = fig.add_subplot(2, 4, 1)
    ax1.imshow(skull_raw, cmap="gray")
    ax1.set_title("Input Raw Skull Mask", fontsize=10, fontweight="bold", pad=5)
    ax1.axis("off")

    for i, (_, _, tag) in enumerate(elements):
        ax = fig.add_subplot(2, 4, i + 2)
        opened, _, _ = results[tag]
        ax.imshow(opened, cmap="gray")
        ax.set_title(f"Opened with {tag} SE (7x7)", fontsize=10, fontweight="bold", pad=5)
        ax.axis("off")

    # Row 2: 80x80 High-Magnification Boundary Zooms
    ax_z1 = fig.add_subplot(2, 4, 5)
    ax_z1.imshow(skull_raw[r_crop, c_crop], cmap="gray")
    ax_z1.set_title("Raw Boundary (80x80 Crop)\nPixelated Edge", fontsize=9.5, fontweight="bold", pad=5)
    ax_z1.axis("off")

    zoom_titles = [
        "Square SE (7x7)\nSevere Blocky Stair-Stepping",
        "Cross SE (7x7)\nDiamond Point Artifacts",
        "Disk SE (7x7)\nSmooth Biological Curvature"
    ]

    for i, ((_, _, tag), z_title) in enumerate(zip(elements, zoom_titles)):
        ax = fig.add_subplot(2, 4, i + 6)
        opened, _, _ = results[tag]
        crop = opened[r_crop, c_crop]
        ax.imshow(crop, cmap="gray")
        color = "#16A34A" if tag == "Disk" else "#DC2626"
        ax.set_title(z_title, fontsize=9.5, fontweight="bold", color=color, pad=5)
        ax.axis("off")

    plt.suptitle("Task 9.1: Structuring Element Geometry Comparison on Cranial Calvarium", fontsize=13, fontweight="bold", y=0.99)
    plt.tight_layout()
    fig_path = os.path.join(out_dir, "exp09_task_9_1_se_geometry.png")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[SAVED] Task 9.1 figure to: {fig_path}")

    return df

if __name__ == "__main__":
    run_task_9_1()
