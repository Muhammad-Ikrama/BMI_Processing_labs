function task_01_matrix_analysis()
% Experiment 01 - Task 1: Matrix Dimension, Data Type & Dynamic Range Analysis
% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
% Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

baseDir = fileparts(fileparts(mfilename('fullpath')));
ctPath = fullfile(baseDir, 'images', 'CT.jpg');
usPath = fullfile(baseDir, 'images', 'ultrasound.jpg');
outDir = fullfile(baseDir, 'outputs');
if ~exist(outDir, 'dir'), mkdir(outDir); end

fprintf('======================================================================\n');
fprintf('STUDENT LAB TASK 1: MATRIX DIMENSIONS, DATA TYPES & DYNAMIC RANGE\n');
fprintf('======================================================================\n');

% Analyze Modality 1: CT
imgCT = imread(ctPath);
if size(imgCT, 3) == 3, imgCT = rgb2gray(imgCT); end
[r1, c1] = size(imgCT);
min1 = min(imgCT(:)); max1 = max(imgCT(:));
mean1 = mean(double(imgCT(:))); std1 = std(double(imgCT(:)));

fprintf('\n--- MODALITY 1: Computed Tomography / Panoramic X-ray (CT) ---\n');
fprintf('  Dimensions (H x W)    : %d x %d pixels\n', r1, c1);
fprintf('  Data Class / Range    : %s [%d to %d]\n', class(imgCT), min1, max1);
fprintf('  Mean +- Std Dev       : %.2f +- %.2f\n', mean1, std1);

% Extract 5x5 ROI from CT
ry1 = 150; rx1 = 200;
subCT = imgCT(ry1:ry1+4, rx1:rx1+4);
fprintf('  Extracted 5x5 ROI at (y=%d:%d, x=%d:%d):\n', ry1, ry1+4, rx1, rx1+4);
disp(subCT);

% Analyze Modality 2: Ultrasound
imgUS = imread(usPath);
if size(imgUS, 3) == 3, imgUS = rgb2gray(imgUS); end
[r2, c2] = size(imgUS);
min2 = min(imgUS(:)); max2 = max(imgUS(:));
mean2 = mean(double(imgUS(:))); std2 = std(double(imgUS(:)));

fprintf('\n--- MODALITY 2: B-Mode Ultrasound Echocardiogram (US) ---\n');
fprintf('  Dimensions (H x W)    : %d x %d pixels\n', r2, c2);
fprintf('  Data Class / Range    : %s [%d to %d]\n', class(imgUS), min2, max2);
fprintf('  Mean +- Std Dev       : %.2f +- %.2f\n', mean2, std2);

% Extract 5x5 ROI from US
ry2 = 200; rx2 = 250;
subUS = imgUS(ry2:ry2+4, rx2:rx2+4);
fprintf('  Extracted 5x5 ROI at (y=%d:%d, x=%d:%d):\n', ry2, ry2+4, rx2, rx2+4);
disp(subUS);

fig = figure('Color', [0.06 0.09 0.16], 'Position', [100, 100, 1050, 800], 'Visible', 'off');

% Row 1: CT Scan & Heatmap
subplot(2, 2, 1);
imshow(imgCT, []);
title(sprintf('CT Modality (%dx%d) | Mean=%.1f', r1, c1, mean1), 'Color', 'w', 'FontWeight', 'bold');
hold on;
rectangle('Position', [rx1, ry1, 5, 5], 'EdgeColor', [0.22 0.74 0.97], 'LineWidth', 2);

subplot(2, 2, 2);
imagesc(double(subCT)); colormap(gca, hot(256)); colorbar('Color', 'w');
title(sprintf('CT 5x5 ROI (Mean=%.1f)', mean(double(subCT(:)))), 'Color', [0.22 0.74 0.97], 'FontWeight', 'bold');
set(gca, 'XTick', 1:5, 'XTickLabel', rx1:rx1+4, 'YTick', 1:5, 'YTickLabel', ry1:ry1+4, 'XColor', 'w', 'YColor', 'w');
for r = 1:5
    for c = 1:5
        val = subCT(r, c);
        tc = 'w'; if val > 140, tc = 'k'; end
        text(c, r, num2str(val), 'Color', tc, 'FontWeight', 'bold', 'HorizontalAlignment', 'center');
    end
end

% Row 2: US Scan & Heatmap
subplot(2, 2, 3);
imshow(imgUS, []);
title(sprintf('Ultrasound Modality (%dx%d) | Mean=%.1f', r2, c2, mean2), 'Color', 'w', 'FontWeight', 'bold');
hold on;
rectangle('Position', [rx2, ry2, 5, 5], 'EdgeColor', [0.22 0.74 0.97], 'LineWidth', 2);

subplot(2, 2, 4);
imagesc(double(subUS)); colormap(gca, hot(256)); colorbar('Color', 'w');
title(sprintf('Ultrasound 5x5 ROI (Mean=%.1f)', mean(double(subUS(:)))), 'Color', [0.22 0.74 0.97], 'FontWeight', 'bold');
set(gca, 'XTick', 1:5, 'XTickLabel', rx2:rx2+4, 'YTick', 1:5, 'YTickLabel', ry2:ry2+4, 'XColor', 'w', 'YColor', 'w');
for r = 1:5
    for c = 1:5
        val = subUS(r, c);
        tc = 'w'; if val > 140, tc = 'k'; end
        text(c, r, num2str(val), 'Color', tc, 'FontWeight', 'bold', 'HorizontalAlignment', 'center');
    end
end

sgtitle('Task 1: Medical Modality Matrix Representation & ROI Comparison (MATLAB)', 'Color', 'w', 'FontSize', 12, 'FontWeight', 'bold');

outPath = fullfile(outDir, 'task_01_matrix_analysis_matlab.png');
saveas(fig, outPath);
close(fig);
fprintf('\n[SAVED] Task 1 Output saved to: %s\n', outPath);
end
