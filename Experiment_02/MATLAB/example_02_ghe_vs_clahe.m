%% Experiment 02 - Example 2: Global Equalization vs CLAHE Benchmarking (MATLAB)
% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
% Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

function example_02_ghe_vs_clahe()
    fprintf('======================================================================\n');
    fprintf('EXAMPLE 2: GLOBAL HE VS CLAHE BENCHMARKING (MATLAB)\n');
    fprintf('======================================================================\n');

    baseDir = fileparts(fileparts(mfilename('fullpath')));
    imgPath = fullfile(baseDir, 'Inputs', 'images', 'Lung-HR-contrast.png');
    if ~exist(imgPath, 'file')
        imgPath = fullfile(fileparts(baseDir), 'images', 'Lung-HR-contrast.png');
    end

    img = imread(imgPath);
    if size(img, 3) == 3, img = rgb2gray(img); end

    % 1. Global Histogram Equalization
    gheImg = histeq(img);

    % 2. CLAHE
    clahe20 = adapthisteq(img, 'ClipLimit', 0.02, 'NumTiles', [8 8]);
    clahe40 = adapthisteq(img, 'ClipLimit', 0.04, 'NumTiles', [8 8]);

    methods = { ...
        'Original Scan', img; ...
        'Global HE (GHE)', gheImg; ...
        'CLAHE (Clip=0.02)', clahe20; ...
        'CLAHE (Clip=0.04)', clahe40 ...
    };

    fprintf('%-22s | %-14s | %-10s\n', 'Method', 'Entropy (bits)', 'Std Dev');
    fprintf('--------------------------------------------------\n');
    for i = 1:size(methods, 1)
        im = methods{i, 2};
        [counts, ~] = imhist(im);
        p = counts / numel(im);
        p_nz = p(p > 0);
        ent = -sum(p_nz .* log2(p_nz));
        fprintf('%-22s | %-14.4f | %-10.2f\n', methods{i, 1}, ent, std(double(im(:))));
    end

    outDir = fullfile(baseDir, 'Outputs', 'MATLAB');
    figDir = fullfile(baseDir, 'Figures');
    if ~exist(outDir, 'dir'), mkdir(outDir); end
    if ~exist(figDir, 'dir'), mkdir(figDir); end

    fig = figure('Color', [0.06 0.09 0.16], 'Position', [100, 100, 1400, 700], 'Visible', 'off');

    for i = 1:4
        im = methods{i, 2};
        name = methods{i, 1};
        [counts, ~] = imhist(im);
        p = counts / numel(im); p_nz = p(p > 0);
        ent = -sum(p_nz .* log2(p_nz));
        s = std(double(im(:)));

        subplot(2, 4, i);
        imshow(im, []);
        title(sprintf('%s\nH=%.2f | Std=%.1f', name, ent, s), 'Color', 'w', 'FontWeight', 'bold');

        subplot(2, 4, i + 4);
        bar(0:255, counts, 'FaceColor', [0.22 0.74 0.97], 'EdgeColor', 'none');
        set(gca, 'Color', [0.12 0.16 0.23], 'XColor', [0.58 0.64 0.72], 'YColor', [0.58 0.64 0.72]);
        title(sprintf('Histogram (%s)', name), 'Color', 'w', 'FontSize', 9);
        xlim([0 255]);
    end

    sgtitle('Example 2: Global HE vs Contextual CLAHE Contrast Benchmarking (MATLAB)', 'Color', [0.22 0.74 0.97], 'FontWeight', 'bold');

    saveas(fig, fullfile(outDir, 'example_02_ghe_vs_clahe_matlab.png'));
    saveas(fig, fullfile(figDir, 'example_02_ghe_vs_clahe_matlab.png'));
    close(fig);
    fprintf('[SAVED] Saved MATLAB Example 2 figure.\n');
end
