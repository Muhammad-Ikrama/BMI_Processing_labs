%% ==============================================================================
%% SCRIPT: task_4_5.m
%% Experiment 04: Noise Modeling & Adaptive Filtering in Medical Images
%% Task 4.5: Multi-Panel Diagnostic Restoration Report (MATLAB)
%% Course: Medical Image Processing | Riphah International University
%% Instructor: Engr. Rana Talha Khalid
%% ==============================================================================

function task_4_5()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 04 - MATLAB TASK 4.5: DIAGNOSTIC RESTORATION REPORT\n');
    fprintf('======================================================================\n');

    script_dir = fileparts(mfilename('fullpath'));
    exp_dir = fileparts(script_dir);
    img_path = fullfile(exp_dir, 'Inputs', 'images', 'MRI.jpg');

    if ~exist(img_path, 'file')
        img_path = fullfile(exp_dir, '..', '..', 'images', 'MRI.jpg');
    end

    ref = imread(img_path);
    if size(ref, 3) == 3; ref = rgb2gray(ref); end

    [H, W] = size(ref);

    % 1. Simulate Mixed Noise: 10% SP + Gaussian (var = 0.005)
    rng(42);
    gNoisy = imnoise(ref, 'gaussian', 0, 0.005);
    noisy = imnoise(gNoisy, 'salt & pepper', 0.10);

    % 2. Filters
    h_mean5 = fspecial('average', [5 5]);
    mean5 = imfilter(noisy, h_mean5, 'replicate');
    med3 = medfilt2(noisy, [3 3], 'symmetric');

    % Fast AMF
    amf_out = run_matlab_amf_quick(noisy, 3, 7);

    % Helper for EPI
    h_lap = fspecial('laplacian', 0.2);
    calc_epi = @(im) sum((imfilter(double(ref), h_lap) - mean(imfilter(double(ref), h_lap), 'all')) .* ...
                         (imfilter(double(im), h_lap)  - mean(imfilter(double(im), h_lap), 'all')), 'all') / ...
                     sqrt(sum((imfilter(double(ref), h_lap) - mean(imfilter(double(ref), h_lap), 'all')).^2, 'all') * ...
                          sum((imfilter(double(im), h_lap)  - mean(imfilter(double(im), h_lap), 'all')).^2, 'all'));

    cases = {
        'Ground Truth Scan', ref;
        'Mixed Noisy Baseline', noisy;
        'Linear Mean 5x5', mean5;
        'Standard Median 3x3', med3;
        'Adaptive Median AMF', amf_out
    };

    fprintf('\n%-24s | %-10s | %-8s | %-10s | %-14s | %-12s\n', ...
            'Condition', 'PSNR (dB)', 'SSIM', 'EPI (beta)', 'BG Noise Var', 'Status');
    fprintf('----------------------------------------------------------------------------------------\n');

    for i = 1:size(cases, 1)
        im = cases{i, 2};
        name = cases{i, 1};
        if strcmp(name, 'Ground Truth Scan')
            p = Inf; s = 1.0; e = 1.0; status = 'Reference';
        else
            p = psnr(im, ref); s = ssim(im, ref); e = calc_epi(im);
            if i <= 3; status = 'Failure'; else; status = 'Good to Go'; end
        end
        bg_patch = double(im(10:50, 10:50));
        bg_var = var(bg_patch(:));

        if isinf(p)
            fprintf('%-24s | %-10s | %-8.4f | %-10.4f | %-14.2f | %-12s\n', name, 'Inf', s, e, bg_var, status);
        else
            fprintf('%-24s | %-10.2f | %-8.4f | %-10.4f | %-14.2f | %-12s\n', name, p, s, e, bg_var, status);
        end
    end
    fprintf('----------------------------------------------------------------------------------------\n');

    % 3. Extract 1D Anatomical Profile at Row H/2 across ventricular boundary
    row_idx = round(H / 2);
    c_start = 125; c_end = 175;
    cols = c_start:c_end;

    prof_ref   = double(ref(row_idx, cols));
    prof_noisy = double(noisy(row_idx, cols));
    prof_mean  = double(mean5(row_idx, cols));
    prof_med   = double(med3(row_idx, cols));
    prof_amf   = double(amf_out(row_idx, cols));

    % 4. Visualization: 2 Rows x 3 Columns
    fig = figure('Visible', 'off', 'Position', [100, 100, 1400, 900]);

    subplot(2, 3, 1);
    imshow(ref);
    title('A: Clean Reference MRI', 'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.12 0.23 0.54]);

    subplot(2, 3, 2);
    imshow(noisy);
    title(sprintf('B: Mixed Noisy Scan\nPSNR: %.2f dB | SSIM: %.4f', psnr(noisy, ref), ssim(noisy, ref)), ...
          'FontSize', 9.5, 'FontWeight', 'bold', 'Color', [0.72 0.15 0.15]);

    subplot(2, 3, 3);
    imshow(mean5);
    title(sprintf('C: Linear Mean 5x5 [Smear Failure]\nPSNR: %.2f dB | SSIM: %.4f', psnr(mean5, ref), ssim(mean5, ref)), ...
          'FontSize', 9.5, 'FontWeight', 'bold', 'Color', [0.72 0.15 0.15]);

    subplot(2, 3, 4);
    imshow(med3);
    title(sprintf('D: Standard Median 3x3\nPSNR: %.2f dB | SSIM: %.4f', psnr(med3, ref), ssim(med3, ref)), ...
          'FontSize', 9.5, 'FontWeight', 'bold', 'Color', [0.12 0.23 0.54]);

    subplot(2, 3, 5);
    imshow(amf_out);
    title(sprintf('E: Adaptive Median AMF\nPSNR: %.2f dB | SSIM: %.4f', psnr(amf_out, ref), ssim(amf_out, ref)), ...
          'FontSize', 9.5, 'FontWeight', 'bold', 'Color', [0.08 0.50 0.24]);

    subplot(2, 3, 6);
    plot(cols, prof_ref, '-k', 'LineWidth', 2.2, 'DisplayName', 'Reference');
    hold on;
    plot(cols, prof_noisy, '-', 'Color', [0.6 0.6 0.6], 'LineWidth', 0.9, 'DisplayName', 'Noisy Scan');
    plot(cols, prof_mean, '--r', 'LineWidth', 1.8, 'DisplayName', 'Mean 5x5 (Smear)');
    plot(cols, prof_med, ':b', 'LineWidth', 1.8, 'DisplayName', 'Median 3x3');
    plot(cols, prof_amf, '-g', 'LineWidth', 2.0, 'DisplayName', 'Adaptive AMF');
    hold off;
    xlabel('Pixel Column (x)', 'FontWeight', 'bold');
    ylabel('Intensity Level', 'FontWeight', 'bold');
    title('F: 1D Anatomical Edge Profiles (Row 256)', 'FontSize', 9.5, 'FontWeight', 'bold');
    legend('Location', 'northwest', 'FontSize', 7.5);
    grid on;

    sgtitle('MATLAB Task 4.5: Quantitative Benchmarking & Multi-Panel Diagnostic Restoration Report', ...
            'FontSize', 13, 'FontWeight', 'bold');

    out_dir_m = fullfile(exp_dir, 'Outputs', 'MATLAB');
    fig_dir = fullfile(exp_dir, 'Figures');

    out_path_1 = fullfile(out_dir_m, 'exp04_task_4_5_diagnostic_report_m.png');
    out_path_2 = fullfile(fig_dir, 'exp04_task_4_5_diagnostic_report_m.png');

    exportgraphics(fig, out_path_1, 'Resolution', 300);
    exportgraphics(fig, out_path_2, 'Resolution', 300);
    close(fig);

    fprintf('[SUCCESS] Saved MATLAB figure to:\n  %s\n  %s\n', out_path_1, out_path_2);
end

function out = run_matlab_amf_quick(im, s_min, s_max)
    out = im;
    [H, W] = size(im);
    pad = floor(s_max / 2);
    padded = padarray(im, [pad pad], 'symmetric');

    for r = 1:H
        for c = 1:W
            pr = r + pad; pc = c + pad;
            k = s_min;
            while k <= s_max
                rad = floor(k / 2);
                sub = padded(pr - rad : pr + rad, pc - rad : pc + rad);
                zmin = min(sub(:)); zmax = max(sub(:));
                zmed = median(sub(:)); zxy = padded(pr, pc);
                if zmin < zmed && zmed < zmax
                    if zmin < zxy && zxy < zmax
                        out(r, c) = zxy;
                    else
                        out(r, c) = zmed;
                    end
                    break;
                else
                    k = k + 2;
                end
                if k > s_max
                    out(r, c) = zmed;
                    break;
                end
            end
        end
    end
end
