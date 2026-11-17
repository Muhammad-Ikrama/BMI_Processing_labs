%% Task 11.5: Intracranial Skull Boundary Extraction on Head CT
% Course: Medical Image Processing (BMI-701) | Riphah International University
% Student: Muhammad Ikrama (Reg ID: 60140)
% Instructor: Engr. Rana Talha Khalid

function task_11_5_head_ct_skull_extraction()
    fprintf('\n===============================================================================================\n');
    fprintf('TASK 11.5: INTRACRANIAL SKULL BOUNDARY EXTRACTION ON HEAD CT (MATLAB)\n');
    fprintf('===============================================================================================\n');
    
    scriptDir = fileparts(mfilename('fullpath'));
    inPath = fullfile(scriptDir, '..', 'Inputs', 'images', 'Head_CT.png');
    outDir = fullfile(scriptDir, '..', 'Outputs', 'MATLAB');
    tableDir = fullfile(scriptDir, '..', 'Tables');
    if ~exist(outDir, 'dir'), mkdir(outDir); end
    if ~exist(tableDir, 'dir'), mkdir(tableDir); end
    
    ct = imread(inPath);
    if size(ct, 3) == 3, ct = rgb2gray(ct); end
    [H, W] = size(ct);
    cx = W / 2.0; cy = H / 2.0;
    
    % Bone mask & Distance Transform Potential
    bone_mask = ct > 180;
    cc = bwconncomp(bone_mask);
    props = regionprops(cc, 'Area', 'PixelIdxList');
    outer_bone = false(H, W);
    if cc.NumObjects > 0
        [~, maxIdx] = max([props.Area]);
        outer_bone(props(maxIdx).PixelIdxList) = true;
    end
    outer_perim = bwperim(outer_bone);
    
    dist_bone = double(bwdist(outer_perim));
    edge_pot = double(100.0 * exp(-(dist_bone.^2) / (2.0 * 15.0^2)));
    [gx_pot, gy_pot] = gradient(edge_pot);
    
    % Initialize Snake (r0 = 235 px, N = 120 points)
    N = 120;
    theta = linspace(0, 2*pi, N + 1); theta(end) = [];
    r0 = 235.0;
    sx = cx + r0 * cos(theta);
    sy = cy + r0 * sin(theta);
    
    alpha = 0.08; beta = 0.15; gamma = 0.25;
    a = 2 * alpha + 6 * beta; b = -(alpha + 4 * beta); c = beta;
    A = zeros(N, N);
    for i = 1:N
        A(i, i) = a;
        A(i, mod(i - 2, N) + 1) = b; A(i, mod(i, N) + 1) = b;
        A(i, mod(i - 3, N) + 1) = c; A(i, mod(i + 1, N) + 1) = c;
    end
    inv_M = inv(eye(N) + gamma * A);
    
    logIters = [30, 60, 100];
    results = cell(length(logIters), 5);
    snaps = cell(length(logIters) + 1, 2);
    snaps{1, 1} = sx; snaps{1, 2} = sy;
    
    fprintf('%-12s | %-20s | %-16s | %-14s | %-20s\n', ...
        'Iteration', 'Enclosed Area (px)', 'Perimeter (px)', 'Circularity', 'Status');
    fprintf('-----------------------------------------------------------------------------------------------\n');
    
    snapIdx = 2;
    for it = 1:100
        ix = max(1, min(W, round(sx)));
        iy = max(1, min(H, round(sy)));
        lin_idx = sub2ind([H, W], iy, ix);
        
        gx_val = gx_pot(lin_idx);
        gy_val = gy_pot(lin_idx);
        
        sx = (inv_M * (sx + gamma * 0.45 * gx_val)')';
        sy = (inv_M * (sy + gamma * 0.45 * gy_val)')';
        
        if ismember(it, logIters)
            mask = poly2mask(double(sx), double(sy), H, W);
            area = sum(mask(:));
            dx = circshift(sx, -1) - sx;
            dy = circshift(sy, -1) - sy;
            perim = sum(sqrt(dx.^2 + dy.^2));
            circ = (4 * pi * area) / (perim^2 + 1e-12);
            
            if it < 100
                status_str = 'Contracting';
            else
                status_str = 'Locked on Outer Skull';
            end
            
            fprintf('Iter %-7d | %-20d | %-16.1f | %-14.4f | %-20s\n', ...
                it, area, perim, circ, status_str);
            
            row = snapIdx - 1;
            results{row, 1} = sprintf('Iter %d', it);
            results{row, 2} = area;
            results{row, 3} = round(perim, 1);
            results{row, 4} = round(circ, 4);
            results{row, 5} = status_str;
            
            snaps{snapIdx, 1} = sx;
            snaps{snapIdx, 2} = sy;
            snapIdx = snapIdx + 1;
        end
    end
    
    t = cell2table(results, 'VariableNames', {'Iteration', 'Enclosed_Area_px', 'Perimeter_px', 'Circularity', 'Status'});
    writetable(t, fullfile(tableDir, 'exp11_task_11_5_head_ct_skull_matlab.csv'));
    
    % Multi-panel figure
    f = figure('Position', [100, 100, 1400, 480], 'Visible', 'off');
    subplot(1, 3, 1);
    imagesc(ct); colormap(gray); axis image; hold on;
    title('Initial Outer Contour (r0=235 px)', 'FontSize', 11, 'FontWeight', 'bold');
    plot([snaps{1, 1}, snaps{1, 1}(1)], [snaps{1, 2}, snaps{1, 2}(1)], 'y-', 'LineWidth', 2.0);
    
    subplot(1, 3, 2);
    imagesc(edge_pot); colormap(hot); axis image; hold on;
    title('Skull Distance Field Potential & Contraction', 'FontSize', 11, 'FontWeight', 'bold');
    plot([snaps{1, 1}, snaps{1, 1}(1)], [snaps{1, 2}, snaps{1, 2}(1)], 'y--', 'LineWidth', 1.5);
    plot([snaps{2, 1}, snaps{2, 1}(1)], [snaps{2, 2}, snaps{2, 2}(1)], 'c-', 'LineWidth', 1.8);
    plot([snaps{3, 1}, snaps{3, 1}(1)], [snaps{3, 2}, snaps{3, 2}(1)], 'm-', 'LineWidth', 1.8);
    plot([snaps{4, 1}, snaps{4, 1}(1)], [snaps{4, 2}, snaps{4, 2}(1)], 'g-', 'LineWidth', 2.2);
    legend({'Iter 0', 'Iter 30', 'Iter 60', 'Iter 100'}, 'Location', 'southwest', 'TextColor', 'w');
    
    subplot(1, 3, 3);
    imagesc(ct); colormap(gray); axis image; hold on;
    title(sprintf('Final Calvarium Extraction (Iter 100)\nArea=%d px | Circ=%.4f', results{3, 2}, results{3, 4}), ...
        'FontSize', 11, 'FontWeight', 'bold');
    plot([snaps{4, 1}, snaps{4, 1}(1)], [snaps{4, 2}, snaps{4, 2}(1)], 'g-', 'LineWidth', 2.2);
    visboundaries(outer_bone, 'Color', 'r', 'LineWidth', 1.0, 'LineStyle', ':');
    legend({'Active Contour Skull', 'Bone Threshold'}, 'Location', 'southwest', 'TextColor', 'w');
    
    saveas(f, fullfile(outDir, 'exp11_matlab_task11_5_skull_extraction.png'));
    close(f);
    fprintf('>>> Task 11.5 completed successfully.\n');
end
