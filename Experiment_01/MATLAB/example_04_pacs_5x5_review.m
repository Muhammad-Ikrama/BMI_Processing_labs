function example_04_pacs_5x5_review()
% Experiment 01 - Section 8: Clinical PACS Workstation 5x5 (25-Panel) Volumetric Series Review
% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
% Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

baseDir = fileparts(fileparts(mfilename('fullpath')));
mriPath = fullfile(baseDir, 'DICOM', 'IMG-0004-00001.dcm');
ctPath = fullfile(baseDir, 'images', 'CT.jpg');
petPath = fullfile(baseDir, 'images', 'PET.jpg');
outDir = fullfile(baseDir, 'outputs');
if ~exist(outDir, 'dir'), mkdir(outDir); end

fprintf('======================================================================\n');
fprintf('EXAMPLE 8: 5x5 (25-PANEL) CLINICAL PACS WORKSTATION SERIES REVIEW\n');
fprintf('======================================================================\n');

mriInfo = dicominfo(mriPath);
rawMRI = dicomread(mriInfo);
if ndims(rawMRI) == 4
    numFrames = size(rawMRI, 4);
else
    numFrames = size(rawMRI, 3);
end
fprintf('Loaded 3D MRI Volume: %d sequential frames (%dx%d pixels)\n', numFrames, size(rawMRI, 1), size(rawMRI, 2));

imgCT = imread(ctPath);
if size(imgCT, 3) == 3, imgCT = rgb2gray(imgCT); end
imgCT = imresize(imgCT, [512, 512]);

imgPET = imread(petPath);
if size(imgPET, 3) == 3, imgPET = rgb2gray(imgPET); end
imgPET = imresize(imgPET, [512, 512]);

fprintf('Loaded Multi-Modal CT & PET Scans: Resized to 512 x 512 pixels\n');

fig = figure('Color', [0.04 0.07 0.13], 'Position', [50, 50, 1100, 950], 'Visible', 'off');

for k = 1:25
    ax = subplot(5, 5, k);
    if k <= 21
        if ndims(rawMRI) == 4
            frameSlice = squeeze(rawMRI(:, :, 1, k));
        else
            frameSlice = rawMRI(:, :, k);
        end
        imshow(frameSlice, []);
        colormap(ax, gray(256));
        title(sprintf('MR Sag S%02d', k), 'Color', 'w', 'FontSize', 7.5, 'FontWeight', 'bold');
        badgeCol = [0.99 0.88 0.28];
    elseif k <= 23
        if k == 22
            imshow(imgCT, []);
            title('CT Bone Window', 'Color', [0.22 0.74 0.97], 'FontSize', 7.5, 'FontWeight', 'bold');
        else
            imshow(imadjust(imgCT, [0.05 0.7], [0 1]), []);
            title('CT Soft Window', 'Color', [0.22 0.74 0.97], 'FontSize', 7.5, 'FontWeight', 'bold');
        end
        colormap(ax, bone(256));
        badgeCol = [0.22 0.74 0.97];
    else
        imshow(imgPET, []);
        if k == 24
            colormap(ax, hot(256));
            title('PET 18F-FDG (Hot)', 'Color', [0.96 0.25 0.37], 'FontSize', 7.5, 'FontWeight', 'bold');
        else
            colormap(ax, turbo(256));
            title('PET Turbo Map', 'Color', [0.96 0.25 0.37], 'FontSize', 7.5, 'FontWeight', 'bold');
        end
        badgeCol = [0.96 0.25 0.37];
    end
    text(15, 35, sprintf('[%02d/25]', k), 'Color', badgeCol, 'FontSize', 6, 'FontWeight', 'bold', 'BackgroundColor', [0.06 0.09 0.16]);
end

sgtitle('PACS 5x5 Multi-Modal Series Review (MATLAB)', 'Color', [0.22 0.74 0.97], 'FontSize', 13, 'FontWeight', 'bold');

outPath = fullfile(outDir, 'example_04_pacs_5x5_review_matlab.png');
saveas(fig, outPath);
close(fig);
fprintf('[SAVED] 5x5 PACS Montage saved to: %s\n', outPath);
end
