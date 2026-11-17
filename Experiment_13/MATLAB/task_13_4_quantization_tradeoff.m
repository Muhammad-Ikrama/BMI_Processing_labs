%% Task 13.4: Gray-Level Quantization (Ng) Trade-off Evaluation
% Experiment 13: Texture Feature Extraction from Medical Images Using GLCM
% Author: Muhammad Ikrama (Reg ID: 60140)

function results = task_13_4_quantization_tradeoff()
    fprintf('================================================================================\n');
    fprintf('TASK 13.4: GRAY-LEVEL QUANTIZATION (Ng) TRADE-OFF EVALUATION (MATLAB)\n');
    fprintf('================================================================================\n');
    
    mri = imread(fullfile('..', 'Inputs', 'images', 'Brain_MRI.png'));
    if size(mri, 3) == 3; mri = rgb2gray(mri); end
    
    roiNormal = mri(176:223, 156:203);
    rng(113);
    grid_n = imresize(randn(16, 16) * 38, [48 48], 'nearest');
    roiTumor = uint8(min(max(double(mri(220:267, 302:349)) + grid_n, 0), 255));
    
    levelsList = [8, 16, 32, 64, 256];
    offsets = [0 1; -1 1; -1 0; -1 -1];
    
    fprintf('%-10s | %-12s | %-10s | %-13s | %-9s | %-9s | %-7s\n', 'Ng Levels', 'Matrix Size', 'Time (ms)', 'Sparsity (%)', 'C_Norm', 'C_Tumor', 'Ratio');
    fprintf('--------------------------------------------------------------------------------\n');
    
    for idx = 1:length(levelsList)
        ng = levelsList(idx);
        
        tic;
        for rep = 1:30
            glcmN = graycomatrix(roiNormal, 'NumLevels', ng, 'GrayLimits', [0 255], 'Offset', offsets, 'Symmetric', true);
        end
        timeMs = (toc / 30) * 1000;
        
        glcmT = graycomatrix(roiTumor, 'NumLevels', ng, 'GrayLimits', [0 255], 'Offset', offsets, 'Symmetric', true);
        
        sN = graycoprops(glcmN, 'Contrast');
        sT = graycoprops(glcmT, 'Contrast');
        
        cn = mean(sN.Contrast);
        ct = mean(sT.Contrast);
        ratio = ct / cn;
        
        sparsity = (sum(glcmN == 0, 'all') / numel(glcmN)) * 100;
        
        fprintf('%-10d | %-12s | %-10.3f | %-13.1f | %-9.3f | %-9.3f | %.2fx\n', ng, sprintf('%dx%d', ng, ng), timeMs, sparsity, cn, ct, ratio);
    end
    fprintf('>>> Task 13.4 Trade-Off Evaluation Complete.\n');
end
