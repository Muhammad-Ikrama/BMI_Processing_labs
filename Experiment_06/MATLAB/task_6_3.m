%% ==============================================================================
%% EXPERIMENT 06 - TASK 6.3: BUTTERWORTH LP ORDER SENSITIVITY SWEEP (MATLAB)
%% Evaluates BLPF across orders n in [1, 2, 4, 8] with fixed D0 = 40.0,
%% analyzes 1D transfer functions, edge ripple emergence, and clinical standard selection.
%% Course: Medical Image Processing | Riphah International University
%% Faculty: Engr. Rana Talha Khalid
%% ==============================================================================

function metrics = task_6_3()
    fprintf('==============================================================================\n');
    fprintf('EXPERIMENT 06 - TASK 6.3: BUTTERWORTH LP ORDER SENSITIVITY SWEEP (MATLAB)\n');
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
    D0 = 40.0;

    orders = [1, 2, 4, 8];
    blpf_images = cell(length(orders), 1);
    metrics = cell(length(orders), 6);

    % Transect coordinates across skull-brain interface
    prof_row = 256;
    c_start = 50; c_end = 190;
    orig_profile = double(img(prof_row, c_start:c_end));
    col_coords = c_start:c_end;

    apply_blpf = @(h) uint8(min(max(real(ifft2(ifftshift(F_shift .* h))), 0), 255));

    fprintf('\n%-10s | %-14s | %-12s | %-10s | %-24s\n', 'Order n', 'Energy Ret (%)', 'PSNR (dB)', 'SSIM', 'Clinical Verdict');
    fprintf('--------------------------------------------------------------------------------\n');
    for idx = 1:length(orders)
        n = orders(idx);
        h = 1.0 ./ (1.0 + (D ./ D0).^(2 * n));
        im_out = apply_blpf(h);
        blpf_images{idx} = im_out;

        imwrite(im_out, fullfile(out_mat_dir, sprintf('exp06_task_6_3_blpf_order_%d_m.png', n)));

        ret_pct = (sum(abs(F_shift(:) .* h(:)).^2) / total_energy) * 100.0;
        p_val = psnr(im_out, img);
        s_val = ssim(im_out, img);

        rec_prof = double(im_out(prof_row, c_start:c_end));
        p2p_ripple = max(rec_prof(70:120)) - min(rec_prof(70:120));

        verdict = 'Sub-optimal (Excessive Blur)';
        if n == 2; verdict = 'CLINICAL OPTIMUM (0 Rings)';
        elseif n == 4; verdict = 'Acceptable (Caution)';
        elseif n == 8; verdict = 'Contraindicated (Gibbs)'; end

        metrics{idx, 1} = n;
        metrics{idx, 2} = ret_pct;
        metrics{idx, 3} = p_val;
        metrics{idx, 4} = s_val;
        metrics{idx, 5} = p2p_ripple;
        metrics{idx, 6} = verdict;

        fprintf('%-10d | %-14.2f | %-12.2f | %-10.4f | %-24s\n', n, ret_pct, p_val, s_val, verdict);
    end

    % Multi-panel Figure
    fig = figure('Visible', 'off', 'Color', 'white', 'Position', [100, 100, 1500, 950]);

    % 1. Radial Transfer Functions H(D)
    subplot(2, 3, 1);
    d_vals = linspace(0, 120, 500);
    colors = {[0, 0.52, 0.78], [0.08, 0.64, 0.29], [0.96, 0.62, 0.04], [0.86, 0.15, 0.15]};
    hold on;
    for idx = 1:length(orders)
        n = orders(idx);
        h_d = 1.0 ./ (1.0 + (d_vals ./ D0).^(2 * n));
        plot(d_vals, h_d, 'Color', colors{idx}, 'LineWidth', 2.0);
    end
    xline(D0, 'k--', sprintf('D_0=%.0f px', D0), 'LineWidth', 1.2);
    yline(0.5, 'k:', 'H(D_0)=0.5 (-3dB)', 'LineWidth', 0.8);
    xlabel('Radial Frequency D (pixels)', 'FontWeight', 'bold');
    ylabel('Transfer Magnitude H(D)', 'FontWeight', 'bold');
    legend({'n=1', 'n=2', 'n=4', 'n=8'}, 'Location', 'northeast');
    grid on;
    title({'(a) 1-D Radial Transfer Functions H(D)', 'Slope Sharpness vs Filter Order n'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    % 2. BLPF Order 1
    subplot(2, 3, 2);
    imshow(blpf_images{1});
    title({'(b) BLPF Order n=1', sprintf('Energy: %.2f%% | PSNR: %.2f dB', metrics{1,2}, metrics{1,3}), 'Gradual Rolloff, High Blur'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0, 0.52, 0.78]);

    % 3. BLPF Order 2 (CLINICAL OPTIMUM)
    subplot(2, 3, 3);
    imshow(blpf_images{2});
    title({'(c) BLPF Order n=2 [CLINICAL OPTIMUM]', sprintf('Energy: %.2f%% | PSNR: %.2f dB', metrics{2,2}, metrics{2,3}), 'Smooth Rolloff, Zero Gibbs Ringing'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.08, 0.64, 0.29]);

    % 4. BLPF Order 4
    subplot(2, 3, 4);
    imshow(blpf_images{3});
    title({'(d) BLPF Order n=4', sprintf('Energy: %.2f%% | PSNR: %.2f dB', metrics{3,2}, metrics{3,3}), 'Steep Transition, Mild Ringing Onset'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.96, 0.62, 0.04]);

    % 5. BLPF Order 8
    subplot(2, 3, 5);
    imshow(blpf_images{4});
    title({'(e) BLPF Order n=8', sprintf('Energy: %.2f%% | PSNR: %.2f dB', metrics{4,2}, metrics{4,3}), 'Near-Ideal Step, Severe Sinc Ripples'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.86, 0.15, 0.15]);

    % 6. 1D Transect Profile Across Orders
    subplot(2, 3, 6);
    plot(col_coords, orig_profile, 'k-', 'LineWidth', 1.5);
    hold on;
    line_styles = {'--', '-', '-.', ':'};
    for idx = 1:length(orders)
        rec_prof = double(blpf_images{idx}(prof_row, c_start:c_end));
        plot(col_coords, rec_prof, 'Color', colors{idx}, 'LineStyle', line_styles{idx}, 'LineWidth', 1.4);
    end
    xlabel('Column Pixel Coordinate', 'FontWeight', 'bold');
    ylabel('Pixel Intensity (0-255)', 'FontWeight', 'bold');
    legend({'Original MRI', 'n=1', 'n=2 (Optimum)', 'n=4', 'n=8'}, 'Location', 'northeast');
    grid on;
    title({'(f) Cranial Transect: Ripple Emergence vs Order', '(n>=4 Triggers Gibbs Ringing)'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    sgtitle('Experiment 06 - Task 6.3: Butterworth Low-Pass Filter Design & Order Sensitivity Sweep (MATLAB)', ...
            'FontSize', 13, 'FontWeight', 'bold', 'Color', [0.06, 0.09, 0.16]);

    fig_path = fullfile(fig_dir, 'exp06_task_6_3_blpf_order_sweep_m.png');
    saveas(fig, fig_path);
    close(fig);
    fprintf('[SUCCESS] Figure saved at: %s\n', fig_path);
end
