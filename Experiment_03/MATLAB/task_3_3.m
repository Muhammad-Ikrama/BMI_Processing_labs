%% ==============================================================================
%% SCRIPT: task_3_3.m
%% Experiment 03: Image Smoothing of Medical Images Using Spatial Domain Mean & Gaussian Filters
%% Task 3.3: 2D Gaussian Kernel Construction, Normalization & Spread Parameter Sweep
%% Course: Medical Image Processing | Riphah International University
%% Instructor: Engr. Rana Talha Khalid
%% ==============================================================================

function task_3_3()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 03 - MATLAB TASK 3.3: 2D GAUSSIAN KERNEL GENERATION\n');
    fprintf('======================================================================\n');

    script_dir = fileparts(mfilename('fullpath'));
    exp_dir = fileparts(script_dir);
    img_path = fullfile(exp_dir, 'Inputs', 'images', 'MRI.jpg');

    if ~exist(img_path, 'file')
        img_path = fullfile(exp_dir, '..', '..', 'images', 'MRI.jpg');
    end

    img = imread(img_path);
    if size(img, 3) == 3
        img = rgb2gray(img);
    end

    % Simulate Gaussian noise
    rng(42);
    noise_var = (18 / 255)^2;
    noisy = imnoise(img, 'gaussian', 0, noise_var);

    k_size = 7;
    radius = floor(k_size / 2);
    [X, Y] = meshgrid(-radius:radius, -radius:radius);

    sigmas = [0.6, 1.2, 2.0];
    kernels = cell(1, 3);
    filtered_images = cell(1, 3);
    psnr_vals = zeros(1, 3);
    ssim_vals = zeros(1, 3);

    fprintf('\nConstructing 7x7 Gaussian Kernels from Mathematical Formula:\n');
    fprintf('----------------------------------------------------------------------\n');

    for idx = 1:length(sigmas)
        sig = sigmas(idx);
        % Mathematical Formula: G(x, y) = 1/(2*pi*sigma^2) * exp(-(x^2+y^2)/(2*sigma^2))
        raw_kernel = (1 / (2 * pi * sig^2)) * exp(-(X.^2 + Y.^2) / (2 * sig^2));
        k_norm = raw_kernel / sum(raw_kernel, 'all');

        k_sum = sum(k_norm, 'all');
        c_peak = k_norm(radius + 1, radius + 1);
        c_tail = k_norm(1, 1);

        fprintf('Sigma = %.1f | Sum = %.6f | Center Peak = %.5f | Corner Tail = %.7f\n', ...
                sig, k_sum, c_peak, c_tail);

        f_im = imfilter(noisy, k_norm, 'replicate');
        p = psnr(f_im, img);
        s = ssim(f_im, img);

        kernels{idx} = k_norm;
        filtered_images{idx} = f_im;
        psnr_vals(idx) = p;
        ssim_vals(idx) = s;
    end

    fprintf('----------------------------------------------------------------------\n');
    fprintf('%-12s | %-14s | %-10s | %-8s | %-30s\n', 'Sigma Spread', 'Center Weight', 'PSNR (dB)', 'SSIM', 'Performance');
    fprintf('----------------------------------------------------------------------\n');
    for idx = 1:3
        sig = sigmas(idx);
        c_wt = kernels{idx}(radius+1, radius+1);
        if sig == 0.6
            perf = 'Sharp edge retention; slight noise';
        elseif sig == 1.2
            perf = 'Optimal clinical trade-off';
        else
            perf = 'Heavy noise elimination; soft blur';
        end
        fprintf('sigma = %-6.1f | %-14.5f | %-10.2f | %-8.4f | %s\n', sig, c_wt, psnr_vals(idx), ssim_vals(idx), perf);
    end

    % Visualization: 3 rows x 3 columns
    fig = figure('Visible', 'off', 'Position', [100, 100, 1300, 1100]);

    for idx = 1:3
        sig = sigmas(idx);
        k_norm = kernels{idx};
        f_im = filtered_images{idx};

        % Row 1: Heatmap
        subplot(3, 3, idx);
        imagesc(-radius:radius, -radius:radius, k_norm);
        colormap(gca, parula); colorbar;
        title(sprintf('Heatmap (sig=%.1f)\nCenter Peak: %.4f', sig, k_norm(radius+1, radius+1)), ...
              'FontSize', 9.5, 'FontWeight', 'bold');
        xlabel('X Offset'); ylabel('Y Offset');

        % Row 2: 3D Surface
        subplot(3, 3, idx + 3);
        surf(X, Y, k_norm);
        shading interp;
        colormap(gca, jet);
        title(sprintf('3D Bell Surface (sig=%.1f)\nVolume Sum = 1.000', sig), ...
              'FontSize', 9.5, 'FontWeight', 'bold');
        xlabel('X'); ylabel('Y'); zlabel('Weight');
        view(45, 30);

        % Row 3: Filtered Scan
        subplot(3, 3, idx + 6);
        imshow(f_im);
        title(sprintf('Filtered Scan (sig=%.1f)\nPSNR: %.2f dB | SSIM: %.4f', sig, psnr_vals(idx), ssim_vals(idx)), ...
              'FontSize', 9.5, 'FontWeight', 'bold', 'Color', [0.12 0.23 0.54]);
    end

    sgtitle('MATLAB Task 3.3: 2D Gaussian Kernel Construction, Normalization & Spread Parameter Sweep', ...
            'FontSize', 13, 'FontWeight', 'bold');

    % Save figures
    out_dir_m = fullfile(exp_dir, 'Outputs', 'MATLAB');
    fig_dir = fullfile(exp_dir, 'Figures');

    out_path_1 = fullfile(out_dir_m, 'exp03_task_3_3_gaussian_kernel_sweep_m.png');
    out_path_2 = fullfile(fig_dir, 'exp03_task_3_3_gaussian_kernel_sweep_m.png');

    exportgraphics(fig, out_path_1, 'Resolution', 300);
    exportgraphics(fig, out_path_2, 'Resolution', 300);
    close(fig);

    fprintf('[SUCCESS] Saved MATLAB figure to:\n  %s\n  %s\n', out_path_1, out_path_2);
end
