%% ==============================================================================
%% EXPERIMENT 09: TASK 9.5 - AUTOMATED CORTICAL SKULL STRIPPING (MATLAB)
%% ==============================================================================
function df = task_9_5_skull_stripping()
    baseDir = fileparts(fileparts(mfilename('fullpath')));
    imgPath = fullfile(baseDir, 'Inputs', 'images', 'Head_CT.png');
    outDir = fullfile(baseDir, 'Outputs', 'MATLAB');
    tabDir = fullfile(baseDir, 'Tables');
    if ~exist(outDir, 'dir'); mkdir(outDir); end
    if ~exist(tabDir, 'dir'); mkdir(tabDir); end

    ct = imread(imgPath);
    if size(ct, 3) == 3; ct = rgb2gray(ct); end
    if size(ct, 1) ~= 512 || size(ct, 2) ~= 512
        ct = imresize(ct, [512, 512]);
    end

    % 1. Global Otsu for whole head
    lvlOtsu = graythresh(ct);
    headMask = imbinarize(ct, lvlOtsu);

    % 2. High-density cortical bone ring
    boneMask = ct > 130;
    se5 = strel('disk', 2, 0);
    boneClean = imopen(boneMask, se5);

    % 3. Fill interior holes of skull ring to create full intracranial compartment
    skullFilled = imfill(boneClean, 'holes');

    % 4. Intracranial cavity = Skull Filled MINUS Bone
    intracranialRaw = skullFilled & ~boneClean;

    % 5. Morphological opening (7x7 disk) to snap dural bridges
    seBrain = strel('disk', 3, 0);
    brainOpened = imopen(intracranialRaw, seBrain);

    % 6. Retain largest connected component (intracranial parenchyma)
    cc = bwconncomp(brainOpened, 8);
    numPixels = cellfun(@numel, cc.PixelIdxList);
    [~, maxIdx] = max(numPixels);
    brainMask = false(size(brainOpened));
    if ~isempty(maxIdx)
        brainMask(cc.PixelIdxList{maxIdx}) = true;
    else
        brainMask = brainOpened;
    end

    % 7. Solidify internal ventricles
    brainSolid = imfill(brainMask, 'holes');

    % 8. Strip skull from original CT
    ctStripped = ct;
    ctStripped(~brainSolid) = 0;

    nTotal = double(numel(ct));
    headPx = sum(headMask(:));
    bonePx = sum(boneClean(:));
    brainPx = sum(brainSolid(:));

    headPct = (headPx / nTotal) * 100.0;
    bonePct = (bonePx / nTotal) * 100.0;
    brainPct = (brainPx / nTotal) * 100.0;
    brainToHead = (double(brainPx) / double(headPx)) * 100.0;

    fprintf('==================================================================\n');
    fprintf('TASK 9.5: AUTOMATED CORTICAL SKULL STRIPPING PIPELINE (MATLAB)\n');
    fprintf('==================================================================\n');
    fprintf('Total Scan Geometry                  : 512 x 512 (%d px)\n', int64(nTotal));
    fprintf('Total Head Volume Area               : %d px (%.2f%%)\n', headPx, headPct);
    fprintf('Calvarial Bone Volume Area           : %d px (%.2f%%)\n', bonePx, bonePct);
    fprintf('Extracted Brain Parenchymal Area     : %d px (%.2f%%)\n', brainPx, brainPct);
    fprintf('Brain-to-Head Parenchymal Ratio      : %.2f%%\n', brainToHead);

    df = table({'Head CT'}, {'512x512'}, int64(nTotal), headPx, bonePx, brainPx, ...
        round(brainPct, 2), round(brainToHead, 2), ...
        'VariableNames', {'Modality', 'Image_Size', 'Total_Pixels', 'Total_Head_Area_Px', ...
        'Bone_Ring_Area_Px', 'Extracted_Brain_Area_Px', 'Brain_Scan_Volume_Pct', 'Brain_to_Head_Ratio_Pct'});
    csvPath = fullfile(tabDir, 'exp09_task_9_5_skull_stripping_matlab.csv');
    writetable(df, csvPath);
    fprintf('\n[SAVED] Task 9.5 table: %s\n', csvPath);

    % Save Visual Figure
    f = figure('Visible', 'off', 'Position', [100, 100, 1300, 750]);
    subplot(2, 3, 1); imshow(ct); title('1. Input Head CT (512x512)', 'FontWeight', 'bold');
    subplot(2, 3, 2); imshow(boneClean); title(sprintf('2. Calvarial Bone Mask\nArea=%d px (%.1f%%)', bonePx, bonePct), 'FontWeight', 'bold');
    subplot(2, 3, 3); imshow(intracranialRaw); title('3. Intracranial Space (Bone Subtracted)', 'FontWeight', 'bold');
    subplot(2, 3, 4); imshow(brainOpened); title('4. Morphological Opening (7x7 Disk)', 'FontWeight', 'bold');
    subplot(2, 3, 5); imshow(brainSolid); title(sprintf('5. Final Brain Mask (Holes Filled)\nArea=%d px (%.1f%%)', brainPx, brainPct), 'FontWeight', 'bold');
    subplot(2, 3, 6); imshow(ctStripped); title('6. Skull-Stripped Intracranial CT', 'FontWeight', 'bold');

    figPath = fullfile(outDir, 'exp09_task_9_5_skull_stripping_m.png');
    saveas(f, figPath);
    close(f);
    fprintf('[SAVED] Task 9.5 figure: %s\n', figPath);
end
