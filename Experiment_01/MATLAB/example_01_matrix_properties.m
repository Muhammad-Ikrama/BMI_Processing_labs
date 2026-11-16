function example_01_matrix_properties()
% Experiment 01 - Example 7.1: Loading Medical Image & Inspecting Matrix Properties
% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
% Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

baseDir = fileparts(fileparts(mfilename('fullpath')));
imgPath = fullfile(baseDir, 'images', 'MRI.jpg');
outDir = fullfile(baseDir, 'outputs');
if ~exist(outDir, 'dir'), mkdir(outDir); end

fprintf('======================================================================\n');
fprintf('EXAMPLE 7.1: LOADING MEDICAL IMAGE & INSPECTING MATRIX PROPERTIES\n');
fprintf('======================================================================\n');

img = imread(imgPath);
if size(img, 3) == 3
    img = rgb2gray(img);
end

[rows, cols] = size(img);
totalPixels = rows * cols;
dataClass = class(img);
minVal = min(img(:));
maxVal = max(img(:));
meanVal = mean(double(img(:)));
stdVal = std(double(img(:)));

fprintf('Matrix Dimensions (H x W) : (%d, %d) Pixels\n', rows, cols);
fprintf('Data Class / Bit Depth    : %s (8-bit Unsigned Integer, 0 to 255)\n', dataClass);
fprintf('Total Number of Pixels    : %d pixels\n', totalPixels);
fprintf('Min / Max Intensity       : %d (Pure Black) / %d (Brightest Tissue)\n', minVal, maxVal);
fprintf('Mean / Std Dev Intensity  : %.2f / %.2f\n', meanVal, stdVal);

centerY = round(rows / 2);
centerX = round(cols / 2);
centerVal = img(centerY, centerX);
fprintf('Center Pixel Value (y=%d, x=%d): %d\n', centerY, centerX, centerVal);

yStart = min(100, rows - 5);
xStart = min(120, cols - 5);
subMatrix = img(yStart:yStart+4, xStart:xStart+4);

fprintf('\nExtracted 5x5 Intensity Sub-Matrix:\n');
disp(subMatrix);

fig = figure('Color', [0.06 0.09 0.16], 'Position', [100, 100, 1000, 480], 'Visible', 'off');

% Full Scan
subplot(1, 2, 1);
imshow(img, []);
title(sprintf('Brain MRI Grayscale (%dx%d)', rows, cols), 'Color', 'w', 'FontWeight', 'bold', 'FontSize', 11);
hold on;
rectangle('Position', [xStart, yStart, 5, 5], 'EdgeColor', [0.94 0.27 0.27], 'LineWidth', 2);
plot(centerX, centerY, 'y+', 'MarkerSize', 12, 'LineWidth', 2);
legend({'Center Pixel'}, 'TextColor', 'w', 'Color', [0.12 0.16 0.23], 'EdgeColor', [0.28 0.33 0.41], 'Location', 'northeast');

% 5x5 ROI Heatmap
subplot(1, 2, 2);
imagesc(double(subMatrix));
colormap(gca, hot(256));
colorbar('Color', 'w');
title(sprintf('5x5 Numerical ROI Intensity Heatmap (y=%d, x=%d)', yStart, xStart), 'Color', 'w', 'FontWeight', 'bold', 'FontSize', 11);
set(gca, 'XTick', 1:5, 'XTickLabel', xStart:xStart+4, 'YTick', 1:5, 'YTickLabel', yStart:yStart+4, 'XColor', 'w', 'YColor', 'w');

for r = 1:5
    for c = 1:5
        val = subMatrix(r, c);
        txtColor = 'w';
        if val > 128, txtColor = 'k'; end
        text(c, r, num2str(val), 'Color', txtColor, 'FontWeight', 'bold', 'HorizontalAlignment', 'center');
    end
end

outPath = fullfile(outDir, 'example_01_matrix_properties_matlab.png');
saveas(fig, outPath);
close(fig);
fprintf('[SAVED] Visualization saved to: %s\n', outPath);
end
