%% ==============================================================================
%% SCRIPT: example_01.m
%% Experiment 04: Noise Modeling & Adaptive Filtering in Medical Images
%% Example 01: Medical Noise Modeling & Multi-Filter Restoration Benchmark
%% Course: Medical Image Processing | Riphah International University
%% Instructor: Engr. Rana Talha Khalid
%% ==============================================================================

function example_01()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 04 - MATLAB EXAMPLE 01: NOISE RESTORATION BENCHMARK\n');
    fprintf('======================================================================\n');

    script_dir = fileparts(mfilename('fullpath'));
    exp_dir = fileparts(script_dir);
    img_path = fullfile(exp_dir, 'Inputs', 'images', 'MRI.jpg');

    if ~exist(img_path, 'file')
        img_path = fullfile(exp_dir, '..', '..', 'images', 'MRI.jpg');
    end

    fprintf('[INFO] Loading reference MRI scan: %s\n', img_path);
    ref = imread(img_path);
    if size(ref, 3) == 3; ref = rgb2gray(ref); end

    [H, W] = size(ref);
    fprintf('[INFO] Dimensions: %d x %d pixels, Class: %s\n', W, H, class(ref));

    % 1. Simulate Mixed Noise: Gaussian (var=0.005) + 10% Salt & Pepper
    rng(42);
    gNoisy = imnoise(ref, 'gaussian', 0, 0.005);
    noisy = imnoise(gNoisy, 'salt & pepper', 0.10);

    % 2. Apply Filters
    fprintf('[INFO] Computing Linear Mean 5x5 Filter...\n');
    hMean5 = fspecial('average', [5 5]);
    mean5 = imfilter(noisy, hMean5, 'replicate');

    fprintf('[INFO] Computing Standard Median 3x3 Filter...\n');
    med3 = medfilt2(noisy, [3 3], 'symmetric');

    fprintf('[INFO] Computing Adaptive Wiener 5x5 Filter...\n');
    wiener5 = wiener2(noisy, [5 5]);

    fprintf('[INFO] Computing Standard Median 5x5 Filter...\n');
    med5 = medfilt2(noisy, [5 5], 'symmetric');

    % 3. Benchmark Metrics
    tests = {
        'Noisy Scan Baseline', noisy;
        'Linear Mean 5x5', mean5;
        'Adaptive Wiener 5x5', wiener5;
        'Standard Median 3x3', med3;
        'Standard Median 5x5', med5
    };

    fprintf('\n%-24s | %-12s | %-10s | %-30s\n', 'Filter', 'PSNR (dB)', 'SSIM', 'Clinical Assessment');
    fprintf('--------------------------------------------------------------------------------------\n');
    for i = 1:size(tests, 1)
        im = tests{i, 2};
        p = psnr(im, ref);
        s = ssim(im, ref);
        if i == 1
            obs = 'Severely corrupted by bipolar noise';
        elseif i == 2
            obs = 'Impulses smeared into gray smudges';
        elseif i == 3
            obs = 'Poor on impulses (Gaussian assumption)';
        elseif i == 4
            obs = 'Impulses removed; high edge retention';
        else
            obs = 'Impulses cleared; slight corner rounding';
        end
        fprintf('%-24s | %-12.2f | %-10.4f | %s\n', tests{i, 1}, p, s, obs);
    end
    fprintf('--------------------------------------------------------------------------------------\n');
    fprintf('>>> Conclusion: Median filters eliminate impulse noise cleanly (> +15 dB PSNR gain).\n');

    % 4. Visualization: 6-Panel Composite
    fig = figure('Visible', 'off', 'Position', [100, 100, 1250, 850]);

    subplot(2, 3, 1);
    imshow(ref);
    title('A: Clean Reference MRI', 'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.12 0.23 0.54]);

    subplot(2, 3, 2);
    imshow(noisy);
    title(sprintf('B: Mixed Noisy Scan (10%% SP + Gauss)\nPSNR: %.2f dB | SSIM: %.4f', psnr(noisy, ref), ssim(noisy, ref)), ...
          'FontSize', 9.5, 'FontWeight', 'bold', 'Color', [0.72 0.15 0.15]);

    subplot(2, 3, 3);
    imshow(mean5);
    title(sprintf('C: Linear Mean 5x5 (Smear Failure)\nPSNR: %.2f dB | SSIM: %.4f', psnr(mean5, ref), ssim(mean5, ref)), ...
          'FontSize', 9.5, 'FontWeight', 'bold', 'Color', [0.72 0.15 0.15]);

    subplot(2, 3, 4);
    imshow(wiener5);
    title(sprintf('D: Adaptive Wiener 5x5 (Gaussian Only)\nPSNR: %.2f dB | SSIM: %.4f', psnr(wiener5, ref), ssim(wiener5, ref)), ...
          'FontSize', 9.5, 'FontWeight', 'bold', 'Color', [0.77 0.54 0.02]);

    subplot(2, 3, 5);
    imshow(med3);
    title(sprintf('E: Standard Median 3x3 [Optimal]\nPSNR: %.2f dB | SSIM: %.4f', psnr(med3, ref), ssim(med3, ref)), ...
          'FontSize', 9.5, 'FontWeight', 'bold', 'Color', [0.08 0.50 0.24]);

    subplot(2, 3, 6);
    imshow(med5);
    title(sprintf('F: Standard Median 5x5 (Heavy Filter)\nPSNR: %.2f dB | SSIM: %.4f', psnr(med5, ref), ssim(med5, ref)), ...
          'FontSize', 9.5, 'FontWeight', 'bold', 'Color', [0.12 0.23 0.54]);

    sgtitle('MATLAB Example 01: Medical Noise Modeling & Multi-Filter Restoration Benchmark', ...
            'FontSize', 13, 'FontWeight', 'bold');

    % Save figures
    out_dir_m = fullfile(exp_dir, 'Outputs', 'MATLAB');
    fig_dir = fullfile(exp_dir, 'Figures');
    if ~exist(out_dir_m, 'dir'); mkdir(out_dir_m); end
    if ~exist(fig_dir, 'dir'); mkdir(fig_dir); end

    out_path_1 = fullfile(out_dir_m, 'exp04_example_01_noise_filtering_m.png');
    out_path_2 = fullfile(fig_dir, 'exp04_example_01_noise_filtering_m.png');

    exportgraphics(fig, out_path_1, 'Resolution', 300);
    exportgraphics(fig, out_path_2, 'Resolution', 300);
    close(fig);

    fprintf('[SUCCESS] Saved MATLAB figure to:\n  %s\n  %s\n', out_path_1, out_path_2);
end
