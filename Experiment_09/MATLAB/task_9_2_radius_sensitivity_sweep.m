%% ==============================================================================
%% EXPERIMENT 09: TASK 9.2 - STRUCTURING ELEMENT RADIUS SWEEP (MATLAB)
%% ==============================================================================
function df = task_9_2_radius_sensitivity_sweep()
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

    se5 = strel('disk', 2, 0);
    gtMorph = imopen(imclose(mri > 175, se5), se5);
    gtArea = double(sum(gtMorph(:)));

    rng(109);
    noisyMask = gtMorph;
    seSmall = strel('disk', 1, 0);
    salt = imdilate((rand(512, 512) < 0.0035) & ~gtMorph, seSmall);
    pepper = imdilate((rand(512, 512) < 0.0080) & gtMorph, seSmall);
    noisyMask = (noisyMask | salt) & ~pepper;

    sizes = [3, 5, 9, 15];
    radii = [1, 2, 4, 7];

    fprintf('==================================================================\n');
    fprintf('TASK 9.2: STRUCTURING ELEMENT RADIUS SENSITIVITY SWEEP (MATLAB)\n');
    fprintf('==================================================================\n');
    fprintf('%-16s | %-10s | %-11s | %-8s | %-6s | %-12s\n', 'Disk Size', 'Dice (DSC)', 'Jaccard IoU', 'CC Count', 'Holes', 'Area Error %');
    fprintf('----------------------------------------------------------------------------------\n');

    sizeNames = {};
    rList = [];
    dscList = [];
    iouList = [];
    ccList = [];
    holeList = [];
    areaList = [];
    errList = [];
    refinedMasks = cell(4, 1);

    for i = 1:length(sizes)
        K = sizes(i);
        r = radii(i);
        se = strel('disk', r, 0);

        mRefined = imclose(imopen(noisyMask, se), se);
        refinedMasks{i} = mRefined;

        inter = sum(gtMorph(:) & mRefined(:));
        dsc = (2.0 * inter) / (sum(gtMorph(:)) + sum(mRefined(:)));
        if isempty(inter) || (sum(gtMorph(:)) + sum(mRefined(:))) == 0; dsc = 0; end
        iou = inter / max(sum(gtMorph(:) | mRefined(:)), 1);
        cc = bwconncomp(mRefined, 8).NumObjects;
        mFilled = imfill(mRefined, 'holes');
        holes = sum(mFilled(:) & ~mRefined(:));
        area = double(sum(mRefined(:)));
        areaErr = (abs(area - gtArea) / gtArea) * 100.0;

        fprintf('%-16s | %-10.4f | %-11.4f | %-8d | %-6d | %-10.2f%%\n', sprintf('%dx%d', K, K), dsc, iou, cc, holes, areaErr);

        sizeNames{end+1} = sprintf('%dx%d', K, K); %#ok<AGROW>
        rList(end+1, 1) = r; %#ok<AGROW>
        dscList(end+1, 1) = round(dsc, 4); %#ok<AGROW>
        iouList(end+1, 1) = round(iou, 4); %#ok<AGROW>
        ccList(end+1, 1) = cc; %#ok<AGROW>
        holeList(end+1, 1) = holes; %#ok<AGROW>
        areaList(end+1, 1) = int64(area); %#ok<AGROW>
        errList(end+1, 1) = round(areaErr, 2); %#ok<AGROW>
    end

    df = table(sizeNames', rList, dscList, iouList, ccList, holeList, areaList, errList, ...
        'VariableNames', {'Disk_Size_K', 'Radius_r', 'Dice_DSC', 'Jaccard_IoU', 'CC_Count', 'Hole_Pixels', 'Area_Pixels', 'Area_Error_Pct'});
    csvPath = fullfile(tabDir, 'exp09_task_9_2_radius_sweep_matlab.csv');
    writetable(df, csvPath);
    fprintf('\n[SAVED] Task 9.2 table: %s\n', csvPath);

    % Save Visual Figure
    f = figure('Visible', 'off', 'Position', [100, 100, 1300, 700]);
    rHorn = 211:310; cHorn = 191:290;
    notes = {
        '3x3: Under-filtered (CC high)';
        '5x5: Optimal Contours';
        '9x9: Horns Blunted';
        '15x15: Horns Amputated!'
    };

    for i = 1:4
        subplot(2, 4, i);
        imshow(refinedMasks{i});
        title(sprintf('%s Disk (DSC=%.4f)', sizeNames{i}, dscList(i)), 'FontWeight', 'bold');

        subplot(2, 4, i + 4);
        imshow(refinedMasks{i}(rHorn, cHorn));
        title(notes{i}, 'FontWeight', 'bold');
    end

    figPath = fullfile(outDir, 'exp09_task_9_2_radius_sweep_m.png');
    saveas(f, figPath);
    close(f);
    fprintf('[SAVED] Task 9.2 figure: %s\n', figPath);
end
