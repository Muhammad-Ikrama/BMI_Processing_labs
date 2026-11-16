%% ==============================================================================
%% SCRIPT: task_4_1.m
%% Experiment 04: Noise Modeling & Adaptive Filtering in Medical Images
%% Task 4.1: Synthetic Noise Modeling & Statistical Probability Density (PDF) Analysis
%% Course: Medical Image Processing | Riphah International University
%% Instructor: Engr. Rana Talha Khalid
%% ==============================================================================

function task_4_1()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 04 - MATLAB TASK 4.1: NOISE MODELING & PDF ANALYSIS\n');
    fprintf('======================================================================\n');

    script_dir = fileparts(mfilename('fullpath'));
    exp_dir = fileparts(script_dir);
    img_path = fullfile(exp_dir, 'Inputs', 'images', 'MRI.jpg');

    if ~exist(img_path, 'file')
        img_path = fullfile(exp_dir, '..', '..', 'images', 'MRI.jpg');
    end

    ref = imread(img_path);
    if size(ref, 3) == 3; ref = rgb2gray(ref); end

    % 1. Simulate 3 distinct noise models
    rng(42);
    fprintf('[INFO] Simulating Additive Gaussian Noise (sigma = 20)...\n');
    noisy_gauss = imnoise(ref, 'gaussian', 0, (20/255)^2);
    res_gauss = double(noisy_gauss) - double(ref);

    fprintf('[INFO] Simulating Salt-and-Pepper Impulse Noise (15%%)...\n');
    noisy_sp = imnoise(ref, 'salt & pepper', 0.15);
    res_sp = double(noisy_sp) - double(ref);

    fprintf('[INFO] Simulating Multiplicative Speckle Noise (var = 0.25)...\n');
    noisy_speckle = imnoise(ref, 'speckle', 0.25);
    res_speckle = double(noisy_speckle) - double(ref);

    % 2. Statistical Moments
    mean_g = mean(res_gauss, 'all'); std_g = std(res_gauss, 0, 'all');
    mean_sp = mean(res_sp, 'all'); std_sp = std(res_sp, 0, 'all');
    mean_spk = mean(res_speckle, 'all'); std_spk = std(res_speckle, 0, 'all');

    fprintf('\n-----------------------------------------------------------------------\n');
    fprintf('STATISTICAL MOMENTS OF RESIDUAL PERTURBATIONS (Noisy - Clean):\n');
    fprintf('  * Gaussian Residual:  Mean = %+.2f (Expected: ~0.0), StdDev = %.2f\n', mean_g, std_g);
    fprintf('  * S&P Residual:       Mean = %+.2f, StdDev = %.2f (Bipolar Extrema)\n', mean_sp, std_sp);
    fprintf('  * Speckle Residual:   Mean = %+.2f, StdDev = %.2f (Signal-Dependent)\n', mean_spk, std_spk);
    fprintf('-----------------------------------------------------------------------\n');

    % 3. Visualization: 2 Rows x 3 Columns
    fig = figure('Visible', 'off', 'Position', [100, 100, 1300, 850]);

    % Row 1: Images
    subplot(2, 3, 1);
    imshow(noisy_gauss);
    title('A: Additive Gaussian (sigma=20)', 'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.12 0.23 0.54]);

    subplot(2, 3, 2);
    imshow(noisy_sp);
    title('B: Salt & Pepper (15%)', 'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.72 0.15 0.15]);

    subplot(2, 3, 3);
    imshow(noisy_speckle);
    title('C: Multiplicative Speckle (var=0.25)', 'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.77 0.54 0.02]);

    % Row 2: Histograms
    subplot(2, 3, 4);
    histogram(res_gauss(:), -70:2:70, 'Normalization', 'pdf', 'FaceColor', [0.23 0.51 0.96]);
    hold on;
    x_g = -70:1:70;
    plot(x_g, normpdf(x_g, mean_g, std_g), '-k', 'LineWidth', 2);
    hold off;
    title('Gaussian Residual PDF (Zero-Mean)', 'FontSize', 9.5, 'FontWeight', 'bold');
    xlabel('Error (g - f)'); ylabel('PDF'); grid on;

    subplot(2, 3, 5);
    histogram(res_sp(:), -255:5:255, 'Normalization', 'pdf', 'FaceColor', [0.93 0.27 0.27]);
    set(gca, 'YScale', 'log');
    title('S&P Residual (Bipolar Impulses)', 'FontSize', 9.5, 'FontWeight', 'bold');
    xlabel('Error (g - f)'); ylabel('Log Probability'); grid on;

    subplot(2, 3, 6);
    histogram(res_speckle(:), -120:4:120, 'Normalization', 'pdf', 'FaceColor', [0.97 0.45 0.09]);
    title('Speckle Residual Distribution', 'FontSize', 9.5, 'FontWeight', 'bold');
    xlabel('Error (g - f)'); ylabel('PDF'); grid on;

    sgtitle('MATLAB Task 4.1: Synthetic Noise Modeling & Statistical Probability Density (PDF) Analysis', ...
            'FontSize', 13, 'FontWeight', 'bold');

    out_dir_m = fullfile(exp_dir, 'Outputs', 'MATLAB');
    fig_dir = fullfile(exp_dir, 'Figures');

    out_path_1 = fullfile(out_dir_m, 'exp04_task_4_1_noise_models_pdf_m.png');
    out_path_2 = fullfile(fig_dir, 'exp04_task_4_1_noise_models_pdf_m.png');

    exportgraphics(fig, out_path_1, 'Resolution', 300);
    exportgraphics(fig, out_path_2, 'Resolution', 300);
    close(fig);

    fprintf('[SUCCESS] Saved MATLAB figure to:\n  %s\n  %s\n', out_path_1, out_path_2);
end
