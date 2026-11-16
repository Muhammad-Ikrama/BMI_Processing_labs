%% Experiment 10: Task 10.4 - Distance-Transform Threshold Sweep in Marker-Controlled Watershed
%% Author: Muhammad Ikrama (Reg ID: 60140)
%% Department of Biomedical Engineering, Riphah International University, Lahore
%% Instructor: Engr. Rana Talha Khalid

function task_10_4_distance_transform_sweep()
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
    
    brightBin = imclose(mriSmooth > 162, strel('disk', 2, 0));
    D = bwdist(~brightBin);
    dMax = max(D(:));
    gradMag = imgradient(mriSmooth);
    
    alphas = [0.15; 0.25; 0.35; 0.55; 0.75];
    nAlphas = length(alphas);
    cutoffs = alphas * dMax;
    fgMarkerCounts = zeros(nAlphas, 1);
    watershedRegions = zeros(nAlphas, 1);
    statuses = cell(nAlphas, 1);
    
    fprintf('\n===============================================================================================\n');
    fprintf('TASK 10.4: DISTANCE-TRANSFORM THRESHOLD SWEEP IN WATERSHED (MATLAB)\n');
    fprintf('===============================================================================================\n');
    fprintf('%-14s | %-18s | %-12s | %-20s | %-25s\n', 'Alpha Factor', 'Cutoff Dist (px)', 'FG Markers', 'Watershed Regions', 'Status');
    fprintf('-----------------------------------------------------------------------------------------------\n');
    
    hFig = figure('Visible', 'off', 'Position', [100, 100, 1350, 850]);
    
    for k = 1:nAlphas
        a = alphas(k);
        c = cutoffs(k);
        fg = D > c;
        cc = bwconncomp(fg);
        numMarkers = cc.NumObjects;
        fgMarkerCounts(k) = numMarkers;
        
        L = watershed(imimposemin(gradMag, fg));
        numRegions = max(L(:));
        watershedRegions(k) = numRegions;
        
        if a < 0.25
            st = 'Over-Segmented (Fragmented Basins)';
        elseif a == 0.35
            st = 'OPTIMAL (6 Clean Anatomical Structures)';
        elseif a <= 0.55
            st = 'Acceptable Separation';
        else
            st = 'Under-Segmented (Marker Shrinkage / Missing Basins)';
        end
        statuses{k} = st;
        fprintf('alpha = %-7.2f | %-18.2f | %-12d | %-20d | %-25s\n', a, c, numMarkers, numRegions, st);
        
        % Subplot for visual
        subplot(2, 3, k);
        rgb = cat(3, mri, mri, mri);
        b = (L == 0);
        rgb_g = rgb(:,:,2); rgb_g(b) = 255; rgb(:,:,2) = rgb_g;
        rgb_r = rgb(:,:,1); rgb_r(fg) = 255; rgb(:,:,1) = rgb_r;
        imshow(rgb);
        title(sprintf('\\alpha = %.2f (Cutoff: %.1f px)\nMarkers: %d | Basins: %d', a, c, numMarkers, numRegions), 'FontSize', 9, 'FontWeight', 'bold');
    end
    
    T_out = table(alphas, round(cutoffs, 2), repmat(round(dMax, 2), nAlphas, 1), fgMarkerCounts, watershedRegions, statuses, ...
        'VariableNames', {'Alpha_Factor', 'Cutoff_Distance_px', 'Max_Distance_px', 'FG_Marker_Count', 'Watershed_Regions', 'Clinical_Status'});
    csvPath = fullfile(tablesDir, 'exp10_task_10_4_distance_sweep_matlab.csv');
    writetable(T_out, csvPath);
    fprintf('[SAVED] Task 10.4 table saved to: %s\n', csvPath);
    
    % Subplot 6: Summary Curve
    subplot(2, 3, 6);
    plot(alphas, fgMarkerCounts, 'r-o', 'LineWidth', 2, 'DisplayName', 'FG Markers');
    hold on;
    plot(alphas, watershedRegions, 'b--s', 'LineWidth', 2, 'DisplayName', 'Watershed Basins');
    xline(0.35, 'g:', 'Optimal \alpha = 0.35', 'LineWidth', 2);
    xlabel('Distance Factor \alpha', 'FontSize', 9, 'FontWeight', 'bold');
    ylabel('Count', 'FontSize', 9, 'FontWeight', 'bold');
    title('Marker & Region Count vs. \alpha', 'FontSize', 9, 'FontWeight', 'bold');
    grid on;
    legend('Location', 'northeast');
    
    figPath = fullfile(outputsDir, 'exp10_task_10_4_distance_sweep_m.png');
    saveas(hFig, figPath);
    close(hFig);
    fprintf('[SAVED] Task 10.4 figure saved to: %s\n', figPath);
end
