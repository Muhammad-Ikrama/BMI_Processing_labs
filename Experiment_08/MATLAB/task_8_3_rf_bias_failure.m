%% ==============================================================================
%% EXPERIMENT 08: TASK 8.3 - RF BIAS SHADING & FAILURE ANALYSIS (MATLAB)
%% ==============================================================================
function df = task_8_3_rf_bias_failure()
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

    % Clean Ground Truth
    mClean = imgaussfilt(double(mri), 6.0, 'FilterSize', 35);
    gtMask = (double(mri) > (mClean + 4)) & (mri > 25);

    [X, Y] = meshgrid(0:511, 0:511);
    rfGrad = 0.45 + 0.95 * ((X / 512.0) * 0.7 + (Y / 512.0) * 0.3);

    alphas = [0.0, 0.3, 0.6, 0.9];
    alphaList = [];
    otsuTList = [];
    otsuDscList = [];
    otsuIouList = [];
    adapDscList = [];
    adapIouList = [];

    f = figure('Visible', 'off', 'Position', [100, 100, 1400, 800]);

    fprintf('==================================================================\n');
    fprintf('TASK 8.3: MRI RF BIAS-FIELD SHADING FAILURE BENCHMARK (MATLAB)\n');
    fprintf('==================================================================\n');
    fprintf('%-15s | %-9s | %-10s | %-10s | %-10s | %-10s\n', 'Severity alpha', 'Otsu T*', 'Otsu DSC', 'Otsu IoU', 'Adap DSC', 'Adap IoU');
    fprintf('----------------------------------------------------------------------------------\n');

    for i = 1:length(alphas)
        alpha = alphas(i);
        field = (1.0 - alpha) + alpha .* rfGrad;
        mriShaded = uint8(min(max(double(mri) .* field, 0), 255));

        % Global Otsu
        lvlOtsu = graythresh(mriShaded);
        tOtsu = round(lvlOtsu * 255);
        maskOtsu = imbinarize(mriShaded, lvlOtsu);

        % Adaptive Gaussian
        T_gauss = adaptthresh(mriShaded, 0.42, 'NeighborhoodSize', [35 35], 'Statistic', 'gaussian');
        maskAdap = imbinarize(mriShaded, T_gauss);

        % Metrics
        interOtsu = sum(gtMask(:) & maskOtsu(:));
        dscOtsu = (2.0 * interOtsu) / (sum(gtMask(:)) + sum(maskOtsu(:)));
        iouOtsu = interOtsu / sum(gtMask(:) | maskOtsu(:));

        interAdap = sum(gtMask(:) & maskAdap(:));
        dscAdap = (2.0 * interAdap) / (sum(gtMask(:)) + sum(maskAdap(:)));
        iouAdap = interAdap / sum(gtMask(:) | maskAdap(:));

        fprintf('%-15.1f | %-9d | %-10.4f | %-10.4f | %-10.4f | %-10.4f\n', alpha, tOtsu, dscOtsu, iouOtsu, dscAdap, iouAdap);

        alphaList(end+1, 1) = alpha; %#ok<AGROW>
        otsuTList(end+1, 1) = tOtsu; %#ok<AGROW>
        otsuDscList(end+1, 1) = round(dscOtsu, 4); %#ok<AGROW>
        otsuIouList(end+1, 1) = round(iouOtsu, 4); %#ok<AGROW>
        adapDscList(end+1, 1) = round(dscAdap, 4); %#ok<AGROW>
        adapIouList(end+1, 1) = round(iouAdap, 4); %#ok<AGROW>

        % Plotting
        subplot(3, 4, i); imshow(mriShaded);
        title(sprintf('Shaded MRI (\\alpha=%.1f)', alpha), 'FontWeight', 'bold');

        subplot(3, 4, i + 4); imshow(maskOtsu);
        title(sprintf('Otsu Mask (T*=%d)\nDSC=%.4f', tOtsu, dscOtsu), 'FontWeight', 'bold');
    end

    % Row 3: Adaptive result at alpha=0.9 and DSC degradation curve
    subplot(3, 4, 9); imshow(maskAdap);
    title(sprintf('Adaptive Gauss (\\alpha=0.9)\nDSC=%.4f', adapDscList(end)), 'FontWeight', 'bold');

    subplot(3, 4, [10, 12]);
    plot(alphas, otsuDscList, '-or', 'LineWidth', 2.0, 'MarkerSize', 6, 'DisplayName', 'Global Otsu (Catastrophic Loss)');
    hold on;
    plot(alphas, adapDscList, '-sg', 'LineWidth', 2.0, 'MarkerSize', 6, 'DisplayName', 'Adaptive Gauss (Robust)');
    yline(0.85, '--b', 'Target Good-to-Go (DSC >= 0.85)', 'LineWidth', 1.5);
    xlabel('RF Shading Severity \alpha', 'FontWeight', 'bold');
    ylabel('Dice Similarity Coefficient (DSC)', 'FontWeight', 'bold');
    title('DSC Degradation vs. RF Shading Severity', 'FontWeight', 'bold');
    legend('Location', 'southwest'); grid on;

    df = table(alphaList, otsuTList, otsuDscList, otsuIouList, adapDscList, adapIouList, ...
        'VariableNames', {'Shading_Severity_Alpha', 'Otsu_T_star', 'Otsu_DSC', 'Otsu_IoU', 'Adap_DSC', 'Adap_IoU'});
    csvPath = fullfile(tabDir, 'exp08_task_8_3_rf_bias_metrics_matlab.csv');
    writetable(df, csvPath);
    fprintf('\n[SAVED] Task 8.3 table: %s\n', csvPath);

    figPath = fullfile(outDir, 'exp08_task_8_3_rf_bias_failure_m.png');
    saveas(f, figPath);
    close(f);
    fprintf('[SAVED] Task 8.3 figure: %s\n', figPath);
end
