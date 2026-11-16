%% ==============================================================================
%% EXPERIMENT 07 - TASK 7.3: 1D TRANSECT & MACH BAND MEASUREMENT (MATLAB)
%% Extracts a 1-D pixel intensity profile across Row 150 (Columns 100 to 250)
%% intersecting the cortical bone margin, quantifies edge slope steepening (dI/dx),
%% overshoot peak height, and Mach band halo width.
%% Course: Medical Image Processing | Riphah International University
%% Faculty: Engr. Rana Talha Khalid
%% ==============================================================================

function metrics = task_7_3()
    fprintf('==============================================================================\n');
    fprintf('EXPERIMENT 07 - TASK 7.3: 1D TRANSECT & MACH BAND MEASUREMENT (MATLAB)\n');
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

    % 1. Load Image & Extract Mask
    img = imread(img_path);
    if size(img, 3) == 3; img = rgb2gray(img); end
    imgD = double(img);

    blurred = imgaussfilt(imgD, 1.5, 'FilterSize', 7);
    g_mask = imgD - blurred;

    sharp_k1_raw = imgD + 1.0 * g_mask;
    sharp_k3_raw = imgD + 3.0 * g_mask;

    sharp_k1 = uint8(min(max(sharp_k1_raw, 0), 255));
    sharp_k3 = uint8(min(max(sharp_k3_raw, 0), 255));

    % 2. Extract Transect across Row 150, Columns 100 to 250 (1-based: 101 to 250)
    prof_row = 150;
    c_start = 100;
    c_end = 250;
    cols = c_start:c_end;

    prof_orig = imgD(prof_row, cols);
    prof_k1 = sharp_k1_raw(prof_row, cols);
    prof_k3 = sharp_k3_raw(prof_row, cols);

    % Save transect overlay image
    img_rgb = repmat(img, [1, 1, 3]);
    img_rgb(prof_row-1:prof_row+1, c_start:c_end, 1) = 0;
    img_rgb(prof_row-1:prof_row+1, c_start:c_end, 2) = 255;
    img_rgb(prof_row-1:prof_row+1, c_start:c_end, 3) = 255;
    imwrite(img_rgb, fullfile(out_mat_dir, 'exp07_task_7_3_transect_overlay_m.png'));

    % 3. Quantitative Measurements
    % Profile metrics helper
    function m = calc_profile_metrics(prof, label)
        diffs = abs(diff(prof));
        max_slope = max(diffs);

        % Transition region in 1-based index (cols 200 to 225 corresponds to index 101:126)
        edge_region = prof(101:126);
        peak_val = max(edge_region);
        trough_val = min(edge_region);
        baseline_bone = mean(prof(41:71));    % cols 140:170
        baseline_lung = mean(prof(116:136));  % cols 215:235

        overshoot = max(0.0, peak_val - baseline_bone);
        undershoot = max(0.0, baseline_lung - trough_val);

        if overshoot > 1.0
            half_max = baseline_bone + 0.5 * overshoot;
            halo_width = sum(edge_region >= half_max);
        else
            halo_width = 0.0;
        end

        comp = 'Pass (<= 2.0 px)';
        if halo_width > 2.0
            comp = 'FAIL (> 2.0 px, Broad Halo)';
        end

        m = struct('Condition', label, 'Max_Edge_Slope', max_slope, ...
                   'Overshoot_Peak', overshoot, 'Undershoot_Trough', undershoot, ...
                   'Mach_Band_Halo_Width_Px', halo_width, 'Halo_Compliance', comp);
    end

    m_orig = calc_profile_metrics(prof_orig, 'Original Scan');
    m_k1 = calc_profile_metrics(prof_k1, 'Unsharp Masking (k=1.0)');
    m_k3 = calc_profile_metrics(prof_k3, 'Over-Boosted (k=3.0)');

    metrics = [m_orig; m_k1; m_k3];

    fprintf('\n%-26s | %-14s | %-14s | %-16s | %-16s | %-20s\n', ...
            'Condition', 'Max Slope', 'Overshoot', 'Undershoot', 'Halo Width (px)', 'Halo Compliance');
    fprintf('----------------------------------------------------------------------------------------------------------------\n');
    for i = 1:length(metrics)
        fprintf('%-26s | %-14.2f | %-14.2f | %-16.2f | %-16.1f | %-20s\n', ...
                metrics(i).Condition, metrics(i).Max_Edge_Slope, metrics(i).Overshoot_Peak, ...
                metrics(i).Undershoot_Trough, metrics(i).Mach_Band_Halo_Width_Px, metrics(i).Halo_Compliance);
    end

    % Export CSV
    cond_col = {metrics.Condition}';
    slope_col = [metrics.Max_Edge_Slope]';
    over_col = [metrics.Overshoot_Peak]';
    under_col = [metrics.Undershoot_Trough]';
    width_col = [metrics.Mach_Band_Halo_Width_Px]';
    comp_col = {metrics.Halo_Compliance}';

    T = table(cond_col, slope_col, over_col, under_col, width_col, comp_col, ...
              'VariableNames', {'Condition', 'Max_Edge_Slope', 'Overshoot_Peak', ...
                               'Undershoot_Trough', 'Mach_Band_Halo_Width_Px', 'Halo_Compliance'});
    writetable(T, fullfile(tab_dir, 'exp07_task_7_3_mach_band_metrics_matlab.csv'));

    % 4. Multi-panel Visualization Figure (1x3 Layout)
    fig = figure('Visible', 'off', 'Color', 'white', 'Position', [100, 100, 1600, 650]);

    % (a) Radiograph with Transect Line
    subplot(1, 3, 1);
    imshow(img); hold on;
    plot([c_start, c_end], [prof_row, prof_row], 'c-', 'LineWidth', 2.5);
    plot([c_start, c_end], [prof_row, prof_row], 'yo', 'MarkerFaceColor', 'y', 'MarkerSize', 6);
    hold off;
    title({'(a) Chest Radiograph with Transect (Cyan)', sprintf('Row %d, Columns [%d, %d]', prof_row, c_start, c_end)}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    % (b) 1-D Profiles
    subplot(1, 3, 2);
    plot(cols, prof_orig, 'Color', [0.28, 0.33, 0.41], 'LineWidth', 1.8, 'DisplayName', 'Original Radiograph'); hold on;
    plot(cols, prof_k1, 'Color', [0.09, 0.64, 0.29], 'LineWidth', 2.2, 'DisplayName', 'Unsharp Mask (k=1.0) [Optimum]');
    plot(cols, prof_k3, 'Color', [0.86, 0.15, 0.15], 'LineWidth', 1.8, 'LineStyle', '--', 'DisplayName', 'Over-Boosted (k=3.0) [Halos]');
    % highlight transition zone
    x_patch = [200, 220, 220, 200];
    y_limits = [min([prof_orig, prof_k1, prof_k3])-5, max([prof_orig, prof_k1, prof_k3])+5];
    patch(x_patch, [y_limits(1), y_limits(1), y_limits(2), y_limits(2)], [1, 1, 0.8], ...
          'FaceAlpha', 0.3, 'EdgeColor', 'none', 'DisplayName', 'Bone-Lung Interface');
    hold off;
    xlabel('Column Pixel Coordinate', 'FontWeight', 'bold');
    ylabel('Pixel Intensity (0-255)', 'FontWeight', 'bold');
    title({'(b) 1-D Cortical Bone Transect Profile', '(Mach Band Overshoot & Edge Slope Steepening)'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);
    legend('Location', 'northeast', 'FontSize', 8.5);
    grid on;

    % (c) Bar Chart of Metrics
    subplot(1, 3, 3);
    bar_data = [slope_col, over_col, width_col];
    b = bar(bar_data);
    b(1).FaceColor = [0.23, 0.51, 0.96];
    b(2).FaceColor = [0.94, 0.27, 0.27];
    b(3).FaceColor = [0.06, 0.73, 0.51];
    set(gca, 'XTickLabel', {'Original', 'k=1.0', 'k=3.0'}, 'FontWeight', 'bold');
    ylabel('Metric Value', 'FontWeight', 'bold');
    title('(c) Quantitative Edge & Halo Metrics', 'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);
    legend({'Edge Slope (dI/dx)', 'Overshoot (Units)', 'Halo Width (Px)'}, 'Location', 'northwest', 'FontSize', 8.5);
    grid on;

    sgtitle('Experiment 07 - Task 7.3: 1D Spatial Transect Profile Extraction & Mach Band Quantitative Measurement (MATLAB)', ...
            'FontSize', 13, 'FontWeight', 'bold', 'Color', [0.06, 0.09, 0.16]);

    fig_path = fullfile(fig_dir, 'exp07_task_7_3_mach_band_profiles_m.png');
    saveas(fig, fig_path);
    close(fig);
    fprintf('[SUCCESS] Figure saved at: %s\n', fig_path);
end
