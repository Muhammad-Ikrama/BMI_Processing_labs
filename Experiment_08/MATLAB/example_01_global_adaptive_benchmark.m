%% ==============================================================================
%% EXPERIMENT 08: BENCHMARK TUTORIAL CODE (MATLAB)
%% Global (Fixed, Isodata, Otsu) & Adaptive (Mean-C, Gaussian-C) Thresholding
%% ==============================================================================
function df = example_01_global_adaptive_benchmark()
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

    % Simulate RF Coil Bias Field
    [X, Y] = meshgrid(0:511, 0:511);
    biasField = 0.45 + 0.95 * ((X / 512.0) * 0.7 + (Y / 512.0) * 0.3);
    mriBiased = uint8(min(max(double(mri) .* biasField, 0), 255));

    % Ground truth local anatomical structures from clean MRI
    mClean = imgaussfilt(double(mri), 6.0, 'FilterSize', 35);
    gtMask = (double(mri) > (mClean + 4)) & (mri > 25);

    % 1. Global Thresholds: Fixed (115), Isodata, and Otsu
    thFixed = mriBiased > 115;

    % Iterative Isodata
    TIso = mean(double(mriBiased(:)));
    for iter = 1:30
        bgMean = mean(double(mriBiased(mriBiased <= TIso)));
        fgMean = mean(double(mriBiased(mriBiased > TIso)));
        TNew = 0.5 * (bgMean + fgMean);
        if abs(TNew - TIso) < 0.05
            TIso = TNew;
            break;
        end
        TIso = TNew;
    end
    thIsodata = mriBiased > TIso;

    % Otsu Global (graythresh)
    [levelOtsu, metricEM] = graythresh(mriBiased);
    tOtsu = round(levelOtsu * 255);
    thOtsu = imbinarize(mriBiased, levelOtsu);

    % 2. Local Adaptive Thresholding (adaptthresh)
    T_mean = adaptthresh(mriBiased, 0.42, 'NeighborhoodSize', [35 35], 'Statistic', 'mean');
    thAdapMean = imbinarize(mriBiased, T_mean);

    T_gauss = adaptthresh(mriBiased, 0.42, 'NeighborhoodSize', [35 35], 'Statistic', 'gaussian');
    thAdapGauss = imbinarize(mriBiased, T_gauss);

    % 3. Quantitative Evaluation
    tests = {
        'Fixed Global (T=115)', thFixed, 115.0;
        sprintf('Isodata Global (T=%d)', round(TIso)), thIsodata, TIso;
        sprintf('Otsu Global (T*=%d)', tOtsu), thOtsu, double(tOtsu);
        'Adaptive Mean (35x35)', thAdapMean, 32.5;
        'Adaptive Gaussian (35x35)', thAdapGauss, 32.5
    };

    fprintf('==================================================================\n');
    fprintf('EXPERIMENT 08: GLOBAL & ADAPTIVE THRESHOLDING BENCHMARK (MATLAB)\n');
    fprintf('==================================================================\n');
    fprintf('%-28s | %-9s | %-10s | %-11s | %-9s\n', 'Method', 'Cutoff T', 'Dice (DSC)', 'Jaccard IoU', 'FG Area %');
    fprintf('----------------------------------------------------------------------------------\n');

    methodNames = {};
    cutoffList = [];
    diceList = [];
    iouList = [];
    fgAreaList = [];

    for i = 1:size(tests, 1)
        name = tests{i, 1};
        mask = logical(tests{i, 2});
        tval = tests{i, 3};

        inter = sum(gtMask(:) & mask(:));
        denom = sum(gtMask(:)) + sum(mask(:));
        dsc = (2.0 * inter) / denom;
        union_px = sum(gtMask(:) | mask(:));
        iou = inter / union_px;
        fg_pct = (sum(mask(:)) / numel(mask)) * 100.0;

        fprintf('%-28s | %-9.1f | %-10.4f | %-11.4f | %-8.2f%%\n', name, tval, dsc, iou, fg_pct);

        methodNames{end+1} = name; %#ok<AGROW>
        cutoffList(end+1, 1) = round(tval, 1); %#ok<AGROW>
        diceList(end+1, 1) = round(dsc, 4); %#ok<AGROW>
        iouList(end+1, 1) = round(iou, 4); %#ok<AGROW>
        fgAreaList(end+1, 1) = round(fg_pct, 2); %#ok<AGROW>
    end

    df = table(methodNames', cutoffList, diceList, iouList, fgAreaList, ...
        'VariableNames', {'Method', 'Cutoff_T', 'Dice_DSC', 'Jaccard_IoU', 'FG_Area_Pct'});
    csvPath = fullfile(tabDir, 'exp08_benchmark_summary_matlab.csv');
    writetable(df, csvPath);
    fprintf('\n[SAVED] MATLAB Benchmark table: %s\n', csvPath);

    % Save Visual Figure
    f = figure('Visible', 'off', 'Position', [100, 100, 1400, 700]);
    subplot(2, 4, 1); imshow(mri); title('1. Original Brain MRI', 'FontWeight', 'bold');
    subplot(2, 4, 2); imshow(mriBiased); title('2. Biased MRI (RF Shading)', 'FontWeight', 'bold');
    subplot(2, 4, 3); imshow(thFixed); title(sprintf('3. Fixed Global (T=115)\nDSC=%.4f', diceList(1)), 'FontWeight', 'bold');
    subplot(2, 4, 4); imshow(thOtsu); title(sprintf('4. Otsu Global (T*=%d)\nDSC=%.4f', tOtsu, diceList(3)), 'FontWeight', 'bold');
    subplot(2, 4, 5); imshow(thIsodata); title(sprintf('5. Isodata Global (T=%d)\nDSC=%.4f', round(TIso), diceList(2)), 'FontWeight', 'bold');
    subplot(2, 4, 6); imshow(thAdapMean); title(sprintf('6. Adaptive Mean (35x35)\nDSC=%.4f', diceList(4)), 'FontWeight', 'bold');
    subplot(2, 4, 7); imshow(thAdapGauss); title(sprintf('7. Adaptive Gauss (35x35)\nDSC=%.4f', diceList(5)), 'FontWeight', 'bold');
    subplot(2, 4, 8); imshow(gtMask); title('8. Ground Truth Mask', 'FontWeight', 'bold');

    figPath = fullfile(outDir, 'exp08_benchmark_clinical_comparison_m.png');
    saveas(f, figPath);
    close(f);
    fprintf('[SAVED] MATLAB Clinical comparison figure: %s\n', figPath);
end
