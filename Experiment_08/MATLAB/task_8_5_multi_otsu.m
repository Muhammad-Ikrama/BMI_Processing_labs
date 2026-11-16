%% ==============================================================================
%% EXPERIMENT 08: TASK 8.5 - MULTI-OTSU TISSUE CLASSIFICATION (MATLAB)
%% ==============================================================================
function df = task_8_5_multi_otsu()
    baseDir = fileparts(fileparts(mfilename('fullpath')));
    imgPath = fullfile(baseDir, 'Inputs', 'images', 'Brain_MRI.png');
    outDir = fullfile(baseDir, 'Outputs', 'MATLAB');
    tabDir = fullfile(baseDir, 'Tables');
    if ~exist(outDir, 'dir'); mkdir(outDir); end
    if ~exist(tabDir, 'dir'); mkdir(tabDir); end

    img = imread(imgPath);
    if size(img, 3) == 3; img = rgb2gray(img); end
    if size(img, 1) ~= 512 || size(img, 2) ~= 512
        img = imresize(img, [512, 512]);
    end

    % 1. Multi-Otsu with 2 thresholds (3 classes)
    thresh = multithresh(img, 2);
    t1 = double(thresh(1));
    t2 = double(thresh(2));

    % Quantize
    seg = imquantize(img, thresh); % values: 1, 2, 3
    nTotal = double(numel(img));
    c0Count = sum(seg(:) == 1);
    c1Count = sum(seg(:) == 2);
    c2Count = sum(seg(:) == 3);

    pct0 = (c0Count / nTotal) * 100.0;
    pct1 = (c1Count / nTotal) * 100.0;
    pct2 = (c2Count / nTotal) * 100.0;

    fprintf('==================================================================\n');
    fprintf('TASK 8.5: MULTI-OTSU (3-CLASS) TISSUE CLASSIFICATION (MATLAB)\n');
    fprintf('==================================================================\n');
    fprintf('Dual Otsu Thresholds (T1*, T2*)     : (%d, %d)\n', round(t1), round(t2));
    fprintf('Class 1 (Background Air, f <= %d)   : %d px (%.2f%%)\n', round(t1), c0Count, pct0);
    fprintf('Class 2 (Parenchyma, %d < f <= %d) : %d px (%.2f%%)\n', round(t1), round(t2), c1Count, pct1);
    fprintf('Class 3 (Ventricles/CSF, f > %d)   : %d px (%.2f%%)\n', round(t2), c2Count, pct2);

    df = table([0; 1; 2], ...
        {'Background Air'; 'Brain Parenchyma'; 'Ventricles & CSF'}, ...
        {sprintf('0 to %d', round(t1)); sprintf('%d to %d', round(t1)+1, round(t2)); sprintf('>%d', round(t2))}, ...
        [c0Count; c1Count; c2Count], ...
        [round(pct0, 2); round(pct1, 2); round(pct2, 2)], ...
        'VariableNames', {'Class_ID', 'Tissue_Name', 'Intensity_Range', 'Pixel_Count', 'Area_Pct'});
    csvPath = fullfile(tabDir, 'exp08_task_8_5_multi_otsu_matlab.csv');
    writetable(df, csvPath);
    fprintf('\n[SAVED] Task 8.5 table: %s\n', csvPath);

    % Color-Coded Map (RGB)
    rgbMap = zeros(512, 512, 3, 'uint8');
    % Class 1 -> Dark Navy [15, 23, 42]
    % Class 2 -> Royal Blue [37, 99, 235]
    % Class 3 -> Bright Gold [234, 179, 8]
    for c = 1:3
        channel = rgbMap(:, :, c);
        if c == 1
            channel(seg == 1) = 15; channel(seg == 2) = 37; channel(seg == 3) = 234;
        elseif c == 2
            channel(seg == 1) = 23; channel(seg == 2) = 99; channel(seg == 3) = 179;
        else
            channel(seg == 1) = 42; channel(seg == 2) = 235; channel(seg == 3) = 8;
        end
        rgbMap(:, :, c) = channel;
    end

    f = figure('Visible', 'off', 'Position', [100, 100, 1200, 400]);
    subplot(1, 3, 1); imshow(img); title('Input Brain MRI', 'FontWeight', 'bold');
    subplot(1, 3, 2);
    counts = imhist(img, 256);
    bins = (0:255)';
    bar(bins, counts, 'FaceColor', [0.3, 0.5, 0.8], 'EdgeColor', 'none');
    xline(t1, '--r', sprintf('T1*=%d', round(t1)), 'LineWidth', 1.8);
    xline(t2, '--g', sprintf('T2*=%d', round(t2)), 'LineWidth', 1.8);
    xlabel('Intensity'); ylabel('Pixel Count');
    title('Dual Otsu Cutoffs on Histogram', 'FontWeight', 'bold'); grid on;

    subplot(1, 3, 3); imshow(rgbMap);
    title(sprintf('3-Class Map (Air:%.1f%%, Brain:%.1f%%, CSF:%.1f%%)', pct0, pct1, pct2), 'FontWeight', 'bold');

    figPath = fullfile(outDir, 'exp08_task_8_5_multi_otsu_m.png');
    saveas(f, figPath);
    close(f);
    fprintf('[SAVED] Task 8.5 figure: %s\n', figPath);
end
