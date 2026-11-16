%% Experiment 02 - Task 2.3: Global Histogram Equalization & Saturation (MATLAB)
% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
% Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

function task_2_3_global_histogram_equalization()
    fprintf('======================================================================\n');
    fprintf('TASK 2.3: GLOBAL HISTOGRAM EQUALIZATION & SATURATION ARTIFACTS (MATLAB)\n');
    fprintf('======================================================================\n');

    baseDir = fileparts(fileparts(mfilename('fullpath')));
    imgPath = fullfile(baseDir, 'Inputs', 'images', 'Lung-HR-contrast.png');
    if ~exist(imgPath, 'file')
        imgPath = fullfile(fileparts(baseDir), 'images', 'Lung-HR-contrast.png');
    end

    img = imread(imgPath);
    if size(img, 3) == 3, img = rgb2gray(img); end
    [H, W] = size(img);
    totalPixels = H * W;

    % Manual discrete GHE formula: s_k = round((L-1) * CDF(r_k))
    [counts, ~] = imhist(img);
    pdf = counts / double(totalPixels);
    cdf = cumsum(pdf);
    T_map = uint8(round(255 * cdf));

    gheImg = T_map(double(img) + 1);

    % Saturation
    origSat = sum(img(:) == 0 | img(:) == 255);
    gheSat = sum(gheImg(:) == 0 | gheImg(:) == 255);

    fprintf('Original Saturated: %d (%.2f%%)\n', origSat, (origSat/totalPixels)*100);
    fprintf('GHE Saturated     : %d (%.2f%%)\n', gheSat, (gheSat/totalPixels)*100);

    outDir = fullfile(baseDir, 'Outputs', 'MATLAB');
    figDir = fullfile(baseDir, 'Figures');
    if ~exist(outDir, 'dir'), mkdir(outDir); end
    if ~exist(figDir, 'dir'), mkdir(figDir); end

    fig = figure('Color', [0.06 0.09 0.16], 'Position', [100, 100, 1200, 900], 'Visible', 'off');

    subplot(2, 2, 1);
    imshow(img, []);
    title('Original Low-Contrast Scan', 'Color', 'w', 'FontWeight', 'bold');

    subplot(2, 2, 2);
    imshow(gheImg, []);
    title('Global Histogram Equalized (GHE)', 'Color', [0.97 0.44 0.44], 'FontWeight', 'bold');

    subplot(2, 2, 3);
    bar(0:255, counts, 'FaceColor', [0.22 0.74 0.97], 'EdgeColor', 'none');
    set(gca, 'Color', [0.12 0.16 0.23], 'XColor', [0.58 0.64 0.72], 'YColor', [0.58 0.64 0.72]);
    title('Original Clumped Histogram', 'Color', 'w');
    xlim([0 255]);

    subplot(2, 2, 4);
    [gheCounts, ~] = imhist(gheImg);
    bar(0:255, gheCounts, 'FaceColor', [0.97 0.44 0.44], 'EdgeColor', 'none');
    set(gca, 'Color', [0.12 0.16 0.23], 'XColor', [0.58 0.64 0.72], 'YColor', [0.58 0.64 0.72]);
    title('GHE Histogram (Comb Gaps & Bone Saturation)', 'Color', [0.97 0.44 0.44]);
    xlim([0 255]);

    sgtitle('Task 2.3: Global Histogram Equalization & Saturation Artifacts (MATLAB)', 'Color', [0.22 0.74 0.97], 'FontWeight', 'bold');

    saveas(fig, fullfile(outDir, 'task_2_3_global_histogram_equalization_matlab.png'));
    saveas(fig, fullfile(figDir, 'task_2_3_global_histogram_equalization_matlab.png'));
    close(fig);
    fprintf('[SAVED] Saved MATLAB Task 2.3 figure.\n');
end
