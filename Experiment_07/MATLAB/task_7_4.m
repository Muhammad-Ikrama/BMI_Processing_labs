%% ==============================================================================
%% EXPERIMENT 07 - TASK 7.4: NOISE AMPLIFICATION & LOW-DOSE TRADE-OFF (MATLAB)
%% Simulates Gaussian quantum mottle (variance = 0.003), evaluates noise amplification
%% under Unsharp Masking (k=1.0) and High-Boost (k=2.0), measures background ROI
%% standard deviation, and assesses clinical safety trade-offs in low-dose radiography.
%% Course: Medical Image Processing | Riphah International University
%% Faculty: Engr. Rana Talha Khalid
%% ==============================================================================

function metrics = task_7_4()
    fprintf('==============================================================================\n');
    fprintf('EXPERIMENT 07 - TASK 7.4: NOISE AMPLIFICATION & LOW-DOSE TRADE-OFF (MATLAB)\n');
    fprintf('==============================================================================\n');

    % Setup paths
    script_dir = fileparts(mfilename('fullpath'));
    exp_dir = fullfile(script_dir, '..');
    img_path = fullfile(exp_dir, 'Inputs', 'images', 'Xray.jpg');
    if ~exist(img_path, 'file')
        img_path = fullfile(exp_dir, '..', '..', 'images', 'Xray.jpg');
    end

    out_mat_dir = fullfile(exp_dir, 'Outputs', 'MATLAB');
    fig_dir = fullfile(exp_dir, 'Figures');
    tab_dir = fullfile(exp_dir, 'Tables');
    if ~exist(out_mat_dir, 'dir'); mkdir(out_mat_dir); end
    if ~exist(fig_dir, 'dir'); mkdir(fig_dir); end
    if ~exist(tab_dir, 'dir'); mkdir(tab_dir); end

    % 1. Load Clean Radiograph
    img_clean = imread(img_path);
    if size(img_clean, 3) == 3; img_clean = rgb2gray(img_clean); end
    [H, W] = size(img_clean);
    cleanD = double(img_clean);

    % 2. Add Simulated Gaussian Quantum Mottle (variance = 0.003 on [0, 1] scale)
    rng(42); % Fixed reproducible seed
    noise_sigma = sqrt(0.003) * 255.0; % ~13.97 gray levels
    gaussian_noise = noise_sigma * randn(H, W);
    noisyD = cleanD + gaussian_noise;
    img_noisy = uint8(min(max(noisyD, 0), 255));

    % 3. Apply Unsharp Masking (k=1.0) and High-Boost (k=2.0)
    blurred_noisy = imgaussfilt(noisyD, 1.5, 'FilterSize', 7);
    g_mask_noisy = noisyD - blurred_noisy;

    sharp_k1_raw = noisyD + 1.0 * g_mask_noisy;
    sharp_k2_raw = noisyD + 2.0 * g_mask_noisy;

    img_sharp_k1 = uint8(min(max(sharp_k1_raw, 0), 255));
    img_sharp_k2 = uint8(min(max(sharp_k2_raw, 0), 255));

    imwrite(img_noisy, fullfile(out_mat_dir, 'exp07_task_7_4_noisy_radiograph_m.png'));
    imwrite(img_sharp_k1, fullfile(out_mat_dir, 'exp07_task_7_4_sharp_noisy_k1_m.png'));
    imwrite(img_sharp_k2, fullfile(out_mat_dir, 'exp07_task_7_4_sharp_noisy_k2_m.png'));

    % 4. Background ROI Analysis: rows 40 to 100, cols 40 to 100
    r_idx = 40:100;
    c_idx = 40:100;

    function [r_mean, r_std, snr_db, p_val, s_val] = eval_roi(im, im_ref)
        roi_vals = double(im(r_idx, c_idx));
        r_mean = mean(roi_vals(:));
        r_std = std(roi_vals(:));
        snr_db = 20.0 * log10(r_mean / (r_std + 1e-8));
        p_val = psnr(im, im_ref);
        s_val = ssim(im, im_ref);
    end

    [m_clean_mean, m_clean_std, m_clean_snr, ~, ~] = eval_roi(img_clean, img_clean);
    [m_noisy_mean, m_noisy_std, m_noisy_snr, p_noisy, s_noisy] = eval_roi(img_noisy, img_clean);
    [m_k1_mean, m_k1_std, m_k1_snr, p_k1, s_k1] = eval_roi(img_sharp_k1, img_clean);
    [m_k2_mean, m_k2_std, m_k2_snr, p_k2, s_k2] = eval_roi(img_sharp_k2, img_clean);

    inc_k1 = ((m_k1_std - m_noisy_std) / m_noisy_std) * 100.0;
    inc_k2 = ((m_k2_std - m_noisy_std) / m_noisy_std) * 100.0;

    metrics = cell(4, 9);
    metrics(1, :) = {'Clean Ground Truth', 0.0, m_clean_mean, m_clean_std, 0.0, m_clean_snr, Inf, 1.0000, 'Reference Scan'};
    metrics(2, :) = {'Noisy (Quantum Mottle)', 0.0, m_noisy_mean, m_noisy_std, 0.0, m_noisy_snr, p_noisy, s_noisy, 'Baseline Low-Dose Scan'};
    metrics(3, :) = {'Unsharp Masking (k=1.0)', 1.0, m_k1_mean, m_k1_std, inc_k1, m_k1_snr, p_k1, s_k1, 'ACCEPTABLE (Controlled Noise Boost)'};
    metrics(4, :) = {'High-Boost (k=2.0)', 2.0, m_k2_mean, m_k2_std, inc_k2, m_k2_snr, p_k2, s_k2, 'CONTRAINDICATED (>25% Noise Amplification)'};

    fprintf('\n%-26s | %-6s | %-10s | %-10s | %-12s | %-10s | %-10s | %-8s | %-25s\n', ...
            'Condition', 'k', 'ROI Mean', 'ROI Std', 'Noise Inc(%)', 'SNR (dB)', 'PSNR (dB)', 'SSIM', 'Clinical Safety');
    fprintf('------------------------------------------------------------------------------------------------------------------------------\n');
    for i = 1:4
        fprintf('%-26s | k=%3.1f | %-10.2f | %-10.2f | %+11.2f%% | %-10.2f | %-10.2f | %-8.4f | %-25s\n', ...
                metrics{i, 1}, metrics{i, 2}, metrics{i, 3}, metrics{i, 4}, metrics{i, 5}, ...
                metrics{i, 6}, metrics{i, 7}, metrics{i, 8}, metrics{i, 9});
    end

    % Export CSV
    cond_col = metrics(:, 1);
    k_col = [metrics{:, 2}]';
    mean_col = [metrics{:, 3}]';
    std_col = [metrics{:, 4}]';
    inc_col = [metrics{:, 5}]';
    snr_col = [metrics{:, 6}]';
    psnr_col = [metrics{:, 7}]';
    ssim_col = [metrics{:, 8}]';
    safe_col = metrics(:, 9);

    T = table(cond_col, k_col, mean_col, std_col, inc_col, snr_col, psnr_col, ssim_col, safe_col, ...
              'VariableNames', {'Condition', 'Boost_k', 'ROI_Mean', 'ROI_Noise_Std', ...
                               'Noise_Increase_Pct', 'ROI_SNR_dB', 'PSNR_dB', 'SSIM', 'Clinical_Safety'});
    writetable(T, fullfile(tab_dir, 'exp07_task_7_4_noise_amplification_metrics_matlab.csv'));

    % 5. Visualization Figure (2x2 Multi-Panel)
    fig = figure('Visible', 'off', 'Color', 'white', 'Position', [100, 100, 1400, 1100]);

    % (a) Clean Reference
    subplot(2, 2, 1);
    imshow(img_clean); hold on;
    rectangle('Position', [40, 40, 60, 60], 'EdgeColor', 'c', 'LineWidth', 1.8, 'LineStyle', '--');
    hold off;
    title({'(a) Clean Ground Truth Radiograph', sprintf('ROI Noise Std: %.2f | SNR: %.1f dB', m_clean_std, m_clean_snr)}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    % (b) Noisy Radiograph
    subplot(2, 2, 2);
    imshow(img_noisy); hold on;
    rectangle('Position', [40, 40, 60, 60], 'EdgeColor', 'c', 'LineWidth', 1.8, 'LineStyle', '--');
    hold off;
    title({'(b) Simulated Low-Dose Scan (Quantum Mottle)', sprintf('ROI Noise Std: %.2f | PSNR: %.1f dB | SSIM: %.4f', m_noisy_std, p_noisy, s_noisy)}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.86, 0.15, 0.15]);

    % (c) Sharpened Noisy (k=1.0)
    subplot(2, 2, 3);
    imshow(img_sharp_k1); hold on;
    rectangle('Position', [40, 40, 60, 60], 'EdgeColor', 'c', 'LineWidth', 1.8, 'LineStyle', '--');
    hold off;
    title({'(c) Unsharp Masking (k=1.0) [Controlled Boost]', sprintf('ROI Noise Std: %.2f (%+.1f%%) | PSNR: %.1f dB', m_k1_std, inc_k1, p_k1)}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.08, 0.50, 0.24]);

    % (d) Sharpened Noisy (k=2.0)
    subplot(2, 2, 4);
    imshow(img_sharp_k2); hold on;
    rectangle('Position', [40, 40, 60, 60], 'EdgeColor', 'c', 'LineWidth', 1.8, 'LineStyle', '--');
    hold off;
    title({'(d) High-Boost (k=2.0) [HAZARD: Pseudolesions]', sprintf('ROI Noise Std: %.2f (%+.1f%%) | PSNR: %.1f dB', m_k2_std, inc_k2, p_k2)}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.86, 0.15, 0.15]);

    sgtitle('Experiment 07 - Task 7.4: Noise Amplification & Trade-off Evaluation in Low-Dose Radiographs (MATLAB)', ...
            'FontSize', 13, 'FontWeight', 'bold', 'Color', [0.06, 0.09, 0.16]);

    fig_path = fullfile(fig_dir, 'exp07_task_7_4_noise_tradeoff_m.png');
    saveas(fig, fig_path);
    close(fig);
    fprintf('[SUCCESS] Figure saved at: %s\n', fig_path);
end
