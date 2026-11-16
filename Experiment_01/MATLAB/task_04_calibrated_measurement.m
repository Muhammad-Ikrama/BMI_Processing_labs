function task_04_calibrated_measurement()
% Experiment 01 - Task 4: Calibrated Real-World Organ Measurement from Pixel Spacing
% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
% Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

baseDir = fileparts(fileparts(mfilename('fullpath')));
dicomPath = fullfile(baseDir, 'DICOM', 'IM-0001-0002.dcm');
outDir = fullfile(baseDir, 'outputs');
if ~exist(outDir, 'dir'), mkdir(outDir); end

fprintf('======================================================================\n');
fprintf('STUDENT LAB TASK 4: CALIBRATED REAL-WORLD ORGAN MEASUREMENT\n');
fprintf('======================================================================\n');

info = dicominfo(dicomPath);
rawPixels = dicomread(info);

dx = info.PixelSpacing(2);
dy = info.PixelSpacing(1);

rescaleSlope = 1.0;
if isfield(info, 'RescaleSlope'), rescaleSlope = info.RescaleSlope; end
calibratedImg = double(rawPixels) * rescaleSlope;

% Define Calipers [row, col] -> (y, x)
p1_1 = [168, 110]; p1_2 = [168, 226];
p2_1 = [134, 134]; p2_2 = [201, 201];

dPix1 = sqrt((p1_2(2) - p1_1(2))^2 + (p1_2(1) - p1_1(1))^2);
dMm1  = sqrt(((p1_2(2) - p1_1(2)) * dx)^2 + ((p1_2(1) - p1_1(1)) * dy)^2);

dPix2 = sqrt((p2_2(2) - p2_1(2))^2 + (p2_2(1) - p2_1(1))^2);
dMm2  = sqrt(((p2_2(2) - p2_1(2)) * dx)^2 + ((p2_2(1) - p2_1(1)) * dy)^2);

fprintf('\n--- Caliper 1: Transverse Brain Span ---\n');
fprintf('  Points: (%d, %d) to (%d, %d)\n', p1_1(2), p1_1(1), p1_2(2), p1_2(1));
fprintf('  Uncalibrated Distance: %.2f pixels\n', dPix1);
fprintf('  Calibrated Metric    : %.2f mm (%.2f cm)\n', dMm1, dMm1/10);

fprintf('\n--- Caliper 2: Lesion Core Span ---\n');
fprintf('  Points: (%d, %d) to (%d, %d)\n', p2_1(2), p2_1(1), p2_2(2), p2_2(1));
fprintf('  Uncalibrated Distance: %.2f pixels\n', dPix2);
fprintf('  Calibrated Metric    : %.2f mm (%.2f cm)\n', dMm2, dMm2/10);

fig = figure('Color', [0.06 0.09 0.16], 'Position', [100, 100, 1100, 520], 'Visible', 'off');

% Panel 1: PET with Calipers
subplot(1, 2, 1);
imshow(calibratedImg, []);
colormap(gca, hot(256));
colorbar('Color', 'w');
title(sprintf('Brain PET Scan (Modality: %s)\nPixelSpacing: [%.3f, %.3f] mm/px', info.Modality, dy, dx), 'Color', 'w', 'FontWeight', 'bold');
hold on;

plot([p1_1(2), p1_2(2)], [p1_1(1), p1_2(1)], 'Color', [0.22 0.74 0.97], 'LineWidth', 2.5, 'Marker', 'o', 'MarkerSize', 6, 'MarkerFaceColor', [0.06 0.09 0.16]);
midX1 = (p1_1(2) + p1_2(2)) / 2; midY1 = (p1_1(1) + p1_2(1)) / 2;
text(midX1, midY1 - 15, sprintf('%.2f mm (%.1f px)', dMm1, dPix1), 'Color', [0.22 0.74 0.97], 'FontWeight', 'bold', 'FontSize', 8.5, 'HorizontalAlignment', 'center', 'BackgroundColor', [0.06 0.09 0.16], 'EdgeColor', [0.22 0.74 0.97]);

plot([p2_1(2), p2_2(2)], [p2_1(1), p2_2(1)], 'Color', [0.99 0.88 0.28], 'LineWidth', 2.5, 'Marker', 'o', 'MarkerSize', 6, 'MarkerFaceColor', [0.06 0.09 0.16]);
midX2 = (p2_1(2) + p2_2(2)) / 2; midY2 = (p2_1(1) + p2_2(1)) / 2;
text(midX2 + 8, midY2 + 10, sprintf('%.2f mm (%.1f px)', dMm2, dPix2), 'Color', [0.99 0.88 0.28], 'FontWeight', 'bold', 'FontSize', 8.5, 'BackgroundColor', [0.06 0.09 0.16], 'EdgeColor', [0.99 0.88 0.28]);

% Panel 2: Bar Comparison
subplot(1, 2, 2);
barData = [dPix1, dMm1; dPix2, dMm2];
b = bar(barData, 'grouped');
b(1).FaceColor = [0.39 0.45 0.55];
b(2).FaceColor = [0.22 0.74 0.97];
set(gca, 'Color', [0.12 0.16 0.23], 'XColor', 'w', 'YColor', 'w');
set(gca, 'XTickLabel', {'Span A (Brain Width)', 'Span B (Lesion Core)'});
legend({'Uncalibrated (Pixels)', 'Calibrated (mm)'}, 'TextColor', 'w', 'Color', [0.06 0.09 0.16], 'EdgeColor', [0.28 0.33 0.41], 'Location', 'north');
grid on; set(gca, 'GridColor', [0.2 0.25 0.35], 'GridAlpha', 0.6);
title('Pixel vs. Physical Metric Dimension Calibration (MATLAB)', 'Color', 'w', 'FontWeight', 'bold');
ylabel('Magnitude Value', 'Color', 'w');

outPath = fullfile(outDir, 'task_04_calibrated_measurement_matlab.png');
saveas(fig, outPath);
close(fig);
fprintf('\n[SAVED] Task 4 Output saved to: %s\n', outPath);
end
