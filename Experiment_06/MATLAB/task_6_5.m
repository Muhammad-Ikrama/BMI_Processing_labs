%% ==============================================================================
%% EXPERIMENT 06 - TASK 6.5: MULTI-FILTER BENCHMARKING & DIAGNOSTIC REPORT (MATLAB)
%% Multi-panel 2x3 diagnostic report evaluating Input, Centered Spectrum, ILPF, BLPF,
%% GLPF, and GHPF, tabulating spectral energy, PSNR, SSIM, and exporting benchmark CSV.
%% Course: Medical Image Processing | Riphah International University
%% Faculty: Engr. Rana Talha Khalid
%% ==============================================================================

function summary_table = task_6_5()
    fprintf('==============================================================================\n');
    fprintf('EXPERIMENT 06 - TASK 6.5: MULTI-FILTER BENCHMARKING & REPORT (MATLAB)\n');
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
    tab_dir = fullfile(exp_dir, 'Tables');
    if ~exist(out_mat_dir, 'dir'); mkdir(out_mat_dir); end
    if ~exist(fig_dir, 'dir'); mkdir(fig_dir); end
    if ~exist(tab_dir, 'dir'); mkdir(tab_dir); end

    % Load image
    img = imread(img_path);
    if size(img, 3) == 3; img = rgb2gray(img); end
    [H, W] = size(img);

    % 2D FFT & Centering
    F = fft2(double(img));
    F_shift = fftshift(F);
    mag_spectrum = log(1.0 + abs(F_shift));
    total_energy = sum(abs(F_shift(:)).^2);

    % Distance Matrix
    u = (1:H) - floor(H / 2);
    v = (1:W) - floor(W / 2);
    [V, U] = meshgrid(v, u);
    D = hypot(U, V);

    D0_lp = 40.0;
    D0_hp = 50.0;

    H_ILPF = double(D <= D0_lp);
    H_BLPF = 1.0 ./ (1.0 + (D ./ D0_lp).^(2 * 2));
    H_GLPF = exp(- (D.^2) ./ (2.0 * (D0_lp^2)));
    H_GHPF = 1.0 - exp(- (D.^2) ./ (2.0 * (D0_hp^2)));

    apply_f = @(h) real(ifft2(ifftshift(F_shift .* h)));

    g_ilpf = apply_f(H_ILPF);
    g_blpf = apply_f(H_BLPF);
    g_glpf = apply_f(H_GLPF);
    g_ghpf = apply_f(H_GHPF);

    img_ilpf = uint8(min(max(g_ilpf, 0), 255));
    img_blpf = uint8(min(max(g_blpf, 0), 255));
    img_glpf = uint8(min(max(g_glpf, 0), 255));
    img_ghpf_vis = uint8(min(max(abs(g_ghpf) * 2.2, 0), 255));

    imwrite(img_ilpf, fullfile(out_mat_dir, 'exp06_task_6_5_ilpf_m.png'));
    imwrite(img_blpf, fullfile(out_mat_dir, 'exp06_task_6_5_blpf_m.png'));
    imwrite(img_glpf, fullfile(out_mat_dir, 'exp06_task_6_5_glpf_m.png'));
    imwrite(img_ghpf_vis, fullfile(out_mat_dir, 'exp06_task_6_5_ghpf_m.png'));

    % Benchmarking
    ret_ilpf = (sum(abs(F_shift(:) .* H_ILPF(:)).^2) / total_energy) * 100.0;
    ret_blpf = (sum(abs(F_shift(:) .* H_BLPF(:)).^2) / total_energy) * 100.0;
    ret_glpf = (sum(abs(F_shift(:) .* H_GLPF(:)).^2) / total_energy) * 100.0;
    ret_ghpf = (sum(abs(F_shift(:) .* H_GHPF(:)).^2) / total_energy) * 100.0;

    psnr_ilpf = psnr(img_ilpf, img);
    psnr_blpf = psnr(img_blpf, img);
    psnr_glpf = psnr(img_glpf, img);
    psnr_ghpf = psnr(img_ghpf_vis, img);

    ssim_ilpf = ssim(img_ilpf, img);
    ssim_blpf = ssim(img_blpf, img);
    ssim_glpf = ssim(img_glpf, img);
    ssim_ghpf = ssim(img_ghpf_vis, img);

    % Build summary table
    Filter_Name = {'Ideal Low-Pass (ILPF)'; 'Butterworth LP (n=2)'; 'Gaussian LP (GLPF)'; 'Gaussian High-Pass (GHPF)'};
    Filter_Class = {'Low-Pass'; 'Low-Pass'; 'Low-Pass'; 'High-Pass'};
    Cutoff_D0 = [40; 40; 40; 50];
    Order_n = {'Infinite (Step)'; '2'; 'Gaussian'; 'Gaussian'};
    Energy_Retention_Pct = [ret_ilpf; ret_blpf; ret_glpf; ret_ghpf];
    PSNR_dB = [psnr_ilpf; psnr_blpf; psnr_glpf; psnr_ghpf];
    SSIM_Val = [ssim_ilpf; ssim_blpf; ssim_glpf; ssim_ghpf];
    Gibbs_Ringing = {'Severe (Concentric halos)'; 'Zero (Smooth rolloff)'; 'Zero (100% ripple-free)'; 'Zero (DC removed)'};
    Clinical_Verdict = {'Contraindicated (Mimics hematomas)'; 'GOLD STANDARD (Optimal denoising)'; 'EXCELLENT (Pre-segmentation)'; 'DIAGNOSTIC (Boundary isolation)'};

    summary_table = table(Filter_Name, Filter_Class, Cutoff_D0, Order_n, Energy_Retention_Pct, PSNR_dB, SSIM_Val, Gibbs_Ringing, Clinical_Verdict);
    csv_path = fullfile(tab_dir, 'exp06_benchmark_summary_matlab.csv');
    writetable(summary_table, csv_path);
    fprintf('\n[INFO] Comprehensive Diagnostic Benchmark saved at: %s\n', csv_path);
    disp(summary_table);

    % Multi-panel Figure
    fig = figure('Visible', 'off', 'Color', 'white', 'Position', [100, 100, 1500, 950]);

    subplot(2, 3, 1);
    imshow(img);
    title({'(a) Input Clinical Brain MRI Scan', 'f(x, y) | Matrix: 512x512 | Unfiltered'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 2);
    imshow(mag_spectrum, []);
    colormap(gca, 'jet');
    hold on;
    theta = linspace(0, 2*pi, 200);
    plot(W/2 + D0_lp*cos(theta), H/2 + D0_lp*sin(theta), 'c--', 'LineWidth', 1.8);
    plot(W/2 + D0_hp*cos(theta), H/2 + D0_hp*sin(theta), 'y:', 'LineWidth', 1.5);
    plot(W/2, H/2, 'w*', 'MarkerSize', 8, 'LineWidth', 1.5);
    legend({sprintf('LP D_0=%.0f', D0_lp), sprintf('HP D_0=%.0f', D0_hp)}, 'Location', 'southeast');
    title({'(b) Centered Log-Spectrum', 'D_0=40 px (Cyan LP) & D_0=50 px (Yellow HP)'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 3);
    imshow(img_ilpf);
    title({'(c) Ideal Low-Pass Filter (D_0=40)', sprintf('Energy: %.2f%% | PSNR: %.2f dB | SSIM: %.4f', ret_ilpf, psnr_ilpf, ssim_ilpf), '[CONTRAINDICATED: Severe Gibbs Ringing]'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.73, 0.11, 0.11]);

    subplot(2, 3, 4);
    imshow(img_blpf);
    title({'(d) Butterworth LP (n=2, D_0=40)', sprintf('Energy: %.2f%% | PSNR: %.2f dB | SSIM: %.4f', ret_blpf, psnr_blpf, ssim_blpf), '[GOLD STANDARD: 0 Ringing, Smooth]'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.08, 0.50, 0.24]);

    subplot(2, 3, 5);
    imshow(img_glpf);
    title({'(e) Gaussian Low-Pass Filter (D_0=40)', sprintf('Energy: %.2f%% | PSNR: %.2f dB | SSIM: %.4f', ret_glpf, psnr_glpf, ssim_glpf), '[OPTIMAL PRE-FILTER: 100% Ripple-Free]'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 6);
    imshow(img_ghpf_vis);
    colormap(gca, 'hot');
    title({'(f) Gaussian High-Pass Filter (D_0=50)', sprintf('Energy: %.2f%% (High-Frequency Core)', ret_ghpf), '[DC Eliminated: Cortical Margin Isolation]'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.58, 0.20, 0.92]);

    sgtitle('Experiment 06 - Task 6.5: Multi-Filter Quantitative Benchmarking & Comprehensive Diagnostic Report (MATLAB)', ...
            'FontSize', 13, 'FontWeight', 'bold', 'Color', [0.06, 0.09, 0.16]);

    fig_path = fullfile(fig_dir, 'exp06_task_6_5_diagnostic_report_m.png');
    saveas(fig, fig_path);
    close(fig);
    fprintf('[SUCCESS] Figure saved at: %s\n', fig_path);
end
