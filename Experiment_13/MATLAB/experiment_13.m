%% Master Script for Experiment 13:
%% Texture Feature Extraction from Medical Images Using the Gray-Level Co-occurrence Matrix (GLCM)
% Author: Muhammad Ikrama (Reg ID: 60140)
% Department of Biomedical Engineering, Riphah International University, Lahore
% Instructor: Engr. Rana Talha Khalid
% Course: Medical Image Processing (BMI-701)

function experiment_13()
    fprintf('********************************************************************************\n');
    fprintf('   RIPHAH INTERNATIONAL UNIVERSITY - FACULTY OF ENGINEERING & APPLIED SCIENCES\n');
    fprintf('   DEPARTMENT OF BIOMEDICAL ENGINEERING - MEDICAL IMAGE PROCESSING LAB (BMI-701)\n');
    fprintf('   EXPERIMENT 13: TEXTURE FEATURE EXTRACTION FROM MEDICAL IMAGES USING GLCM\n');
    fprintf('   Student: Muhammad Ikrama (Reg ID: 60140) | Instructor: Engr. Rana Talha Khalid\n');
    fprintf('********************************************************************************\n\n');

    t0 = tic;

    % 1. Clinical Benchmark (Section 5)
    fprintf('>>> Running Section 5 Clinical Benchmark Extraction in MATLAB...\n');
    mri = imread(fullfile('..', 'Inputs', 'images', 'Brain_MRI.png'));
    if size(mri, 3) == 3; mri = rgb2gray(mri); end
    
    roiNormal = mri(176:223, 156:203);
    roiCortex = mri(121:168, 121:168);
    
    rng(113);
    grid_n = imresize(randn(16, 16) * 38, [48 48], 'nearest');
    roiTumor = uint8(min(max(double(mri(220:267, 302:349)) + grid_n, 0), 255));
    
    offsets = [0 1; -1 1; -1 0; -1 -1];
    rois = {'Normal White Matter ROI', roiNormal; 
            'Cortical Folding ROI',     roiCortex; 
            'Heterogeneous Tumor ROI', roiTumor};
            
    fprintf('%-25s | %-9s | %-9s | %-8s | %-8s | %-7s\n', 'Clinical Tissue ROI', 'Contrast', 'Homogen.', 'Energy', 'Entropy', 'Correl.');
    fprintf('-------------------------------------------------------------------------------\n');
    
    for k = 1:size(rois, 1)
        patch = rois{k, 2};
        glcms = graycomatrix(patch, 'NumLevels', 16, 'GrayLimits', [0 255], 'Offset', offsets, 'Symmetric', true);
        stats = graycoprops(glcms, {'Contrast', 'Homogeneity', 'Energy', 'Correlation'});
        
        entVals = zeros(1, 4);
        for d = 1:4
            P = double(glcms(:, :, d)) / sum(glcms(:, :, d), 'all');
            nz = P > 0;
            entVals(d) = -sum(P(nz) .* log2(P(nz)));
        end
        
        fprintf('%-25s | %-9.3f | %-9.3f | %-8.4f | %-8.3f | %-7.3f\n', rois{k, 1}, ...
            mean(stats.Contrast), mean(stats.Homogeneity), mean(stats.Energy), mean(entVals), mean(stats.Correlation));
    end
    fprintf('>>> Status: Haralick second-order statistics differentiate pathological heterogeneity.\n\n');

    % 2. Task 13.1
    fprintf('>>> Running Task 13.1: Hand-Verified 4x4 GLCM Construction...\n');
    task_13_1_synthetic_glcm();
    fprintf('\n');

    % 3. Task 13.2
    fprintf('>>> Running Task 13.2: Distance Sensitivity Sweep...\n');
    task_13_2_distance_sweep();
    fprintf('\n');

    % 4. Task 13.3
    fprintf('>>> Running Task 13.3: Directional Anisotropy Analysis...\n');
    task_13_3_directional_anisotropy();
    fprintf('\n');

    % 5. Task 13.4
    fprintf('>>> Running Task 13.4: Gray-Level Quantization Trade-Off...\n');
    task_13_4_quantization_tradeoff();
    fprintf('\n');

    % 6. Task 13.5
    fprintf('>>> Running Task 13.5: Sliding-Window Texture Feature Maps...\n');
    task_13_5_texture_maps();
    fprintf('\n');

    totalTime = toc(t0);
    fprintf('================================================================================\n');
    fprintf('EXPERIMENT 13 MATLAB RUN COMPLETE in %.2f seconds.\n', totalTime);
    fprintf('================================================================================\n');
end
