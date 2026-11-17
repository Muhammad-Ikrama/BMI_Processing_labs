%% Task 13.2: Inter-Pixel Distance (d) Sensitivity Sweep on Brain MRI
% Experiment 13: Texture Feature Extraction from Medical Images Using GLCM
% Author: Muhammad Ikrama (Reg ID: 60140)

function results = task_13_2_distance_sweep()
    fprintf('================================================================================\n');
    fprintf('TASK 13.2: INTER-PIXEL DISTANCE (d) SENSITIVITY SWEEP (MATLAB)\n');
    fprintf('================================================================================\n');
    
    mri = imread(fullfile('..', 'Inputs', 'images', 'Brain_MRI.png'));
    if size(mri, 3) == 3; mri = rgb2gray(mri); end
    
    roiNormal = mri(176:223, 156:203);
    
    % Replicate simulated tumor micro-texture
    rng(113);
    grid_n = imresize(randn(16, 16) * 38, [48 48], 'nearest');
    roiTumor = uint8(min(max(double(mri(220:267, 302:349)) + grid_n, 0), 255));
    
    distances = [1, 2, 4, 8, 12];
    fprintf('%-6s | %-10s | %-9s | %-9s | %-8s | %-7s\n', 'd (px)', 'ROI Type', 'Contrast', 'Homogen.', 'Energy', 'Correl.');
    fprintf('-------------------------------------------------------------------\n');
    
    results = struct();
    for idx = 1:length(distances)
        d = distances(idx);
        offsets = [0 d; -d d; -d 0; -d -d];
        
        glcmNorm = graycomatrix(roiNormal, 'NumLevels', 16, 'GrayLimits', [0 255], 'Offset', offsets, 'Symmetric', true);
        glcmTumor = graycomatrix(roiTumor, 'NumLevels', 16, 'GrayLimits', [0 255], 'Offset', offsets, 'Symmetric', true);
        
        sNorm = graycoprops(glcmNorm, {'Contrast', 'Homogeneity', 'Energy', 'Correlation'});
        sTumor = graycoprops(glcmTumor, {'Contrast', 'Homogeneity', 'Energy', 'Correlation'});
        
        cn = mean(sNorm.Contrast); hn = mean(sNorm.Homogeneity); en = mean(sNorm.Energy); rn = mean(sNorm.Correlation);
        ct = mean(sTumor.Contrast); ht = mean(sTumor.Homogeneity); et = mean(sTumor.Energy); rt = mean(sTumor.Correlation);
        
        fprintf('%-6d | %-10s | %-9.3f | %-9.3f | %-8.4f | %-7.3f\n', d, 'Normal', cn, hn, en, rn);
        fprintf('%-6d | %-10s | %-9.3f | %-9.3f | %-8.4f | %-7.3f\n', d, 'Tumor', ct, ht, et, rt);
    end
    fprintf('>>> Task 13.2 Sweep Complete.\n');
end
