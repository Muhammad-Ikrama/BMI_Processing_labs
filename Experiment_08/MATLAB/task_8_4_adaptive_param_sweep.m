%% ==============================================================================
%% EXPERIMENT 08: TASK 8.4 - ADAPTIVE GAUSSIAN PARAMETER SWEEP (MATLAB)
%% ==============================================================================
function df = task_8_4_adaptive_param_sweep()
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

    [X, Y] = meshgrid(0:511, 0:511);
    biasField = 0.45 + 0.95 * ((X / 512.0) * 0.7 + (Y / 512.0) * 0.3);
    mriBiased = uint8(min(max(double(mri) .* biasField, 0), 255));

    mClean = imgaussfilt(double(mri), 6.0, 'FilterSize', 35);
    gtMask = (double(mri) > (mClean + 4)) & (mri > 25);

    WList = [7, 15, 35, 75];
    sensList = [0.20, 0.35, 0.42, 0.55]; % Sensitivity parameter in MATLAB adaptthresh

    wRec = [];
    sensRec = [];
    dscRec = [];
    iouRec = [];
    fgRec = [];

    masks = cell(4, 4);

    fprintf('==================================================================\n');
    fprintf('TASK 8.4: ADAPTIVE PARAMETER SWEEP (W x Sensitivity GRID) (MATLAB)\n');
    fprintf('==================================================================\n');
    fprintf('%-10s | %-12s | %-11s | %-12s | %-10s\n', 'Window W', 'Sensitivity', 'Dice (DSC)', 'Jaccard IoU', 'FG Area %');
    fprintf('----------------------------------------------------------------------------------\n');

    for i = 1:length(WList)
        W = WList(i);
        for j = 1:length(sensList)
            sens = sensList(j);
            T = adaptthresh(mriBiased, sens, 'NeighborhoodSize', [W, W], 'Statistic', 'gaussian');
            bw = imbinarize(mriBiased, T);
            masks{i, j} = bw;

            inter = sum(gtMask(:) & bw(:));
            dsc = (2.0 * inter) / (sum(gtMask(:)) + sum(bw(:)));
            iou = inter / sum(gtMask(:) | bw(:));
            fgPct = (sum(bw(:)) / numel(bw)) * 100.0;

            fprintf('%-10d | %-12.2f | %-11.4f | %-12.4f | %-8.2f%%\n', W, sens, dsc, iou, fgPct);

            wRec(end+1, 1) = W; %#ok<AGROW>
            sensRec(end+1, 1) = sens; %#ok<AGROW>
            dscRec(end+1, 1) = round(dsc, 4); %#ok<AGROW>
            iouRec(end+1, 1) = round(iou, 4); %#ok<AGROW>
            fgRec(end+1, 1) = round(fgPct, 2); %#ok<AGROW>
        end
    end

    df = table(wRec, sensRec, dscRec, iouRec, fgRec, ...
        'VariableNames', {'Window_W', 'Sensitivity', 'Dice_DSC', 'Jaccard_IoU', 'FG_Area_Pct'});
    csvPath = fullfile(tabDir, 'exp08_task_8_4_adaptive_sweep_matlab.csv');
    writetable(df, csvPath);
    fprintf('\n[SAVED] Task 8.4 table: %s\n', csvPath);

    % Save Grid Figure
    f = figure('Visible', 'off', 'Position', [100, 100, 1200, 1200]);
    for i = 1:4
        for j = 1:4
            idx = (i - 1) * 4 + j;
            subplot(4, 4, idx);
            imshow(masks{i, j});
            title(sprintf('W=%d, S=%.2f\nDSC=%.4f', WList(i), sensList(j), dscRec(idx)), 'FontSize', 8, 'FontWeight', 'bold');
        end
    end
    figPath = fullfile(outDir, 'exp08_task_8_4_adaptive_sweep_m.png');
    saveas(f, figPath);
    close(f);

    % Hollow Core Zoom
    fZ = figure('Visible', 'off', 'Position', [100, 100, 1200, 350]);
    r = 181:320; c = 181:320;
    subplot(1, 4, 1); imshow(mriBiased(r, c)); title('Input Biased ROI', 'FontWeight', 'bold');
    subplot(1, 4, 2); imshow(masks{1, 3}(r, c)); title('W=7x7: Hollow Core', 'FontWeight', 'bold');
    subplot(1, 4, 3); imshow(masks{3, 3}(r, c)); title('W=35x35: Solid Fill', 'FontWeight', 'bold');
    subplot(1, 4, 4); imshow(masks{4, 3}(r, c)); title('W=75x75: Over-Merged', 'FontWeight', 'bold');
    zoomPath = fullfile(outDir, 'exp08_task_8_4_hollow_core_zoom_m.png');
    saveas(fZ, zoomPath);
    close(fZ);
    fprintf('[SAVED] Task 8.4 zoom figure: %s\n', zoomPath);
end
