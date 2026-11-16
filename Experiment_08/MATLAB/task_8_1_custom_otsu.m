%% ==============================================================================
%% EXPERIMENT 08: TASK 8.1 - CUSTOM OTSU THRESHOLDING (MATLAB)
%% First-principles variance maximization, exact built-in validation, and Head CT bone segmentation
%% ==============================================================================
function df = task_8_1_custom_otsu()
    baseDir = fileparts(fileparts(mfilename('fullpath')));
    imgPath = fullfile(baseDir, 'Inputs', 'images', 'Head_CT.png');
    outDir = fullfile(baseDir, 'Outputs', 'MATLAB');
    tabDir = fullfile(baseDir, 'Tables');
    if ~exist(outDir, 'dir'); mkdir(outDir); end
    if ~exist(tabDir, 'dir'); mkdir(tabDir); end

    img = imread(imgPath);
    if size(img, 3) == 3; img = rgb2gray(img); end
    if size(img, 1) ~= 512 || size(img, 2) ~= 512
        img = imresize(img, [512, 512]);
    end

    % 1. Custom First-Principles 256-bin Histogram
    counts = imhist(img, 256);
    totalPixels = numel(img);
    p = counts / double(totalPixels);

    omega = cumsum(p);
    bins = (0:255)';
    mu = cumsum(p .* bins);
    muTotal = mu(end);

    denom = omega .* (1.0 - omega);
    valid = denom > 1e-12;
    sigmaB2 = zeros(256, 1);
    sigmaB2(valid) = ((muTotal .* omega(valid) - mu(valid)).^2) ./ denom(valid);

    [maxSigma, idxMax] = max(sigmaB2);
    T_custom = idxMax - 1; % 0-based intensity

    % 2. Built-in MATLAB graythresh
    [levelMatlab, metricEM] = graythresh(img);
    T_matlab = round(levelMatlab * 255);

    % Total Variance & Separability Metric
    sigmaTotal2 = sum(((bins - muTotal).^2) .* p);
    eta = maxSigma / sigmaTotal2;

    matchStatus = (T_custom == T_matlab);

    fprintf('==================================================================\n');
    fprintf('TASK 8.1: CUSTOM OTSU THRESHOLDING FROM FIRST PRINCIPLES (HEAD CT)\n');
    fprintf('==================================================================\n');
    fprintf('Custom First-Principles Threshold T* : %d\n', T_custom);
    fprintf('MATLAB Built-in graythresh Cutoff    : %d\n', T_matlab);
    fprintf('Exact Integer Match Verified         : %s\n', mat2str(matchStatus));
    fprintf('Between-Class Variance sigma_B^2(T*) : %.4f\n', maxSigma);
    fprintf('Total Histogram Variance sigma_Tot^2 : %.4f\n', sigmaTotal2);
    fprintf('Otsu Separability Metric eta         : %.4f (%.2f%%)\n', eta, eta*100);

    boneMask = img > T_custom;
    bonePixels = sum(boneMask(:));
    bonePct = (bonePixels / totalPixels) * 100.0;
    fprintf('Segmented Calvarial Bone Area        : %d px (%.2f%%)\n', bonePixels, bonePct);

    % Save CSV
    df = table({'Head CT'}, {sprintf('%dx%d', size(img, 1), size(img, 2))}, T_custom, T_matlab, matchStatus, ...
        round(maxSigma, 2), round(sigmaTotal2, 2), round(eta, 4), round(bonePct, 2), ...
        'VariableNames', {'Modality', 'Image_Size', 'Custom_T_star', 'MATLAB_T_star', 'Exact_Match', ...
        'Between_Class_Var', 'Total_Var', 'Separability_eta', 'Bone_Area_Pct'});
    csvPath = fullfile(tabDir, 'exp08_task_8_1_otsu_metrics_matlab.csv');
    writetable(df, csvPath);
    fprintf('\n[SAVED] Task 8.1 metrics table: %s\n', csvPath);

    % Generate Figure
    f = figure('Visible', 'off', 'Position', [100, 100, 1200, 400]);
    subplot(1, 3, 1);
    imshow(img);
    title('Input Head CT (512x512)', 'FontWeight', 'bold');

    subplot(1, 3, 2);
    bar(bins, counts / max(counts), 'FaceColor', [0.15, 0.39, 0.92], 'FaceAlpha', 0.55, 'EdgeColor', 'none');
    hold on;
    yyaxis right;
    plot(bins, sigmaB2, 'Color', [0.86, 0.15, 0.15], 'LineWidth', 2.0);
    xline(T_custom, '--', sprintf('T*=%d', T_custom), 'Color', [0.09, 0.64, 0.29], 'LineWidth', 1.8);
    xlabel('Intensity T'); ylabel('\sigma_B^2(T)');
    title('Overlaid Histogram & \sigma_B^2(T)', 'FontWeight', 'bold');
    grid on;

    subplot(1, 3, 3);
    imshow(boneMask);
    title(sprintf('Bone Mask (T*=%d, Area=%.1f%%)', T_custom, bonePct), 'FontWeight', 'bold');

    figPath = fullfile(outDir, 'exp08_task_8_1_custom_otsu_m.png');
    saveas(f, figPath);
    close(f);
    fprintf('[SAVED] Task 8.1 figure: %s\n', figPath);
end
