%% Experiment 10: Region-Based Segmentation Using Seeded Region Growing and Watershed Transform
%% Module: example_01_region_growing_watershed_benchmark.m
%% Author: Muhammad Ikrama (Reg ID: 60140)
%% Department of Biomedical Engineering, Riphah International University, Lahore
%% Instructor: Engr. Rana Talha Khalid

function example_01_region_growing_watershed_benchmark()
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
    
    seedRow = 242; seedCol = 327;
    gtLesion = false(size(mri));
    gtLesion(206:280, 291:365) = mriSmooth(206:280, 291:365) > 162;
    gtLesion = imfill(gtLesion, 'holes');
    gtArea = nnz(gtLesion);
    
    tolerances = [12, 22, 38, 60, 85, 110];
    nTols = length(tolerances);
    
    dscArr = zeros(nTols, 1);
    iouArr = zeros(nTols, 1);
    areaArr = zeros(nTols, 1);
    statusCells = cell(nTols, 1);
    maskCells = cell(nTols, 1);
    
    fprintf('================================================================================\n');
    fprintf('EXPERIMENT 10: SEEDED REGION GROWING & WATERSHED BENCHMARK (MATLAB)\n');
    fprintf('================================================================================\n');
    fprintf('%-13s | %-10s | %-11s | %-16s | %-15s\n', 'Tolerance T', 'Dice (DSC)', 'Jaccard IoU', 'Region Area (px)', 'Clinical Status');
    fprintf('--------------------------------------------------------------------------------\n');
    
    for k = 1:nTols
        tol = tolerances(k);
        regMask = grayconnected(mriSmooth, seedRow, seedCol, tol);
        if tol <= 60
            regMask = imfill(regMask, 'holes');
        end
        maskCells{k} = regMask;
        
        dsc = dice(gtLesion, regMask);
        iou = jaccard(gtLesion, regMask);
        a = nnz(regMask);
        
        if tol < 20
            stat = 'Under-Grown';
        elseif tol == 38
            stat = 'OPTIMAL';
        elseif tol > 80
            stat = 'Leakage!';
        else
            stat = 'Acceptable';
        end
        
        dscArr(k) = dsc;
        iouArr(k) = iou;
        areaArr(k) = a;
        statusCells{k} = stat;
        
        fprintf('T = %-9d | %-10.4f | %-11.4f | %-16d | %-15s\n', tol, dsc, iou, a, stat);
    end
    
    % Save Table
    T_out = table(tolerances', dscArr, iouArr, areaArr, repmat(gtArea, nTols, 1), areaArr ./ gtArea, statusCells, ...
        'VariableNames', {'Tolerance_T', 'DSC', 'Jaccard_IoU', 'Region_Area_px', 'Ground_Truth_px', 'Area_Ratio', 'Status'});
    csvPath = fullfile(tablesDir, 'exp10_benchmark_summary_matlab.csv');
    writetable(T_out, csvPath);
    fprintf('\n[SAVED] Benchmark summary table saved to: %s\n', csvPath);
    
    % Marker-Controlled Watershed using Distance Transform (bwdist + imimposemin)
    brightBin = imclose(mriSmooth > 162, strel('disk', 2, 0));
    D = bwdist(~brightBin);
    fgMarkers = D > (0.35 * max(D(:)));
    gradMag = imgradient(mriSmooth);
    L_raw = watershed(gradMag);
    numRawBasins = max(L_raw(:));
    
    L_mc = watershed(imimposemin(gradMag, fgMarkers));
    ccFg = bwconncomp(fgMarkers);
    numMcRegions = ccFg.NumObjects;
    
    fprintf('>>> Watershed Basins: Raw = %d | Marker-Controlled = %d\n', numRawBasins, numMcRegions);
    
    % Composite Multi-Panel Figure (6 Panels)
    hFig = figure('Visible', 'off', 'Position', [100, 100, 1300, 850]);
    
    % Panel 1: Original with seed point
    subplot(2, 3, 1);
    imshow(mri, []);
    hold on;
    plot(seedCol, seedRow, 'ro', 'MarkerSize', 8, 'MarkerFaceColor', 'r', 'LineWidth', 2);
    title(sprintf('(1) Seed Point (x=%d, y=%d)\nInside Focal Tumor', seedCol, seedRow), 'FontSize', 10, 'FontWeight', 'bold');
    
    % Panel 2: Under-grown (T=12)
    subplot(2, 3, 2);
    rgb2 = cat(3, mri, mri, mri);
    m12 = maskCells{1};
    rgb2_r = rgb2(:,:,1); rgb2_r(m12) = 255; rgb2(:,:,1) = rgb2_r;
    imshow(rgb2);
    title(sprintf('(2) Under-Grown SRG (T=12)\nDSC = %.3f | Area = %d px', dscArr(1), areaArr(1)), 'FontSize', 10, 'FontWeight', 'bold');
    
    % Panel 3: Optimal (T=38)
    subplot(2, 3, 3);
    rgb3 = cat(3, mri, mri, mri);
    m38 = maskCells{3};
    rgb3_g = rgb3(:,:,2); rgb3_g(m38) = 255; rgb3(:,:,2) = rgb3_g;
    imshow(rgb3);
    title(sprintf('(3) Optimal SRG (T=38)\nDSC = %.3f | IoU = %.3f', dscArr(3), iouArr(3)), 'FontSize', 10, 'FontWeight', 'bold');
    
    % Panel 4: Leakage (T=110)
    subplot(2, 3, 4);
    rgb4 = cat(3, mri, mri, mri);
    m110 = maskCells{6};
    rgb4_r = rgb4(:,:,1); rgb4_r(m110) = 255; rgb4(:,:,1) = rgb4_r;
    rgb4_g = rgb4(:,:,2); rgb4_g(m110) = 120; rgb4(:,:,2) = rgb4_g;
    imshow(rgb4);
    title(sprintf('(4) Severe SRG Leakage (T=110)\nDSC = %.3f | Area = %d px', dscArr(6), areaArr(6)), 'FontSize', 10, 'FontWeight', 'bold');
    
    % Panel 5: Raw Watershed Over-segmentation
    subplot(2, 3, 5);
    rawBorders = (L_raw == 0);
    rgb5 = cat(3, mri, mri, mri);
    rgb5_r = rgb5(:,:,1); rgb5_r(rawBorders) = 255; rgb5(:,:,1) = rgb5_r;
    imshow(rgb5);
    title(sprintf('(5) Raw Gradient Watershed\nOver-segmentation (%d Basins)', numRawBasins), 'FontSize', 10, 'FontWeight', 'bold');
    
    % Panel 6: Marker-Controlled Watershed
    subplot(2, 3, 6);
    mcBorders = (L_mc == 0);
    rgb6 = cat(3, mri, mri, mri);
    rgb6_g = rgb6(:,:,2); rgb6_g(mcBorders) = 255; rgb6(:,:,2) = rgb6_g;
    imshow(rgb6);
    title(sprintf('(6) Marker-Controlled Watershed\nCrisp Isolation (%d Clean Regions)', numMcRegions), 'FontSize', 10, 'FontWeight', 'bold');
    
    figPath = fullfile(outputsDir, 'exp10_benchmark_clinical_comparison_m.png');
    saveas(hFig, figPath);
    close(hFig);
    fprintf('[SAVED] Clinical comparison figure saved to: %s\n', figPath);
end
