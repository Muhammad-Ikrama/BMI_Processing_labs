%% ==============================================================================
%% EXPERIMENT 09: TASK 9.3 - ORDER OF OPERATIONS BENCHMARK (MATLAB)
%% ==============================================================================
function df = task_9_3_order_of_operations()
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

    % High salt noise
    rng(209);
    noisyHigh = gtMorph;
    seSmall = strel('disk', 1, 0);
    saltHigh = imdilate((rand(512, 512) < 0.0075) & ~gtMorph, seSmall);
    pepperHigh = imdilate((rand(512, 512) < 0.0080) & gtMorph, seSmall);
    noisyHigh = (noisyHigh | saltHigh) & ~pepperHigh;

    % Pipeline A: Open first, then Close
    pipeA = imclose(imopen(noisyHigh, se5), se5);

    % Pipeline B: Close first, then Open
    pipeB = imopen(imclose(noisyHigh, se5), se5);

    pipelines = {
        'Noisy Input (High Salt)', noisyHigh, 'Input';
        'Pipeline A: Open-then-Close', pipeA, 'PipeA';
        'Pipeline B: Close-then-Open', pipeB, 'PipeB'
    };

    fprintf('==================================================================\n');
    fprintf('TASK 9.3: ORDER OF OPERATIONS BENCHMARK (MATLAB)\n');
    fprintf('==================================================================\n');
    fprintf('%-28s | %-10s | %-11s | %-8s | %-7s | %-8s\n', 'Pipeline Strategy', 'Dice (DSC)', 'Jaccard IoU', 'CC Count', 'Hole Px', 'Area Px');
    fprintf('----------------------------------------------------------------------------------\n');

    stratNames = {};
    tagList = {};
    dscList = [];
    iouList = [];
    ccList = [];
    holeList = [];
    areaList = [];

    for i = 1:size(pipelines, 1)
        name = pipelines{i, 1};
        m = logical(pipelines{i, 2});
        inter = sum(gtMorph(:) & m(:));
        denom = sum(gtMorph(:)) + sum(m(:));
        dsc = (2.0 * inter) / denom;
        union_px = sum(gtMorph(:) | m(:));
        iou = inter / union_px;
        cc = bwconncomp(m, 8).NumObjects;
        mFilled = imfill(m, 'holes');
        holes = sum(mFilled(:) & ~m(:));
        area = sum(m(:));

        fprintf('%-28s | %-10.4f | %-11.4f | %-8d | %-7d | %-8d\n', name, dsc, iou, cc, holes, area);

        stratNames{end+1} = name; %#ok<AGROW>
        tagList{end+1} = pipelines{i, 3}; %#ok<AGROW>
        dscList(end+1, 1) = round(dsc, 4); %#ok<AGROW>
        iouList(end+1, 1) = round(iou, 4); %#ok<AGROW>
        ccList(end+1, 1) = cc; %#ok<AGROW>
        holeList(end+1, 1) = holes; %#ok<AGROW>
        areaList(end+1, 1) = area; %#ok<AGROW>
    end

    df = table(stratNames', tagList', dscList, iouList, ccList, holeList, areaList, ...
        'VariableNames', {'Pipeline_Strategy', 'Tag', 'Dice_DSC', 'Jaccard_IoU', 'CC_Count', 'Hole_Pixels', 'Area_Pixels'});
    csvPath = fullfile(tabDir, 'exp09_task_9_3_order_of_ops_matlab.csv');
    writetable(df, csvPath);
    fprintf('\n[SAVED] Task 9.3 table: %s\n', csvPath);

    % Save Visual Figure with Background Salt Zoom
    f = figure('Visible', 'off', 'Position', [100, 100, 1300, 750]);
    rZ = 51:180; cZ = 51:180;

    subplot(2, 3, 1); imshow(noisyHigh); title('Input High Salt Mask', 'FontWeight', 'bold');
    subplot(2, 3, 2); imshow(pipeA); title(sprintf('Pipeline A: Open-Close\nDSC=%.4f (Optimal)', dscList(2)), 'FontWeight', 'bold', 'Color', [0, 0.6, 0]);
    subplot(2, 3, 3); imshow(pipeB); title(sprintf('Pipeline B: Close-Open\nDSC=%.4f (Fused Salt!)', dscList(3)), 'FontWeight', 'bold', 'Color', [0.8, 0, 0]);

    subplot(2, 3, 4); imshow(noisyHigh(rZ, cZ)); title('Background Salt Field (Crop)', 'FontWeight', 'bold');
    subplot(2, 3, 5); imshow(pipeA(rZ, cZ)); title('Pipeline A: Clean Air', 'FontWeight', 'bold', 'Color', [0, 0.6, 0]);
    subplot(2, 3, 6); imshow(pipeB(rZ, cZ)); title('Pipeline B: Fused Blobs!', 'FontWeight', 'bold', 'Color', [0.8, 0, 0]);

    figPath = fullfile(outDir, 'exp09_task_9_3_order_of_ops_m.png');
    saveas(f, figPath);
    close(f);
    fprintf('[SAVED] Task 9.3 figure: %s\n', figPath);
end
