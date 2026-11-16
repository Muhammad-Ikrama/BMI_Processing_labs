function example_03_dicom_metadata()
% Experiment 01 - Example 7.3: DICOM Metadata Extraction & Real Metric mm Measurement
% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
% Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

baseDir = fileparts(fileparts(mfilename('fullpath')));
dicomPath = fullfile(baseDir, 'DICOM', 'IM-0001-0002.dcm');
outDir = fullfile(baseDir, 'outputs');
if ~exist(outDir, 'dir'), mkdir(outDir); end

fprintf('======================================================================\n');
fprintf('EXAMPLE 7.3: DICOM METADATA EXTRACTION & PHYSICAL CALIBRATION\n');
fprintf('======================================================================\n');

info = dicominfo(dicomPath);
fprintf('Loaded DICOM File: %s\n', dicomPath);

pName = 'Anonymous';
if isfield(info, 'PatientName')
    if isstruct(info.PatientName) && isfield(info.PatientName, 'FamilyName')
        pName = info.PatientName.FamilyName;
    else
        pName = char(info.PatientName);
    end
end

pID = 'Unknown'; if isfield(info, 'PatientID'), pID = char(info.PatientID); end
pSex = 'N/A'; if isfield(info, 'PatientSex'), pSex = char(info.PatientSex); end
pAge = 'N/A'; if isfield(info, 'PatientAge'), pAge = char(info.PatientAge); end
modality = 'PT'; if isfield(info, 'Modality'), modality = char(info.Modality); end
studyDesc = 'N/A'; if isfield(info, 'StudyDescription'), studyDesc = char(info.StudyDescription); end

fprintf('Patient Demographics: Name = %s | ID = %s | Sex = %s | Age = %s\n', pName, pID, pSex, pAge);
fprintf('Modality: %s (Positron Emission Tomography) | Study: %s\n', modality, studyDesc);

dx = info.PixelSpacing(2);
dy = info.PixelSpacing(1);
sliceThickness = 0.0;
if isfield(info, 'SliceThickness'), sliceThickness = info.SliceThickness; end

rescaleSlope = 1.0;
if isfield(info, 'RescaleSlope'), rescaleSlope = info.RescaleSlope; end
rescaleIntercept = 0.0;
if isfield(info, 'RescaleIntercept'), rescaleIntercept = info.RescaleIntercept; end

fprintf('Matrix Dimensions: %d Rows x %d Columns | Bits Allocated/Stored: %d/%d\n', info.Rows, info.Columns, info.BitsAllocated, info.BitsStored);
fprintf('Pixel Spacing (dy, dx): [%.4f mm, %.4f mm] | Slice Thickness: %.2f mm\n', dy, dx, sliceThickness);
fprintf('Radiometric Scaling: Rescale Slope = %.5f | Rescale Intercept = %.1f\n', rescaleSlope, rescaleIntercept);

rawPixels = dicomread(info);
calibratedImage = double(rawPixels) * rescaleSlope + rescaleIntercept;

fprintf('Raw Integer Pixel Range: Min = %d, Max = %d\n', min(rawPixels(:)), max(rawPixels(:)));
fprintf('Calibrated Activity Range: Min = %.2f, Max = %.2f SUV\n', min(calibratedImage(:)), max(calibratedImage(:)));

p1 = [134, 134];
p2 = [201, 201];

distPixels = sqrt((p2(2) - p1(2))^2 + (p2(1) - p1(1))^2);
distMm = sqrt(((p2(2) - p1(2)) * dx)^2 + ((p2(1) - p1(1)) * dy)^2);

fprintf('\nMetric Caliper Test (p1=[%d, %d] to p2=[%d, %d]):\n', p1(1), p1(2), p2(1), p2(2));
fprintf('  Pixel Distance      : %.2f pixels\n', distPixels);
fprintf('  Calibrated Distance : %.2f millimeters (mm)\n', distMm);

fig = figure('Color', [0.06 0.09 0.16], 'Position', [100, 100, 1050, 500], 'Visible', 'off');

% Panel 1: Image with Caliper
subplot(1, 2, 1);
imshow(calibratedImage, []);
colormap(gca, hot(256));
colorbar('Color', 'w');
title(sprintf('Brain PET Scan (Calibrated SUV)\nModality: %s | Spacing: %.3f mm/px', modality, dx), 'Color', 'w', 'FontWeight', 'bold', 'FontSize', 10.5);
hold on;

plot([p1(2), p2(2)], [p1(1), p2(1)], 'Color', [0.22 0.74 0.97], 'LineWidth', 2.5, 'Marker', 'o', 'MarkerSize', 6, 'MarkerFaceColor', [0.99 0.88 0.28]);
midX = (p1(2) + p2(2)) / 2;
midY = (p1(1) + p2(1)) / 2;
text(midX + 8, midY - 8, sprintf('%.2f mm\n(%.1f px)', distMm, distPixels), 'Color', [0.99 0.88 0.28], 'FontWeight', 'bold', 'FontSize', 9, 'BackgroundColor', [0.06 0.09 0.16], 'EdgeColor', [0.99 0.88 0.28]);

% Panel 2: Histogram
subplot(1, 2, 2);
nonZero = calibratedImage(calibratedImage > 0);
h = histogram(nonZero, 60, 'FaceColor', [0.22 0.74 0.97], 'EdgeColor', [0.06 0.09 0.16]);
set(gca, 'Color', [0.12 0.16 0.23], 'XColor', 'w', 'YColor', 'w');
grid on; set(gca, 'GridColor', [0.2 0.25 0.35], 'GridAlpha', 0.6);
title('Calibrated Radiometric Intensity Distribution', 'Color', 'w', 'FontWeight', 'bold', 'FontSize', 10.5);
xlabel('Calibrated Tracer Uptake (SUV)', 'Color', 'w', 'FontSize', 9.5);
ylabel('Pixel Frequency Count', 'Color', 'w', 'FontSize', 9.5);

outPath = fullfile(outDir, 'example_03_dicom_metadata_matlab.png');
saveas(fig, outPath);
close(fig);
fprintf('[SAVED] Visualization saved to: %s\n', outPath);
end
