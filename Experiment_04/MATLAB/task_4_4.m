%% ==============================================================================
%% SCRIPT: task_4_4.m
%% Experiment 04: Noise Modeling & Adaptive Filtering in Medical Images
%% Task 4.4: Custom Adaptive Median Filter (AMF) & High-Density Stress Test
%% Course: Medical Image Processing | Riphah International University
%% Instructor: Engr. Rana Talha Khalid
%% ==============================================================================

function task_4_4()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 04 - MATLAB TASK 4.4: ADAPTIVE MEDIAN (AMF) STRESS TEST\n');
    fprintf('======================================================================\n');

    script_dir = fileparts(mfilename('fullpath'));
    exp_dir = fileparts(script_dir);
    img_path = fullfile(exp_dir, 'Inputs', 'images', 'MRI.jpg');

    if ~exist(img_path, 'file')
        img_path = fullfile(exp_dir, '..', '..', 'images', 'MRI.jpg');
    end

    ref = imread(img_path);
    if size(ref, 3) == 3; ref = rgb2gray(ref); end

    densities = [0.10, 0.25, 0.40, 0.50];
    med3_psnr = zeros(1, 4);
    med3_ssim = zeros(1, 4);
    amf_psnr  = zeros(1, 4);
    amf_ssim  = zeros(1, 4);

    med3_imgs = cell(1, 4);
    amf_imgs  = cell(1, 4);

    fprintf('%-10s | %-14s | %-14s | %-12s | %-10s | %-14s\n', ...
            'Density', 'Med 3x3 PSNR', 'Med 3x3 SSIM', 'AMF PSNR', 'AMF SSIM', 'AMF Advantage');
    fprintf('--------------------------------------------------------------------------------------\n');

    for idx = 1:4
        d = densities(idx);
        rng(42);
        noisy = imnoise(ref, 'salt & pepper', d);

        % Standard Median 3x3
        f_med3 = medfilt2(noisy, [3 3], 'symmetric');
        p_m3 = psnr(f_med3, ref);
        s_m3 = ssim(f_med3, ref);

        % Adaptive Median Filter (3 to 7/9)
        f_amf = run_matlab_amf(noisy, 3, 7);
        p_amf = psnr(f_amf, ref);
        s_amf = ssim(f_amf, ref);

        med3_psnr(idx) = p_m3;
        med3_ssim(idx) = s_m3;
        amf_psnr(idx)  = p_amf;
        amf_ssim(idx)  = s_amf;

        med3_imgs{idx} = f_med3;
        amf_imgs{idx}  = f_amf;

        fprintf('%2d%% noise   | %-14.2f | %-14.4f | %-12.2f | %-10.4f | +%.2f dB gain\n', ...
                round(d*100), p_m3, s_m3, p_amf, s_amf, p_amf - p_m3);
    end
    fprintf('--------------------------------------------------------------------------------------\n');

    % Visualization: 2 Rows x 4 Columns
    fig = figure('Visible', 'off', 'Position', [100, 100, 1400, 750]);

    for idx = 1:4
        d = densities(idx);

        % Top Row: Standard Median
        subplot(2, 4, idx);
        imshow(med3_imgs{idx});
        title(sprintf('Standard Med 3x3 (%d%% Noise)\nPSNR: %.2f dB | SSIM: %.4f', ...
                      round(d*100), med3_psnr(idx), med3_ssim(idx)), ...
              'FontSize', 9, 'FontWeight', 'bold');

        % Bottom Row: AMF
        subplot(2, 4, idx + 4);
        imshow(amf_imgs{idx});
        title(sprintf('Adaptive AMF (%d%% Noise)\nPSNR: %.2f dB | SSIM: %.4f', ...
                      round(d*100), amf_psnr(idx), amf_ssim(idx)), ...
              'FontSize', 9, 'FontWeight', 'bold', 'Color', [0.08 0.50 0.24]);
    end

    sgtitle('MATLAB Task 4.4: Custom Two-Stage Adaptive Median Filter (AMF) Stress Test (10% to 50%)', ...
            'FontSize', 13, 'FontWeight', 'bold');

    out_dir_m = fullfile(exp_dir, 'Outputs', 'MATLAB');
    fig_dir = fullfile(exp_dir, 'Figures');

    out_path_1 = fullfile(out_dir_m, 'exp04_task_4_4_adaptive_median_stress_m.png');
    out_path_2 = fullfile(fig_dir, 'exp04_task_4_4_adaptive_median_stress_m.png');

    exportgraphics(fig, out_path_1, 'Resolution', 300);
    exportgraphics(fig, out_path_2, 'Resolution', 300);
    close(fig);

    fprintf('[SUCCESS] Saved MATLAB figure to:\n  %s\n  %s\n', out_path_1, out_path_2);
end

function out = run_matlab_amf(im, s_min, s_max)
    % Fast MATLAB Two-Stage Adaptive Median Filter
    out = im;
    [H, W] = size(im);
    pad = floor(s_max / 2);
    padded = padarray(im, [pad pad], 'symmetric');

    % Loop over pixels
    for r = 1:H
        for c = 1:W
            pr = r + pad;
            pc = c + pad;
            k = s_min;
            while k <= s_max
                rad = floor(k / 2);
                sub = padded(pr - rad : pr + rad, pc - rad : pc + rad);
                zmin = min(sub(:));
                zmax = max(sub(:));
                zmed = median(sub(:));
                zxy  = padded(pr, pc);

                % Stage A: Check if median is clean
                if zmin < zmed && zmed < zmax
                    % Stage B: Check if center is clean
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
