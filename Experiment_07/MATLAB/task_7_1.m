%% ==============================================================================
%% EXPERIMENT 07 - TASK 7.1: HIGH-BOOST SWEEP & CLIPPING ANALYSIS (MATLAB)
%% Evaluates underflow/overflow clipping, Shannon entropy, and gradient magnitude
%% across boost factors k in [0.5, 1.0, 1.8, 3.0] on a clinical radiograph.
%% Course: Medical Image Processing | Riphah International University
%% Faculty: Engr. Rana Talha Khalid
%% ==============================================================================

function metrics = task_7_1()
    fprintf('==============================================================================\n');
    fprintf('EXPERIMENT 07 - TASK 7.1: HIGH-BOOST SWEEP & CLIPPING ANALYSIS (MATLAB)\n');
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
    [H, W] = size(img);
    total_pixels = H * W;
    imgD = double(img);

    % 2. Extract High-Frequency Mask (sigma = 1.5, FilterSize = 5)
    blurred = imgaussfilt(imgD, 1.5, 'FilterSize', 5);
    g_mask = imgD - blurred;

    [Gx, Gy] = gradient(imgD);
    baseGrad = mean(hypot(Gx, Gy), 'all');
    baseEntropy = entropy(img);

    k_vals = [0.5, 1.0, 1.8, 3.0];
    metrics = cell(length(k_vals), 8);
    sharpened_images = cell(length(k_vals), 1);

    fprintf('\n%-6s | %-12s | %-16s | %-12s | %-12s | %-14s | %-12s\n', ...
            'k', 'Mean Grad', 'Grad Boost (%)', 'Clip 0 (%)', 'Sat 255 (%)', 'Total Clip (%)', 'Entropy (b)');
    fprintf('--------------------------------------------------------------------------------------------------\n');

    for i = 1:length(k_vals)
        k = k_vals(i);
        raw_sharp = imgD + k * g_mask;
        clip_0 = sum(raw_sharp(:) < 0.0);
        sat_255 = sum(raw_sharp(:) > 255.0);
        total_clip = clip_0 + sat_255;

        pct_clip_0 = (clip_0 / total_pixels) * 100.0;
        pct_sat_255 = (sat_255 / total_pixels) * 100.0;
        pct_total_clip = (total_clip / total_pixels) * 100.0;

        sharp_u8 = uint8(min(max(raw_sharp, 0), 255));
        sharpened_images{i} = sharp_u8;
        imwrite(sharp_u8, fullfile(out_mat_dir, sprintf('exp07_task_7_1_sharp_k_%.1f_m.png', k)));

        [gx, gy] = gradient(raw_sharp);
        mg = mean(hypot(gx, gy), 'all');
        grad_boost = ((mg - baseGrad) / baseGrad) * 100.0;
        ent = entropy(sharp_u8);

        metrics{i, 1} = k;
        metrics{i, 2} = mg;
        metrics{i, 3} = grad_boost;
        metrics{i, 4} = pct_clip_0;
        metrics{i, 5} = pct_sat_255;
        metrics{i, 6} = pct_total_clip;
        metrics{i, 7} = ent;
        metrics{i, 8} = 'Acceptable';
        if k == 1.0; metrics{i, 8} = 'OPTIMAL (Good to Go)';
        elseif k > 2.0; metrics{i, 8} = 'CONTRAINDICATED'; end

        fprintf('k=%3.1f | %-12.2f | %+15.2f%% | %-12.3f | %-12.3f | %-14.3f | %-12.3f\n', ...
                k, mg, grad_boost, pct_clip_0, pct_sat_255, pct_total_clip, ent);
    end

    % Export CSV
    k_col = [metrics{:, 1}]';
    mg_col = [metrics{:, 2}]';
    boost_col = [metrics{:, 3}]';
    clip0_col = [metrics{:, 4}]';
    sat255_col = [metrics{:, 5}]';
    totclip_col = [metrics{:, 6}]';
    ent_col = [metrics{:, 7}]';
    verdict_col = metrics(:, 8);

    T = table(k_col, mg_col, boost_col, clip0_col, sat255_col, totclip_col, ent_col, verdict_col, ...
              'VariableNames', {'Boost_k', 'Mean_Gradient', 'Grad_Boost_Pct', 'Clip_0_Pct', 'Sat_255_Pct', 'Total_Clip_Pct', 'Entropy_Bits', 'Clinical_Verdict'});
    writetable(T, fullfile(tab_dir, 'exp07_task_7_1_clipping_metrics_matlab.csv'));

    % Multi-panel Figure
    fig = figure('Visible', 'off', 'Color', 'white', 'Position', [100, 100, 1500, 950]);

    subplot(2, 3, 1);
    imshow(img);
    title({'(a) Original Radiograph', sprintf('Grad: %.2f | Entropy: %.2f b/px', baseGrad, baseEntropy)}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 2);
    imshow(sharpened_images{1});
    title({'(b) Mild Boost (k=0.5)', sprintf('Boost: %+.1f%% | Clip: %.2f%%', metrics{1,3}, metrics{1,6})}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0, 0.52, 0.78]);

    subplot(2, 3, 3);
    imshow(sharpened_images{2});
    title({'(c) Unsharp Masking (k=1.0) [OPTIMUM]', sprintf('Boost: %+.1f%% | Clip: %.2f%%', metrics{2,3}, metrics{2,6})}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.08, 0.50, 0.24]);

    subplot(2, 3, 4);
    imshow(sharpened_images{3});
    title({'(d) High-Boost (k=1.8)', sprintf('Boost: %+.1f%% | Clip: %.2f%%', metrics{3,3}, metrics{3,6})}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.96, 0.62, 0.04]);

    subplot(2, 3, 5);
    imshow(sharpened_images{4});
    title({'(e) Over-Boosted (k=3.0) [HAZARD]', sprintf('Boost: %+.1f%% | Clip: %.2f%%', metrics{4,3}, metrics{4,6})}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.86, 0.15, 0.15]);

    subplot(2, 3, 6);
    yyaxis left;
    plot(k_col, boost_col, 'b-o', 'LineWidth', 2.0);
    ylabel('Gradient Boost (%)', 'FontWeight', 'bold');
    yyaxis right;
    plot(k_col, totclip_col, 'r--s', 'LineWidth', 2.0);
    ylabel('Total Pixels Clipped (%)', 'FontWeight', 'bold');
    xlabel('Boost Factor k', 'FontWeight', 'bold');
    title('(f) Gradient Boost vs Saturation Clipping', 'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);
    grid on;

    sgtitle('Experiment 07 - Task 7.1: High-Boost Factor Sweep & Dynamic Range Clipping Analysis (MATLAB)', ...
            'FontSize', 13, 'FontWeight', 'bold', 'Color', [0.06, 0.09, 0.16]);

    fig_path = fullfile(fig_dir, 'exp07_task_7_1_clipping_sweep_m.png');
    saveas(fig, fig_path);
    close(fig);
    fprintf('[SUCCESS] Figure saved at: %s\n', fig_path);
end
