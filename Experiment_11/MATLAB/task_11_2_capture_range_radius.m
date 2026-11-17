%% Task 11.2: Capture Range and Initial Contour Radius Evaluation
% Course: Medical Image Processing (BMI-701) | Riphah International University
% Student: Muhammad Ikrama (Reg ID: 60140)
% Instructor: Engr. Rana Talha Khalid

function task_11_2_capture_range_radius()
    fprintf('\n===============================================================================================\n');
    fprintf('TASK 11.2: CAPTURE RANGE & INITIAL CONTOUR RADIUS EVALUATION (MATLAB)\n');
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
    
    pot_12 = double(100.0 * exp(-(dist_edge.^2) / (2.0 * (12.0^2))));
    [gx_12, gy_12] = gradient(pot_12);
    
    pot_24 = double(100.0 * exp(-(dist_edge.^2) / (2.0 * (24.0^2))));
    [gx_24, gy_24] = gradient(pot_24);
    
    configs = {
        'r0=28 px (Interior)',              28.0, 12.0, 'Optimal Convergence';
        'r0=38 px (Optimal Baseline)',      38.0, 12.0, 'Optimal Convergence';
        'r0=52 px (Extended Margin)',       52.0, 12.0, 'Optimal Convergence';
        'r0=70 px (Outside Capture sigma=12)', 70.0, 12.0, 'Stalled Outside Capture Range';
        'r0=70 px (Expanded sigma=24)',     70.0, 24.0, 'Partial Capture'
    };
    
    N = 80;
    theta = linspace(0, 2*pi, N + 1); theta(end) = [];
    alpha = 0.06; beta = 0.12; gamma = 0.25;
    numIters = 120;
    
    a = 2 * alpha + 6 * beta; b = -(alpha + 4 * beta); c = beta;
    A = zeros(N, N);
    for i = 1:N
        A(i, i) = a;
        A(i, mod(i - 2, N) + 1) = b; A(i, mod(i, N) + 1) = b;
        A(i, mod(i - 3, N) + 1) = c; A(i, mod(i + 1, N) + 1) = c;
    end
    inv_M = inv(eye(N) + gamma * A);
    
    fprintf('%-35s | %-8s | %-6s | %-10s | %-10s | %-25s\n', ...
        'Configuration', 'r0 (px)', 'sigma', 'Final DSC', 'Final IoU', 'Status');
    fprintf('-----------------------------------------------------------------------------------------------\n');
    
    results = cell(size(configs, 1), 6);
    finalSnakes = cell(size(configs, 1), 2);
    
    for c_idx = 1:size(configs, 1)
        name = configs{c_idx, 1};
        r0 = configs{c_idx, 2};
        sigma = configs{c_idx, 3};
        status = configs{c_idx, 4};
        
        if sigma == 12.0
            gx = gx_12; gy = gy_12;
        else
            gx = gx_24; gy = gy_24;
        end
        
        sx = cx + r0 * cos(theta);
        sy = cy + r0 * sin(theta);
        
        for it = 1:numIters
            ix = max(1, min(W, round(sx)));
            iy = max(1, min(H, round(sy)));
            lin_idx = sub2ind([H, W], iy, ix);
            
            gx_val = gx(lin_idx);
            gy_val = gy(lin_idx);
            
            sx = (inv_M * (sx + gamma * 0.55 * gx_val)')';
            sy = (inv_M * (sy + gamma * 0.55 * gy_val)')';
        end
        
        mask = poly2mask(double(sx), double(sy), H, W);
        inter = sum(mask(:) & gt_lesion(:));
        dsc = 2.0 * inter / (sum(mask(:)) + sum(gt_lesion(:)) + 1e-12);
        iou = inter / (sum(mask(:) | gt_lesion(:)) + 1e-12);
        
        fprintf('%-35s | %-8.1f | %-6.1f | %-10.4f | %-10.4f | %-25s\n', ...
            name, r0, sigma, dsc, iou, status);
        
        results{c_idx, 1} = name;
        results{c_idx, 2} = r0;
        results{c_idx, 3} = sigma;
        results{c_idx, 4} = round(dsc, 4);
        results{c_idx, 5} = round(iou, 4);
        results{c_idx, 6} = status;
        
        finalSnakes{c_idx, 1} = sx;
        finalSnakes{c_idx, 2} = sy;
    end
    
    t = cell2table(results, 'VariableNames', {'Configuration', 'r0_px', 'sigma', 'Final_DSC', 'Final_IoU', 'Status'});
    writetable(t, fullfile(tableDir, 'exp11_task_11_2_capture_range_matlab.csv'));
    
    % Multi-panel figure
    f = figure('Position', [100, 100, 1400, 480], 'Visible', 'off');
    colors = {'y-', 'c-', 'g-', 'm-', 'r-'};
    for c_idx = 1:size(configs, 1)
        subplot(1, 5, c_idx);
        imagesc(img); colormap(gray); axis image; hold on;
        title(sprintf('r0=%.0f, \\sigma=%.0f\nDSC=%.4f', configs{c_idx, 2}, configs{c_idx, 3}, results{c_idx, 4}), ...
            'FontSize', 9, 'FontWeight', 'bold');
        plot([finalSnakes{c_idx, 1}, finalSnakes{c_idx, 1}(1)], [finalSnakes{c_idx, 2}, finalSnakes{c_idx, 2}(1)], ...
            colors{c_idx}, 'LineWidth', 2.0);
        visboundaries(gt_lesion, 'Color', 'w', 'LineWidth', 1.2, 'LineStyle', '--');
    end
    saveas(f, fullfile(outDir, 'exp11_matlab_task11_2_capture_range.png'));
    close(f);
    fprintf('>>> Task 11.2 completed successfully.\n');
end
