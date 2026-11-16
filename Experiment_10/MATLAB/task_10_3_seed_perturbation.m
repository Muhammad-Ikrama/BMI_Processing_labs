%% Experiment 10: Task 10.3 - Seed Point Placement Perturbation & Robustness Test
%% Author: Muhammad Ikrama (Reg ID: 60140)
%% Department of Biomedical Engineering, Riphah International University, Lahore
%% Instructor: Engr. Rana Talha Khalid

function task_10_3_seed_perturbation()
    scriptDir = fileparts(mfilename('fullpath'));
    expDir = fullfile(scriptDir, '..');
    inputsDir = fullfile(expDir, 'Inputs', 'images');
    outputsDir = fullfile(expDir, 'Outputs', 'MATLAB');
    tablesDir = fullfile(expDir, 'Tables');
    if ~exist(outputsDir, 'dir'); mkdir(outputsDir); end
    if ~exist(tablesDir, 'dir'); mkdir(tablesDir); end
    
    mriPath = fullfile(inputsDir, 'Brain_MRI.png');
    mri = imread(mriPath);
    if size(mri, 3) == 3; mri = rgb2gray(mri); end
    mriSmooth = imgaussfilt(mri, 0.8, 'FilterSize', 3);
    tol = 38;
    
    gtLesion = false(size(mri));
    gtLesion(206:280, 291:365) = mriSmooth(206:280, 291:365) > 162;
    gtLesion = imfill(gtLesion, 'holes');
    gtArea = nnz(gtLesion);
    
    seedNames = {'Centroid'; 'Interior Point 1'; 'Interior Point 2'; 'Peripheral Rim 1'; 'Peripheral Rim 2'};
    seedTypes = {'Center Core'; 'Interior Paracentral'; 'Interior Paracentral'; 'Marginal Boundary Rim'; 'Marginal Boundary Rim'};
    seedCols = [327; 320; 332; 305; 345];
    seedRows = [242; 238; 248; 228; 255];
    nSeeds = length(seedCols);
    
    areas = zeros(nSeeds, 1);
    dscs = zeros(nSeeds, 1);
    ious = zeros(nSeeds, 1);
    seedInts = zeros(nSeeds, 1);
    statuses = cell(nSeeds, 1);
    masks = cell(nSeeds, 1);
    
    fprintf('\n===============================================================================================\n');
    fprintf('TASK 10.3: SEED POINT PLACEMENT PERTURBATION & ROBUSTNESS TEST (MATLAB)\n');
    fprintf('===============================================================================================\n');
    fprintf('%-18s | %-10s | %-8s | %-10s | %-8s | %-8s | %-20s\n', 'Seed Location', '(X, Y)', 'I_seed', 'Area (px)', 'DSC', 'IoU', 'Clinical Status');
    fprintf('-----------------------------------------------------------------------------------------------\n');
    
    for k = 1:nSeeds
        sr = seedRows(k); sc = seedCols(k);
        seedInts(k) = double(mriSmooth(sr, sc));
        m = grayconnected(mriSmooth, sr, sc, tol);
        m = imfill(m, 'holes');
        masks{k} = m;
        
        a = nnz(m);
        d = dice(gtLesion, m);
        i = jaccard(gtLesion, m);
        
        if d >= 0.95
            st = 'Optimal Capture';
        elseif d >= 0.85
            st = 'Robust Interior';
        else
            st = 'Rim Degradation / Under-grown';
        end
        
        areas(k) = a;
        dscs(k) = d;
        ious(k) = i;
        statuses{k} = st;
        
        fprintf('%-18s | (%3d, %3d) | %-8.1f | %-10d | %-8.4f | %-8.4f | %-20s\n', seedNames{k}, sc, sr, seedInts(k), a, d, i, st);
    end
    
    T_out = table(seedNames, seedTypes, seedCols, seedRows, seedInts, areas, repmat(gtArea, nSeeds, 1), ...
        areas ./ gtArea, dscs, ious, statuses, ...
        'VariableNames', {'Seed_Location', 'Seed_Type', 'Coord_X', 'Coord_Y', 'Seed_Intensity', 'Area_px', 'Ground_Truth_px', 'Area_Ratio', 'DSC', 'Jaccard_IoU', 'Status'});
    csvPath = fullfile(tablesDir, 'exp10_task_10_3_seed_perturbation_matlab.csv');
    writetable(T_out, csvPath);
    fprintf('[SAVED] Task 10.3 table saved to: %s\n', csvPath);
    
    % Figure: 3 subplots (Seed Map, Mask Comparison, Bar Chart)
    hFig = figure('Visible', 'off', 'Position', [100, 100, 1350, 480]);
    zy = 191:290; zx = 281:380;
    zoomMri = mri(zy, zx);
    
    % Subplot 1: Seed map
    subplot(1, 3, 1);
    rgbSeed = cat(3, zoomMri, zoomMri, zoomMri);
    imshow(rgbSeed);
    hold on;
    colors = [0, 1, 0; 0, 1, 1; 1, 1, 0; 1, 0.5, 0; 1, 0, 0];
    for k = 1:nSeeds
        plot(seedCols(k) - 280, seedRows(k) - 190, 'o', 'MarkerSize', 8, 'MarkerFaceColor', colors(k,:), 'LineWidth', 1.5);
        text(seedCols(k) - 280 + 3, seedRows(k) - 190 - 2, sprintf('S%d', k), 'Color', 'w', 'FontSize', 9, 'FontWeight', 'bold');
    end
    title('5 Tested Seed Coordinates\nInside & on Tumor Rim', 'FontSize', 9, 'FontWeight', 'bold');
    
    % Subplot 2: Centroid vs S4
    subplot(1, 3, 2);
    compRgb = zeros(length(zy), length(zx), 3, 'uint8');
    m1_z = masks{1}(zy, zx);
    m4_z = masks{4}(zy, zx);
    compRgb(:,:,2) = uint8(m1_z) * 255;
    compRgb(:,:,1) = uint8(m4_z) * 255;
    compRgb(:,:,2) = uint8(m4_z) * 120 + uint8(m1_z & ~m4_z) * 255;
    imshow(compRgb);
    title('Centroid (Green) vs. Rim Seed S4 (Orange)\nRim Seed misses bright core!', 'FontSize', 9, 'FontWeight', 'bold');
    
    % Subplot 3: Bar chart
    subplot(1, 3, 3);
    b = bar(dscs, 'FaceColor', [0.2, 0.6, 0.8]);
    hold on;
    yline(0.90, 'r--', 'Clinical Goal (DSC \ge 0.90)', 'LineWidth', 1.5);
    set(gca, 'XTick', 1:nSeeds, 'XTickLabel', {'S1: Centroid', 'S2: Int 1', 'S3: Int 2', 'S4: Rim 1', 'S5: Rim 2'});
    ylabel('Dice Similarity Coefficient (DSC)', 'FontSize', 9, 'FontWeight', 'bold');
    title('Segmentation Fidelity vs. Seed Location', 'FontSize', 9, 'FontWeight', 'bold');
    ylim([0, 1.05]);
    grid on;
    
    figPath = fullfile(outputsDir, 'exp10_task_10_3_seed_perturbation_m.png');
    saveas(hFig, figPath);
    close(hFig);
    fprintf('[SAVED] Task 10.3 figure saved to: %s\n', figPath);
end
