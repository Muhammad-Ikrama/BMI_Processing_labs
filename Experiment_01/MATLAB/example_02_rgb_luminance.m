function example_02_rgb_luminance()
% Experiment 01 - Example 7.2: RGB Decomposition & Perceptual Luminance Conversion
% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
% Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

baseDir = fileparts(fileparts(mfilename('fullpath')));
imgPath = fullfile(baseDir, 'images', 'PET.jpg');
outDir = fullfile(baseDir, 'outputs');
if ~exist(outDir, 'dir'), mkdir(outDir); end

fprintf('======================================================================\n');
fprintf('EXAMPLE 7.2: RGB DECOMPOSITION & PERCEPTUAL LUMINANCE CONVERSION\n');
fprintf('======================================================================\n');

imgRGB = imread(imgPath);
[rows, cols, channels] = size(imgRGB);
fprintf('Loaded Color Image Shape: (%d, %d, %d) [Height, Width, Channels]\n', rows, cols, channels);

R = double(imgRGB(:, :, 1));
G = double(imgRGB(:, :, 2));
B = double(imgRGB(:, :, 3));

fprintf('Red Channel (R)   : Mean = %.2f, Dynamic Range = [%.0f, %.0f]\n', mean(R(:)), min(R(:)), max(R(:)));
fprintf('Green Channel (G) : Mean = %.2f, Dynamic Range = [%.0f, %.0f]\n', mean(G(:)), min(G(:)), max(G(:)));
fprintf('Blue Channel (B)  : Mean = %.2f, Dynamic Range = [%.0f, %.0f]\n', mean(B(:)), min(B(:)), max(B(:)));

% Human Perceptual Luminance Formula (ITU-R BT.601)
grayPerceptual = uint8(0.299 * R + 0.587 * G + 0.114 * B);
grayUnweighted = uint8((R + G + B) / 3.0);

diffMatrix = abs(double(grayPerceptual) - double(grayUnweighted));
maxDiff = max(diffMatrix(:));
meanDiff = mean(diffMatrix(:));

fprintf('\nPerceptual Grayscale Shape: (%d, %d) [1-Channel 2D Matrix]\n', size(grayPerceptual, 1), size(grayPerceptual, 2));
fprintf('Max Intensity Discrepancy (Perceptual vs Unweighted): %.2f intensity levels\n', maxDiff);
fprintf('Mean Absolute Difference: %.2f levels (Confirms perceptual contrast preservation)\n', meanDiff);

fig = figure('Color', [0.06 0.09 0.16], 'Position', [80, 80, 1100, 700], 'Visible', 'off');

subplot(2, 3, 1);
imshow(imgRGB);
title('Original RGB Composite', 'Color', 'w', 'FontWeight', 'bold', 'FontSize', 10);

subplot(2, 3, 2);
imshow(uint8(R));
title(sprintf('Red Channel (29.9%%)\nMean: %.1f', mean(R(:))), 'Color', [0.97 0.44 0.44], 'FontWeight', 'bold', 'FontSize', 9.5);

subplot(2, 3, 3);
imshow(uint8(G));
title(sprintf('Green Channel (58.7%%)\nMean: %.1f', mean(G(:))), 'Color', [0.29 0.87 0.50], 'FontWeight', 'bold', 'FontSize', 9.5);

subplot(2, 3, 4);
imshow(uint8(B));
title(sprintf('Blue Channel (11.4%%)\nMean: %.1f', mean(B(:))), 'Color', [0.38 0.65 0.98], 'FontWeight', 'bold', 'FontSize', 9.5);

subplot(2, 3, 5);
imshow(grayPerceptual);
title(sprintf('Human Perceptual Grayscale\n(0.299*R + 0.587*G + 0.114*B)'), 'Color', [0.22 0.74 0.97], 'FontWeight', 'bold', 'FontSize', 9.5);

subplot(2, 3, 6);
imagesc(diffMatrix);
colormap(gca, turbo(256));
colorbar('Color', 'w');
title(sprintf('Absolute Difference Map\nMax: %.1f | Mean: %.2f', maxDiff, meanDiff), 'Color', [0.98 0.75 0.14], 'FontWeight', 'bold', 'FontSize', 9.5);
axis off;

sgtitle('RGB Decomposition & Human Perceptual Luminance Analysis', 'Color', 'w', 'FontWeight', 'bold', 'FontSize', 12);

outPath = fullfile(outDir, 'example_02_rgb_luminance_matlab.png');
saveas(fig, outPath);
close(fig);
fprintf('[SAVED] Visualization saved to: %s\n', outPath);
end
