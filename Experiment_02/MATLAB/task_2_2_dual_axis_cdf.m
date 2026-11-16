%% Experiment 02 - Task 2.2: Dual-Axis Histogram and CDF Curve (MATLAB)
% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
% Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

function task_2_2_dual_axis_cdf()
    fprintf('======================================================================\n');
    fprintf('TASK 2.2: DUAL-AXIS HISTOGRAM & CDF CURVE (MATLAB)\n');
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

    [counts, ~] = imhist(img);
    pdf = counts / double(totalPixels);
    cdf = cumsum(pdf);

    [maxCount, maxIdx] = max(counts);
    steepestIntensity = maxIdx - 1;

    fprintf('Steepest Derivative Peak: r = %d (Count = %d)\n', steepestIntensity, maxCount);

    outDir = fullfile(baseDir, 'Outputs', 'MATLAB');
    figDir = fullfile(baseDir, 'Figures');
    if ~exist(outDir, 'dir'), mkdir(outDir); end
    if ~exist(figDir, 'dir'), mkdir(figDir); end

    fig = figure('Color', [0.06 0.09 0.16], 'Position', [100, 100, 1200, 500], 'Visible', 'off');

    % Left: Image
    subplot(1, 2, 1);
    imshow(img, []);
    title(sprintf('Chest Radiograph\n%dx%d (%d px)', W, H, totalPixels), 'Color', 'w', 'FontWeight', 'bold');

    % Right: Dual-Axis Plot
    subplot(1, 2, 2);
    yyaxis left;
    bar(0:255, counts, 'FaceColor', [0.22 0.74 0.97], 'EdgeColor', 'none');
    ylabel('Frequency Count (n_k)');
    xlim([0 255]);

    yyaxis right;
    plot(0:255, cdf, 'Color', [0.29 0.87 0.50], 'LineWidth', 2.5);
    ylabel('Cumulative Probability P(r_k)');
    ylim([0 1.05]);

    set(gca, 'Color', [0.12 0.16 0.23], 'XColor', [0.58 0.64 0.72]);
    title('Dual-Axis Histogram & CDF Response', 'Color', 'w', 'FontWeight', 'bold');
    xlabel('Intensity Level r_k', 'Color', [0.58 0.64 0.72]);
    grid on;

    sgtitle('Task 2.2: Dual-Axis Histogram Analysis & CDF Slope Identification (MATLAB)', 'Color', [0.22 0.74 0.97], 'FontWeight', 'bold');

    saveas(fig, fullfile(outDir, 'task_2_2_dual_axis_cdf_matlab.png'));
    saveas(fig, fullfile(figDir, 'task_2_2_dual_axis_cdf_matlab.png'));
    close(fig);
    fprintf('[SAVED] Saved MATLAB Task 2.2 figure.\n');
end
