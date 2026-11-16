%% Experiment 05 - Task 5.3: Manual Implementation of Non-Maximum Suppression (NMS)
%% Stage 3 of Canny Optimal Edge Detector: 4-Sector Geometric Quantization & Ridge Thinning
%% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
%% Faculty: Engr. Rana Talha Khalid | Riphah International University

function results = task_5_3()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 05 - TASK 5.3: MANUAL NON-MAXIMUM SUPPRESSION (MATLAB)\n');
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

    % Stage 1: Gaussian pre-smoothing
    blurred = imgaussfilt(double(img), 1.2);

    % Stage 2: Sobel Gradients
    Gx_kernel = [-1, 0, 1; -2, 0, 2; -1, 0, 1];
    Gy_kernel = [-1, -2, -1; 0, 0, 0; 1, 2, 1];
    Gx = imfilter(blurred, Gx_kernel, 'replicate');
    Gy = imfilter(blurred, Gy_kernel, 'replicate');
    mag = sqrt(Gx.^2 + Gy.^2);
    theta = atan2(Gy, Gx);
    theta_deg = mod(rad2deg(theta), 180);

    % Stage 3: Manual NMS Algorithm
    [H, W] = size(img);
    nmsOut = zeros(H, W);
    sectorMap = zeros(H, W);

    % Vectorized sector assignments:
    % Sector 0: 0 deg (Horizontal gradient, vertical edge)
    s0 = (theta_deg < 22.5) | (theta_deg >= 157.5);
    % Sector 1: 45 deg (Diagonal)
    s1 = (theta_deg >= 22.5) & (theta_deg < 67.5);
    % Sector 2: 90 deg (Vertical gradient, horizontal edge)
    s2 = (theta_deg >= 67.5) & (theta_deg < 112.5);
    % Sector 3: 135 deg (Anti-diagonal)
    s3 = (theta_deg >= 112.5) & (theta_deg < 157.5);

    sectorMap(s0) = 0;
    sectorMap(s1) = 1;
    sectorMap(s2) = 2;
    sectorMap(s3) = 3;

    % Pad magnitude
    padMag = padarray(mag, [1, 1], 0, 'both');

    for r = 2:H+1
        for c = 2:W+1
            curr = padMag(r, c);
            if curr <= 0; continue; end

            sec = sectorMap(r-1, c-1);
            if sec == 0
                q = padMag(r, c+1);
                p = padMag(r, c-1);
            elseif sec == 1
                q = padMag(r-1, c+1);
                p = padMag(r+1, c-1);
            elseif sec == 2
                q = padMag(r-1, c);
                p = padMag(r+1, c);
            else
                q = padMag(r-1, c-1);
                p = padMag(r+1, c+1);
            end

            if curr >= q && curr >= p
                nmsOut(r-1, c-1) = curr;
            end
        end
    end

    % Threshold for binary demonstration
    thresh = 40.0;
    unthinnedBin = mag > thresh;
    thinnedBin = nmsOut > thresh;

    unthinnedCnt = sum(unthinnedBin(:));
    thinnedCnt = sum(thinnedBin(:));
    thinPct = (1.0 - (double(thinnedCnt) / double(unthinnedCnt))) * 100.0;

    fprintf('[METRIC] Un-thinned Sobel Edges (Thresh > %.1f): %d pixels\n', thresh, unthinnedCnt);
    fprintf('[METRIC] Manual NMS 1-px Skeletons:           %d pixels\n', thinnedCnt);
    fprintf('[DECISION] Ridge Thinning Efficiency: %.1f%% data reduction with 1-pixel skeletonization.\n', thinPct);

    % Save outputs
    outDir = fullfile(expDir, 'Outputs', 'MATLAB');
    if ~exist(outDir, 'dir'); mkdir(outDir); end
    imwrite(unthinnedBin, fullfile(outDir, 'exp05_task_5_3_unthinned_sobel.png'));
    imwrite(thinnedBin, fullfile(outDir, 'exp05_task_5_3_nms_thinned.png'));

    % Visualization
    fig = figure('Visible', 'off', 'Units', 'pixels', 'Position', [100, 100, 1200, 950]);

    % (a) Un-thinned Sobel
    subplot(2, 2, 1);
    imagesc(mag);
    colormap(gca, 'hot');
    colorbar;
    axis image off;
    title({sprintf('Un-Thinned Sobel Gradient Magnitude'), ...
           sprintf('(Ramped 3-5 Pixel Bands: %d Pixels > %d)', unthinnedCnt, int32(thresh))}, ...
        'FontWeight', 'bold', 'FontSize', 11);

    % (b) Quantized Direction Sectors Map
    subplot(2, 2, 2);
    imagesc(sectorMap);
    colormap(gca, lines(4));
    cbar = colorbar('Ticks', [0.375, 1.125, 1.875, 2.625], ...
                    'TickLabels', {'0° (H)', '45° (Diag)', '90° (V)', '135° (Anti-D)'});
    set(cbar, 'FontWeight', 'bold');
    axis image off;
    title({'Quantized 4-Sector Gradient Direction Map', '[0°, 45°, 90°, 135° Normal Discretization]'}, ...
        'FontWeight', 'bold', 'FontSize', 11);

    % (c) Manual NMS Output
    subplot(2, 2, 3);
    imshow(thinnedBin);
    title({sprintf('Manual Non-Maximum Suppression (NMS)'), ...
           sprintf('(Crisp 1-Pixel Skeletons: %d Pixels | %.1f%% Thinner)', thinnedCnt, thinPct)}, ...
        'FontWeight', 'bold', 'FontSize', 11);

    % (d) Zoom Comparison Window on Skull Boundary [180:260, 80:160]
    zr1 = 180; zr2 = 260; zc1 = 80; zc2 = 160;
    zoomUnthinned = unthinnedBin(zr1:zr2, zc1:zc2);
    zoomThinned = thinnedBin(zr1:zr2, zc1:zc2);

    [zH, zW] = size(zoomUnthinned);
    zoomComposite = zeros(zH, zW * 2 + 10, 3);
    % Left: unthinned (red)
    zoomComposite(:, 1:zW, 1) = double(zoomUnthinned);
    zoomComposite(:, 1:zW, 2) = double(zoomUnthinned) * 0.3;
    % Divider
    zoomComposite(:, zW+1:zW+10, :) = 0.5;
    % Right: thinned (cyan)
    zoomComposite(:, zW+11:zW*2+10, 2) = double(zoomThinned);
    zoomComposite(:, zW+11:zW*2+10, 3) = double(zoomThinned);

    subplot(2, 2, 4);
    imshow(zoomComposite);
    title({'High-Res Zoom Window (Skull Boundary ROI)', 'Left: Un-thinned Sobel (3-5 px) | Right: NMS 1-px Skeleton'}, ...
        'FontWeight', 'bold', 'FontSize', 11);

    sgtitle({'Task 5.3: Manual Non-Maximum Suppression (NMS) Algorithm Architecture', ...
             'Discretized Normal-Vector Ridge Tracking & 1-Pixel Skeletonization (MATLAB)'}, ...
        'FontWeight', 'bold', 'FontSize', 13);

    figDir = fullfile(expDir, 'Figures');
    if ~exist(figDir, 'dir'); mkdir(figDir); end
    figPath = fullfile(figDir, 'exp05_task_5_3_manual_nms_m.png');
    exportgraphics(fig, figPath, 'Resolution', 300);
    close(fig);
    fprintf('[SUCCESS] Figure saved to %s\n', figPath);

    results.unthinnedCnt = unthinnedCnt;
    results.thinnedCnt = thinnedCnt;
    results.thinPct = thinPct;
end
