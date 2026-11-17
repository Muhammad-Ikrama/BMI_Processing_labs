%% Task 11.4: Edge-Based Snake vs. Chan-Vese Region-Based Active Contour under Noise
% Course: Medical Image Processing (BMI-701) | Riphah International University
% Student: Muhammad Ikrama (Reg ID: 60140)
% Instructor: Engr. Rana Talha Khalid

function task_11_4_edge_vs_chan_vese_noise()
    fprintf('\n===============================================================================================\n');
    fprintf('TASK 11.4: EDGE-BASED SNAKE VS. CHAN-VESE REGION-BASED ACTIVE CONTOUR (NOISE sigma=28) (MATLAB)\n');
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
    
    % Add Gaussian noise (sigma = 28)
    rng(42);
    noise = randn(H, W) * 28.0;
    img_noisy = uint8(max(0, min(255, imgD + noise)));
    img_noisy_d = double(img_noisy);
    
    % Model 1: Edge-based Snake
    [Gx, Gy] = imgradientxy(img_noisy_d);
    grad_mag = sqrt(Gx.^2 + Gy.^2);
    grad_smooth = imgaussfilt(grad_mag, 2.0);
    edge_pot = double(-100.0 * (grad_smooth / (max(grad_smooth(:)) + 1e-12)));
    [gx_pot, gy_pot] = gradient(edge_pot);
    
    N = 80;
    theta = linspace(0, 2*pi, N + 1); theta(end) = [];
    sx = cx + 38.0 * cos(theta);
    sy = cy + 38.0 * sin(theta);
    
    alpha = 0.06; beta = 0.12; gamma = 0.25;
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
    mask_edge = poly2mask(double(sx), double(sy), H, W);
    
    % Model 2: Chan-Vese Region-Based Active Contour
    [Xg, Yg] = meshgrid(1:W, 1:H);
    init_mask = ((Xg - cx).^2 + (Yg - cy).^2) <= (38.0^2);
    cv_raw = activecontour(img_noisy, init_mask, 35, 'Chan-Vese', 'SmoothFactor', 3);
    
    cc = bwconncomp(cv_raw);
    props = regionprops(cc, 'Centroid', 'Area');
    mask_cv = false(H, W);
    if cc.NumObjects > 0
        minDist = Inf;
        bestIdx = 1;
        for k = 1:cc.NumObjects
            d = hypot(props(k).Centroid(1) - cx, props(k).Centroid(2) - cy);
            if d < minDist
                minDist = d;
                bestIdx = k;
            end
        end
        mask_cv(cc.PixelIdxList{bestIdx}) = true;
        mask_cv = imfill(mask_cv, 'holes');
    else
        mask_cv = cv_raw;
    end
    
    % Metrics
    area_edge = sum(mask_edge(:));
    inter_edge = sum(mask_edge(:) & gt_lesion(:));
    dsc_edge = 2.0 * inter_edge / (area_edge + gt_area + 1e-12);
    iou_edge = inter_edge / (sum(mask_edge(:) | gt_lesion(:)) + 1e-12);
    
    area_cv = sum(mask_cv(:));
    inter_cv = sum(mask_cv(:) & gt_lesion(:));
    dsc_cv = 2.0 * inter_cv / (area_cv + gt_area + 1e-12);
    iou_cv = inter_cv / (sum(mask_cv(:) | gt_lesion(:)) + 1e-12);
    
    fprintf('%-32s | %-12s | %-8s | %-8s | %-30s\n', ...
        'Method', 'Area (px)', 'DSC', 'IoU', 'Clinical Status');
    fprintf('-----------------------------------------------------------------------------------------------\n');
    fprintf('%-32s | %-12d | %-8.4f | %-8.4f | %-30s\n', ...
        'Edge-Based Snake (Local Grad)', area_edge, dsc_edge, iou_edge, 'Snagged on Noise Spikes');
    fprintf('%-32s | %-12d | %-8.4f | %-8.4f | %-30s\n', ...
        'Chan-Vese Region Model', area_cv, dsc_cv, iou_cv, 'Robust Global Region Averaging');
    
    results = {
        'Edge-Based Snake', 'Local Gradient Magnitude ||grad I||^2', area_edge, gt_area, round(dsc_edge, 4), round(iou_edge, 4), 'Poor (Trapped in Local Noise Minima)';
        'Chan-Vese Region Model', 'Global Mean Intensity Variance (c1, c2)', area_cv, gt_area, round(dsc_cv, 4), round(iou_cv, 4), 'Superior (Integral Averages Out Thermal Noise)'
    };
    t = cell2table(results, 'VariableNames', {'Model_Type', 'Formulation', 'Area_px', 'Ground_Truth_px', 'DSC', 'Jaccard_IoU', 'Noise_Robustness'});
    writetable(t, fullfile(tableDir, 'exp11_task_11_4_edge_vs_chan_vese_matlab.csv'));
    
    % Figure
    f = figure('Position', [100, 100, 1400, 480], 'Visible', 'off');
    subplot(1, 3, 1);
    imagesc(img_noisy); colormap(gray); axis image; hold on;
    title('Noisy Brain MRI (\sigma_{noise}=28)', 'FontSize', 11, 'FontWeight', 'bold');
    visboundaries(gt_lesion, 'Color', 'g', 'LineWidth', 1.5, 'LineStyle', '--');
    
    subplot(1, 3, 2);
    imagesc(img_noisy); colormap(gray); axis image; hold on;
    title(sprintf('Edge Snake: Trapped by Noise\nArea=%d px | DSC=%.4f', area_edge, dsc_edge), 'FontSize', 10, 'FontWeight', 'bold');
    plot([sx, sx(1)], [sy, sy(1)], 'r-', 'LineWidth', 2.0);
    visboundaries(gt_lesion, 'Color', 'g', 'LineWidth', 1.2, 'LineStyle', '--');
    legend({'Edge Snake', 'Ground Truth'}, 'Location', 'southwest', 'TextColor', 'w');
    
    subplot(1, 3, 3);
    imagesc(img_noisy); colormap(gray); axis image; hold on;
    title(sprintf('Chan-Vese: Noise Robust\nArea=%d px | DSC=%.4f', area_cv, dsc_cv), 'FontSize', 10, 'FontWeight', 'bold');
    visboundaries(mask_cv, 'Color', 'c', 'LineWidth', 2.2);
    visboundaries(gt_lesion, 'Color', 'g', 'LineWidth', 1.2, 'LineStyle', '--');
    legend({'Chan-Vese Region', 'Ground Truth'}, 'Location', 'southwest', 'TextColor', 'w');
    
    saveas(f, fullfile(outDir, 'exp11_matlab_task11_4_noise_robustness.png'));
    close(f);
    fprintf('>>> Task 11.4 completed successfully.\n');
end
