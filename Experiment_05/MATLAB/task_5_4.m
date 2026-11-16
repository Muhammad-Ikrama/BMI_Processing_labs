%% Experiment 05 - Task 5.4: Canny Hysteresis Threshold Tuning & Broken Contour Analysis
%% Investigating Hysteresis Dual-Threshold Dynamics on Clinical Anatomical Continuity
%% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
%% Faculty: Engr. Rana Talha Khalid | Riphah International University

function results = task_5_4()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 05 - TASK 5.4: CANNY HYSTERESIS TUNING & ANALYSIS (MATLAB)\n');
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

    totalPixels = double(numel(img));

    % Sweep configs (normalized threshold [T_low, T_high] in MATLAB)
    % Sweep A: Fixed T_low = 0.05, varying T_high in [0.10, 0.20, 0.32]
    configsA = {
        'Case A1: Low Thigh (0.05/0.10)', [0.05, 0.10], 'Excessive Clutter & Loops'; ...
        'Case A2: Balanced Thigh (0.05/0.20)', [0.05, 0.20], 'Good Boundary Connectivity'; ...
        'Case A3: High Thigh (0.05/0.32)', [0.05, 0.32], 'Broken Skull & Ventricle Boundaries'
    };

    % Sweep B: Fixed T_high = 0.20, varying T_low in [0.02, 0.08, 0.15]
    configsB = {
        'Case B1: Low Tlow (0.02/0.20)', [0.02, 0.20], 'Noise Breakthrough in Background'; ...
        'Case B2: Recommended (0.08/0.20)', [0.08, 0.20], 'Optimal Clinical Trade-off'; ...
        'Case B3: High Tlow (0.15/0.20)', [0.15, 0.20], 'Severe Boundary Fragmentation'
    };

    allConfigs = [configsA; configsB];

    fprintf('\n--------------------------------------------------------------------------------\n');
    fprintf('%-22s | %-6s | %-6s | %-6s | %-12s | %-10s\n', 'Configuration', 'T_low', 'T_high', 'Ratio', 'Edge Pixels', 'Density (%)');
    fprintf('--------------------------------------------------------------------------------\n');

    outDir = fullfile(expDir, 'Outputs', 'MATLAB');
    if ~exist(outDir, 'dir'); mkdir(outDir); end

    results = cell(size(allConfigs, 1), 1);
    edgeMaps = cell(size(allConfigs, 1), 1);

    for i = 1:size(allConfigs, 1)
        lbl = allConfigs{i, 1};
        th = allConfigs{i, 2};
        diag = allConfigs{i, 3};

        tLow = th(1);
        tHigh = th(2);
        ratio = tHigh / tLow;

        edges = edge(img, 'canny', [tLow, tHigh], 1.2);
        cnt = sum(edges(:));
        density = (double(cnt) / totalPixels) * 100.0;

        results{i} = struct('label', lbl, 'tLow', tLow, 'tHigh', tHigh, ...
                            'ratio', ratio, 'count', cnt, 'density', density, 'diagnosis', diag);
        edgeMaps{i} = edges;

        fprintf('%-22s | %-6.2f | %-6.2f | %-6.2f | %-12d | %-10.2f\n', ...
            strtok(lbl, ':'), tLow, tHigh, ratio, cnt, density);

        cfgName = sprintf('exp05_task_5_4_canny_tlow%02d_thigh%02d.png', round(tLow*100), round(tHigh*100));
        imwrite(edges, fullfile(outDir, cfgName));
    end
    fprintf('--------------------------------------------------------------------------------\n');

    % Visualization: 2x3 Grid
    fig = figure('Visible', 'off', 'Units', 'pixels', 'Position', [100, 100, 1400, 950]);

    for i = 1:6
        subplot(2, 3, i);
        imshow(edgeMaps{i});
        res = results{i};
        title({res.label, sprintf('Edges: %d | Density: %.2f%% (Ratio: %.1f)', res.count, res.density, res.ratio)}, ...
            'FontWeight', 'bold', 'FontSize', 9);
    end

    sgtitle({'Task 5.4: Canny Hysteresis Dual-Threshold Sensitivity Analysis', ...
             'Balancing Boundary Continuity vs. Spurious Noise Breakthrough (MATLAB)'}, ...
        'FontWeight', 'bold', 'FontSize', 13);

    figDir = fullfile(expDir, 'Figures');
    if ~exist(figDir, 'dir'); mkdir(figDir); end
    figPath = fullfile(figDir, 'exp05_task_5_4_hysteresis_tuning_m.png');
    exportgraphics(fig, figPath, 'Resolution', 300);
    close(fig);
    fprintf('[SUCCESS] Figure saved to %s\n', figPath);
end
