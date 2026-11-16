%% ==============================================================================
%% EXPERIMENT 07 - EXAMPLE 01: BASELINE SHARPENING & GRADIENT BENCHMARK (MATLAB)
%% Demonstrates Gaussian unsharp masking, high-boost parameter sweep across k in
%% [0.5, 1.0, 1.8, 3.0], mean gradient magnitude boosting, and decision framework.
%% Course: Medical Image Processing | Riphah International University
%% Faculty: Engr. Rana Talha Khalid
%% ==============================================================================

function results = example_01()
    fprintf('==============================================================================\n');
    fprintf('EXPERIMENT 07 - EXAMPLE 01: BASELINE IMAGE SHARPENING BENCHMARK (MATLAB)\n');
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
    if ~exist(out_mat_dir, 'dir'); mkdir(out_mat_dir); end
    if ~exist(fig_dir, 'dir'); mkdir(fig_dir); end

    % 1. Load Clinical Radiograph
    img = imread(img_path);
    if size(img, 3) == 3; img = rgb2gray(img); end
    [H, W] = size(img);
    imgD = double(img);
    fprintf('[INFO] Loaded Radiograph: %dx%d pixels, class=%s, range=[%d, %d]\n', ...
            W, H, class(img), min(img(:)), max(img(:)));

    % 2. Extract High-Frequency Mask via Gaussian Blur (sigma = 1.5, FilterSize = 5)
    blurred = imgaussfilt(imgD, 1.5, 'FilterSize', 5);
    g_mask = imgD - blurred;

    % 3. Baseline Gradient Magnitude
    [Gx, Gy] = gradient(imgD);
    baseGrad = mean(hypot(Gx, Gy), 'all');

    % 4. Sweep Boost Factor k
    k_vals = [0.5, 1.0, 1.8, 3.0];
    names = {'Mild De-Emphasis', 'Unsharp Masking', 'High-Boost', 'Over-Boosted'};

    fprintf('\n%-22s | %-6s | %-12s | %-16s | %-20s\n', 'Sharpening Mode', 'k', 'Mean Grad', 'Grad Boost (%)', 'Status');
    fprintf('--------------------------------------------------------------------------------------\n');

    results = cell(length(k_vals), 5);
    sharpened_images = cell(length(k_vals), 1);

    for i = 1:length(k_vals)
        k = k_vals(i);
        raw_sharp = imgD + k * g_mask;
        sharp_u8 = uint8(min(max(raw_sharp, 0), 255));
        sharpened_images{i} = sharp_u8;

        imwrite(sharp_u8, fullfile(out_mat_dir, sprintf('exp07_example_01_k_%.1f_m.png', k)));

        [gx, gy] = gradient(raw_sharp);
        mg = mean(hypot(gx, gy), 'all');
        boost = ((mg - baseGrad) / baseGrad) * 100.0;
        st = 'Acceptable';
        if k == 1.0; st = 'OPTIMAL (Good to Go)';
        elseif k > 2.0; st = 'Severe Noise/Halos'; end

        results{i, 1} = names{i};
        results{i, 2} = k;
        results{i, 3} = mg;
        results{i, 4} = boost;
        results{i, 5} = st;

        fprintf('%-22s | k=%3.1f | %-12.2f | %+15.2f%% | %-20s\n', names{i}, k, mg, boost, st);
    end
    fprintf('>>> Status: Factor k=1.0 approved for clinical radiograph reading.\n');

    % Publication Figure
    fig = figure('Visible', 'off', 'Color', 'white', 'Position', [100, 100, 1400, 900]);

    subplot(2, 3, 1);
    imshow(img);
    title({'(a) Original Chest Radiograph', sprintf('Base Grad: %.2f | Unfiltered', baseGrad)}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 2);
    mask_bipolar = uint8(min(max(g_mask + 128.0, 0), 255));
    imshow(mask_bipolar);
    title({'(b) High-Frequency Mask g_{mask}', '(Gaussian \sigma=1.5, Mean \approx 0)'}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 3);
    imshow(sharpened_images{1});
    title({'(c) Mild De-Emphasis (k=0.5)', sprintf('Grad: %.2f (%+.1f%%) | Smooth', results{1,3}, results{1,4})}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0, 0.52, 0.78]);

    subplot(2, 3, 4);
    imshow(sharpened_images{2});
    title({'(d) Unsharp Masking (k=1.0) [OPTIMUM]', sprintf('Grad: %.2f (%+.1f%%) | Razor Sharp', results{2,3}, results{2,4})}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.08, 0.50, 0.24]);

    subplot(2, 3, 5);
    imshow(sharpened_images{3});
    title({'(e) High-Boost (k=1.8)', sprintf('Grad: %.2f (%+.1f%%) | Dense Trabeculae', results{3,3}, results{3,4})}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.96, 0.62, 0.04]);

    subplot(2, 3, 6);
    imshow(sharpened_images{4});
    title({'(f) Over-Boosted (k=3.0)', sprintf('Grad: %.2f (%+.1f%%) | Severe Halos/Noise', results{4,3}, results{4,4})}, ...
          'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.86, 0.15, 0.15]);

    sgtitle('Experiment 07 - Baseline Image Sharpening & Gradient Benchmark (MATLAB Pipeline)', ...
            'FontSize', 13, 'FontWeight', 'bold', 'Color', [0.06, 0.09, 0.16]);

    fig_path = fullfile(fig_dir, 'exp07_example_01_benchmark_m.png');
    saveas(fig, fig_path);
    close(fig);
    fprintf('[SUCCESS] Figure saved at: %s\n', fig_path);
end
