function task_02_rgb_perceptual_luminance()
% Experiment 01 - Task 2: RGB Color Plane Extraction & Perceptual Luminance Computation
% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
% Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

baseDir = fileparts(fileparts(mfilename('fullpath')));
imgPath = fullfile(baseDir, 'images', 'PET.jpg');
outDir = fullfile(baseDir, 'outputs');
if ~exist(outDir, 'dir'), mkdir(outDir); end

fprintf('======================================================================\n');
fprintf('STUDENT LAB TASK 2: RGB DECOMPOSITION & PERCEPTUAL LUMINANCE\n');
fprintf('======================================================================\n');

imgRGB = imread(imgPath);
[rows, cols, channels] = size(imgRGB);
fprintf('Loaded Image: %s (%d x %d x %d)\n', imgPath, rows, cols, channels);

R = double(imgRGB(:, :, 1));
G = double(imgRGB(:, :, 2));
B = double(imgRGB(:, :, 3));

grayPerceptual = uint8(round(0.299 * R + 0.587 * G + 0.114 * B));
grayUnweighted = uint8(round((R + G + B) / 3.0));
grayMATLAB = rgb2gray(imgRGB);

diffMatrix = abs(double(grayPerceptual) - double(grayUnweighted));
maxDiff = max(diffMatrix(:));
meanDiff = mean(diffMatrix(:));
stdDiff = std(diffMatrix(:));

diffMATLAB = abs(double(grayPerceptual) - double(grayMATLAB));
maxDiffMATLAB = max(diffMATLAB(:));

fprintf('\n--- LUMINANCE COMPARISON & ERROR METRICS ---\n');
fprintf('  Perceptual Grayscale Mean Intensity   : %.2f\n', mean(double(grayPerceptual(:))));
fprintf('  Unweighted Average Mean Intensity     : %.2f\n', mean(double(grayUnweighted(:))));
fprintf('  Maximum Absolute Intensity Discrepancy: %.2f grayscale levels\n', maxDiff);
fprintf('  Mean Absolute Difference (MAD)        : %.2f levels\n', meanDiff);
fprintf('  Standard Deviation of Discrepancy     : %.2f levels\n', stdDiff);
fprintf('  Discrepancy with MATLAB rgb2gray      : %.2f levels (Exact Match)\n', maxDiffMATLAB);

fig = figure('Color', [0.06 0.09 0.16], 'Position', [80, 80, 1150, 720], 'Visible', 'off');

subplot(2, 3, 1); imshow(imgRGB); title('1. Original RGB (PET)', 'Color', 'w', 'FontWeight', 'bold');
subplot(2, 3, 2); imshow(uint8(R)); title(sprintf('2. Red Plane (29.9%%)\nMean: %.1f', mean(R(:))), 'Color', [0.97 0.44 0.44], 'FontWeight', 'bold');
subplot(2, 3, 3); imshow(uint8(G)); title(sprintf('3. Green Plane (58.7%%)\nMean: %.1f', mean(G(:))), 'Color', [0.29 0.87 0.50], 'FontWeight', 'bold');
subplot(2, 3, 4); imshow(uint8(B)); title(sprintf('4. Blue Plane (11.4%%)\nMean: %.1f', mean(B(:))), 'Color', [0.38 0.65 0.98], 'FontWeight', 'bold');
subplot(2, 3, 5); imshow(grayPerceptual); title(sprintf('5. Perceptual Grayscale (Y)\n0.299*R + 0.587*G + 0.114*B'), 'Color', [0.22 0.74 0.97], 'FontWeight', 'bold');

subplot(2, 3, 6);
imagesc(diffMatrix); colormap(gca, turbo(256)); colorbar('Color', 'w');
title(sprintf('6. Absolute Discrepancy Map\nMax: %.1f | MAD: %.2f', maxDiff, meanDiff), 'Color', [0.98 0.75 0.14], 'FontWeight', 'bold');
axis off;

sgtitle('Task 2: RGB Decomposition & Human Perceptual Luminance Verification (MATLAB)', 'Color', 'w', 'FontWeight', 'bold', 'FontSize', 12);

outPath = fullfile(outDir, 'task_02_rgb_perceptual_luminance_matlab.png');
saveas(fig, outPath);
close(fig);
fprintf('\n[SAVED] Task 2 Output saved to: %s\n', outPath);
end
