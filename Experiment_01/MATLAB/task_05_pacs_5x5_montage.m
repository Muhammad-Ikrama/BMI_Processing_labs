function task_05_pacs_5x5_montage()
% Experiment 01 - Task 5: 5x5 (25-Panel) Volumetric & Multi-Modal Series Review Montage
% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
% Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

baseDir = fileparts(fileparts(mfilename('fullpath')));
mriPath = fullfile(baseDir, 'DICOM', 'IMG-0004-00001.dcm');
ctPath = fullfile(baseDir, 'images', 'CT.jpg');
petPath = fullfile(baseDir, 'images', 'PET.jpg');
outDir = fullfile(baseDir, 'outputs');
if ~exist(outDir, 'dir'), mkdir(outDir); end

fprintf('======================================================================\n');
fprintf('STUDENT LAB TASK 5: 5x5 (25-PANEL) CLINICAL PACS WORKSTATION MONTAGE\n');
fprintf('======================================================================\n');

mriInfo = dicominfo(mriPath);
rawMRI = dicomread(mriInfo);

imgCT = imread(ctPath);
if size(imgCT, 3) == 3, imgCT = rgb2gray(imgCT); end
imgCT = imresize(imgCT, [512, 512]);

imgPET = imread(petPath);
if size(imgPET, 3) == 3, imgPET = rgb2gray(imgPET); end
imgPET = imresize(imgPET, [512, 512]);

fig = figure('Color', [0.04 0.07 0.13], 'Position', [50, 50, 1150, 1000], 'Visible', 'off');

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
        title(sprintf('MR Sag S%02d', k), 'Color', 'w', 'FontSize', 8, 'FontWeight', 'bold');
        badgeCol = [0.99 0.88 0.28];
        tagStr = 'MRI T1 TSE';
    elseif k <= 23
        if k == 22
            imshow(imgCT, []);
            title('CT Bone Window', 'Color', [0.22 0.74 0.97], 'FontSize', 8, 'FontWeight', 'bold');
            tagStr = 'CT Bone Window';
        else
            imshow(imadjust(imgCT, [0.05 0.75], [0 1]), []);
            title('CT Soft Window', 'Color', [0.22 0.74 0.97], 'FontSize', 8, 'FontWeight', 'bold');
            tagStr = 'CT Soft Tissue';
        end
        colormap(ax, bone(256));
        badgeCol = [0.22 0.74 0.97];
    else
        imshow(imgPET, []);
        if k == 24
            colormap(ax, hot(256));
            title('PET 18F-FET (Hot)', 'Color', [0.96 0.25 0.37], 'FontSize', 8, 'FontWeight', 'bold');
            tagStr = 'PET Metabolic';
        else
            colormap(ax, turbo(256));
            title('PET 18F-FET (Turbo)', 'Color', [0.96 0.25 0.37], 'FontSize', 8, 'FontWeight', 'bold');
            tagStr = 'PET Turbo Map';
        end
        badgeCol = [0.96 0.25 0.37];
    end
    
    text(15, 38, sprintf('[%02d/25]', k), 'Color', badgeCol, 'FontSize', 6.5, 'FontWeight', 'bold', 'BackgroundColor', [0.06 0.09 0.16]);
    text(15, 485, tagStr, 'Color', [0.58 0.64 0.72], 'FontSize', 5.5, 'BackgroundColor', [0.06 0.09 0.16]);
end

sgtitle('Task 5: PACS Diagnostic Workstation 5x5 Multi-Modal Series Review (MATLAB)', 'Color', [0.22 0.74 0.97], 'FontSize', 12.5, 'FontWeight', 'bold');

outPath = fullfile(outDir, 'task_05_pacs_5x5_montage_matlab.png');
saveas(fig, outPath);
close(fig);
fprintf('\n[SAVED] Task 5 5x5 Montage saved to: %s\n', outPath);
end
