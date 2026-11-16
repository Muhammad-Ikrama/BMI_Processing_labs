%% Experiment 05 - Example 01: Medical Edge Detection Benchmark
%% Sobel, Prewitt, and Canny Operators Implementation & Quantitative Comparison
%% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
%% Faculty: Engr. Rana Talha Khalid | Riphah International University

function results = example_01()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 05 - EXAMPLE 01: MEDICAL EDGE DETECTION BENCHMARK (MATLAB)\n');
    fprintf('======================================================================\n');

    % Setup paths
    scriptDir = fileparts(mfilename('fullpath'));
    expDir = fileparts(scriptDir);
    imgPath = fullfile(expDir, 'Inputs', 'images', 'CT.jpg');
    if ~exist(imgPath, 'file')
        imgPath = fullfile(expDir, '..', '..', 'images', 'CT.jpg');
    end

    img = imread(imgPath);
    if size(img, 3) == 3
        img = rgb2gray(img);
    end

    totalPixels = numel(img);
    fprintf('[INFO] Loaded CT Image: %dx%d pixels (%s total pixels)\n', ...
        size(img, 2), size(img, 1), num2str(totalPixels));

    % 1. Prewitt and Sobel Gradient Operators
    prewEdge = edge(img, 'prewitt');
    sobelEdge = edge(img, 'sobel');

    % 2. Canny Multi-Stage Operator (NMS + Hysteresis)
    cannyEdge = edge(img, 'canny', [0.08 0.20], 1.2);

    % 3. Benchmarking
    tests = {'Prewitt Operator', prewEdge; ...
             'Sobel Operator', sobelEdge; ...
             'Canny Edge Detector', cannyEdge};

    fprintf('\n----------------------------------------------------\n');
    fprintf('%-22s | %-12s | %-10s\n', 'Operator', 'Edge Pixels', 'Density (%)');
    fprintf('----------------------------------------------------\n');

    results = struct();
    for i = 1:size(tests, 1)
        name = tests{i, 1};
        bMap = tests{i, 2};
        cnt = sum(bMap(:));
        pct = (cnt / totalPixels) * 100.0;
        
        cleanField = regexprep(name, '\s+', '_');
        results.(cleanField).count = cnt;
        results.(cleanField).density = pct;

        fprintf('%-22s | %-12d | %-10.2f\n', name, cnt, pct);
    end
    fprintf('----------------------------------------------------\n');

    thinPct = (1.0 - (results.Canny_Edge_Detector.count / results.Sobel_Operator.count)) * 100.0;
    fprintf('[DECISION] Canny Operator achieves OPTIMAL 1-pixel skeletonization (%.1f%% thinner than Sobel).\n', thinPct);

    % Save output images
    outDir = fullfile(expDir, 'Outputs', 'MATLAB');
    if ~exist(outDir, 'dir'); mkdir(outDir); end
    imwrite(prewEdge, fullfile(outDir, 'exp05_example_01_prewitt.png'));
    imwrite(sobelEdge, fullfile(outDir, 'exp05_example_01_sobel.png'));
    imwrite(cannyEdge, fullfile(outDir, 'exp05_example_01_canny.png'));

    % 4. Publication-Grade Visualization
    fig = figure('Visible', 'off', 'Units', 'pixels', 'Position', [100, 100, 1100, 950]);

    % Original
    subplot(2, 2, 1);
    imshow(img);
    title({'Original Clinical Head CT Scan', '(Ground Truth Anatomy)'}, ...
        'FontWeight', 'bold', 'FontSize', 11);

    % Prewitt
    subplot(2, 2, 2);
    imshow(prewEdge);
    title({sprintf('Prewitt Operator (Orthogonal Diff)'), ...
           sprintf('Edges: %d | Density: %.2f%% (Thick Ramps)', results.Prewitt_Operator.count, results.Prewitt_Operator.density)}, ...
        'FontWeight', 'bold', 'FontSize', 11);

    % Sobel
    subplot(2, 2, 3);
    imshow(sobelEdge);
    title({sprintf('Sobel Operator (Binomial Filter)'), ...
           sprintf('Edges: %d | Density: %.2f%% (Thick Borders)', results.Sobel_Operator.count, results.Sobel_Operator.density)}, ...
        'FontWeight', 'bold', 'FontSize', 11);

    % Canny
    subplot(2, 2, 4);
    imshow(cannyEdge);
    title({sprintf('Canny Edge Detector ([0.08, 0.20], \\sigma=1.2)'), ...
           sprintf('Edges: %d | Density: %.2f%% (1-px Skeletons)', results.Canny_Edge_Detector.count, results.Canny_Edge_Detector.density)}, ...
        'FontWeight', 'bold', 'FontSize', 11);

    sgtitle({'Clinical Head CT Edge Detection Benchmark (MATLAB)', ...
             'Spatial Gradient Operators vs. Multi-Stage Optimal Canny Pipeline'}, ...
        'FontWeight', 'bold', 'FontSize', 13);

    figDir = fullfile(expDir, 'Figures');
    if ~exist(figDir, 'dir'); mkdir(figDir); end
    figPath = fullfile(figDir, 'exp05_example_01_benchmark_m.png');
    exportgraphics(fig, figPath, 'Resolution', 300);
    close(fig);
    fprintf('[SUCCESS] Figure saved to %s\n', figPath);
end
