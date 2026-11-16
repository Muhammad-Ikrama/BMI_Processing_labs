%% ==============================================================================
%% SCRIPT: task_3_1.m
%% Experiment 03: Image Smoothing of Medical Images Using Spatial Domain Mean & Gaussian Filters
%% Task 3.1: 2D Spatial Discrete Convolution & Boundary Padding Comparison
%% Course: Medical Image Processing | Riphah International University
%% Instructor: Engr. Rana Talha Khalid
%% ==============================================================================

function task_3_1()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 03 - MATLAB TASK 3.1: 2D CONVOLUTION & BOUNDARY PADDING\n');
    fprintf('======================================================================\n');

    script_dir = fileparts(mfilename('fullpath'));
    exp_dir = fileparts(script_dir);
    img_path = fullfile(exp_dir, 'Inputs', 'images', 'MRI.jpg');

    if ~exist(img_path, 'file')
        img_path = fullfile(exp_dir, '..', '..', 'images', 'MRI.jpg');
    end

    img = imread(img_path);
    if size(img, 3) == 3
        img = rgb2gray(img);
    end

    [H, W] = size(img);
    fprintf('[INFO] Loaded MRI Scan: %d x %d pixels\n', W, H);

    % 1. Define 3x3 Averaging Kernel
    k_size = 3;
    h = ones(k_size, k_size) / (k_size * k_size);

    % 2. Execute custom discrete 2D convolution with Zero and Replicate padding
    fprintf('[INFO] Filtering with Zero-Padding (Constant 0 border)...\n');
    % In MATLAB, imfilter with default is zero padding (0)
    filtered_zero = imfilter(img, h, 0);

    fprintf('[INFO] Filtering with Replicate-Padding (Clamp boundary)...\n');
    filtered_repl = imfilter(img, h, 'replicate');

    % 3. Quantify boundary padding error in the 5-pixel perimeter band
    border_mask = false(H, W);
    border_mask(1:5, :) = true;
    border_mask(end-4:end, :) = true;
    border_mask(:, 1:5) = true;
    border_mask(:, end-4:end) = true;

    diff_abs = abs(double(filtered_repl) - double(filtered_zero));
    border_mae = mean(diff_abs(border_mask));
    border_rmse = sqrt(mean(diff_abs(border_mask).^2));
    max_drop = max(diff_abs(border_mask));

    fprintf('\n-----------------------------------------------------------------\n');
    fprintf('BOUNDARY PADDING ERROR METRICS (5-Pixel Perimeter Region):\n');
    fprintf('  * Mean Absolute Error (MAE):     %.2f intensity levels\n', border_mae);
    fprintf('  * Root Mean Squared Error (RMSE): %.2f intensity levels\n', border_rmse);
    fprintf('  * Maximum Intensity Drop:        %.2f intensity levels\n', max_drop);
    fprintf('-----------------------------------------------------------------\n');
    fprintf('Clinical Conclusion: Zero-padding introduces dark boundary decay (halo artifact),\n');
    fprintf('whereas replicate padding eliminates border distortion in clinical diagnosis.\n');

    % 4. Visualization: 4-panel comparison
    fig = figure('Visible', 'off', 'Position', [100, 100, 1100, 900]);

    % Panel 1: Full Zero-padded
    subplot(2, 2, 1);
    imshow(filtered_zero);
    title('A: Zero-Padding Full Scan (Dark Border Decay)', 'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.72 0.15 0.15]);
    rectangle('Position', [1, 1, 25, 25], 'EdgeColor', 'r', 'LineWidth', 1.5, 'LineStyle', '--');

    % Panel 2: Full Replicate-padded
    subplot(2, 2, 2);
    imshow(filtered_repl);
    title('B: Replicate-Padding Full Scan (Clinical Standard)', 'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.08 0.50 0.24]);
    rectangle('Position', [1, 1, 25, 25], 'EdgeColor', 'g', 'LineWidth', 1.5, 'LineStyle', '--');

    % Panel 3: Magnified corner zero-padding
    subplot(2, 2, 3);
    imagesc(filtered_zero(1:25, 1:25));
    colormap(gca, hot); colorbar; caxis([0 255]);
    title(sprintf('C: Magnified Corner (Zero-Pad)\nMAE = %.2f at perimeter', border_mae), ...
          'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.72 0.15 0.15]);
    xlabel('Column Index (1-25)'); ylabel('Row Index (1-25)');

    % Panel 4: Magnified corner replicate-padding
    subplot(2, 2, 4);
    imagesc(filtered_repl(1:25, 1:25));
    colormap(gca, hot); colorbar; caxis([0 255]);
    title('D: Magnified Corner (Replicate-Pad)\nContinuous Tissue Intensities', ...
          'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.08 0.50 0.24]);
    xlabel('Column Index (1-25)'); ylabel('Row Index (1-25)');

    sgtitle('MATLAB Task 3.1: 2D Spatial Discrete Convolution & Boundary Padding Comparison', ...
            'FontSize', 13, 'FontWeight', 'bold');

    % Save figures
    out_dir_m = fullfile(exp_dir, 'Outputs', 'MATLAB');
    fig_dir = fullfile(exp_dir, 'Figures');

    out_path_1 = fullfile(out_dir_m, 'exp03_task_3_1_boundary_padding_m.png');
    out_path_2 = fullfile(fig_dir, 'exp03_task_3_1_boundary_padding_m.png');

    exportgraphics(fig, out_path_1, 'Resolution', 300);
    exportgraphics(fig, out_path_2, 'Resolution', 300);
    close(fig);

    fprintf('[SUCCESS] Saved MATLAB figure to:\n  %s\n  %s\n', out_path_1, out_path_2);
end
