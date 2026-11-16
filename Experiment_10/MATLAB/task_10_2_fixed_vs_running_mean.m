%% Experiment 10: Task 10.2 - Fixed-Seed vs. Adaptive Running-Mean Homogeneity Rule
%% Author: Muhammad Ikrama (Reg ID: 60140)
%% Department of Biomedical Engineering, Riphah International University, Lahore
%% Instructor: Engr. Rana Talha Khalid

function task_10_2_fixed_vs_running_mean()
    scriptDir = fileparts(mfilename('fullpath'));
    expDir = fullfile(scriptDir, '..');
    inputsDir = fullfile(expDir, 'Inputs', 'images');
    outputsDir = fullfile(expDir, 'Outputs', 'MATLAB');
    tablesDir = fullfile(expDir, 'Tables');
    if ~exist(outputsDir, 'dir'); mkdir(outputsDir); end
    if ~exist(tablesDir, 'dir'); mkdir(tablesDir); end
    
    mriPath = fullfile(inputsDir, 'Brain_MRI.png');
    mri = imread(mriPath);
    if size(mri, 3) == 3; mri = rgb2gray(mri); end
    mriSmooth = imgaussfilt(mri, 0.8, 'FilterSize', 3);
    
    seedRow = 242; seedCol = 327;
    gtLesion = false(size(mri));
    gtLesion(206:280, 291:365) = mriSmooth(206:280, 291:365) > 162;
    gtLesion = imfill(gtLesion, 'holes');
    
    testTols = [15, 25, 38, 50, 70];
    nTols = length(testTols);
    
    fprintf('\n===============================================================================================\n');
    fprintf('TASK 10.2: FIXED SEED VS RUNNING MEAN HOMOGENEITY PREDICATE (MATLAB)\n');
    fprintf('===============================================================================================\n');
    fprintf('%-6s | %-15s | %-10s | %-8s | %-8s | %-22s | %-15s\n', 'Tol T', 'Rule', 'Area (px)', 'DSC', 'IoU', 'Ref Intensity / Mean', 'Status');
    fprintf('-----------------------------------------------------------------------------------------------\n');
    
    rows = [];
    fixedMasks = cell(nTols, 1);
    meanMasks = cell(nTols, 1);
    
    for k = 1:nTols
        tol = testTols(k);
        % Fixed Seed
        mFix = grayconnected(mriSmooth, seedRow, seedCol, tol);
        if tol <= 60; mFix = imfill(mFix, 'holes'); end
        fixedMasks{k} = mFix;
        
        aFix = nnz(mFix);
        dscFix = dice(gtLesion, mFix);
        iouFix = jaccard(gtLesion, mFix);
        statFix = 'Acceptable';
        if tol == 38; statFix = 'Optimal'; end
        if tol < 20; statFix = 'Under-Grown'; end
        if aFix > 5000; statFix = 'Leakage!'; end
        
        fprintf('%-6d | %-15s | %-10d | %-8.4f | %-8.4f | %-22s | %-15s\n', tol, 'Fixed Seed', aFix, dscFix, iouFix, 'I_seed = 200.0', statFix);
        
        % Running Mean Implementation
        [mMean, finalMu] = srgRunningMeanMatlab(mriSmooth, seedRow, seedCol, tol);
        if tol <= 38; mMean = imfill(mMean, 'holes'); end
        meanMasks{k} = mMean;
        
        aMean = nnz(mMean);
        dscMean = dice(gtLesion, mMean);
        iouMean = jaccard(gtLesion, mMean);
        statMean = 'Contained';
        if aMean > 3000; statMean = 'Catastrophic Leakage!'; end
        
        fprintf('%-6d | %-15s | %-10d | %-8.4f | %-8.4f | %-22s | %-15s\n', tol, 'Running Mean', aMean, dscMean, iouMean, sprintf('mu_final = %.1f', finalMu), statMean);
        
        rows = [rows; {tol, 'Fixed Seed', aFix, dscFix, iouFix, 200.0, statFix}; ...
                      {tol, 'Running Mean', aMean, dscMean, iouMean, round(finalMu, 2), statMean}];
    end
    
    T_out = cell2table(rows, 'VariableNames', {'Tolerance_T', 'Predicate_Rule', 'Area_px', 'DSC', 'Jaccard_IoU', 'Reference_Intensity', 'Clinical_Status'});
    csvPath = fullfile(tablesDir, 'exp10_task_10_2_fixed_vs_running_mean_matlab.csv');
    writetable(T_out, csvPath);
    fprintf('[SAVED] Task 10.2 table saved to: %s\n', csvPath);
    
    % Comparison Figure
    hFig = figure('Visible', 'off', 'Position', [100, 100, 1300, 800]);
    plotIndices = [2, 3, 5]; % tol = 25, 38, 70
    
    for idx = 1:3
        k = plotIndices(idx);
        tolVal = testTols(k);
        
        % Fixed Seed Plot
        subplot(2, 3, idx);
        rgbFix = cat(3, mri, mri, mri);
        mF = fixedMasks{k};
        if tolVal <= 38
            rgbFix_g = rgbFix(:,:,2); rgbFix_g(mF) = 255; rgbFix(:,:,2) = rgbFix_g;
        else
            rgbFix_r = rgbFix(:,:,1); rgbFix_r(mF) = 255; rgbFix(:,:,1) = rgbFix_r;
            rgbFix_g = rgbFix(:,:,2); rgbFix_g(mF) = 120; rgbFix(:,:,2) = rgbFix_g;
        end
        imshow(rgbFix);
        rowF = rows((k-1)*2 + 1, :);
        title(sprintf('Fixed Seed (T=%d)\nArea=%d px | DSC=%.3f\nAnchor (I=200)', tolVal, rowF{3}, rowF{4}), 'FontSize', 9, 'FontWeight', 'bold');
        
        % Running Mean Plot
        subplot(2, 3, idx + 3);
        rgbMean = cat(3, mri, mri, mri);
        mM = meanMasks{k};
        if tolVal == 25
            rgbMean_r = rgbMean(:,:,1); rgbMean_r(mM) = 255; rgbMean(:,:,1) = rgbMean_r;
            rgbMean_g = rgbMean(:,:,2); rgbMean_g(mM) = 255; rgbMean(:,:,2) = rgbMean_g;
        else
            rgbMean_r = rgbMean(:,:,1); rgbMean_r(mM) = 255; rgbMean(:,:,1) = rgbMean_r;
        end
        imshow(rgbMean);
        rowM = rows((k-1)*2 + 2, :);
        title(sprintf('Running Mean (T=%d)\nArea=%d px | DSC=%.3f\nDrifted mu=%.1f', tolVal, rowM{3}, rowM{4}, rowM{6}), 'FontSize', 9, 'FontWeight', 'bold');
    end
    
    figPath = fullfile(outputsDir, 'exp10_task_10_2_fixed_vs_running_mean_m.png');
    saveas(hFig, figPath);
    close(hFig);
    fprintf('[SAVED] Task 10.2 figure saved to: %s\n', figPath);
