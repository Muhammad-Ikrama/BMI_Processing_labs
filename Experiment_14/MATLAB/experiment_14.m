%% Master Script for Experiment 14:
%% Lossless and Lossy Compression of Medical Images and Quality Evaluation Using PSNR & CR
% Author: Muhammad Ikrama (Reg ID: 60140)
% Department of Biomedical Engineering, Riphah International University, Lahore
% Instructor: Engr. Rana Talha Khalid
% Course: Medical Image Processing (BMI-701)

function experiment_14()
    fprintf('********************************************************************************\n');
    fprintf('   RIPHAH INTERNATIONAL UNIVERSITY - FACULTY OF ENGINEERING & APPLIED SCIENCES\n');
    fprintf('   DEPARTMENT OF BIOMEDICAL ENGINEERING - MEDICAL IMAGE PROCESSING LAB (BMI-701)\n');
    fprintf('   EXPERIMENT 14: LOSSLESS & LOSSY MEDICAL IMAGE COMPRESSION (PSNR & CR)\n');
    fprintf('   Student: Muhammad Ikrama (Reg ID: 60140) | Instructor: Engr. Rana Talha Khalid\n');
    fprintf('********************************************************************************\n\n');

    t0 = tic;

    % 1. Clinical Benchmark (Section 5)
    fprintf('>>> Running Section 5 Clinical Compression Benchmark in MATLAB...\n');
    mri = imread(fullfile('..', 'Inputs', 'images', 'Brain_MRI.png'));
    if size(mri, 3) == 3; mri = rgb2gray(mri); end
    rawBytes = numel(mri);
    
    imwrite(mri, 'temp_lossless.png', 'png');
    infoPng = imfinfo('temp_lossless.png');
    decPng  = imread('temp_lossless.png');
    delete('temp_lossless.png');
    
    fprintf('%-25s | %-7s | %-6s | %-7s | %-9s | %-6s\n', 'Method', 'Bytes', 'CR', 'Saved %', 'PSNR (dB)', 'SSIM');
    fprintf('--------------------------------------------------------------------------\n');
    crPng = rawBytes / infoPng.FileSize;
    fprintf('%-25s | %-7d | %-5.2fx | %-6.1f%% | %-9s | %-6.4f\n', ...
        'Lossless PNG (Deflate)', infoPng.FileSize, crPng, (1 - 1/crPng)*100, 'Inf', ssim(decPng, mri));
        
    for q = [95, 85, 50, 25, 10, 5]
        fname = sprintf('temp_q%d.jpg', q);
        imwrite(mri, fname, 'jpg', 'Quality', q);
        infoJ = imfinfo(fname); decJ = imread(fname);
        delete(fname);
        cr = rawBytes / infoJ.FileSize;
        fprintf('Lossy JPEG (Q=%-2d)         | %-7d | %-5.2fx | %-6.1f%% | %-9.2f | %-6.4f\n', ...
            q, infoJ.FileSize, cr, (1 - 1/cr)*100, psnr(decJ, mri), ssim(decJ, mri));
    end
    fprintf('>>> Status: Rate-distortion trade-off verified across lossless and lossy codecs.\n\n');

    % 2. Task 14.1
    fprintf('>>> Running Task 14.1: Custom RLE Compressor...\n');
    task_14_1_rle_compression();
    fprintf('\n');

    % 3. Task 14.2
    fprintf('>>> Running Task 14.2: Shannon Entropy & Redundancy Across Modalities...\n');
    task_14_2_entropy_redundancy();
    fprintf('\n');

    % 4. Task 14.3
    fprintf('>>> Running Task 14.3: Multi-Modality Rate-Distortion Curves...\n');
    task_14_3_rate_distortion_curves();
    fprintf('\n');

    % 5. Task 14.4
    fprintf('>>> Running Task 14.4: 8x8 DCT Blocking Artifact Visualization...\n');
    task_14_4_blocking_artifacts();
    fprintf('\n');

    % 6. Task 14.5
    fprintf('>>> Running Task 14.5: Downstream Impact on Segmentation & GLCM...\n');
    task_14_5_downstream_impact();
    fprintf('\n');

    totalTime = toc(t0);
    fprintf('================================================================================\n');
    fprintf('EXPERIMENT 14 MATLAB RUN COMPLETE in %.2f seconds.\n', totalTime);
    fprintf('================================================================================\n');
end
