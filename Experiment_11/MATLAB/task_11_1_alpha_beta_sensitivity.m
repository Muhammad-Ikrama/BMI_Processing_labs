%% Task 11.1: Elasticity (Alpha) and Stiffness (Beta) Parameter Sensitivity
% Course: Medical Image Processing (BMI-701) | Riphah International University
% Student: Muhammad Ikrama (Reg ID: 60140)
% Instructor: Engr. Rana Talha Khalid

function task_11_1_alpha_beta_sensitivity()
    fprintf('\n===============================================================================================\n');
    fprintf('TASK 11.1: ELASTICITY (ALPHA) & STIFFNESS (BETA) PARAMETER SENSITIVITY SWEEP (MATLAB)\n');
    fprintf('===============================================================================================\n');
    
    scriptDir = fileparts(mfilename('fullpath'));
    inPath = fullfile(scriptDir, '..', 'Inputs', 'images', 'Brain_MRI.png');
    outDir = fullfile(scriptDir, '..', 'Outputs', 'MATLAB');
    tableDir = fullfile(scriptDir, '..', 'Tables');
    if ~exist(outDir, 'dir'), mkdir(outDir); end
    if ~exist(tableDir, 'dir'), mkdir(tableDir); end
    
    img = imread(inPath);
    if size(img, 3) == 3, img = rgb2gray(img); end
    [H, W] = size(img);
    
    sub = double(img(206:280, 291:365));
    sub_smooth = imgaussfilt(sub, 0.8);
    raw_l = false(H, W);
    raw_l(206:280, 291:365) = (sub_smooth > 162);
    cc = bwconncomp(raw_l);
    props = regionprops(cc, 'Area', 'PixelIdxList');
    [~, maxIdx] = max([props.Area]);
    gt_lesion = false(H, W);
    gt_lesion(props(maxIdx).PixelIdxList) = true;
    gt_lesion = imfill(gt_lesion, 'holes');
    
    [ys, xs] = find(gt_lesion);
    cx = mean(xs);
    cy = mean(ys);
    
    edge_mask = bwperim(gt_lesion);
    dist_edge = double(bwdist(edge_mask));
    edge_pot = double(100.0 * exp(-(dist_edge.^2) / (2.0 * (18.0^2))));
    [gx_pot, gy_pot] = gradient(edge_pot);
    
    regimes = {
        'High Tension',             0.80, 0.05, 'Inward Over-Shrinkage';
        'High Stiffness',           0.05, 2.50, 'Rigid Circle (No Conformal Bending)';
        'Balanced Clinical Tuning', 0.06, 0.12, 'Optimal Boundary Lock'
    };
    
    N = 80;
    theta = linspace(0, 2*pi, N + 1); theta(end) = [];
    gamma = 0.25;
    numIters = 120;
    
    fprintf('%-25s | %-6s | %-6s | %-8s | %-8s | %-10s | %-10s | %-20s\n', ...
        'Regime Name', 'alpha', 'beta', 'DSC', 'IoU', 'Area (px)', 'E_total', 'Status');
    fprintf('-----------------------------------------------------------------------------------------------\n');
    
    results = cell(size(regimes, 1), 8);
    finalSnakes = cell(size(regimes, 1), 2);
    
    for r = 1:size(regimes, 1)
        name = regimes{r, 1};
        alpha = regimes{r, 2};
        beta = regimes{r, 3};
        status = regimes{r, 4};
        
        a = 2 * alpha + 6 * beta;
        b = -(alpha + 4 * beta);
        c = beta;
        A = zeros(N, N);
        for i = 1:N
            A(i, i) = a;
            A(i, mod(i - 2, N) + 1) = b;
            A(i, mod(i, N) + 1) = b;
            A(i, mod(i - 3, N) + 1) = c;
            A(i, mod(i + 1, N) + 1) = c;
        end
        inv_M = inv(eye(N) + gamma * A);
        
        sx = cx + 38.0 * cos(theta);
        sy = cy + 38.0 * sin(theta);
        
        for it = 1:numIters
            ix = max(1, min(W, round(sx)));
            iy = max(1, min(H, round(sy)));
            lin_idx = sub2ind([H, W], iy, ix);
            
            gx_val = gx_pot(lin_idx);
            gy_val = gy_pot(lin_idx);
            
            sx = (inv_M * (sx + gamma * 0.55 * gx_val)')';
            sy = (inv_M * (sy + gamma * 0.55 * gy_val)')';
        end
        
        mask = poly2mask(double(sx), double(sy), H, W);
        area = sum(mask(:));
        inter = sum(mask(:) & gt_lesion(:));
        dsc = 2.0 * inter / (area + sum(gt_lesion(:)) + 1e-12);
        iou = inter / (sum(mask(:) | gt_lesion(:)) + 1e-12);
        
        dx1 = circshift(sx, -1) - sx;
        dy1 = circshift(sy, -1) - sy;
        dx2 = circshift(sx, -1) - 2 * sx + circshift(sx, 1);
        dy2 = circshift(sy, -1) - 2 * sy + circshift(sy, 1);
        
        ix = max(1, min(W, round(sx)));
        iy = max(1, min(H, round(sy)));
        lin_idx = sub2ind([H, W], iy, ix);
        
        e_int = 0.5 * mean(alpha * (dx1.^2 + dy1.^2) + beta * (dx2.^2 + dy2.^2));
        e_ext = -mean(edge_pot(lin_idx));
        e_tot = e_int + e_ext;
        
        fprintf('%-25s | %-6.2f | %-6.2f | %-8.4f | %-8.4f | %-10d | %-10.2f | %-20s\n', ...
            name, alpha, beta, dsc, iou, area, e_tot, status);
        
        results{r, 1} = name;
        results{r, 2} = alpha;
        results{r, 3} = beta;
        results{r, 4} = round(dsc, 4);
        results{r, 5} = round(iou, 4);
        results{r, 6} = area;
        results{r, 7} = round(e_tot, 2);
        results{r, 8} = status;
        
        finalSnakes{r, 1} = sx;
        finalSnakes{r, 2} = sy;
    end
    
    t = cell2table(results, 'VariableNames', {'Regime_Name', 'alpha', 'beta', 'DSC', 'IoU', 'Area_px', 'E_total', 'Status'});
    writetable(t, fullfile(tableDir, 'exp11_task_11_1_alpha_beta_matlab.csv'));
    
    % Multi-panel figure
    f = figure('Position', [100, 100, 1400, 450], 'Visible', 'off');
    colors = {'m-', 'r-', 'g-'};
    for r = 1:size(regimes, 1)
        subplot(1, 3, r);
        imagesc(img); colormap(gray); axis image; hold on;
        title(sprintf('%s (\\alpha=%.2f, \\beta=%.2f)\nDSC=%.4f | Area=%d px', ...
            regimes{r, 1}, regimes{r, 2}, regimes{r, 3}, results{r, 4}, results{r, 6}), ...
            'FontSize', 10, 'FontWeight', 'bold');
        plot([finalSnakes{r, 1}, finalSnakes{r, 1}(1)], [finalSnakes{r, 2}, finalSnakes{r, 2}(1)], ...
            colors{r}, 'LineWidth', 2.2);
        visboundaries(gt_lesion, 'Color', 'y', 'LineWidth', 1.5, 'LineStyle', '--');
        legend({regimes{r, 1}, 'Ground Truth'}, 'Location', 'southwest', 'TextColor', 'w');
    end
    saveas(f, fullfile(outDir, 'exp11_matlab_task11_1_sensitivity.png'));
    close(f);
    fprintf('>>> Task 11.1 completed successfully.\n');
end
