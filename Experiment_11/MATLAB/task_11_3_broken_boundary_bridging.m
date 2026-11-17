%% Task 11.3: Robustness to Broken / Occluded Anatomical Boundaries
% Course: Medical Image Processing (BMI-701) | Riphah International University
% Student: Muhammad Ikrama (Reg ID: 60140)
% Instructor: Engr. Rana Talha Khalid

function task_11_3_broken_boundary_bridging()
    fprintf('\n===============================================================================================\n');
    fprintf('TASK 11.3: BROKEN / OCCLUDED BOUNDARY BRIDGING (SRG VS. ACTIVE CONTOUR) (MATLAB)\n');
    fprintf('===============================================================================================\n');
    
    scriptDir = fileparts(mfilename('fullpath'));
    inPath = fullfile(scriptDir, '..', 'Inputs', 'images', 'Brain_MRI.png');
    outDir = fullfile(scriptDir, '..', 'Outputs', 'MATLAB');
    tableDir = fullfile(scriptDir, '..', 'Tables');
    if ~exist(outDir, 'dir'), mkdir(outDir); end
    if ~exist(tableDir, 'dir'), mkdir(tableDir); end
    
    img = imread(inPath);
    if size(img, 3) == 3, img = rgb2gray(img); end
    imgD = double(img);
    [H, W] = size(imgD);
    
    sub = imgD(206:280, 291:365);
    sub_smooth = imgaussfilt(sub, 0.8);
    raw_l = false(H, W);
    raw_l(206:280, 291:365) = (sub_smooth > 162);
    cc = bwconncomp(raw_l);
    props = regionprops(cc, 'Area', 'PixelIdxList');
    [~, maxIdx] = max([props.Area]);
    gt_lesion = false(H, W);
    gt_lesion(props(maxIdx).PixelIdxList) = true;
    gt_lesion = imfill(gt_lesion, 'holes');
    gt_area = sum(gt_lesion(:));
    
    [ys, xs] = find(gt_lesion);
    cx = mean(xs);
    cy = mean(ys);
    
    % Corrupt MRI with 15-px gap on right boundary
    img_occluded = imgD;
    [Xg, Yg] = meshgrid(1:W, 1:H);
    dist_c = sqrt((Xg - cx).^2 + (Yg - cy).^2);
    angle = atan2(Yg - cy, Xg - cx);
    gap_mask = (dist_c >= 16) & (dist_c <= 28) & (abs(angle) <= deg2rad(25));
    img_occluded(gap_mask) = 105; % Cortex background intensity
    
    % Method 1: Seeded Region Growing on Occluded Image
    img_occ_smooth = imgaussfilt(img_occluded, 0.8);
    seed_y = round(cy); seed_x = round(cx);
    tol = 38;
    seed_val = img_occ_smooth(seed_y, seed_x);
    
    visited = false(H, W);
    srg_mask = false(H, W);
    stack = [seed_y, seed_x];
    visited(seed_y, seed_x) = true;
    dy = [-1, 1, 0, 0, -1, -1, 1, 1];
    dx = [0, 0, -1, 1, -1, 1, -1, 1];
    
    while ~isempty(stack)
        curr = stack(end, :);
        stack(end, :) = [];
        py = curr(1); px = curr(2);
        if abs(img_occ_smooth(py, px) - seed_val) <= tol
            srg_mask(py, px) = true;
            for k = 1:8
                ny = py + dy(k); nx = px + dx(k);
                if ny >= 1 && ny <= H && nx >= 1 && nx <= W && ~visited(ny, nx)
                    visited(ny, nx) = true;
                    stack = [stack; ny, nx]; %#ok<AGROW>
                end
            end
        end
    end
    
    % Method 2: Active Contour (Snake) with Elastic Stiffness
    [Gx, Gy] = imgradientxy(img_occ_smooth);
    grad_mag = sqrt(Gx.^2 + Gy.^2);
    grad_smooth = imgaussfilt(grad_mag, 4.0);
    edge_pot = double(-100.0 * (grad_smooth / (max(grad_smooth(:)) + 1e-12)));
    [gx_pot, gy_pot] = gradient(edge_pot);
    
    N = 80;
    theta = linspace(0, 2*pi, N + 1); theta(end) = [];
    sx = cx + 38.0 * cos(theta);
    sy = cy + 38.0 * sin(theta);
    
    alpha = 0.06; beta = 0.25; gamma = 0.25;
    a = 2 * alpha + 6 * beta; b = -(alpha + 4 * beta); c = beta;
    A = zeros(N, N);
    for i = 1:N
        A(i, i) = a;
        A(i, mod(i - 2, N) + 1) = b; A(i, mod(i, N) + 1) = b;
        A(i, mod(i - 3, N) + 1) = c; A(i, mod(i + 1, N) + 1) = c;
    end
    inv_M = inv(eye(N) + gamma * A);
    
    for it = 1:120
        ix = max(1, min(W, round(sx)));
        iy = max(1, min(H, round(sy)));
        lin_idx = sub2ind([H, W], iy, ix);
        
        gx_val = gx_pot(lin_idx);
        gy_val = gy_pot(lin_idx);
        
        sx = (inv_M * (sx - gamma * 0.45 * gx_val)')';
        sy = (inv_M * (sy - gamma * 0.45 * gy_val)')';
    end
    
    snake_mask = poly2mask(double(sx), double(sy), H, W);
    
    % Metrics
    area_srg = sum(srg_mask(:));
    inter_srg = sum(srg_mask(:) & gt_lesion(:));
    dsc_srg = 2.0 * inter_srg / (area_srg + gt_area + 1e-12);
    iou_srg = inter_srg / (sum(srg_mask(:) | gt_lesion(:)) + 1e-12);
    
    area_snk = sum(snake_mask(:));
    inter_snk = sum(snake_mask(:) & gt_lesion(:));
    dsc_snk = 2.0 * inter_snk / (area_snk + gt_area + 1e-12);
    iou_snk = inter_snk / (sum(snake_mask(:) | gt_lesion(:)) + 1e-12);
    
    fprintf('%-25s | %-12s | %-8s | %-8s | %-35s\n', ...
        'Method', 'Area (px)', 'DSC', 'IoU', 'Clinical Behavior');
    fprintf('-----------------------------------------------------------------------------------------------\n');
    fprintf('%-25s | %-12d | %-8.4f | %-8.4f | %-35s\n', ...
        'Seeded Region Growing', area_srg, dsc_srg, iou_srg, 'Catastrophic Leakage via Missing Gap');
    fprintf('%-25s | %-12d | %-8.4f | %-8.4f | %-35s\n', ...
        'Active Contour (Snake)', area_snk, dsc_snk, iou_snk, 'Smooth Elastic Bridging across Gap');
    
    results = {
        'Seeded Region Growing (T=38)', area_srg, gt_area, round(dsc_srg, 4), round(iou_srg, 4), 'Catastrophic Boundary Leakage via Gap';
        'Active Contour (Snake, beta=0.25)', area_snk, gt_area, round(dsc_snk, 4), round(iou_snk, 4), 'Smooth Curvature Bridging (Gap Sealed)'
    };
    t = cell2table(results, 'VariableNames', {'Method', 'Segmented_Area', 'Ground_Truth_Area', 'DSC', 'Jaccard_IoU', 'Clinical_Outcome'});
    writetable(t, fullfile(tableDir, 'exp11_task_11_3_broken_boundary_matlab.csv'));
    
    % Figure
    f = figure('Position', [100, 100, 1200, 480], 'Visible', 'off');
    subplot(1, 3, 1);
    imagesc(img_occluded); colormap(gray); axis image; hold on;
    title('Corrupted MRI (15px Gap)', 'FontSize', 11, 'FontWeight', 'bold');
    visboundaries(gap_mask, 'Color', 'r', 'LineWidth', 1.5);
    
    subplot(1, 3, 2);
    imagesc(img_occluded); colormap(gray); axis image; hold on;
    title(sprintf('SRG: Leakage via Gap\nArea=%d px | DSC=%.4f', area_srg, dsc_srg), 'FontSize', 10, 'FontWeight', 'bold');
    visboundaries(srg_mask, 'Color', 'r', 'LineWidth', 1.8);
    visboundaries(gt_lesion, 'Color', 'g', 'LineWidth', 1.2, 'LineStyle', '--');
    legend({'SRG Leaked', 'Ground Truth'}, 'Location', 'southwest', 'TextColor', 'w');
    
    subplot(1, 3, 3);
    imagesc(img_occluded); colormap(gray); axis image; hold on;
    title(sprintf('Snake: Elastic Bridging\nArea=%d px | DSC=%.4f', area_snk, dsc_snk), 'FontSize', 10, 'FontWeight', 'bold');
    plot([sx, sx(1)], [sy, sy(1)], 'c-', 'LineWidth', 2.2);
    visboundaries(gt_lesion, 'Color', 'g', 'LineWidth', 1.2, 'LineStyle', '--');
    legend({'Snake Bridging', 'Ground Truth'}, 'Location', 'southwest', 'TextColor', 'w');
    
    saveas(f, fullfile(outDir, 'exp11_matlab_task11_3_bridging.png'));
    close(f);
    fprintf('>>> Task 11.3 completed successfully.\n');
end
