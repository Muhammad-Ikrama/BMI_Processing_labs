%% ==============================================================================
%% SCRIPT: task_4_2.m
%% Experiment 04: Noise Modeling & Adaptive Filtering in Medical Images
%% Task 4.2: Failure Analysis of Linear Averaging & Gaussian Smoothing on Impulse Noise
%% Course: Medical Image Processing | Riphah International University
%% Instructor: Engr. Rana Talha Khalid
%% ==============================================================================

function task_4_2()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 04 - MATLAB TASK 4.2: LINEAR FILTER FAILURE ANALYSIS\n');
    fprintf('======================================================================\n');

    script_dir = fileparts(mfilename('fullpath'));
    exp_dir = fileparts(script_dir);
    img_path = fullfile(exp_dir, 'Inputs', 'images', 'CT.jpg');

    if ~exist(img_path, 'file')
        img_path = fullfile(exp_dir, 'Inputs', 'images', 'MRI.jpg');
    end

    ref = imread(img_path);
    if size(ref, 3) == 3; ref = rgb2gray(ref); end

    [H, W] = size(ref);

    % 1. Add 10% Salt & Pepper noise
    rng(42);
    noisy = imnoise(ref, 'salt & pepper', 0.10);

    % 2. Apply Linear Filters
    h_mean5 = fspecial('average', [5 5]);
    mean5 = imfilter(noisy, h_mean5, 'replicate');

    h_gauss5 = fspecial('gaussian', [5 5], 1.2);
    gauss5 = imfilter(noisy, h_gauss5, 'replicate');

    med5 = medfilt2(noisy, [5 5], 'symmetric');

    p_noisy = psnr(noisy, ref);
    p_mean  = psnr(mean5, ref);
    p_gauss = psnr(gauss5, ref);
    p_med   = psnr(med5, ref);

    s_noisy = ssim(noisy, ref);
    s_mean  = ssim(mean5, ref);
    s_gauss = ssim(gauss5, ref);
    s_med   = ssim(med5, ref);

    fprintf('\n-----------------------------------------------------------------------\n');
    fprintf('MATHEMATICAL SMEAR MECHANISM ANALYSIS (CT Scan):\n');
    fprintf('  * Linear Mean 5x5:     PSNR = %.2f dB, SSIM = %.4f (Smear blotches)\n', p_mean, s_mean);
    fprintf('  * Linear Gaussian 5x5: PSNR = %.2f dB, SSIM = %.4f (Weighted smudge)\n', p_gauss, s_gauss);
    fprintf('  * Non-Linear Med 5x5:  PSNR = %.2f dB, SSIM = %.4f (Outliers cleared)\n', p_med, s_med);
    fprintf('-----------------------------------------------------------------------\n');

    % Define ROI for magnification
    r1 = round(H/2) - 30; r2 = round(H/2) + 30;
    c1 = round(W/2) - 30; c2 = round(W/2) + 30;

    roi_mean = mean5(r1:r2, c1:c2);
    roi_med  = med5(r1:r2, c1:c2);

    % Visualization: 4-Panel Figure
    fig = figure('Visible', 'off', 'Position', [100, 100, 1100, 900]);

    subplot(2, 2, 1);
    imshow(noisy);
    hold on;
    rectangle('Position', [c1, r1, 60, 60], 'EdgeColor', 'r', 'LineWidth', 2, 'LineStyle', '--');
    hold off;
    title(sprintf('A: 10%% Impulse Noisy Scan\nPSNR: %.2f dB | SSIM: %.4f', p_noisy, s_noisy), ...
          'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.72 0.15 0.15]);

    subplot(2, 2, 2);
    imshow(mean5);
    title(sprintf('B: Linear Mean 5x5 Output\nPSNR: %.2f dB | SSIM: %.4f [Smear Failure]', p_mean, s_mean), ...
          'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.77 0.54 0.02]);

    subplot(2, 2, 3);
    imshow(roi_mean);
    title('C: Magnified ROI (Mean 5x5 Smear)\n[Impulses Form Broad Gray Smudge Halos]', ...
          'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.72 0.15 0.15]);

    subplot(2, 2, 4);
    imshow(roi_med);
    title(sprintf('D: Magnified ROI (Median 5x5 Success)\nPSNR: %.2f dB [Outliers Filtered by Sorting]', p_med), ...
          'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.08 0.50 0.24]);

    sgtitle('MATLAB Task 4.2: Failure Analysis of Linear Averaging & Gaussian Smoothing on Impulse Noise', ...
            'FontSize', 13, 'FontWeight', 'bold');

    out_dir_m = fullfile(exp_dir, 'Outputs', 'MATLAB');
    fig_dir = fullfile(exp_dir, 'Figures');

    out_path_1 = fullfile(out_dir_m, 'exp04_task_4_2_linear_failure_smear_m.png');
    out_path_2 = fullfile(fig_dir, 'exp04_task_4_2_linear_failure_smear_m.png');

    exportgraphics(fig, out_path_1, 'Resolution', 300);
    exportgraphics(fig, out_path_2, 'Resolution', 300);
    close(fig);

    fprintf('[SUCCESS] Saved MATLAB figure to:\n  %s\n  %s\n', out_path_1, out_path_2);
end
