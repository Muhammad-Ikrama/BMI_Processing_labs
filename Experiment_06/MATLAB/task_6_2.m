%% ==============================================================================
%% EXPERIMENT 06 - TASK 6.2: GIBBS PHENOMENON & RINGING ARTIFACT ANALYSIS (MATLAB)
%% Implements Ideal Low-Pass Filters with D0 in [20, 40, 80] pixels, extracts
%% 1-D cranial edge transect, quantifies ripple amplitude, and analyzes Gibbs artifacts.
%% Course: Medical Image Processing | Riphah International University
%% Faculty: Engr. Rana Talha Khalid
%% ==============================================================================

function metrics = task_6_2()
    fprintf('==============================================================================\n');
    fprintf('EXPERIMENT 06 - TASK 6.2: GIBBS RINGING & ILPF ANALYSIS (MATLAB)\n');
    fprintf('==============================================================================\n');

    % Setup paths
    script_dir = fileparts(mfilename('fullpath'));
    exp_dir = fullfile(script_dir, '..');
    img_path = fullfile(exp_dir, 'Inputs', 'images', 'MRI.jpg');
    if ~exist(img_path, 'file')
        img_path = fullfile(exp_dir, '..', '..', 'images', 'MRI.jpg');
    end

    out_mat_dir = fullfile(exp_dir, 'Outputs', 'MATLAB');
    fig_dir = fullfile(exp_dir, 'Figures');
    if ~exist(out_mat_dir, 'dir'); mkdir(out_mat_dir); end
    if ~exist(fig_dir, 'dir'); mkdir(fig_dir); end

    % Load image
    img = imread(img_path);
    if size(img, 3) == 3; img = rgb2gray(img); end
    [H, W] = size(img);

    % 2D FFT & Centering
    F = fft2(double(img));
    F_shift = fftshift(F);
    total_energy = sum(abs(F_shift(:)).^2);

    % Distance Matrix
    u = (1:H) - floor(H / 2);
    v = (1:W) - floor(W / 2);
    [V, U] = meshgrid(v, u);
    D = hypot(U, V);

    cutoffs = [20.0, 40.0, 80.0];
    ilpf_images = cell(length(cutoffs), 1);
    metrics = cell(length(cutoffs), 6);

    % Transect Coordinates: Row 256, cols 50 to 190
    prof_row = 256;
    c_start = 50; c_end = 190;
    orig_profile = double(img(prof_row, c_start:c_end));
    col_coords = c_start:c_end;

    % Uniform Brain Parenchyma ROI: rows 240:270, cols 220:250
    roi_r = 240:270; roi_c = 220:250;
    orig_roi_std = std(double(img(roi_r, roi_c)), 0, 'all');

    apply_ilpf = @(h) uint8(min(max(real(ifft2(ifftshift(F_shift .* h))), 0), 255));

    fprintf('\n%-12s | %-14s | %-12s | %-10s | %-12s\n', 'Cutoff D0', 'Energy Ret (%)', 'PSNR (dB)', 'SSIM', 'ROI Std');
    fprintf('----------------------------------------------------------------------\n');
    for idx = 1:length(cutoffs)
        D0 = cutoffs(idx);
        h = double(D <= D0);
        im_out = apply_ilpf(h);
        ilpf_images{idx} = im_out;

        imwrite(im_out, fullfile(out_mat_dir, sprintf('exp06_task_6_2_ilpf_D0_%d_m.png', round(D0))));

        ret_pct = (sum(abs(F_shift(:) .* h(:)).^2) / total_energy) * 100.0;
        p_val = psnr(im_out, img);
        s_val = ssim(im_out, img);

        rec_prof = double(im_out(prof_row, c_start:c_end));
        p2p_ripple = max(rec_prof(70:120)) - min(rec_prof(70:120));
        roi_std = std(double(im_out(roi_r, roi_c)), 0, 'all');

        metrics{idx, 1} = D0;
        metrics{idx, 2} = ret_pct;
        metrics{idx, 3} = p_val;
        metrics{idx, 4} = s_val;
        metrics{idx, 5} = p2p_ripple;
        metrics{idx, 6} = roi_std;

        fprintf('%-12d | %-14.2f | %-12.2f | %-10.4f | %-12.2f\n', ...
                round(D0), ret_pct, p_val, s_val, roi_std);
    end

    % Multi-panel Figure
    fig = figure('Visible', 'off', 'Color', 'white', 'Position', [100, 100, 1500, 950]);

    subplot(2, 3, 1);
    imshow(img);
    hold on;
    plot([c_start, c_end], [prof_row, prof_row], 'c-', 'LineWidth', 2);
    rectangle('Position', [roi_c(1), roi_r(1), length(roi_c), length(roi_r)], ...
              'EdgeColor', 'y', 'LineStyle', '--', 'LineWidth', 1.5);
    title({'(a) Clinical MRI with Transect (Cyan)', sprintf('Row %d, Cols [%d, %d]', prof_row, c_start, c_end)}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 2);
    imshow(ilpf_images{1});
    title({'(b) ILPF (D_0=20 px)', sprintf('Energy: %.2f%% | PSNR: %.2f dB', metrics{1,2}, metrics{1,3}), 'Severe Low-Frequency Ringing'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.73, 0.11, 0.11]);

    subplot(2, 3, 3);
    imshow(ilpf_images{2});
    title({'(c) ILPF (D_0=40 px)', sprintf('Energy: %.2f%% | PSNR: %.2f dB', metrics{2,2}, metrics{2,3}), 'Noticeable Sinc Ripple Halos'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.73, 0.11, 0.11]);

    subplot(2, 3, 4);
    imshow(ilpf_images{3});
    title({'(d) ILPF (D_0=80 px)', sprintf('Energy: %.2f%% | PSNR: %.2f dB', metrics{3,2}, metrics{3,3}), 'Tight High-Frequency Ringing'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.73, 0.11, 0.11]);

    subplot(2, 3, 5);
    plot(col_coords, orig_profile, 'k-', 'LineWidth', 1.5);
    hold on;
    colors = {'r--', 'b-', 'g:'};
    for idx = 1:3
        rec_prof = double(ilpf_images{idx}(prof_row, c_start:c_end));
        plot(col_coords, rec_prof, colors{idx}, 'LineWidth', 1.4);
    end
    xlabel('Column Pixel Coordinate', 'FontWeight', 'bold');
    ylabel('Pixel Intensity (0-255)', 'FontWeight', 'bold');
    legend({'Original MRI', 'D_0=20 (Broad)', 'D_0=40 (Distinct)', 'D_0=80 (Fast)'}, 'Location', 'northeast');
    grid on;
    title({'(e) 1-D Cranial Edge Profile Comparison', '(Gibbs Overshoot & Sinc Ripples)'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 6);
    p2p_arr = [metrics{1,5}, metrics{2,5}, metrics{3,5}];
    std_arr = [metrics{1,6}, metrics{2,6}, metrics{3,6}];
    bar_data = [p2p_arr; std_arr]';
    bar(bar_data);
    set(gca, 'XTickLabel', {'D_0=20', 'D_0=40', 'D_0=80'}, 'FontWeight', 'bold');
    ylabel('Intensity Variation', 'FontWeight', 'bold');
    legend({'P2P Ripple Amp', 'ROI Ripple Std'}, 'Location', 'northwest');
    grid on;
    title('(f) Ringing Severity & Artifact Quantification', 'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    sgtitle('Experiment 06 - Task 6.2: Gibbs Phenomenon & Ringing Artifact Analysis of Ideal Low-Pass Filters (MATLAB)', ...
            'FontSize', 13, 'FontWeight', 'bold', 'Color', [0.06, 0.09, 0.16]);

    fig_path = fullfile(fig_dir, 'exp06_task_6_2_ilpf_gibbs_ringing_m.png');
    saveas(fig, fig_path);
    close(fig);
    fprintf('[SUCCESS] Figure saved at: %s\n', fig_path);
end