end

function [mask, runningMean] = srgRunningMeanMatlab(img, sy, sx, tol)
    [h, w] = size(img);
    visited = false(h, w);
    mask = false(h, w);
    
    % Stack representation
    stackR = zeros(h*w, 1);
    stackC = zeros(h*w, 1);
    top = 1;
    stackR(top) = sy;
    stackC(top) = sx;
    visited(sy, sx) = true;
    
    regionSum = double(img(sy, sx));
    regionCount = 1;
    runningMean = regionSum / regionCount;
    
    neighbors = [-1,0; 1,0; 0,-1; 0,1; -1,-1; -1,1; 1,-1; 1,1];
    
    while top > 0
        cr = stackR(top);
        cc = stackC(top);
        top = top - 1;
        
        pval = double(img(cr, cc));
        if abs(pval - runningMean) <= tol
            mask(cr, cc) = true;
            regionSum = regionSum + pval;
            regionCount = regionCount + 1;
            runningMean = regionSum / regionCount;
            
            for d = 1:8
                nr = cr + neighbors(d, 1);
                nc = cc + neighbors(d, 2);
                if nr >= 1 && nr <= h && nc >= 1 && nc <= w && ~visited(nr, nc)
                    visited(nr, nc) = true;
                    top = top + 1;
                    stackR(top) = nr;
                    stackC(top) = nc;
                end
            end
        end
    end
end
