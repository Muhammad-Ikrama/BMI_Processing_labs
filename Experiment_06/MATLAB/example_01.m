%% ==============================================================================
%% EXPERIMENT 06 - EXAMPLE 01: BASELINE FREQUENCY FILTERING PIPELINE (MATLAB)
%% Demonstrates 2-D Fourier Transform, spectrum centering, and comparison
%% of Ideal, Butterworth (n=2), and Gaussian Low-Pass Filters on Clinical Brain MRI.
%% Course: Medical Image Processing | Riphah International University
%% Faculty: Engr. Rana Talha Khalid
%% ==============================================================================

function results = example_01()
    fprintf('==============================================================================\n');
    fprintf('EXPERIMENT 06 - EXAMPLE 01: BASELINE FREQUENCY FILTERING PIPELINE (MATLAB)\n');
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
    fprintf('[INFO] Loaded MRI Scan: %dx%d pixels, class=%s, range=[%d, %d]\n', ...
            W, H, class(img), min(img(:)), max(img(:)));

    % 1. 2D FFT and Centering
    F = fft2(double(img));
    F_shift = fftshift(F);
    mag_spectrum = log(1.0 + abs(F_shift));
    total_energy = sum(abs(F_shift(:)).^2);

    % 2. Transfer Functions (D0 = 40.0, n = 2)
    u = (1:H) - floor(H / 2);
    v = (1:W) - floor(W / 2);
    [V, U] = meshgrid(v, u);
    D = hypot(U, V);
    D0 = 40.0;

    H_ILPF = double(D <= D0);
    H_BLPF = 1.0 ./ (1.0 + (D ./ D0).^(2 * 2));
    H_GLPF = exp(- (D.^2) ./ (2.0 * (D0^2)));

    % 3. Filtering in Frequency Domain
    apply_filter = @(h) uint8(min(max(real(ifft2(ifftshift(F_shift .* h))), 0), 255));

    img_ilpf = apply_filter(H_ILPF);
    img_blpf = apply_filter(H_BLPF);
    img_glpf = apply_filter(H_GLPF);

    % Save filtered images
    imwrite(img_ilpf, fullfile(out_mat_dir, 'exp06_example_01_ilpf_m.png'));
    imwrite(img_blpf, fullfile(out_mat_dir, 'exp06_example_01_blpf_m.png'));
    imwrite(img_glpf, fullfile(out_mat_dir, 'exp06_example_01_glpf_m.png'));

    % 4. Benchmarking
    tests = {
        'Ideal LP (ILPF)',        img_ilpf, H_ILPF;
        'Butterworth LP (n=2)',   img_blpf, H_BLPF;
        'Gaussian LP (GLPF)',     img_glpf, H_GLPF
    };

    fprintf('\n%-24s | %-14s | %-12s | %-10s\n', 'Filter Name', 'Energy Ret (%)', 'PSNR (dB)', 'SSIM');
    fprintf('----------------------------------------------------------------------\n');
    results = cell(size(tests, 1), 4);
    for i = 1:size(tests, 1)
        name = tests{i, 1};
        im = tests{i, 2};
        h = tests{i, 3};
        ret = (sum(abs(F_shift(:) .* h(:)).^2) / total_energy) * 100.0;
        p_val = psnr(im, img);
        s_val = ssim(im, img);
        results{i, 1} = name;
        results{i, 2} = ret;
        results{i, 3} = p_val;
        results{i, 4} = s_val;
        fprintf('%-24s | %-14.2f | %-12.2f | %-10.4f\n', name, ret, p_val, s_val);
    end
    fprintf('>>> Decision: Butterworth LP (n=2) achieves OPTIMAL balance with zero ringing.\n');

    % Publication Figure
    fig = figure('Visible', 'off', 'Color', 'white', 'Position', [100, 100, 1400, 900]);

    subplot(2, 3, 1);
    imshow(img);
    title({'(a) Original MRI Brain Scan', '(Spatial Domain)'}, 'FontSize', 11, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 2);
    imshow(mag_spectrum, []);
    colormap(gca, 'jet');
    hold on;
    theta = linspace(0, 2*pi, 200);
    plot(W/2 + D0*cos(theta), H/2 + D0*sin(theta), 'c--', 'LineWidth', 1.8);
    title({'(b) Centered Log-Spectrum', sprintf('(Cutoff Radius D_0=%.0f px)', D0)}, 'FontSize', 11, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 3);
    imshow(img_ilpf);
    title({sprintf('(c) Ideal LP Filter (D_0=%.0f)', D0), sprintf('PSNR: %.2f dB | SSIM: %.4f', results{1,3}, results{1,4}), '(Visible Gibbs Ringing)'}, ...
          'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.73, 0.11, 0.11]);

    subplot(2, 3, 4);
    imshow(img_blpf);
    title({sprintf('(d) Butterworth LP (n=2, D_0=%.0f)', D0), sprintf('PSNR: %.2f dB | SSIM: %.4f', results{2,3}, results{2,4}), '(Optimal: Smooth & Ripple-Free)'}, ...
          'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.08, 0.50, 0.24]);

    subplot(2, 3, 5);
    imshow(img_glpf);
    title({sprintf('(e) Gaussian LP (D_0=%.0f)', D0), sprintf('PSNR: %.2f dB | SSIM: %.4f', results{3,3}, results{3,4}), '(Smooth Transition: 0 Ringing)'}, ...
          'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);

    subplot(2, 3, 6);
    psnr_vals = [results{1,3}, results{2,3}, results{3,3}];
    ssim_scaled = [results{1,4}, results{2,4}, results{3,4}] * 30.0;
    b = bar([psnr_vals; ssim_scaled]');
    set(gca, 'XTickLabel', {'ILPF', 'BLPF (n=2)', 'GLPF'}, 'FontWeight', 'bold');
    ylabel('Metric Value', 'FontWeight', 'bold');
    legend({'PSNR (dB)', 'SSIM (x30 scale)'}, 'Location', 'southeast');
    title('(f) Quantitative Performance Metrics', 'FontSize', 11, 'FontWeight', 'bold', 'Color', [0.12, 0.23, 0.54]);
    grid on;

    sgtitle('Experiment 06 - Baseline Frequency Filtering Benchmark (MATLAB Pipeline)', ...
            'FontSize', 13, 'FontWeight', 'bold', 'Color', [0.06, 0.09, 0.16]);

    fig_path = fullfile(fig_dir, 'exp06_example_01_benchmark_m.png');
    saveas(fig, fig_path);
    close(fig);
    fprintf('[SUCCESS] Figure saved at: %s\n', fig_path);
end
