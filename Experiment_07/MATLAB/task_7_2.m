%% ==============================================================================
%% EXPERIMENT 07 - TASK 7.2: INFLUENCE OF SMOOTHING KERNEL BLUR (MATLAB)
%% Varies Gaussian blur standard deviation sigma across [0.8, 1.5, 3.0] with fixed k = 1.0,
%% evaluates high-frequency mask spatial bandwidth, mask dynamic range, and edge injection scale.
%% Course: Medical Image Processing | Riphah International University
%% Faculty: Engr. Rana Talha Khalid
%% ==============================================================================

function metrics = task_7_2()
    fprintf('==============================================================================\n');
    fprintf('EXPERIMENT 07 - TASK 7.2: SMOOTHING KERNEL BLUR & MASK BANDWIDTH (MATLAB)\n');
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

    % 1. Load Image
    img = imread(img_path);
    if size(img, 3) == 3; img = rgb2gray(img); end
    imgD = double(img);

    [Gx, Gy] = gradient(imgD);
    baseGrad = mean(hypot(Gx, Gy), 'all');

    sigmas = [0.8, 1.5, 3.0];
    metrics = cell(length(sigmas), 8);
    masks = cell(length(sigmas), 1);
    sharpened_images = cell(length(sigmas), 1);

    fprintf('\n%-6s | %-10s | %-14s | %-12s | %-14s | %-12s | %-16s\n', ...
            'Sigma', 'Window', 'Cutoff (cyc/px)', 'Mask Std', 'Dynamic Range', 'Mean Grad', 'Grad Boost (%)');
    fprintf('--------------------------------------------------------------------------------------------------\n');

    for i = 1:length(sigmas)
        s = sigmas(i);
        win_size = 2 * ceil(2 * s) + 1;
        blurred = imgaussfilt(imgD, s, 'FilterSize', win_size);
        mask = imgD - blurred;
        masks{i} = mask;

        raw_sharp = imgD + 1.0 * mask;
        sharp_u8 = uint8(min(max(raw_sharp, 0), 255));
        sharpened_images{i} = sharp_u8;

        s_str = strrep(sprintf('%.1f', s), '.', '_');
        bipolar_mask = uint8(min(max(mask + 128.0, 0), 255));
        imwrite(bipolar_mask, fullfile(out_mat_dir, sprintf('exp07_task_7_2_mask_sigma_%s_m.png', s_str)));
        imwrite(sharp_u8, fullfile(out_mat_dir, sprintf('exp07_task_7_2_sharp_sigma_%s_m.png', s_str)));

        mask_std = std(mask(:));
        mask_range = max(mask(:)) - min(mask(:));
        [gx, gy] = gradient(raw_sharp);
        mg = mean(hypot(gx, gy), 'all');
        boost = ((mg - baseGrad) / baseGrad) * 100.0;
        cutoff = 1.0 / (2.0 * pi * s);

        interp = 'Microscopic Edge Mask (Fine textures)';
        if s == 1.5
            interp = 'Balanced Diagnostic Mask (Cortical borders & trabeculae)';
        elseif s == 3.0
            interp = 'Macroscopic Boundary Mask (Thick structures, wide halos)';
        end

        metrics{i, 1} = s;
        metrics{i, 2} = sprintf('%dx%d', win_size, win_size);
        metrics{i, 3} = cutoff;
        metrics{i, 4} = mask_std;
        metrics{i, 5} = mask_range;
        metrics{i, 6} = mg;
        metrics{i, 7} = boost;
        metrics{i, 8} = interp;

        fprintf('s=%3.1f | %-10s | %-14.4f | %-12.2f | %-14.2f | %-12.2f | %+15.2f%%\n', ...
                s, metrics{i, 2}, cutoff, mask_std, mask_range, mg, boost);
    end

    % Export CSV
    sig_col = [metrics{:, 1}]';
    win_col = metrics(:, 2);
    cut_col = [metrics{:, 3}]';
    std_col = [metrics{:, 4}]';
    rng_col = [metrics{:, 5}]';
    mg_col = [metrics{:, 6}]';
    boost_col = [metrics{:, 7}]';
    interp_col = metrics(:, 8);

    T = table(sig_col, win_col, cut_col, std_col, rng_col, mg_col, boost_col, interp_col, ...
              'VariableNames', {'Sigma_Pixels', 'Equivalent_Window', 'Cutoff_Freq_Cycles_Px', ...
                               'Mask_Std_Dev', 'Mask_Dynamic_Range', 'Sharpened_Mean_Grad', ...
                               'Grad_Boost_Pct', 'Bandwidth_Interpretation'});
    writetable(T, fullfile(tab_dir, 'exp07_task_7_2_bandwidth_metrics_matlab.csv'));

    % Multi-panel Figure (2x3)
    fig = figure('Visible', 'off', 'Color', 'white', 'Position', [100, 100, 1500, 950]);

    % Top row: The 3 High-Frequency Masks (bipolar display)
    subplot(2, 3, 1);
    imshow(uint8(min(max(masks{1} + 128.0, 0), 255)));
    title({'(a) High-Freq Mask (\sigma=0.8, 5\times 5)', sprintf('Mask Std: %.2f | Micro-Edges Only', metrics{1,4})}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.01, 0.52, 0.78]);

    subplot(2, 3, 2);
    imshow(uint8(min(max(masks{2} + 128.0, 0), 255)));
    title({'(b) High-Freq Mask (\sigma=1.5, 7\times 7)', sprintf('Mask Std: %.2f | Balanced Detail', metrics{2,4})}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.08, 0.50, 0.24]);

    subplot(2, 3, 3);
    imshow(uint8(min(max(masks{3} + 128.0, 0), 255)));
    title({'(c) High-Freq Mask (\sigma=3.0, 13\times 13)', sprintf('Mask Std: %.2f | Broad Structures', metrics{3,4})}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.71, 0.33, 0.04]);

    % Bottom row: Reconstructed Sharpened Outputs (k = 1.0)
    subplot(2, 3, 4);
    imshow(sharpened_images{1});
    title({'(d) Sharpened Image (\sigma=0.8)', sprintf('Boost: %+.1f%% | Fine Trabeculae', metrics{1,7})}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.01, 0.52, 0.78]);

    subplot(2, 3, 5);
    imshow(sharpened_images{2});
    title({'(e) Sharpened Image (\sigma=1.5) [OPTIMUM]', sprintf('Boost: %+.1f%% | Clinical Standard', metrics{2,7})}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.08, 0.50, 0.24]);

    subplot(2, 3, 6);
    imshow(sharpened_images{3});
    title({'(f) Sharpened Image (\sigma=3.0)', sprintf('Boost: %+.1f%% | Thick Bone Halos', metrics{3,7})}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.71, 0.33, 0.04]);

    sgtitle('Experiment 07 - Task 7.2: Influence of Smoothing Kernel Blur Parameter on Mask Bandwidth (MATLAB)', ...
            'FontSize', 13, 'FontWeight', 'bold', 'Color', [0.06, 0.09, 0.16]);

    fig_path = fullfile(fig_dir, 'exp07_task_7_2_mask_bandwidth_m.png');
    saveas(fig, fig_path);
    close(fig);
    fprintf('[SUCCESS] Figure saved at: %s\n', fig_path);
end
