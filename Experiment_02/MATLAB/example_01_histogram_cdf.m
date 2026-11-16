%% Experiment 02 - Example 1: Medical Image Histogram & CDF Computation (MATLAB)
% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
% Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

function example_01_histogram_cdf()
    fprintf('======================================================================\n');
    fprintf('EXAMPLE 1: MEDICAL IMAGE HISTOGRAM & CDF COMPUTATION (MATLAB)\n');
    fprintf('======================================================================\n');

    baseDir = fileparts(fileparts(mfilename('fullpath')));
    imgPath = fullfile(baseDir, 'Inputs', 'images', 'Xray.jpg');
    if ~exist(imgPath, 'file')
        imgPath = fullfile(fileparts(baseDir), 'images', 'Xray.jpg');
    end

    img = imread(imgPath);
    if size(img, 3) == 3, img = rgb2gray(img); end
    [H, W] = size(img);
    totalPixels = H * W;

    % 1. Discrete Histogram and Normalized Empirical PDF
    [counts, grayLevels] = imhist(img);
    pdf = counts / totalPixels;

    % 2. Cumulative Distribution Function (CDF)
    cdf = cumsum(pdf);

    % 3. Shannon Information Entropy
    p_nz = pdf(pdf > 0);
    entropyVal = -sum(p_nz .* log2(p_nz));

    fprintf('Resolution: %d x %d (%d pixels)\n', W, H, totalPixels);
    fprintf('Dynamic Range: [%d, %d] | Mean: %.2f | Std: %.2f\n', min(img(:)), max(img(:)), mean(double(img(:))), std(double(img(:))));
    fprintf('Shannon Entropy: %.4f bits/pixel\n', entropyVal);
    fprintf('CDF Final Sum: %.6f\n', cdf(end));

    % Visualization
    outDir = fullfile(baseDir, 'Outputs', 'MATLAB');
    figDir = fullfile(baseDir, 'Figures');
    if ~exist(outDir, 'dir'), mkdir(outDir); end
    if ~exist(figDir, 'dir'), mkdir(figDir); end

    fig = figure('Color', [0.06 0.09 0.16], 'Position', [100, 100, 1200, 450], 'Visible', 'off');

    % Subplot 1: Image
    subplot(1, 3, 1);
    imshow(img, []);
    title(sprintf('Chest Radiograph\n%dx%d (%d px)', W, H, totalPixels), 'Color', 'w', 'FontWeight', 'bold');

    % Subplot 2: Histogram
    subplot(1, 3, 2);
    bar(0:255, counts, 'FaceColor', [0.22 0.74 0.97], 'EdgeColor', 'none');
    set(gca, 'Color', [0.12 0.16 0.23], 'XColor', [0.58 0.64 0.72], 'YColor', [0.58 0.64 0.72]);
    title('Discrete Histogram h(r_k)', 'Color', 'w', 'FontWeight', 'bold');
    xlabel('Intensity r_k', 'Color', [0.58 0.64 0.72]);
    ylabel('Pixel Count n_k', 'Color', [0.58 0.64 0.72]);
    xlim([0 255]); grid on;

    % Subplot 3: CDF
    subplot(1, 3, 3);
    plot(0:255, cdf, 'Color', [0.29 0.87 0.50], 'LineWidth', 2.5);
    set(gca, 'Color', [0.12 0.16 0.23], 'XColor', [0.58 0.64 0.72], 'YColor', [0.58 0.64 0.72]);
    title('Cumulative Distribution Function (CDF)', 'Color', 'w', 'FontWeight', 'bold');
    xlabel('Intensity r_k', 'Color', [0.58 0.64 0.72]);
    ylabel('Cumulative Probability P(r_k)', 'Color', [0.58 0.64 0.72]);
    xlim([0 255]); ylim([0 1.05]); grid on;

    sgtitle('Example 1: Radiograph Intensity Distribution and Cumulative Response (MATLAB)', 'Color', [0.22 0.74 0.97], 'FontWeight', 'bold');

    saveas(fig, fullfile(outDir, 'example_01_histogram_cdf_matlab.png'));
    saveas(fig, fullfile(figDir, 'example_01_histogram_cdf_matlab.png'));
    close(fig);
    fprintf('[SAVED] Saved MATLAB Example 1 figure.\n');
end
