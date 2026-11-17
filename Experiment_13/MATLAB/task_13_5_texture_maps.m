%% Task 13.5: Sliding-Window Local Texture Feature Map Generation
% Experiment 13: Texture Feature Extraction from Medical Images Using GLCM
% Author: Muhammad Ikrama (Reg ID: 60140)

function [contrastMap, entropyMap] = task_13_5_texture_maps()
    fprintf('================================================================================\n');
    fprintf('TASK 13.5: SLIDING-WINDOW LOCAL TEXTURE FEATURE MAP GENERATION (MATLAB)\n');
    fprintf('================================================================================\n');
    
    mri = imread(fullfile('..', 'Inputs', 'images', 'Brain_MRI.png'));
    if size(mri, 3) == 3; mri = rgb2gray(mri); end
    
    rng(113);
    grid_n = imresize(randn(16, 16) * 38, [48 48], 'nearest');
    mri(220:267, 302:349) = uint8(min(max(double(mri(220:267, 302:349)) + grid_n, 0), 255));
    
    tic;
    winSize = 16;
    stride = 8;
    [H, W] = size(mri);
    rows = 1:stride:(H - winSize + 1);
    cols = 1:stride:(W - winSize + 1);
    
    contrastMap = zeros(length(rows), length(cols));
    entropyMap = zeros(length(rows), length(cols));
    
    levels = 16;
    qImg = floor(double(mri) * levels / 256);
    qImg(qImg >= levels) = levels - 1;
    
    offsets = [0 1; -1 1; -1 0; -1 -1];
    [Igrid, Jgrid] = meshgrid(0:levels-1, 0:levels-1);
    diffSq = (Igrid - Jgrid).^2;
    
    for rIdx = 1:length(rows)
        r = rows(rIdx);
        for cIdx = 1:length(cols)
            c = cols(cIdx);
            patch = qImg(r:r+winSize-1, c:c+winSize-1);
            
            % Compute 4-directional GLCM
            glcm = graycomatrix(patch, 'NumLevels', levels, 'GrayLimits', [0 levels-1], 'Offset', offsets, 'Symmetric', true);
            glcmSum = sum(glcm, 3);
            tot = sum(glcmSum, 'all');
            if tot > 0
                P = double(glcmSum) / tot;
                contrastMap(rIdx, cIdx) = sum(P .* diffSq, 'all');
                nz = P > 0;
                entropyMap(rIdx, cIdx) = -sum(P(nz) .* log2(P(nz)));
            end
        end
    end
    elapsed = toc;
    
    fprintf('Generated 2D Texture Maps (%dx%d grid) in %.2f seconds.\n', length(rows), length(cols), elapsed);
    fprintf('  Contrast Map: min = %.3f, max = %.3f, mean = %.3f\n', min(contrastMap(:)), max(contrastMap(:)), mean(contrastMap(:)));
    fprintf('  Entropy Map:  min = %.3f, max = %.3f, mean = %.3f\n', min(entropyMap(:)), max(entropyMap(:)), mean(entropyMap(:)));
    fprintf('>>> Task 13.5 Complete.\n');
end
