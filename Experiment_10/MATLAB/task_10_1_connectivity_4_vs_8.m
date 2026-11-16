%% Experiment 10: Task 10.1 - 4-Connected vs. 8-Connected Neighborhood Region Growing
%% Author: Muhammad Ikrama (Reg ID: 60140)
%% Department of Biomedical Engineering, Riphah International University, Lahore
%% Instructor: Engr. Rana Talha Khalid

function task_10_1_connectivity_4_vs_8()
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
    
    seedRow = 242; seedCol = 327; tol = 38;
    gtLesion = false(size(mri));
    gtLesion(206:280, 291:365) = mriSmooth(206:280, 291:365) > 162;
    gtLesion = imfill(gtLesion, 'holes');
    
    % Timing 4-connected vs 8-connected
    tic;
    for k = 1:5
        mask4 = srgMatlab(mriSmooth, seedRow, seedCol, tol, 4);
    end
    t4 = (toc / 5) * 1000; % ms
    
    tic;
    for k = 1:5
        mask8 = srgMatlab(mriSmooth, seedRow, seedCol, tol, 8);
    end
    t8 = (toc / 5) * 1000; % ms
    
    mask4Filled = imfill(mask4, 'holes');
    mask8Filled = imfill(mask8, 'holes');
    
    area4 = nnz(mask4Filled);
    area8 = nnz(mask8Filled);
    dsc4 = dice(gtLesion, mask4Filled);
    dsc8 = dice(gtLesion, mask8Filled);
    iou4 = jaccard(gtLesion, mask4Filled);
    iou8 = jaccard(gtLesion, mask8Filled);
    
    b4 = bwboundaries(mask4Filled);
    perim4 = sum(cellfun(@length, b4));
    comp4 = (4 * pi * area4) / (perim4^2);
    
    b8 = bwboundaries(mask8Filled);
    perim8 = sum(cellfun(@length, b8));
    comp8 = (4 * pi * area8) / (perim8^2);
    
    fprintf('\n================================================================================\n');
    fprintf('TASK 10.1: 4-CONNECTED VS 8-CONNECTED SEEDED REGION GROWING (MATLAB)\n');
    fprintf('================================================================================\n');
    fprintf('%-15s | %-10s | %-8s | %-8s | %-15s | %-12s | %-10s\n', 'Connectivity', 'Area (px)', 'DSC', 'IoU', 'Perimeter (px)', 'Compactness', 'Time (ms)');
    fprintf('----------------------------------------------------------------------------------------\n');
    fprintf('%-15s | %-10d | %-8.4f | %-8.4f | %-15.1f | %-12.4f | %-10.2f\n', '4-Connected', area4, dsc4, iou4, perim4, comp4, t4);
    fprintf('%-15s | %-10d | %-8.4f | %-8.4f | %-15.1f | %-12.4f | %-10.2f\n', '8-Connected', area8, dsc8, iou8, perim8, comp8, t8);
    
    T_out = table({'4-Connected'; '8-Connected'}, [4; 8], [area4; area8], [dsc4; dsc8], [iou4; iou8], ...
        [perim4; perim8], [comp4; comp8], [t4; t8], {'Severe (Orthogonal Only)'; 'Smooth (Diagonal Infiltration)'}, ...
        'VariableNames', {'Neighborhood', 'Neighbors', 'Area_px', 'DSC', 'Jaccard_IoU', 'Perimeter_px', 'Compactness', 'Exec_Time_ms', 'Stair_Stepping'});
    csvPath = fullfile(tablesDir, 'exp10_task_10_1_connectivity_matlab.csv');
    writetable(T_out, csvPath);
    fprintf('[SAVED] Task 10.1 table saved to: %s\n', csvPath);
    
    % Zoom Multi-Panel Plot
    hFig = figure('Visible', 'off', 'Position', [100, 100, 1200, 420]);
    zy = 191:290; zx = 281:380;
    zoomMri = mri(zy, zx);
    
    % Panel 1: 4-connected
    subplot(1, 3, 1);
    rgb4 = cat(3, zoomMri, zoomMri, zoomMri);
    b4_zoom = bwperim(mask4Filled(zy, zx));
    rgb4_r = rgb4(:,:,1); rgb4_r(b4_zoom) = 255; rgb4(:,:,1) = rgb4_r;
    rgb4_g = rgb4(:,:,2); rgb4_g(b4_zoom) = 140; rgb4(:,:,2) = rgb4_g;
    imshow(rgb4);
    title(sprintf('(A) 4-Connected SRG (T=38)\nArea = %d px | DSC = %.4f\nNotice Orthogonal Stepping', area4, dsc4), 'FontSize', 9, 'FontWeight', 'bold');
    
    % Panel 2: 8-connected
    subplot(1, 3, 2);
    rgb8 = cat(3, zoomMri, zoomMri, zoomMri);
    b8_zoom = bwperim(mask8Filled(zy, zx));
    rgb8_g = rgb8(:,:,2); rgb8_g(b8_zoom) = 255; rgb8(:,:,2) = rgb8_g;
    imshow(rgb8);
    title(sprintf('(B) 8-Connected SRG (T=38)\nArea = %d px | DSC = %.4f\nOptimal Diagonal Capture', area8, dsc8), 'FontSize', 9, 'FontWeight', 'bold');
    
    % Panel 3: Difference Map
    subplot(1, 3, 3);
    diffRgb = zeros(length(zy), length(zx), 3, 'uint8');
    m8_z = mask8Filled(zy, zx);
    m4_z = mask4Filled(zy, zx);
    diffRgb(:,:,2) = uint8(m8_z) * 255;
    diffRgb(:,:,1) = uint8(m4_z) * 255;
    diffRgb(:,:,2) = uint8(m4_z) * 120 + uint8(m8_z & ~m4_z) * 255;
    imshow(diffRgb);
    title(sprintf('(C) Discrepancy Map\nGreen Rim = %d px missed\nDiagonal Infiltration Gap', area8 - area4), 'FontSize', 9, 'FontWeight', 'bold');
    
    figPath = fullfile(outputsDir, 'exp10_task_10_1_connectivity_m.png');
    saveas(hFig, figPath);
    close(hFig);
    fprintf('[SAVED] Task 10.1 figure saved to: %s\n', figPath);
end

function mask = srgMatlab(img, sy, sx, tol, conn)
    [h, w] = size(img);
    visited = false(h, w);
    mask = false(h, w);
    
    stackR = zeros(h*w, 1);
    stackC = zeros(h*w, 1);
    top = 1;
    stackR(top) = sy;
    stackC(top) = sx;
    visited(sy, sx) = true;
    seedVal = double(img(sy, sx));
    
    if conn == 4
        neighbors = [-1,0; 1,0; 0,-1; 0,1];
        numN = 4;
    else
        neighbors = [-1,0; 1,0; 0,-1; 0,1; -1,-1; -1,1; 1,-1; 1,1];
        numN = 8;
    end
    
    while top > 0
        cr = stackR(top);
        cc = stackC(top);
        top = top - 1;
        
        if abs(double(img(cr, cc)) - seedVal) <= tol
            mask(cr, cc) = true;
            for d = 1:numN
                nr = cr + neighbors(d, 1);
                nc = cc + neighbors(d, 2);
                if nr >= 1 && nr <= h && nc >= 1 && nc <= w && ~visited(nr, nc)
                    visited(nr, nc) = true;
                    top = top + 1;
                    stackR(top) = nr;
                    stackC(top) = nc;
                end
            end
        end
    end
end
