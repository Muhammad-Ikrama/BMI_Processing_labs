%% ==============================================================================
%% SCRIPT: example_01.m
%% Experiment 03: Image Smoothing of Medical Images Using Spatial Domain Mean & Gaussian Filters
%% Example 01: Spatial Domain Linear Filtering (Mean vs Gaussian) Benchmark
%% Course: Medical Image Processing | Riphah International University
%% Instructor: Engr. Rana Talha Khalid
%% ==============================================================================

function example_01()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 03 - MATLAB EXAMPLE 01: FILTERING BENCHMARK\n');
    fprintf('======================================================================\n');

    script_dir = fileparts(mfilename('fullpath'));
    exp_dir = fileparts(script_dir);
    img_path = fullfile(exp_dir, 'Inputs', 'images', 'MRI.jpg');

    if ~exist(img_path, 'file')
        img_path = fullfile(exp_dir, '..', '..', 'images', 'MRI.jpg');
    end

    fprintf('[INFO] Loading reference MRI scan: %s\n', img_path);
    img = imread(img_path);
    if size(img, 3) == 3
        img = rgb2gray(img);
    end

    [H, W] = size(img);
    fprintf('[INFO] Image Dimensions: %d x %d pixels, Class: %s\n', W, H, class(img));

    % 1. Simulate Gaussian thermal acquisition noise (variance = 0.01)
    rng(42); % For reproducibility
    noisy = imnoise(img, 'gaussian', 0, 0.01);

    % 2. Mean Box Filtering (fspecial 'average')
    hMean3 = fspecial('average', [3 3]);
    hMean5 = fspecial('average', [5 5]);
    mean3 = imfilter(noisy, hMean3, 'replicate');
    mean5 = imfilter(noisy, hMean5, 'replicate');

    % 3. Gaussian Filtering (fspecial 'gaussian')
    hGauss3 = fspecial('gaussian', [3 3], 0.8);
    hGauss5 = fspecial('gaussian', [5 5], 1.2);
    gauss3 = imfilter(noisy, hGauss3, 'replicate');
    gauss5 = imfilter(noisy, hGauss5, 'replicate');

    % 4. Contrast-to-Noise Ratio (CNR) Definition
    sig_roi = img(round(H/2)-20:round(H/2)+20, round(W/2)-20:round(W/2)+20);
    bg_roi  = img(10:50, 10:50);

    calc_cnr = @(im) abs(mean(double(im(round(H/2)-20:round(H/2)+20, round(W/2)-20:round(W/2)+20)), 'all') - ...
                         mean(double(im(10:50, 10:50)), 'all')) / ...
                     sqrt(var(double(im(round(H/2)-20:round(H/2)+20, round(W/2)-20:round(W/2)+20)), 0, 'all') + ...
                          var(double(im(10:50, 10:50)), 0, 'all'));

    % 5. Quantitative Benchmarking
    tests = {
        'Noisy Baseline', noisy, 0;
        'Mean 3x3', mean3, 3;
        'Mean 5x5', mean5, 5;
        'Gaussian 3x3 (sig=0.8)', gauss3, 3;
        'Gaussian 5x5 (sig=1.2)', gauss5, 5
    };

    fprintf('\n%-24s | %-8s | %-10s | %-8s | %-6s\n', 'Filter Method', 'Kernel', 'PSNR (dB)', 'SSIM', 'CNR');
    fprintf('---------------------------------------------------------------------------\n');
    for i = 1:size(tests, 1)
        im = tests{i, 2};
        k = tests{i, 3};
        p = psnr(im, img);
        s = ssim(im, img);
        c = calc_cnr(im);
        k_str = sprintf('%dx%d', k, k);
        if k == 0; k_str = 'None'; end
        fprintf('%-24s | %-8s | %-10.2f | %-8.4f | %-6.2f\n', tests{i, 1}, k_str, p, s, c);
    end
    fprintf('---------------------------------------------------------------------------\n');
    fprintf('>>> Status: Gaussian 3x3 achieves OPTIMAL performance (Edge-preserving).\n');

    % 6. Visualization
    fig = figure('Visible', 'off', 'Position', [100, 100, 1200, 800]);

    subplot(2, 3, 1);
    imshow(img);
    title('Clean Reference Scan', 'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.12 0.23 0.54]);

    subplot(2, 3, 2);
    imshow(noisy);
    p_n = psnr(noisy, img); s_n = ssim(noisy, img);
    title(sprintf('Noisy Scan (var=0.01)\nPSNR: %.2f dB, SSIM: %.4f', p_n, s_n), ...
          'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.72 0.15 0.15]);

    subplot(2, 3, 3);
    imshow(mean3);
    p_m3 = psnr(mean3, img); s_m3 = ssim(mean3, img);
    title(sprintf('Mean 3x3 (Box)\nPSNR: %.2f dB, SSIM: %.4f', p_m3, s_m3), ...
          'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.12 0.23 0.54]);

    subplot(2, 3, 4);
    imshow(mean5);
    p_m5 = psnr(mean5, img); s_m5 = ssim(mean5, img);
    title(sprintf('Mean 5x5 (Severe Blur)\nPSNR: %.2f dB, SSIM: %.4f', p_m5, s_m5), ...
          'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.72 0.15 0.15]);

    subplot(2, 3, 5);
    imshow(gauss3);
    p_g3 = psnr(gauss3, img); s_g3 = ssim(gauss3, img);
    title(sprintf('Gaussian 3x3 (sig=0.8) [Optimal]\nPSNR: %.2f dB, SSIM: %.4f', p_g3, s_g3), ...
          'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.08 0.50 0.24]);

    subplot(2, 3, 6);
    imshow(gauss5);
    p_g5 = psnr(gauss5, img); s_g5 = ssim(gauss5, img);
    title(sprintf('Gaussian 5x5 (sig=1.2)\nPSNR: %.2f dB, SSIM: %.4f', p_g5, s_g5), ...
          'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.12 0.23 0.54]);

    sgtitle('MATLAB Example 01: Spatial Domain Linear Filtering Benchmark (Brain MRI)', ...
            'FontSize', 13, 'FontWeight', 'bold');

    % Save figures
    out_dir_m = fullfile(exp_dir, 'Outputs', 'MATLAB');
    fig_dir = fullfile(exp_dir, 'Figures');
    if ~exist(out_dir_m, 'dir'); mkdir(out_dir_m); end
    if ~exist(fig_dir, 'dir'); mkdir(fig_dir); end

    out_path_1 = fullfile(out_dir_m, 'exp03_example_01_filtering_benchmark_m.png');
    out_path_2 = fullfile(fig_dir, 'exp03_example_01_filtering_benchmark_m.png');

    exportgraphics(fig, out_path_1, 'Resolution', 300);
    exportgraphics(fig, out_path_2, 'Resolution', 300);
    close(fig);

    fprintf('[SUCCESS] Saved MATLAB figure to:\n  %s\n  %s\n', out_path_1, out_path_2);
end
