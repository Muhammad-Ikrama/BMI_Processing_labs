%% Example 01: Parametric Active Contour (Snake) Benchmark
% Course: Medical Image Processing (BMI-701) | Riphah International University
% Student: Muhammad Ikrama (Reg ID: 60140)
% Instructor: Engr. Rana Talha Khalid

function example_01_snake_benchmark()
    fprintf('================================================================================\n');
    fprintf('EXPERIMENT 11: PARAMETRIC ACTIVE CONTOUR (SNAKE) BENCHMARK (MATLAB)\n');
    fprintf('================================================================================\n');
    
    scriptDir = fileparts(mfilename('fullpath'));
    inPath = fullfile(scriptDir, '..', 'Inputs', 'images', 'Brain_MRI.png');
    outDir = fullfile(scriptDir, '..', 'Outputs', 'MATLAB');
    tableDir = fullfile(scriptDir, '..', 'Tables');
    if ~exist(outDir, 'dir'), mkdir(outDir); end
    if ~exist(tableDir, 'dir'), mkdir(tableDir); end
    
    img = imread(inPath);
    if size(img, 3) == 3, img = rgb2gray(img); end
    [H, W] = size(img);
    
    % Ground truth lesion extraction
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
    
    % Edge mask and distance transform potential (sigma = 18.0)
    edge_mask = bwperim(gt_lesion);
    dist_edge = double(bwdist(edge_mask));
    edge_pot = double(100.0 * exp(-(dist_edge.^2) / (2.0 * (18.0^2))));
    [gx_pot, gy_pot] = gradient(edge_pot);
    
    % Initialize Snake (r0 = 38 px, N = 80 vertices)
    N = 80;
    theta = linspace(0, 2*pi, N + 1); theta(end) = [];
    sx = cx + 38.0 * cos(theta);
    sy = cy + 38.0 * sin(theta);
    
    alpha = 0.06;
    beta = 0.12;
    gamma = 0.25;
    numIters = 120;
    
    % Assemble Pentadiagonal Matrix A
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
    
    logIters = [1, 15, 40, 80, 120];
    results = cell(length(logIters), 6);
    snakeSnaps = cell(length(logIters), 2);
    
    fprintf('%-11s | %-10s | %-10s | %-10s | %-10s | %-11s\n', ...
        'Iteration', 'E_internal', 'E_external', 'E_total', 'Dice (DSC)', 'Jaccard IoU');
    fprintf('--------------------------------------------------------------------------\n');
    
    snapIdx = 1;
    for it = 1:numIters
        ix = max(1, min(W, round(sx)));
        iy = max(1, min(H, round(sy)));
        lin_idx = sub2ind([H, W], iy, ix);
        
        gx_val = gx_pot(lin_idx);
        gy_val = gy_pot(lin_idx);
        
        sx = (inv_M * (sx + gamma * 0.55 * gx_val)')';
        sy = (inv_M * (sy + gamma * 0.55 * gy_val)')';
        
        dx1 = circshift(sx, -1) - sx;
        dy1 = circshift(sy, -1) - sy;
        dx2 = circshift(sx, -1) - 2 * sx + circshift(sx, 1);
        dy2 = circshift(sy, -1) - 2 * sy + circshift(sy, 1);
        
        e_int = 0.5 * mean(alpha * (dx1.^2 + dy1.^2) + beta * (dx2.^2 + dy2.^2));
        e_ext = -mean(edge_pot(lin_idx));
        e_tot = e_int + e_ext;
        
        if ismember(it, logIters)
            mask = poly2mask(double(sx), double(sy), H, W);
            inter = sum(mask(:) & gt_lesion(:));
            dsc = 2.0 * inter / (sum(mask(:)) + sum(gt_lesion(:)) + 1e-12);
            iou = inter / (sum(mask(:) | gt_lesion(:)) + 1e-12);
            
            fprintf('Iter %-6d | %-10.2f | %-10.2f | %-10.2f | %-10.4f | %-11.4f\n', ...
                it, e_int, e_ext, e_tot, dsc, iou);
            
            results{snapIdx, 1} = sprintf('Iter %d', it);
            results{snapIdx, 2} = round(e_int, 4);
            results{snapIdx, 3} = round(e_ext, 4);
            results{snapIdx, 4} = round(e_tot, 4);
            results{snapIdx, 5} = round(dsc, 4);
            results{snapIdx, 6} = round(iou, 4);
            
            snakeSnaps{snapIdx, 1} = sx;
            snakeSnaps{snapIdx, 2} = sy;
            snapIdx = snapIdx + 1;
        end
    end
    
    % Save Table
    t = cell2table(results, 'VariableNames', {'Iteration', 'E_internal', 'E_external', 'E_total', 'Dice_DSC', 'Jaccard_IoU'});
    writetable(t, fullfile(tableDir, 'exp11_benchmark_summary_matlab.csv'));
    
    % Plot Evolution and Clinical Comparison
    f = figure('Position', [100, 100, 1400, 480], 'Visible', 'off');
    
    subplot(1, 3, 1);
    imagesc(img); colormap(gray); axis image; hold on;
    title('Input Brain MRI & Initial Snake (Iter 1)', 'FontSize', 11, 'FontWeight', 'bold');
    plot([snakeSnaps{1, 1}, snakeSnaps{1, 1}(1)], [snakeSnaps{1, 2}, snakeSnaps{1, 2}(1)], 'y-', 'LineWidth', 2);
    visboundaries(gt_lesion, 'Color', 'g', 'LineWidth', 1.5, 'LineStyle', '--');
    legend({'Initial Snake', 'Ground Truth'}, 'Location', 'southwest', 'TextColor', 'w');
    
    subplot(1, 3, 2);
    imagesc(edge_pot); colormap(hot); axis image; hold on;
    title('Edge Attraction Potential & Trajectory', 'FontSize', 11, 'FontWeight', 'bold');
    colors = {'y-', 'c-', 'm-', 'g-', 'r-'};
    for k = 1:length(logIters)
        plot([snakeSnaps{k, 1}, snakeSnaps{k, 1}(1)], [snakeSnaps{k, 2}, snakeSnaps{k, 2}(1)], ...
            colors{k}, 'LineWidth', 1.8);
    end
    legend({'Iter 1', 'Iter 15', 'Iter 40', 'Iter 80', 'Iter 120'}, 'Location', 'southwest', 'TextColor', 'w');
    
    subplot(1, 3, 3);
    imagesc(img); colormap(gray); axis image; hold on;
    title(sprintf('Final Convergence (Iter 120: DSC=%.4f)', results{end, 5}), 'FontSize', 11, 'FontWeight', 'bold');
    plot([snakeSnaps{end, 1}, snakeSnaps{end, 1}(1)], [snakeSnaps{end, 2}, snakeSnaps{end, 2}(1)], 'r-', 'LineWidth', 2.2);
    visboundaries(gt_lesion, 'Color', 'g', 'LineWidth', 1.5, 'LineStyle', '--');
    legend({'Converged Snake', 'Ground Truth'}, 'Location', 'southwest', 'TextColor', 'w');
    
    saveas(f, fullfile(outDir, 'exp11_matlab_benchmark_evolution.png'));
    close(f);
    
    fprintf('>>> Benchmark completed successfully.\n');
end
