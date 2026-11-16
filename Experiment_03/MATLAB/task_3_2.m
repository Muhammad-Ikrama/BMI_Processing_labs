%% ==============================================================================
%% SCRIPT: task_3_2.m
%% Experiment 03: Image Smoothing of Medical Images Using Spatial Domain Mean & Gaussian Filters
%% Task 3.2: Spatial Mean Averaging Filter & Kernel Dimension Sensitivity Sweep
%% Course: Medical Image Processing | Riphah International University
%% Instructor: Engr. Rana Talha Khalid
%% ==============================================================================

function task_3_2()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 03 - MATLAB TASK 3.2: MEAN FILTER KERNEL SWEEP [3x3 to 9x9]\n');
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

    % 1. Degrade scan with simulated Gaussian noise (sigma = 15/255 -> variance = (15/255)^2 = 0.00346)
    rng(42);
    noise_var = (15 / 255)^2;
    noisy = imnoise(img, 'gaussian', 0, noise_var);

    p_noisy = psnr(noisy, img);
    s_noisy = ssim(noisy, img);

    % 2. Sweep kernel sizes [3x3, 5x5, 7x7, 9x9]
    k_sizes = [3, 5, 7, 9];
    filtered_images = cell(1, 4);
    psnr_vals = zeros(1, 4);
    ssim_vals = zeros(1, 4);

    fprintf('%-12s | %-10s | %-8s | %-30s\n', 'Kernel Size', 'PSNR (dB)', 'SSIM', 'Observation');
    fprintf('----------------------------------------------------------------------\n');
    fprintf('%-12s | %-10.2f | %-8.4f | Unfiltered noisy scan\n', 'Noisy Input', p_noisy, s_noisy);

    for idx = 1:length(k_sizes)
        k = k_sizes(idx);
        h = fspecial('average', [k k]);
        f_im = imfilter(noisy, h, 'replicate');
        p = psnr(f_im, img);
        s = ssim(f_im, img);

        filtered_images{idx} = f_im;
        psnr_vals(idx) = p;
        ssim_vals(idx) = s;

        if k == 3
            obs = 'Optimal noise suppression without blur';
        elseif k == 5
            obs = 'Moderate edge erosion';
        elseif k == 7
            obs = 'Severe spatial blur';
        else
            obs = 'Catastrophic anatomical washout';
        end
        fprintf('%-12s | %-10.2f | %-8.4f | %s\n', sprintf('%dx%d', k, k), p, s, obs);
    end
    fprintf('----------------------------------------------------------------------\n');
    fprintf('Peak PSNR at 3x3 (%.2f dB). Beyond 3x3, structural fidelity SSIM drops rapidly.\n', psnr_vals(1));

    % 3. Visualization: 6-panel composite
    fig = figure('Visible', 'off', 'Position', [100, 100, 1300, 850]);

    % Panel 1: Noisy scan
    subplot(2, 3, 1);
    imshow(noisy);
    title(sprintf('Noisy Scan (var=%.4f)\nPSNR: %.2f dB | SSIM: %.4f', noise_var, p_noisy, s_noisy), ...
          'FontSize', 9.5, 'FontWeight', 'bold', 'Color', [0.72 0.15 0.15]);

    % Panels 2-5: Filtered scans
    titles = {
        sprintf('Mean 3x3 (Optimal)\nPSNR: %.2f dB | SSIM: %.4f', psnr_vals(1), ssim_vals(1));
        sprintf('Mean 5x5 (Edge Erosion)\nPSNR: %.2f dB | SSIM: %.4f', psnr_vals(2), ssim_vals(2));
        sprintf('Mean 7x7 (Severe Blur)\nPSNR: %.2f dB | SSIM: %.4f', psnr_vals(3), ssim_vals(3));
        sprintf('Mean 9x9 (Catastrophic Washout)\nPSNR: %.2f dB | SSIM: %.4f', psnr_vals(4), ssim_vals(4));
    };
    sp_indices = [2, 3, 4, 5];
    for idx = 1:4
        subplot(2, 3, sp_indices(idx));
        imshow(filtered_images{idx});
        title(titles{idx}, 'FontSize', 9.5, 'FontWeight', 'bold', 'Color', [0.12 0.23 0.54]);
    end

    % Panel 6: Dual-axis Line Plot
    subplot(2, 3, 6);
    yyaxis left
    plot(k_sizes, psnr_vals, 'o-b', 'LineWidth', 2, 'MarkerSize', 6);
    ylabel('PSNR (dB)', 'FontWeight', 'bold', 'Color', 'b');
    grid on;

    yyaxis right
    plot(k_sizes, ssim_vals, 's--g', 'LineWidth', 2, 'MarkerSize', 6);
    ylabel('SSIM', 'FontWeight', 'bold', 'Color', [0.08 0.50 0.24]);

    set(gca, 'XTick', k_sizes, 'XTickLabel', {'3x3', '5x5', '7x7', '9x9'});
    xlabel('Kernel Dimension (K x K)', 'FontWeight', 'bold');
    title('PSNR & SSIM Trajectory vs Kernel Size', 'FontSize', 10, 'FontWeight', 'bold');

    sgtitle('MATLAB Task 3.2: Spatial Mean Averaging Filter & Kernel Dimension Sensitivity Sweep', ...
            'FontSize', 13, 'FontWeight', 'bold');

    % Save figures
    out_dir_m = fullfile(exp_dir, 'Outputs', 'MATLAB');
    fig_dir = fullfile(exp_dir, 'Figures');

    out_path_1 = fullfile(out_dir_m, 'exp03_task_3_2_mean_kernel_sweep_m.png');
    out_path_2 = fullfile(fig_dir, 'exp03_task_3_2_mean_kernel_sweep_m.png');

    exportgraphics(fig, out_path_1, 'Resolution', 300);
    exportgraphics(fig, out_path_2, 'Resolution', 300);
    close(fig);

    fprintf('[SUCCESS] Saved MATLAB figure to:\n  %s\n  %s\n', out_path_1, out_path_2);
end
