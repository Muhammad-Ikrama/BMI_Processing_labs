%% ==============================================================================
%% EXPERIMENT 09: BENCHMARK TUTORIAL CODE (MATLAB)
%% Binary Morphological Operations (imerode, imdilate, imopen, imclose, imopenclose)
%% ==============================================================================
function df = example_01_morphology_benchmark()
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

    % 1. Clean Reference Mask (Ventricles + Tumor)
    seDisk = strel('disk', 2, 0); % 5x5 disk
    gtMorph = imopen(imclose(mri > 175, seDisk), seDisk);

    % 2. Simulate realistic segmentation noise (salt speckles + pepper holes)
    rng(109);
    noisyMask = gtMorph;
    seSmall = strel('disk', 1, 0); % 3x3 disk
    salt = imdilate((rand(512, 512) < 0.0035) & ~gtMorph, seSmall);
    pepper = imdilate((rand(512, 512) < 0.0080) & gtMorph, seSmall);
    noisyMask = (noisyMask | salt) & ~pepper;

    % 3. Execute Operations (5x5 Disk SE)
    mErode = imerode(noisyMask, seDisk);
    mDilate = imdilate(noisyMask, seDisk);
    mOpen = imopen(noisyMask, seDisk);
    mClose = imclose(noisyMask, seDisk);
    mOpenClose = imclose(mOpen, seDisk);

    ops = {
        'Corrupted Mask', noisyMask;
        'Erosion (5x5 Disk)', mErode;
        'Dilation (5x5 Disk)', mDilate;
        'Opening (5x5 Disk)', mOpen;
        'Closing (5x5 Disk)', mClose;
        'Open + Close (5x5)', mOpenClose
    };

    fprintf('==================================================================\n');
    fprintf('EXPERIMENT 09: MORPHOLOGICAL SHAPE REFINEMENT BENCHMARK (MATLAB)\n');
    fprintf('==================================================================\n');
    fprintf('%-24s | %-10s | %-11s | %-8s | %-7s | %-8s\n', 'Operation', 'Dice (DSC)', 'Jaccard IoU', 'CC Count', 'Hole Px', 'Area Px');
    fprintf('----------------------------------------------------------------------------------\n');

    opNames = {};
    dscList = [];
    iouList = [];
    ccList = [];
    holeList = [];
    areaList = [];

    for i = 1:size(ops, 1)
        name = ops{i, 1};
        m = logical(ops{i, 2});
        inter = sum(gtMorph(:) & m(:));
        denom = sum(gtMorph(:)) + sum(m(:));
        dsc = (2.0 * inter) / denom;
        union_px = sum(gtMorph(:) | m(:));
        iou = inter / union_px;
        cc = bwconncomp(m, 8).NumObjects;
        mFilled = imfill(m, 'holes');
        holes = sum(mFilled(:) & ~m(:));
        area = sum(m(:));

        fprintf('%-24s | %-10.4f | %-11.4f | %-8d | %-7d | %-8d\n', name, dsc, iou, cc, holes, area);

        opNames{end+1} = name; %#ok<AGROW>
        dscList(end+1, 1) = round(dsc, 4); %#ok<AGROW>
        iouList(end+1, 1) = round(iou, 4); %#ok<AGROW>
        ccList(end+1, 1) = cc; %#ok<AGROW>
        holeList(end+1, 1) = holes; %#ok<AGROW>
        areaList(end+1, 1) = area; %#ok<AGROW>
    end

    df = table(opNames', dscList, iouList, ccList, holeList, areaList, ...
        'VariableNames', {'Operation', 'Dice_DSC', 'Jaccard_IoU', 'CC_Count', 'Hole_Pixels', 'Area_Pixels'});
    csvPath = fullfile(tabDir, 'exp09_benchmark_summary_matlab.csv');
    writetable(df, csvPath);
    fprintf('\n[SAVED] MATLAB Benchmark table: %s\n', csvPath);

    % Save Visual Figure
    f = figure('Visible', 'off', 'Position', [100, 100, 1300, 750]);
    for i = 1:size(ops, 1)
        subplot(2, 3, i);
        imshow(ops{i, 2});
        title(sprintf('%s\nDSC=%.4f | CC=%d | Holes=%d', opNames{i}, dscList(i), ccList(i), holeList(i)), ...
            'FontWeight', 'bold');
    end
    figPath = fullfile(outDir, 'exp09_benchmark_clinical_comparison_m.png');
    saveas(f, figPath);
    close(f);
    fprintf('[SAVED] MATLAB Clinical comparison figure: %s\n', figPath);
end
