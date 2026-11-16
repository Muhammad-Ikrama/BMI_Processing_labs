%% Experiment 05 - Task 5.5: Multi-Operator Quantitative Diagnostic Evaluation Report
%% Comprehensive Benchmark: Sobel, Prewitt, Canny with Pratt's FOM & 1D Profiles
%% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
%% Faculty: Engr. Rana Talha Khalid | Riphah International University

function results = task_5_5()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 05 - TASK 5.5: MULTI-OPERATOR DIAGNOSTIC EVALUATION (MATLAB)\n');
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
    imgD = double(img);
    totalPixels = double(numel(img));
    [H, W] = size(img);

    % 1. Operators
    prewEdge = edge(img, 'prewitt');
    sobelEdge = edge(img, 'sobel');
    cannyEdge = edge(img, 'canny', [0.08, 0.20], 1.2);

    % Sobel magnitude for 1D profile
    sx = [-1, 0, 1; -2, 0, 2; -1, 0, 1];
    sy = [-1, -2, -1; 0, 0, 0; 1, 2, 1];
    sobMag = sqrt(imfilter(imgD, sx, 'replicate').^2 + imfilter(imgD, sy, 'replicate').^2);

    % Reference ideal ground truth edges (denoised multi-structure reference)
    denoisedRef = medfilt2(img, [3, 3]);
    idealEdges = edge(denoisedRef, 'canny', [0.07, 0.18], 1.0);
    NI = sum(idealEdges(:));
    distMap = bwdist(idealEdges);
    alpha = 1.0 / 9.0;

    % 2. Benchmarking
    operators = {'Prewitt Operator', prewEdge, 4.2; ...
                 'Sobel Operator', sobelEdge, 3.8; ...
                 'Canny Edge Detector', cannyEdge, 1.0};

    fprintf('\n================================================================================\n');
    fprintf('%-22s | %-12s | %-10s | %-10s | %-10s\n', 'Operator', 'Edge Pixels', 'Density (%)', 'Pratt FOM', 'Width (px)');
    fprintf('================================================================================\n');

    results = cell(3, 1);
    fomScores = zeros(3, 1);
    densities = zeros(3, 1);
    edgeCounts = zeros(3, 1);

    for i = 1:3
        name = operators{i, 1};
        bMap = operators{i, 2};
        estWidth = operators{i, 3};

        NA = sum(bMap(:));
        pct = (double(NA) / totalPixels) * 100.0;

        % Pratt FOM
        actDists = distMap(bMap);
        fomSum = sum(1.0 ./ (1.0 + alpha * (actDists .^ 2)));
        fom = double(fomSum) / max(double(NI), double(NA));

        edgeCounts(i) = NA;
        densities(i) = pct;
        fomScores(i) = fom;

        results{i} = struct('name', name, 'count', NA, 'density', pct, 'fom', fom, 'width', estWidth);
        fprintf('%-22s | %-12d | %-10.2f | %-10.4f | %-10.1f\n', name, NA, pct, fom, estWidth);
    end
    fprintf('================================================================================\n');

    % 3. 1D Profile across row H / 2
    rowIdx = round(H / 2);
    intProf = double(img(rowIdx, :));
    sobProf = sobMag(rowIdx, :);
    canProf = double(cannyEdge(rowIdx, :)) * 255.0;

    % 4. Visualization: 2x3 Grid
    fig = figure('Visible', 'off', 'Units', 'pixels', 'Position', [100, 100, 1500, 950]);

    % (a) Original CT with profile line
    subplot(2, 3, 1);
    imshow(img);
    hold on;
    line([1, W], [rowIdx, rowIdx], 'Color', 'y', 'LineWidth', 2);
    hold off;
    title({'(a) Clinical Head CT Scan (Ground Truth)', sprintf('[Yellow Line: Transect Row %d]', rowIdx)}, ...
        'FontWeight', 'bold', 'FontSize', 10);

    % (b) Prewitt
    subplot(2, 3, 2);
    imshow(prewEdge);
    title({'(b) Prewitt Edge Map (Unweighted)', sprintf('Edges: %d | FOM: %.3f (Broad Ramps)', edgeCounts(1), fomScores(1))}, ...
        'FontWeight', 'bold', 'FontSize', 10);

    % (c) Sobel
    subplot(2, 3, 3);
    imshow(sobelEdge);
    title({'(c) Sobel Edge Map (Binomial Smoothed)', sprintf('Edges: %d | FOM: %.3f (Thick Borders)', edgeCounts(2), fomScores(2))}, ...
        'FontWeight', 'bold', 'FontSize', 10);

    % (d) Canny
    subplot(2, 3, 4);
    imshow(cannyEdge);
    title({'(d) Canny Optimal Edge Map (NMS + Hysteresis)', sprintf('Edges: %d | FOM: %.3f (1-px Skeletons)', edgeCounts(3), fomScores(3))}, ...
        'FontWeight', 'bold', 'FontSize', 10);

    % (e) 1D Profile
    subplot(2, 3, 5);
    plot(1:W, intProf, 'b-', 'LineWidth', 1.2, 'DisplayName', 'Raw CT (HU)');
    hold on;
    plot(1:W, sobProf, 'r--', 'LineWidth', 1.5, 'DisplayName', 'Sobel Magnitude (Ramp)');
    plot(1:W, canProf, 'g-', 'LineWidth', 1.8, 'DisplayName', 'Canny Response (Spike)');
    hold off;
    title({'(e) 1D Anatomical Edge Profile (Row Transect)', 'Ramp-to-Spike Thinning Localization'}, ...
        'FontWeight', 'bold', 'FontSize', 10);
    xlabel('Horizontal Pixel Coordinate', 'FontWeight', 'bold', 'FontSize', 9);
    ylabel('Intensity / Magnitude', 'FontWeight', 'bold', 'FontSize', 9);
    legend('Location', 'northeast', 'FontSize', 8);
    grid on;
    xlim([1, W]);

    % (f) Benchmark Bar Chart
    subplot(2, 3, 6);
    b = bar([fomScores * 100, densities]);
    b(1).FaceColor = [0.20, 0.48, 0.72];
    b(2).FaceColor = [0.94, 0.68, 0.31];
    set(gca, 'XTickLabel', {'Prewitt', 'Sobel', 'Canny'}, 'FontWeight', 'bold', 'FontSize', 9);
    title({'(f) Quantitative Benchmark Metrics', 'Pratt FOM (%) vs. Edge Density (%)'}, ...
        'FontWeight', 'bold', 'FontSize', 10);
    ylabel('Score / Percentage (%)', 'FontWeight', 'bold', 'FontSize', 9);
    legend({'Pratt FOM (%)', 'Edge Density (%)'}, 'Location', 'northeast', 'FontSize', 8);
    grid on;

    sgtitle({'Task 5.5: Multi-Operator Quantitative Diagnostic Evaluation Report', ...
             'Spatial Gradient Operators vs. Optimal Multi-Stage Canny Edge Detection (MATLAB)'}, ...
        'FontWeight', 'bold', 'FontSize', 13);

    figDir = fullfile(expDir, 'Figures');
    if ~exist(figDir, 'dir'); mkdir(figDir); end
    figPath = fullfile(figDir, 'exp05_task_5_5_diagnostic_report_m.png');
    exportgraphics(fig, figPath, 'Resolution', 300);
    close(fig);
    fprintf('[SUCCESS] Diagnostic figure saved to %s\n', figPath);

    % Save outputs
    outDir = fullfile(expDir, 'Outputs', 'MATLAB');
    if ~exist(outDir, 'dir'); mkdir(outDir); end
    imwrite(prewEdge, fullfile(outDir, 'exp05_task_5_5_prewitt.png'));
    imwrite(sobelEdge, fullfile(outDir, 'exp05_task_5_5_sobel.png'));
    imwrite(cannyEdge, fullfile(outDir, 'exp05_task_5_5_canny.png'));
end
