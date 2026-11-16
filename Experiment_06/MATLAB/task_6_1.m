%% ==============================================================================
%% EXPERIMENT 06 - TASK 6.1: 2-D DFT & MAGNITUDE SPECTRUM COMPUTATION (MATLAB)
%% Computes uncentered/centered 2D-DFT, log-magnitude spectrum, phase spectrum,
%% DC component localization, energy concentration, and crosshair profile analysis.
%% Course: Medical Image Processing | Riphah International University
%% Faculty: Engr. Rana Talha Khalid
%% ==============================================================================

function metrics = task_6_1()
    fprintf('==============================================================================\n');
    fprintf('EXPERIMENT 06 - TASK 6.1: 2-D DFT & MAGNITUDE SPECTRUM (MATLAB)\n');
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
    if size(img, 3) == 3
        img = rgb2gray(img);
    end
    [H, W] = size(img);
    mean_intensity = mean(double(img(:)));

    % 1. Forward 2D-DFT
    F_raw = fft2(double(img));
    F_shift = fftshift(F_raw);

    % 2. Spectra
    mag_raw = abs(F_raw);
    mag_shift = abs(F_shift);
    log_mag_raw = log(1.0 + mag_raw);
    log_mag_shift = log(1.0 + mag_shift);
    phase_shift = angle(F_shift);

    % 3. DC Component Coordinates
    % In MATLAB 1-based indexing:
    % Uncentered DC is at (1, 1)
    % Centered DC is at (floor(H/2)+1, floor(W/2)+1)
    dc_uncentered_idx = [1, 1];
    dc_centered_idx = [floor(H/2) + 1, floor(W/2) + 1];

    dc_val_uncentered = mag_raw(dc_uncentered_idx(1), dc_uncentered_idx(2));
    dc_val_centered = mag_shift(dc_centered_idx(1), dc_centered_idx(2));
    theoretical_dc = sum(double(img(:)));

    total_energy = sum(mag_shift(:).^2);
    dc_energy = dc_val_centered^2;
    dc_energy_fraction = (dc_energy / total_energy) * 100.0;

    fprintf('[INFO] Image Dimensions: %dx%d pixels\n', W, H);
    fprintf('[INFO] Spatial Mean Intensity: %.2f\n', mean_intensity);
    fprintf('[INFO] Theoretical DC Component (Sum of Pixels): %.2f\n', theoretical_dc);
    fprintf('[INFO] Uncentered DC Coordinate: (1, 1) | Measured DC: %.2f\n', dc_val_uncentered);
    fprintf('[INFO] Centered DC Coordinate: (%d, %d) | Measured DC: %.2f\n', ...
            dc_centered_idx(1), dc_centered_idx(2), dc_val_centered);
    fprintf('[INFO] Total Spectral Energy: %.3e\n', total_energy);
    fprintf('[INFO] DC Energy Fraction: %.2f%% of Total Power\n', dc_energy_fraction);

    % 4. Radial Energy Accumulation Curve
    u = (1:H) - floor(H / 2);
    v = (1:W) - floor(W / 2);
    [V, U] = meshgrid(v, u);
    D = hypot(U, V);

    max_radius = floor(min(H, W) / 2);
    radial_distances = 1:max_radius;
    cumulative_energy = zeros(size(radial_distances));
    for idx = 1:length(radial_distances)
        r = radial_distances(idx);
        mask = (D <= r);
        cumulative_energy(idx) = (sum(mag_shift(mask).^2) / total_energy) * 100.0;
    end

    r_90 = radial_distances(find(cumulative_energy >= 90.0, 1, 'first'));
    r_95 = radial_distances(find(cumulative_energy >= 95.0, 1, 'first'));
    r_99 = radial_distances(find(cumulative_energy >= 99.0, 1, 'first'));
    fprintf('[INFO] Radial Radius for 90%% Energy Retention: D <= %d pixels\n', r_90);
    fprintf('[INFO] Radial Radius for 95%% Energy Retention: D <= %d pixels\n', r_95);
    fprintf('[INFO] Radial Radius for 99%% Energy Retention: D <= %d pixels\n', r_99);

    % 5. Crosshair Profile Analysis
    horiz_arm = log_mag_shift(dc_centered_idx(1), :);
    diag_indices = sub2ind([H, W], 1:min(H, W), 1:min(H, W));
    diag_profile = log_mag_shift(diag_indices);

    % Save output images
    norm_log_raw = uint8(mat2gray(log_mag_raw) * 255);
    norm_log_shift = uint8(mat2gray(log_mag_shift) * 255);
    norm_phase = uint8(mat2gray(phase_shift) * 255);

    imwrite(norm_log_raw, fullfile(out_mat_dir, 'exp06_task_6_1_raw_log_spectrum.png'));
    imwrite(norm_log_shift, fullfile(out_mat_dir, 'exp06_task_6_1_centered_log_spectrum.png'));
    imwrite(norm_phase, fullfile(out_mat_dir, 'exp06_task_6_1_phase_spectrum.png'));

    % Multi-panel Figure
    fig = figure('Visible', 'off', 'Color', 'white', 'Position', [100, 100, 1500, 950]);

    subplot(2, 3, 1);
    imshow(img);
    title({'(a) Clinical Brain MRI Scan', sprintf('Size: %dx%d px | Mean: %.1f', W, H, mean_intensity)}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 2);
    imshow(log_mag_raw, []);
    colormap(gca, 'jet');
    hold on;
    plot(1, 1, 'co', 'MarkerSize', 8, 'LineWidth', 2);
    title({'(b) Uncentered Log-Spectrum', 'DC at Top-Left Corner (1, 1)'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 3);
    imshow(log_mag_shift, []);
    colormap(gca, 'jet');
    hold on;
    plot(dc_centered_idx(2), dc_centered_idx(1), 'w*', 'MarkerSize', 10, 'LineWidth', 2);
    plot([1, W], [dc_centered_idx(1), dc_centered_idx(1)], 'w:', 'LineWidth', 0.8);
    plot([dc_centered_idx(2), dc_centered_idx(2)], [1, H], 'w:', 'LineWidth', 0.8);
    title({'(c) Centered Log-Spectrum (fftshift)', sprintf('DC Star at (%d, %d) & Crosshairs', dc_centered_idx(1), dc_centered_idx(2))}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 4);
    imshow(phase_shift, []);
    colormap(gca, 'hsv');
    title({'(d) 2-D Phase Spectrum \phi(u, v)', 'Structural Spatial Alignment'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 5);
    plot(radial_distances, cumulative_energy, 'b-', 'LineWidth', 2.0);
    hold on;
    yline(90.0, 'g--', sprintf('90%% at D<=%d', r_90), 'LineWidth', 1.2);
    yline(95.0, 'm--', sprintf('95%% at D<=%d', r_95), 'LineWidth', 1.2);
    yline(99.0, 'r--', sprintf('99%% at D<=%d', r_99), 'LineWidth', 1.2);
    xlabel('Radial Frequency Radius D (pixels)', 'FontWeight', 'bold');
    ylabel('Spectral Energy Retained (%)', 'FontWeight', 'bold');
    xlim([0, 150]); ylim([50, 100.5]);
    grid on;
    title({'(e) Radial Energy Concentration', '(>95% Energy in Low-Frequency Core)'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 6);
    v_axis = (1:W) - floor(W / 2);
    diag_axis = linspace(-length(diag_profile)/2, length(diag_profile)/2, length(diag_profile));
    plot(v_axis, horiz_arm, 'r-', 'LineWidth', 1.8);
    hold on;
    plot(diag_axis, diag_profile, 'k--', 'LineWidth', 1.2);
    xlim([-150, 150]);
    xlabel('Frequency Distance from DC', 'FontWeight', 'bold');
    ylabel('Log-Magnitude Intensity', 'FontWeight', 'bold');
    legend({'Horizontal Crosshair (u=0)', 'Diagonal Transect (45 deg)'}, 'Location', 'northeast');
    grid on;
    title({'(f) Crosshair Boundary Artifact', '(Rectangular Windowing Spectral Leakage)'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    sgtitle('Experiment 06 - Task 6.1: 2-D Discrete Fourier Transform & Magnitude Spectrum Analysis (MATLAB)', ...
            'FontSize', 13, 'FontWeight', 'bold', 'Color', [0.06, 0.09, 0.16]);

    fig_path = fullfile(fig_dir, 'exp06_task_6_1_dft_spectrum_m.png');
    saveas(fig, fig_path);
    close(fig);
    fprintf('[SUCCESS] Figure saved at: %s\n', fig_path);

    metrics = struct('r_90', r_90, 'r_95', r_95, 'r_99', r_99, 'total_energy', total_energy);
end
