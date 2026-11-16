%% Experiment 02 - Task 2.5: Clinical Multi-Panel Radiograph Contrast Report (MATLAB)
% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
% Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

function task_2_5_multipanel_contrast_report()
    fprintf('======================================================================\n');
    fprintf('TASK 2.5: CLINICAL MULTI-PANEL RADIOGRAPH CONTRAST REPORT (MATLAB)\n');
    fprintf('======================================================================\n');

    baseDir = fileparts(fileparts(mfilename('fullpath')));
    imgPath = fullfile(baseDir, 'Inputs', 'images', 'Lung-HR-contrast.png');
    if ~exist(imgPath, 'file')
        imgPath = fullfile(fileparts(baseDir), 'images', 'Lung-HR-contrast.png');
    end

    img = imread(imgPath);
    if size(img, 3) == 3, img = rgb2gray(img); end

    gheImg = histeq(img);
    claheImg = adapthisteq(img, 'ClipLimit', 0.02, 'NumTiles', [8 8]);

    outDir = fullfile(baseDir, 'Outputs', 'MATLAB');
    figDir = fullfile(baseDir, 'Figures');
    if ~exist(outDir, 'dir'), mkdir(outDir); end
    if ~exist(figDir, 'dir'), mkdir(figDir); end

    fig = figure('Color', [0.06 0.09 0.16], 'Position', [100, 100, 1400, 900], 'Visible', 'off');

    scans = {img, gheImg, claheImg};
    titles = {'Original Scan', 'Global HE (GHE)', 'CLAHE (Clip=0.02) [OPTIMAL]'};
    colors = {[0.58 0.64 0.72], [0.97 0.44 0.44], [0.29 0.87 0.50]};

    for k = 1:3
        % Top row: Image
        subplot(2, 3, k);
        imshow(scans{k}, []);
        title(titles{k}, 'Color', colors{k}, 'FontWeight', 'bold');
        hold on;
        % ROIs: Lung Parenchyma (Cyan) & Background Air (Yellow)
        [H, W] = size(img);
        rectangle('Position', [W*0.65, H*0.45, 100, 100], 'EdgeColor', 'c', 'LineWidth', 2);
        rectangle('Position', [W*0.05, H*0.05, 80, 80], 'EdgeColor', 'y', 'LineWidth', 2, 'LineStyle', '--');

        % Bottom row: Histogram
        subplot(2, 3, k + 3);
        [c, ~] = imhist(scans{k});
        bar(0:255, c, 'FaceColor', colors{k}, 'EdgeColor', 'none');
        set(gca, 'Color', [0.12 0.16 0.23], 'XColor', [0.58 0.64 0.72], 'YColor', [0.58 0.64 0.72]);
        title(sprintf('Histogram: %s', titles{k}), 'Color', 'w');
        xlim([0 255]); grid on;
    end

    sgtitle('Task 2.5: Clinical Multi-Panel Radiograph Contrast Report with ROI Benchmarking (MATLAB)', 'Color', [0.22 0.74 0.97], 'FontWeight', 'bold');

    saveas(fig, fullfile(outDir, 'task_2_5_multipanel_contrast_report_matlab.png'));
    saveas(fig, fullfile(figDir, 'task_2_5_multipanel_contrast_report_matlab.png'));
    close(fig);
    fprintf('[SAVED] Saved MATLAB Task 2.5 figure.\n');
end
