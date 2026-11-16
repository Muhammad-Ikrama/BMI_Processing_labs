%% Experiment 02 - Task 2.4: Contextual CLAHE Optimization & Sensitivity (MATLAB)
% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
% Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

function task_2_4_clahe_clip_sensitivity()
    fprintf('======================================================================\n');
    fprintf('TASK 2.4: CLAHE CLIP LIMIT SENSITIVITY SWEEP (MATLAB)\n');
    fprintf('======================================================================\n');

    baseDir = fileparts(fileparts(mfilename('fullpath')));
    imgPath = fullfile(baseDir, 'Inputs', 'images', 'Lung-HR-contrast.png');
    if ~exist(imgPath, 'file')
        imgPath = fullfile(fileparts(baseDir), 'images', 'Lung-HR-contrast.png');
    end

    img = imread(imgPath);
    if size(img, 3) == 3, img = rgb2gray(img); end

    clipValues = [0.01, 0.02, 0.03, 0.04, 0.08]; % In MATLAB, normalized clip limits
    entropies = zeros(1, 5);
    stds = zeros(1, 5);

    fprintf('%-12s | %-14s | %-10s\n', 'Clip Limit', 'Entropy (bits)', 'Std Dev');
    fprintf('-----------------------------------------\n');

    enhancedImages = cell(1, 5);
    for k = 1:5
        clahe = adapthisteq(img, 'ClipLimit', clipValues(k), 'NumTiles', [8 8]);
        enhancedImages{k} = clahe;
        [counts, ~] = imhist(clahe);
        p = counts / numel(clahe); p_nz = p(p > 0);
        ent = -sum(p_nz .* log2(p_nz));
        s = std(double(clahe(:)));
        entropies(k) = ent;
        stds(k) = s;
        fprintf('%-12.2f | %-14.4f | %-10.2f\n', clipValues(k), ent, s);
    end

    outDir = fullfile(baseDir, 'Outputs', 'MATLAB');
    figDir = fullfile(baseDir, 'Figures');
    if ~exist(outDir, 'dir'), mkdir(outDir); end
    if ~exist(figDir, 'dir'), mkdir(figDir); end

    fig = figure('Color', [0.06 0.09 0.16], 'Position', [100, 100, 1400, 800], 'Visible', 'off');

    for k = 1:5
        subplot(2, 5, k);
        imshow(enhancedImages{k}, []);
        title(sprintf('Clip = %.2f\nH = %.2f', clipValues(k), entropies(k)), 'Color', 'w', 'FontWeight', 'bold');
    end

    subplot(2, 5, 6:10);
    plot(clipValues, entropies, '-o', 'Color', [0.22 0.74 0.97], 'LineWidth', 2.5, 'MarkerSize', 8, 'MarkerFaceColor', [0.22 0.74 0.97]);
    hold on;
    xline(0.02, '--g', 'Optimal Point (Clip=0.02)', 'LineWidth', 2);
    set(gca, 'Color', [0.12 0.16 0.23], 'XColor', [0.58 0.64 0.72], 'YColor', [0.58 0.64 0.72]);
    title('Information Entropy vs Clip Limit Parameter (MATLAB)', 'Color', 'w', 'FontWeight', 'bold');
    xlabel('Clip Limit Parameter', 'Color', [0.58 0.64 0.72]);
    ylabel('Shannon Entropy (bits/pixel)', 'Color', [0.58 0.64 0.72]);
    grid on;

    sgtitle('Task 2.4: Contextual CLAHE Optimization & Sensitivity Sweep (MATLAB)', 'Color', [0.22 0.74 0.97], 'FontWeight', 'bold');

    saveas(fig, fullfile(outDir, 'task_2_4_clahe_clip_sensitivity_matlab.png'));
    saveas(fig, fullfile(figDir, 'task_2_4_clahe_clip_sensitivity_matlab.png'));
    close(fig);
    fprintf('[SAVED] Saved MATLAB Task 2.4 figure.\n');
end
