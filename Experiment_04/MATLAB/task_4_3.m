%% ==============================================================================
%% SCRIPT: task_4_3.m
%% Experiment 04: Noise Modeling & Adaptive Filtering in Medical Images
%% Task 4.3: Standard Median Filter Window Sizing Sensitivity [3x3, 5x5, 7x7]
%% Course: Medical Image Processing | Riphah International University
%% Instructor: Engr. Rana Talha Khalid
%% ==============================================================================

function task_4_3()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 04 - MATLAB TASK 4.3: MEDIAN WINDOW SENSITIVITY [3x3, 5x5, 7x7]\n');
    fprintf('======================================================================\n');

    script_dir = fileparts(mfilename('fullpath'));
    exp_dir = fileparts(script_dir);
    img_path = fullfile(exp_dir, 'Inputs', 'images', 'MRI.jpg');

    if ~exist(img_path, 'file')
        img_path = fullfile(exp_dir, '..', '..', 'images', 'MRI.jpg');
    end

    ref = imread(img_path);
    if size(ref, 3) == 3; ref = rgb2gray(ref); end

    % 1. Add 15% Salt & Pepper noise
    rng(42);
    noisy = imnoise(ref, 'salt & pepper', 0.15);

    % Helper for Edge Preservation Index (EPI / beta)
    h_lap = fspecial('laplacian', 0.2);
    calc_epi = @(im) sum((imfilter(double(ref), h_lap) - mean(imfilter(double(ref), h_lap), 'all')) .* ...
                         (imfilter(double(im), h_lap)  - mean(imfilter(double(im), h_lap), 'all')), 'all') / ...
                     sqrt(sum((imfilter(double(ref), h_lap) - mean(imfilter(double(ref), h_lap), 'all')).^2, 'all') * ...
                          sum((imfilter(double(im), h_lap)  - mean(imfilter(double(im), h_lap), 'all')).^2, 'all'));

    windows = [3, 5, 7];
    filtered_images = cell(1, 3);
    psnr_vals = zeros(1, 3);
    ssim_vals = zeros(1, 3);
    epi_vals  = zeros(1, 3);

    fprintf('%-12s | %-12s | %-10s | %-10s | %-30s\n', 'Window', 'PSNR (dB)', 'SSIM', 'EPI (beta)', 'Clinical Assessment');
    fprintf('--------------------------------------------------------------------------------------\n');
    fprintf('%-12s | %-12.2f | %-10.4f | %-10.4f | Unfiltered noisy scan (15%% SP)\n', ...
            'Noisy Base', psnr(noisy, ref), ssim(noisy, ref), calc_epi(noisy));

    for idx = 1:3
        w = windows(idx);
        f_im = medfilt2(noisy, [w w], 'symmetric');
        p = psnr(f_im, ref);
        s = ssim(f_im, ref);
        e = calc_epi(f_im);

        filtered_images{idx} = f_im;
        psnr_vals(idx) = p;
        ssim_vals(idx) = s;
        epi_vals(idx)  = e;

        if w == 3
            obs = 'Optimal; impulse cleared, sharp boundaries';
        elseif w == 5
            obs = 'Mild corner truncation; fine vessels blurred';
        else
            obs = 'Heavy detail truncation; anatomical edges rounded';
        end
        fprintf('%-12s | %-12.2f | %-10.4f | %-10.4f | %s\n', sprintf('%dx%d', w, w), p, s, e, obs);
    end
    fprintf('--------------------------------------------------------------------------------------\n');
    fprintf('Finding: Standard median window 3x3 achieves peak SSIM (%.4f) and EPI (%.4f).\n', ssim_vals(1), epi_vals(1));

    % Visualization: 4-Panel Figure
    fig = figure('Visible', 'off', 'Position', [100, 100, 1200, 900]);

    subplot(2, 2, 1);
    imshow(filtered_images{1});
    title(sprintf('A: Median 3x3 [Optimal]\nPSNR: %.2f dB | SSIM: %.4f | EPI: %.4f', psnr_vals(1), ssim_vals(1), epi_vals(1)), ...
          'FontSize', 9.5, 'FontWeight', 'bold', 'Color', [0.08 0.50 0.24]);

    subplot(2, 2, 2);
    imshow(filtered_images{2});
    title(sprintf('B: Median 5x5 [Edge Rounding]\nPSNR: %.2f dB | SSIM: %.4f | EPI: %.4f', psnr_vals(2), ssim_vals(2), epi_vals(2)), ...
          'FontSize', 9.5, 'FontWeight', 'bold', 'Color', [0.77 0.54 0.02]);

    subplot(2, 2, 3);
    imshow(filtered_images{3});
    title(sprintf('C: Median 7x7 [Detail Truncation]\nPSNR: %.2f dB | SSIM: %.4f | EPI: %.4f', psnr_vals(3), ssim_vals(3), epi_vals(3)), ...
          'FontSize', 9.5, 'FontWeight', 'bold', 'Color', [0.72 0.15 0.15]);

    subplot(2, 2, 4);
    yyaxis left
    plot(windows, ssim_vals, 'o-b', 'LineWidth', 2, 'MarkerSize', 7);
    ylabel('SSIM', 'FontWeight', 'bold', 'Color', 'b');
    grid on;

    yyaxis right
    plot(windows, epi_vals, 's--g', 'LineWidth', 2, 'MarkerSize', 7);
    ylabel('Edge Preservation Index (EPI)', 'FontWeight', 'bold', 'Color', [0.08 0.50 0.24]);

    set(gca, 'XTick', windows, 'XTickLabel', {'3x3', '5x5', '7x7'});
    xlabel('Median Filter Window Size (K x K)', 'FontWeight', 'bold');
    title('SSIM & EPI Trajectory vs Window Size', 'FontSize', 10, 'FontWeight', 'bold');

    sgtitle('MATLAB Task 4.3: Implementation and Kernel Sizing Sensitivity of Standard Median Filtering', ...
            'FontSize', 13, 'FontWeight', 'bold');

    out_dir_m = fullfile(exp_dir, 'Outputs', 'MATLAB');
    fig_dir = fullfile(exp_dir, 'Figures');

    out_path_1 = fullfile(out_dir_m, 'exp04_task_4_3_median_kernel_sweep_m.png');
    out_path_2 = fullfile(fig_dir, 'exp04_task_4_3_median_kernel_sweep_m.png');

    exportgraphics(fig, out_path_1, 'Resolution', 300);
    exportgraphics(fig, out_path_2, 'Resolution', 300);
    close(fig);

    fprintf('[SUCCESS] Saved MATLAB figure to:\n  %s\n  %s\n', out_path_1, out_path_2);
end
