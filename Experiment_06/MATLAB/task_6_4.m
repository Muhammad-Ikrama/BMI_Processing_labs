%% ==============================================================================
%% EXPERIMENT 06 - TASK 6.4: GAUSSIAN LP VS HP FILTERING & BOUNDARY ISOLATION (MATLAB)
%% Implements matching GLPF and GHPF (1 - GLPF) with D0 = 50.0, computes energy
%% retention, spatial mean, and Michelson contrast, proving complete DC elimination.
%% Course: Medical Image Processing | Riphah International University
%% Faculty: Engr. Rana Talha Khalid
%% ==============================================================================

function metrics = task_6_4()
    fprintf('==============================================================================\n');
    fprintf('EXPERIMENT 06 - TASK 6.4: GAUSSIAN LP VS HP FILTERING (MATLAB)\n');
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

    % Distance Matrix & Filters (D0 = 50.0)
    u = (1:H) - floor(H / 2);
    v = (1:W) - floor(W / 2);
    [V, U] = meshgrid(v, u);
    D = hypot(U, V);
    D0 = 50.0;

    H_GLPF = exp(- (D.^2) ./ (2.0 * (D0^2)));
    H_GHPF = 1.0 - H_GLPF;

    fprintf('[INFO] GLPF DC Value H(0,0): %.4f (Unity Pass)\n', H_GLPF(floor(H/2)+1, floor(W/2)+1));
    fprintf('[INFO] GHPF DC Value H(0,0): %.4f (Total Block / 0 DC)\n', H_GHPF(floor(H/2)+1, floor(W/2)+1));

    % Reconstructed outputs
    g_glpf_raw = real(ifft2(ifftshift(F_shift .* H_GLPF)));
    g_ghpf_raw = real(ifft2(ifftshift(F_shift .* H_GHPF)));

    img_glpf = uint8(min(max(g_glpf_raw, 0), 255));
    img_ghpf_bipolar = uint8(min(max(g_ghpf_raw + 128.0, 0), 255));
    img_ghpf_mag = uint8(min(max(abs(g_ghpf_raw) * 2.0, 0), 255));

    imwrite(img_glpf, fullfile(out_mat_dir, 'exp06_task_6_4_glpf_smooth_m.png'));
    imwrite(img_ghpf_bipolar, fullfile(out_mat_dir, 'exp06_task_6_4_ghpf_bipolar_m.png'));
    imwrite(img_ghpf_mag, fullfile(out_mat_dir, 'exp06_task_6_4_ghpf_magnitude_m.png'));

    % Metrics calculation
    calc_row = @(raw_arr, h_filt) struct(...
        'ret', (sum(abs(F_shift(:) .* h_filt(:)).^2) / total_energy) * 100.0, ...
        'mean_b', mean(raw_arr(:)), ...
        'std_b', std(raw_arr(:)), ...
        'mich', (max(abs(raw_arr(:))) - min(abs(raw_arr(:)))) / (max(abs(raw_arr(:))) + min(abs(raw_arr(:))) + 1e-8), ...
        'rms', std(raw_arr(:)) / (abs(mean(raw_arr(:))) + 1e-8));

    m_glpf = calc_row(g_glpf_raw, H_GLPF);
    m_ghpf = calc_row(g_ghpf_raw, H_GHPF);

    fprintf('\n%-26s | %-14s | %-12s | %-10s | %-12s\n', 'Condition', 'Energy Ret (%)', 'Mean Brightness', 'Std Dev', 'Michelson');
    fprintf('--------------------------------------------------------------------------------------\n');
    fprintf('%-26s | %-14.2f | %-12.2f | %-10.2f | %-12.4f\n', 'Gaussian Low-Pass (GLPF)', m_glpf.ret, m_glpf.mean_b, m_glpf.std_b, m_glpf.mich);
    fprintf('%-26s | %-14.2f | %-12.4f | %-10.2f | %-12.4f\n', 'Gaussian High-Pass (GHPF)', m_ghpf.ret, m_ghpf.mean_b, m_ghpf.std_b, m_ghpf.mich);
    fprintf('>>> Proof: GHPF eliminates bulk DC background (Mean = %.4f ~ 0.0), isolating boundaries!\n', m_ghpf.mean_b);

    % Multi-panel Figure
    fig = figure('Visible', 'off', 'Color', 'white', 'Position', [100, 100, 1500, 950]);

    subplot(2, 3, 1);
    imshow(H_GLPF, []);
    colormap(gca, 'parula');
    title({'(a) GLPF Transfer Function H_{GLP}(u,v)', sprintf('D_0=%.0f px | Low-Pass Core', D0)}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 2);
    imshow(H_GHPF, []);
    colormap(gca, 'parula');
    title({'(b) GHPF Transfer Function H_{GHP}(u,v)', '1 - H_{GLP} | Center DC Hollowed to 0'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 3);
    d_vals = linspace(0, 150, 500);
    h_glp_1d = exp(- (d_vals.^2) ./ (2.0 * (D0^2)));
    h_ghp_1d = 1.0 - h_glp_1d;
    plot(d_vals, h_glp_1d, 'g-', 'LineWidth', 2.0);
    hold on;
    plot(d_vals, h_ghp_1d, 'r-', 'LineWidth', 2.0);
    xline(D0, 'k--', sprintf('D_0=%.0f px', D0), 'LineWidth', 1.2);
    xlabel('Radial Frequency Distance D (pixels)', 'FontWeight', 'bold');
    ylabel('Transfer Magnitude H(D)', 'FontWeight', 'bold');
    legend({'GLPF H_{LP}(D)', 'GHPF H_{HP}(D) = 1 - H_{LP}'}, 'Location', 'east');
    grid on;
    title({'(c) Complementary Radial Transfer Functions', '(H_{LP} + H_{HP} = 1.0 Across All D)'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 4);
    imshow(img_glpf);
    title({'(d) GLPF Output (Smooth Parenchyma)', sprintf('Energy: %.1f%% | Mean: %.1f | RMS: %.2f', m_glpf.ret, m_glpf.mean_b, m_glpf.rms), '(Bulk Anatomy Preserved, 0 Ringing)'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.08, 0.50, 0.24]);

    subplot(2, 3, 5);
    imshow(img_ghpf_bipolar);
    title({'(e) GHPF Bipolar Map (g + 128)', sprintf('Energy: %.1f%% | Mean: %.2f ~ 0', m_ghpf.ret, m_ghpf.mean_b), '(DC Removed, Bone/Vessel Interface Raised)'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.73, 0.11, 0.11]);

    subplot(2, 3, 6);
    imshow(img_ghpf_mag);
    colormap(gca, 'hot');
    title({'(f) GHPF Edge Isolation Map (|g| x 2)', sprintf('Michelson Contrast: %.3f', m_ghpf.mich), '(Isolated Cranial Vault, Ventricles, Sulci)'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.58, 0.20, 0.92]);

    sgtitle('Experiment 06 - Task 6.4: Gaussian Low-Pass vs. High-Pass Filtering for Boundary Isolation (MATLAB)', ...
            'FontSize', 13, 'FontWeight', 'bold', 'Color', [0.06, 0.09, 0.16]);

    fig_path = fullfile(fig_dir, 'exp06_task_6_4_glpf_ghpf_contrast_m.png');
    saveas(fig, fig_path);
    close(fig);
    fprintf('[SUCCESS] Figure saved at: %s\n', fig_path);

    metrics = struct('glpf', m_glpf, 'ghpf', m_ghpf);
end
