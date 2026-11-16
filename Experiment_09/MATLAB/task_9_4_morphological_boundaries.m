%% ==============================================================================
%% EXPERIMENT 09: TASK 9.4 - MORPHOLOGICAL BOUNDARY EXTRACTION (MATLAB)
%% ==============================================================================
function df = task_9_4_morphological_boundaries()
    baseDir = fileparts(fileparts(mfilename('fullpath')));
    imgPath = fullfile(baseDir, 'Inputs', 'images', 'Brain_MRI.png');
    outDir = fullfile(baseDir, 'Outputs', 'MATLAB');
    tabDir = fullfile(baseDir, 'Tables');
    if ~exist(outDir, 'dir'); mkdir(outDir); end
    if ~exist(tabDir, 'dir'); mkdir(tabDir); end

    mri = imread(imgPath);
    if size(mri, 3) == 3; mri = rgb2gray(mri); end
    if size(mri, 1) ~= 512 || size(mri, 2) ~= 512
        mri = imresize(mri, [512, 512]);
    end

    se3 = strel('disk', 1, 0);
    cleanTumor = imopen(imclose(mri > 175, se3), se3);

    % (a) Internal Boundary: A - (A (-) B)
    bInternal = cleanTumor & ~imerode(cleanTumor, se3);

    % (b) External Boundary: (A (+) B) - A
    bExternal = imdilate(cleanTumor, se3) & ~cleanTumor;

    % (c) Symmetrical Gradient: (A (+) B) - (A (-) B)
    bGradient = imdilate(cleanTumor, se3) & ~imerode(cleanTumor, se3);

    pInt = sum(bInternal(:));
    pExt = sum(bExternal(:));
    pGrad = sum(bGradient(:));

    fprintf('==================================================================\n');
    fprintf('TASK 9.4: MORPHOLOGICAL BOUNDARY EXTRACTION BENCHMARK (MATLAB)\n');
    fprintf('==================================================================\n');
    fprintf('%-34s | %-20s | %-24s\n', 'Boundary Formulation', 'Perimeter (Pixels)', 'Theoretical Thickness');
    fprintf('----------------------------------------------------------------------------------\n');
    fprintf('%-34s | %-20d | 1 Pixel Wide (Inside)\n', 'Internal Boundary: A - (A ⊖ B)', pInt);
    fprintf('%-34s | %-20d | 1 Pixel Wide (Outside)\n', 'External Boundary: (A ⊕ B) - A', pExt);
    fprintf('%-34s | %-20d | 2 Pixels Wide (Centered)\n', 'Symmetrical Gradient: (A ⊕ B) - (A ⊖ B)', pGrad);

    df = table({
        'Internal Boundary: A - (A ⊖ B)';
        'External Boundary: (A ⊕ B) - A';
        'Symmetrical Gradient: (A ⊕ B) - (A ⊖ B)'
    }, [pInt; pExt; pGrad], [1; 1; 2], {
        'Inside true boundary';
        'Outside true boundary';
        'Straddles true boundary'
    }, 'VariableNames', {'Formulation', 'Perimeter_Pixels', 'Thickness_Pixels', 'Location'});
    csvPath = fullfile(tabDir, 'exp09_task_9_4_boundary_metrics_matlab.csv');
    writetable(df, csvPath);
    fprintf('\n[SAVED] Task 9.4 table: %s\n', csvPath);

    % Color Overlay (RGB)
    rgbOverlay = cat(3, mri, mri, mri);
    rChan = rgbOverlay(:, :, 1);
    gChan = rgbOverlay(:, :, 2);
    bChan = rgbOverlay(:, :, 3);

    % Internal: Cyan [0, 240, 255]
    rChan(bInternal) = 0; gChan(bInternal) = 240; bChan(bInternal) = 255;
    % External: Coral/Magenta [255, 50, 150]
    rChan(bExternal) = 255; gChan(bExternal) = 50; bChan(bExternal) = 150;

    rgbOverlay = cat(3, rChan, gChan, bChan);

    f = figure('Visible', 'off', 'Position', [100, 100, 1200, 1100]);
    subplot(2, 2, 1); imshow(cleanTumor); title('Input Solid Tumor Mask A', 'FontWeight', 'bold');
    subplot(2, 2, 2); imshow(bGradient); title(sprintf('Symmetrical Gradient (Perim=%d px)', pGrad), 'FontWeight', 'bold');
    subplot(2, 2, 3); imshow(rgbOverlay); title('Internal (Cyan) vs External (Magenta) Overlay', 'FontWeight', 'bold');
    rZ = 151:350; cZ = 151:350;
    subplot(2, 2, 4); imshow(rgbOverlay(rZ, cZ, :)); title('High-Mag Anatomical Zoom (200x200 Crop)', 'FontWeight', 'bold');

    figPath = fullfile(outDir, 'exp09_task_9_4_boundary_extraction_m.png');
    saveas(f, figPath);
    close(f);
    fprintf('[SAVED] Task 9.4 figure: %s\n', figPath);
end
