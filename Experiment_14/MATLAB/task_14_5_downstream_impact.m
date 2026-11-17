%% Task 14.5: Impact of Lossy Compression on Downstream Segmentation & GLCM
% Experiment 14: Medical Image Compression and Quality Evaluation
% Author: Muhammad Ikrama (Reg ID: 60140)

function results = task_14_5_downstream_impact()
    fprintf('================================================================================\n');
    fprintf('TASK 14.5: DOWNSTREAM IMPACT ON SEGMENTATION & GLCM (MATLAB)\n');
    fprintf('================================================================================\n');
    
    mri = imread(fullfile('..', 'Inputs', 'images', 'Brain_MRI.png'));
    if size(mri, 3) == 3; mri = rgb2gray(mri); end
    
    rng(113);
    grid_n = imresize(randn(16, 16) * 38, [48 48], 'nearest');
    mri(220:267, 302:349) = uint8(min(max(double(mri(220:267, 302:349)) + grid_n, 0), 255));
    
    % Ground truth SRG tumor segmentation
    seed = [244, 326]; % 1-based indexing for MATLAB
    gtMask = srg_mat(mri, seed, 35);
    
    % GLCM ground truth on tumor patch
    offsets = [0 1; -1 1; -1 0; -1 -1];
    patchGT = mri(220:267, 302:349);
    glcmGT = graycomatrix(patchGT, 'NumLevels', 16, 'GrayLimits', [0 255], 'Offset', offsets, 'Symmetric', true);
    sGT = graycoprops(glcmGT, 'Contrast');
    gtCon = mean(sGT.Contrast);
    
    qualities = [100, 95, 85, 50, 25, 10, 5];
    fprintf('%-14s | %-18s | %-15s | %-14s\n', 'JPEG Quality', 'Tumor Dice (DSC)', 'GLCM Contrast', 'Con. Error %');
    fprintf('----------------------------------------------------------------------\n');
    
    for q = qualities
        if q == 100
            dec = mri;
            dsc = 1.0000;
        else
            tempJ = sprintf('temp_ds_q%d.jpg', q);
            imwrite(mri, tempJ, 'jpg', 'Quality', q);
            dec = imread(tempJ);
            delete(tempJ);
            
            maskDec = srg_mat(dec, seed, 35);
            inter = sum(gtMask & maskDec, 'all');
            dsc = 2.0 * inter / (sum(gtMask, 'all') + sum(maskDec, 'all') + 1e-12);
        end
        
        patchDec = dec(220:267, 302:349);
        glcmDec = graycomatrix(patchDec, 'NumLevels', 16, 'GrayLimits', [0 255], 'Offset', offsets, 'Symmetric', true);
        sDec = graycoprops(glcmDec, 'Contrast');
        conDec = mean(sDec.Contrast);
        conErr = abs(conDec - gtCon) / gtCon * 100;
        
        qStr = sprintf('Q=%d', q);
        if q == 100; qStr = 'Uncompressed'; end
        fprintf('%-14s | %-18.4f | %-15.4f | %-13.1f%%\n', qStr, dsc, conDec, conErr);
    end
    fprintf('>>> Task 14.5 Downstream Evaluation Complete.\n');
end

function mask = srg_mat(img, seed, tol)
    [H, W] = size(img);
    visited = false(H, W);
    mask = false(H, W);
    seedVal = double(img(seed(1), seed(2)));
    
    stack = [seed(1), seed(2)];
    visited(seed(1), seed(2)) = true;
    mask(seed(1), seed(2)) = true;
    
    while ~isempty(stack)
        curr = stack(end, :);
        stack(end, :) = [];
        cy = curr(1); cx = curr(2);
        
        neighbors = [cy-1, cx; cy+1, cx; cy, cx-1; cy, cx+1];
        for k = 1:4
            ny = neighbors(k, 1); nx = neighbors(k, 2);
            if ny >= 1 && ny <= H && nx >= 1 && nx <= W && ~visited(ny, nx)
                visited(ny, nx) = true;
                if abs(double(img(ny, nx)) - seedVal) <= tol
                    mask(ny, nx) = true;
                    stack = [stack; ny, nx];
                end
            end
        end
    end
end
