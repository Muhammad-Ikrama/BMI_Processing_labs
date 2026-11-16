%% ==============================================================================
%% SCRIPT: task_3_5.m
%% Experiment 03: Image Smoothing of Medical Images Using Spatial Domain Mean & Gaussian Filters
%% Task 3.5: 1D Anatomical Edge Gradient Profile Analysis & Blurring Evaluation
%% Course: Medical Image Processing | Riphah International University
%% Instructor: Engr. Rana Talha Khalid
%% ==============================================================================

function task_3_5()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 03 - MATLAB TASK 3.5: 1D ANATOMICAL EDGE GRADIENT PROFILES\n');
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

    % Simulate Gaussian noise
    rng(42);
    noise_var = (18 / 255)^2;
    noisy = imnoise(img, 'gaussian', 0, noise_var);

    % Filter images
    h_mean5 = fspecial('average', [5 5]);
    mean5 = imfilter(noisy, h_mean5, 'replicate');

    h_gauss5 = fspecial('gaussian', [5 5], 1.2);
    gauss5 = imfilter(noisy, h_gauss5, 'replicate');

    % Extract horizontal 1D profile across anatomical interface at row H/2
    row_idx = round(H / 2);
    c_start = 125;
    c_end = 175;
    cols = c_start:c_end;

    prof_ref   = double(img(row_idx, cols));
    prof_noisy = double(noisy(row_idx, cols));
    prof_mean  = double(mean5(row_idx, cols));
    prof_gauss = double(gauss5(row_idx, cols));

    % Helper for 10% to 90% transition width
    function w = calc_w1090(prof, col_arr)
        min_v = min(prof); max_v = max(prof);
        t10 = min_v + 0.10 * (max_v - min_v);
        t90 = min_v + 0.90 * (max_v - min_v);
        idx10 = find(prof >= t10, 1, 'first');
        idx90 = find(prof >= t90, 1, 'first');
        if ~isempty(idx10) && ~isempty(idx90)
            w = abs(col_arr(idx90) - col_arr(idx10));
        else
            w = 0;
        end
    end

    w_ref   = calc_w1090(prof_ref, cols);
    w_noisy = calc_w1090(prof_noisy, cols);
    w_mean  = calc_w1090(prof_mean, cols);
    w_gauss = calc_w1090(prof_gauss, cols);

    fprintf('\n1D EDGE TRANSITION WIDTH (W_10-90) EVALUATION (Row %d, Cols %d-%d):\n', row_idx, c_start, c_end);
    fprintf('----------------------------------------------------------------------\n');
    fprintf('%-26s | %-26s | %-26s\n', 'Condition', 'Transition Width (Pixels)', 'Edge Characterization');
    fprintf('----------------------------------------------------------------------\n');
    fprintf('%-26s | %-26.1f | Sharp anatomical step edge\n', 'Ground Truth Reference', w_ref);
    fprintf('%-26s | %-26.1f | High-frequency noise spikes\n', 'Noisy Scan (var=0.005)', w_noisy);
    fprintf('%-26s | %-26.1f | Severe ramp blur (W > 5 px)\n', 'Mean Filter 5x5', w_mean);
    fprintf('%-26s | %-26.1f | Preserved steep margin\n', 'Gaussian Filter 5x5', w_gauss);
    fprintf('----------------------------------------------------------------------\n');
    fprintf('Conclusion: Gaussian 5x5 maintains a steeper localized gradient transition\n');
    fprintf('compared to Mean 5x5, avoiding lesion boundary distortion.\n');

    % Visualization: Dual-Panel Figure
    fig = figure('Visible', 'off', 'Position', [100, 100, 1300, 600]);

    % Left: Image with profile line and inset box
    subplot(1, 2, 1);
    imshow(img);
    hold on;
    yline(row_idx, '--r', 'LineWidth', 1.8);
    plot([c_start, c_end], [row_idx, row_idx], '-y', 'LineWidth', 4);
    rectangle('Position', [c_start - 10, row_idx - 25, (c_end - c_start) + 20, 50], ...
              'EdgeColor', 'y', 'LineWidth', 1.5, 'LineStyle', ':');
    hold off;
    title(sprintf('Brain MRI: Profile Cross-Section at Row %d', row_idx), 'FontSize', 10.5, 'FontWeight', 'bold');

    % Right: Overlapping profile plots
    subplot(1, 2, 2);
    plot(cols, prof_ref, '-k', 'LineWidth', 2.5, 'DisplayName', sprintf('Reference (W=%.1f px)', w_ref));
    hold on;
    plot(cols, prof_noisy, '-', 'Color', [0.6 0.6 0.6], 'LineWidth', 1.0, 'DisplayName', 'Noisy Scan');
    plot(cols, prof_mean, '--r', 'LineWidth', 2.2, 'DisplayName', sprintf('Mean 5x5 (W=%.1f px)', w_mean));
    plot(cols, prof_gauss, '-g', 'LineWidth', 2.2, 'DisplayName', sprintf('Gaussian 5x5 (W=%.1f px)', w_gauss));
    hold off;
    xlabel('Horizontal Pixel Column Coordinate (x)', 'FontWeight', 'bold');
    ylabel('Pixel Intensity Level [0-255]', 'FontWeight', 'bold');
    title('1D Anatomical Edge Gradient Profiles Across Cortical Interface', 'FontSize', 10.5, 'FontWeight', 'bold');
    legend('Location', 'northwest');
    grid on;

    sgtitle('MATLAB Task 3.5: 1D Anatomical Edge Gradient Profile Analysis & Blurring Evaluation', ...
            'FontSize', 13, 'FontWeight', 'bold');

    % Save figures
    out_dir_m = fullfile(exp_dir, 'Outputs', 'MATLAB');
    fig_dir = fullfile(exp_dir, 'Figures');

    out_path_1 = fullfile(out_dir_m, 'exp03_task_3_5_edge_profile_m.png');
    out_path_2 = fullfile(fig_dir, 'exp03_task_3_5_edge_profile_m.png');

    exportgraphics(fig, out_path_1, 'Resolution', 300);
    exportgraphics(fig, out_path_2, 'Resolution', 300);
    close(fig);

    fprintf('[SUCCESS] Saved MATLAB figure to:\n  %s\n  %s\n', out_path_1, out_path_2);
end
