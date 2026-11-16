%% Experiment 05 - Task 5.2: Prewitt vs. Sobel Noise Sensitivity Benchmarking
%% Quantifying Spurious Edge Breakthrough in Homogeneous Background Air ROI
%% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
%% Faculty: Engr. Rana Talha Khalid | Riphah International University

function results = task_5_2()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 05 - TASK 5.2: PREWITT VS SOBEL NOISE SENSITIVITY (MATLAB)\n');
    fprintf('======================================================================\n');

    % Setup paths
    scriptDir = fileparts(mfilename('fullpath'));
    expDir = fileparts(scriptDir);
    imgPath = fullfile(expDir, 'Inputs', 'images', 'CT.jpg');
    if ~exist(imgPath, 'file')
        imgPath = fullfile(expDir, '..', '..', 'images', 'CT.jpg');
    end

    img = imread(imgPath);
    if size(img, 3) == 3; img = rgb2gray(img); end

    % Add simulated Gaussian electronic noise (sigma = 15 / 255)
    rng(42);
    noiseSigma = 15.0;
    noisyD = double(img) + randn(size(img)) * noiseSigma;
    noisyD = max(0, min(noisyD, 255));
    noisyImg = uint8(noisyD);

    % Background air ROI [20:80, 20:80]
    r1 = 20; r2 = 80;
    c1 = 20; c2 = 80;
    roiArea = double((r2 - r1 + 1) * (c2 - c1 + 1));
    fprintf('[INFO] Background Air ROI: [%d:%d, %d:%d] (Area: %d pixels)\n', ...
        r1, r2, c1, c2, int32(roiArea));

    % Prewitt
    px = [-1, 0, 1; -1, 0, 1; -1, 0, 1];
    py = [-1, -1, -1; 0, 0, 0; 1, 1, 1];
    prewMag = sqrt(imfilter(noisyD, px, 'replicate').^2 + imfilter(noisyD, py, 'replicate').^2);

    % Sobel
    sx = [-1, 0, 1; -2, 0, 2; -1, 0, 1];
    sy = [-1, -2, -1; 0, 0, 0; 1, 2, 1];
    sobMag = sqrt(imfilter(noisyD, sx, 'replicate').^2 + imfilter(noisyD, sy, 'replicate').^2);

    % Calibrated sensitivity thresholds: Sobel has 4/3 orthogonal gain of Prewitt
    levels = {'Level 1 (Low)', 35.0, 46.7; ...
              'Level 2 (Standard)', 45.0, 60.0; ...
              'Level 3 (High)', 55.0, 73.3; ...
              'Level 4 (Strict)', 65.0, 86.7};

    prewCounts = zeros(size(levels, 1), 1);
    sobCounts = zeros(size(levels, 1), 1);
    prewRates = zeros(size(levels, 1), 1);
    sobRates = zeros(size(levels, 1), 1);

    fprintf('\n-------------------------------------------------------------------------------------\n');
    fprintf('%-20s | %-11s | %-10s | %-14s | %-14s\n', 'Sensitivity Level', 'Prewitt Th', 'Sobel Th', 'Prewitt False', 'Sobel False');
    fprintf('-------------------------------------------------------------------------------------\n');

    for i = 1:size(levels, 1)
        pTh = levels{i, 2};
        sTh = levels{i, 3};

        pBin = prewMag > pTh;
        sBin = sobMag > sTh;

        pRoiCnt = sum(sum(pBin(r1:r2, c1:c2)));
        sRoiCnt = sum(sum(sBin(r1:r2, c1:c2)));

        pRate = (double(pRoiCnt) / roiArea) * 100.0;
        sRate = (double(sRoiCnt) / roiArea) * 100.0;

        prewCounts(i) = pRoiCnt;
        sobCounts(i) = sRoiCnt;
        prewRates(i) = pRate;
        sobRates(i) = sRate;

        fprintf('%-20s | %-11.1f | %-10.1f | %-5d (%5.1f%%) | %-5d (%5.1f%%)\n', ...
            levels{i, 1}, pTh, sTh, pRoiCnt, pRate, sRoiCnt, sRate);
    end
    fprintf('-------------------------------------------------------------------------------------\n');

    % Standard edge maps (Level 2: 45 vs 60)
    prewEdgeStd = prewMag > 45.0;
    sobEdgeStd = sobMag > 60.0;

    % Save outputs
    outDir = fullfile(expDir, 'Outputs', 'MATLAB');
    if ~exist(outDir, 'dir'); mkdir(outDir); end
    imwrite(noisyImg, fullfile(outDir, 'exp05_task_5_2_noisy_input.png'));
    imwrite(prewEdgeStd, fullfile(outDir, 'exp05_task_5_2_prewitt_noisy.png'));
    imwrite(sobEdgeStd, fullfile(outDir, 'exp05_task_5_2_sobel_noisy.png'));

    % Visualization
    fig = figure('Visible', 'off', 'Units', 'pixels', 'Position', [100, 100, 1200, 950]);

    % 1. Noisy scan with ROI box
    subplot(2, 2, 1);
    imshow(noisyImg);
    hold on;
    rectangle('Position', [c1, r1, c2-c1, r2-r1], 'EdgeColor', 'r', 'LineWidth', 2);
    hold off;
    title({'Noisy Clinical CT Scan (\sigma = 15)', '[Red Box: Evaluated Air ROI]'}, ...
        'FontWeight', 'bold', 'FontSize', 11);

    % 2. Prewitt at Th=45
    subplot(2, 2, 2);
    imshow(prewEdgeStd);
    hold on;
    rectangle('Position', [c1, r1, c2-c1, r2-r1], 'EdgeColor', 'r', 'LineWidth', 2);
    hold off;
    title({sprintf('Prewitt Operator (Calibrated Th = 45.0)'), ...
           sprintf('Air False Edges: %d (%.1f%%) [Box Clutter]', prewCounts(2), prewRates(2))}, ...
        'FontWeight', 'bold', 'FontSize', 11);

    % 3. Sobel at Th=60
    subplot(2, 2, 3);
    imshow(sobEdgeStd);
    hold on;
    rectangle('Position', [c1, r1, c2-c1, r2-r1], 'EdgeColor', 'g', 'LineWidth', 2);
    hold off;
    title({sprintf('Sobel Operator (Calibrated Th = 60.0)'), ...
           sprintf('Air False Edges: %d (%.1f%%) [Binomial Smoothing]', sobCounts(2), sobRates(2))}, ...
        'FontWeight', 'bold', 'FontSize', 11);

    % 4. Bar Chart
    subplot(2, 2, 4);
    b = bar([prewRates, sobRates]);
    b(1).FaceColor = [0.85, 0.33, 0.31];
    b(2).FaceColor = [0.36, 0.72, 0.36];
    set(gca, 'XTickLabel', {'L1 (35/47)', 'L2 (45/60)', 'L3 (55/73)', 'L4 (65/87)'}, 'FontWeight', 'bold');
    ylabel('False Spurious Edge Rate (%) in Air ROI', 'FontWeight', 'bold');
    xlabel('Calibrated Sensitivity Levels', 'FontWeight', 'bold');
    title({'Spurious Edge Breakthrough vs. Calibrated Thresholds', 'Sobel vs. Prewitt Frequency Selectivity'}, ...
        'FontWeight', 'bold', 'FontSize', 11);
    legend({'Prewitt ([1,1,1])', 'Sobel ([1,2,1])'}, 'Location', 'northeast');
    grid on;

    sgtitle({'Task 5.2: Noise Sensitivity Benchmarking: Prewitt vs. Sobel Kernels', ...
             'Binomial Orthogonal Smoothing vs. Moving Average in Noisy Scans (MATLAB)'}, ...
        'FontWeight', 'bold', 'FontSize', 13);

    figDir = fullfile(expDir, 'Figures');
    if ~exist(figDir, 'dir'); mkdir(figDir); end
    figPath = fullfile(figDir, 'exp05_task_5_2_noise_sensitivity_m.png');
    exportgraphics(fig, figPath, 'Resolution', 300);
    close(fig);
    fprintf('[SUCCESS] Figure saved to %s\n', figPath);

    results.prewRates = prewRates;
    results.sobRates = sobRates;
end
