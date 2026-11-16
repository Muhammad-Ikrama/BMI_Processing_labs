%% ==============================================================================
%% SCRIPT: task_3_4.m
%% Experiment 03: Image Smoothing of Medical Images Using Spatial Domain Mean & Gaussian Filters
%% Task 3.4: Quantitative Image Quality Benchmarking (PSNR, SSIM, CNR)
%% Course: Medical Image Processing | Riphah International University
%% Instructor: Engr. Rana Talha Khalid
%% ==============================================================================

function task_3_4()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 03 - MATLAB TASK 3.4: QUANTITATIVE BENCHMARKING (PSNR, SSIM, CNR)\n');
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

    % Define ROIs
    % ROI 1: Signal (Cortex / Parenchyma) [rows H/2-20:H/2+20, cols W/2-20:W/2+20]
    r_sig_y1 = round(H/2) - 20; r_sig_y2 = round(H/2) + 20;
    r_sig_x1 = round(W/2) - 20; r_sig_x2 = round(W/2) + 20;

    % ROI 2: Background Air [rows 10:50, cols 10:50]
    r_bg_y1 = 10; r_bg_y2 = 50;
    r_bg_x1 = 10; r_bg_x2 = 50;

    calc_metrics = @(im) deal( ...
        psnr(im, img), ...
        ssim(im, img), ...
        abs(mean(double(im(r_sig_y1:r_sig_y2, r_sig_x1:r_sig_x2)), 'all') - ...
            mean(double(im(r_bg_y1:r_bg_y2, r_bg_x1:r_bg_x2)), 'all')) / ...
        sqrt(var(double(im(r_sig_y1:r_sig_y2, r_sig_x1:r_sig_x2)), 0, 'all') + ...
             var(double(im(r_bg_y1:r_bg_y2, r_bg_x1:r_bg_x2)), 0, 'all')), ...
        std(double(im(r_bg_y1:r_bg_y2, r_bg_x1:r_bg_x2)), 0, 'all') ...
    );

    cases = {
        'Noisy Baseline', noisy;
        'Mean Filter 5x5', mean5;
        'Gaussian Filter 5x5 (sig=1.2)', gauss5
    };

    fprintf('%-28s | %-10s | %-8s | %-6s | %-12s | %-12s\n', 'Condition', 'PSNR (dB)', 'SSIM', 'CNR', 'Noise std_bg', 'Status');
    fprintf('----------------------------------------------------------------------------------------\n');

    psnr_arr = zeros(1, 3);
    ssim_arr = zeros(1, 3);
    cnr_arr  = zeros(1, 3);

    for i = 1:3
        im = cases{i, 2};
        [p, s, c, s_bg] = calc_metrics(im);
        psnr_arr(i) = p;
        ssim_arr(i) = s;
        cnr_arr(i)  = c;

        if p >= 27.5 && s >= 0.50 && c >= 1.0
            status = 'Good to Go';
        else
            status = 'Clinical Review';
        end
        fprintf('%-28s | %-10.2f | %-8.4f | %-6.2f | %-12.2f | %-12s\n', ...
                cases{i, 1}, p, s, c, s_bg, status);
    end

    % Visualization: Dual-Panel Figure
    fig = figure('Visible', 'off', 'Position', [100, 100, 1200, 550]);

    % Left: Image with ROI rectangles
    subplot(1, 2, 1);
    imshow(img);
    hold on;
    rectangle('Position', [r_sig_x1, r_sig_y1, 40, 40], 'EdgeColor', 'c', 'LineWidth', 2.5);
    text(r_sig_x1, r_sig_y1 - 6, 'ROI 1: Cortex', 'Color', 'c', 'FontWeight', 'bold', 'FontSize', 9);
    rectangle('Position', [r_bg_x1, r_bg_y1, 40, 40], 'EdgeColor', 'r', 'LineWidth', 2.5);
    text(r_bg_x1, r_bg_y2 + 15, 'ROI 2: Background Air', 'Color', 'r', 'FontWeight', 'bold', 'FontSize', 9);
    hold off;
    title('Brain MRI: Signal & Background ROI Definitions', 'FontSize', 10.5, 'FontWeight', 'bold');

    % Right: Grouped bar chart
    subplot(1, 2, 2);
    bar_data = [psnr_arr', (ssim_arr * 30)', (cnr_arr * 15)'];
    b = bar(bar_data);
    b(1).FaceColor = [0.23 0.51 0.96]; % Blue
    b(2).FaceColor = [0.06 0.72 0.50]; % Green
    b(3).FaceColor = [0.96 0.62 0.04]; % Yellow
    hold on;
    yline(28.0, '--b', 'Good to Go PSNR (28 dB)', 'LineWidth', 1.5);
    hold off;
    set(gca, 'XTick', 1:3, 'XTickLabel', {'Noisy', 'Mean 5x5', 'Gaussian 5x5'});
    ylabel('Metric Value (with visual scaling)', 'FontWeight', 'bold');
    title('Quantitative Quality Benchmark Comparison', 'FontSize', 10.5, 'FontWeight', 'bold');
    legend({'PSNR (dB)', 'SSIM (x30 scale)', 'CNR (x15 scale)'}, 'Location', 'northwest');
    grid on;

    sgtitle('MATLAB Task 3.4: Quantitative Image Quality Benchmarking (PSNR, SSIM, and CNR)', ...
            'FontSize', 13, 'FontWeight', 'bold');

    % Save figures
    out_dir_m = fullfile(exp_dir, 'Outputs', 'MATLAB');
    fig_dir = fullfile(exp_dir, 'Figures');

    out_path_1 = fullfile(out_dir_m, 'exp03_task_3_4_quality_benchmarking_m.png');
    out_path_2 = fullfile(fig_dir, 'exp03_task_3_4_quality_benchmarking_m.png');

    exportgraphics(fig, out_path_1, 'Resolution', 300);
    exportgraphics(fig, out_path_2, 'Resolution', 300);
    close(fig);

    fprintf('[SUCCESS] Saved MATLAB figure to:\n  %s\n  %s\n', out_path_1, out_path_2);
end
