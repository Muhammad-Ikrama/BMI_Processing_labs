%% Experiment 02 - Task 2.1: Manual Discrete Histogram and Empirical PDF (MATLAB)
% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
% Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

function task_2_1_manual_histogram()
    fprintf('======================================================================\n');
    fprintf('TASK 2.1: MANUAL HISTOGRAM & EMPIRICAL PDF COMPUTATION (MATLAB)\n');
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

    % Primitive nested loop computation (WITHOUT imhist)
    histManual = zeros(256, 1);
    for r = 1:H
        for c = 1:W
            val = double(img(r, c));
            histManual(val + 1) = histManual(val + 1) + 1;
        end
    end

    pdfManual = histManual / double(totalPixels);

    sumHist = sum(histManual);
    sumPdf = sum(pdfManual);

    fprintf('Total Pixels : %d\n', totalPixels);
    fprintf('Sum of Counts: %d -> %s\n', sumHist, mat2str(sumHist == totalPixels));
    fprintf('Sum of PDF   : %.6f -> %s\n', sumPdf, mat2str(abs(sumPdf - 1.0) < 1e-9));

    outDir = fullfile(baseDir, 'Outputs', 'MATLAB');
    figDir = fullfile(baseDir, 'Figures');
    if ~exist(outDir, 'dir'), mkdir(outDir); end
    if ~exist(figDir, 'dir'), mkdir(figDir); end

    fig = figure('Color', [0.06 0.09 0.16], 'Position', [100, 100, 1100, 500], 'Visible', 'off');

    subplot(1, 2, 1);
    imshow(img, []);
    title(sprintf('Chest Radiograph (Xray.jpg)\n%dx%d (%d px)', W, H, totalPixels), 'Color', 'w', 'FontWeight', 'bold');

    subplot(1, 2, 2);
    bar(0:255, histManual, 'FaceColor', [0.22 0.74 0.97], 'EdgeColor', 'none');
    set(gca, 'Color', [0.12 0.16 0.23], 'XColor', [0.58 0.64 0.72], 'YColor', [0.58 0.64 0.72]);
    title(sprintf('Manual Histogram (Sum=%d, PDF Sum=%.4f)', sumHist, sumPdf), 'Color', 'w', 'FontWeight', 'bold');
    xlabel('Intensity r_k', 'Color', [0.58 0.64 0.72]);
    ylabel('Frequency n_k', 'Color', [0.58 0.64 0.72]);
    xlim([0 255]); grid on;

    sgtitle('Task 2.1: Manual Discrete Histogram & Empirical PDF (MATLAB)', 'Color', [0.22 0.74 0.97], 'FontWeight', 'bold');

    saveas(fig, fullfile(outDir, 'task_2_1_manual_histogram_matlab.png'));
    saveas(fig, fullfile(figDir, 'task_2_1_manual_histogram_matlab.png'));
    close(fig);
    fprintf('[SAVED] Saved MATLAB Task 2.1 figure.\n');
end
