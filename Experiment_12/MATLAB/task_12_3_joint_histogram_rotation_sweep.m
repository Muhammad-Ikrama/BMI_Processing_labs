%% Task 12.3: 2D Joint Histogram & Mutual Information Rotation Sweep
% Course: Medical Image Processing (BMI-701) | Riphah International University
% Student: Muhammad Ikrama (Reg ID: 60140)
% Instructor: Engr. Rana Talha Khalid

function task_12_3_joint_histogram_rotation_sweep()
    fprintf('\n==========================================================================================\n');
    fprintf('TASK 12.3: 2D JOINT HISTOGRAM & MUTUAL INFORMATION ROTATION SWEEP (-30° to +30°) (MATLAB)\n');
    fprintf('==========================================================================================\n');
    
    scriptDir = fileparts(mfilename('fullpath'));
    inDir = fullfile(scriptDir, '..', 'Inputs', 'images');
    outDir = fullfile(scriptDir, '..', 'Outputs', 'MATLAB');
    tableDir = fullfile(scriptDir, '..', 'Tables');
    if ~exist(outDir, 'dir'), mkdir(outDir); end
    if ~exist(tableDir, 'dir'), mkdir(tableDir); end
    
    mri = imread(fullfile(inDir, 'Brain_MRI.png'));
    if size(mri, 3) == 3, mri = rgb2gray(mri); end
    pet_aligned = imread(fullfile(inDir, 'Brain_PET_Aligned.png'));
    if size(pet_aligned, 3) == 3, pet_aligned = rgb2gray(pet_aligned); end
    
    angles = -30:2:30;
    numA = length(angles);
    results = cell(numA, 5);
    key_angles = [-30, -10, 0, 10, 30];
    key_hists = cell(5, 1);
    key_idx = 1;
    
    fprintf('%-20s | %-12s | %-22s | %-10s | %-10s\n', ...
        'Rotation Δθ (deg)', 'MI (bits)', 'Joint Entropy H(F,M)', 'NCC', 'MSE');
    fprintf('------------------------------------------------------------------------------------------\n');
    
    for idx = 1:numA
        th = angles(idx);
        pet_rot = imrotate(pet_aligned, th, 'bilinear', 'crop');
        
        [mi, ncc, mse, h_fm, h2d] = compute_metrics_task3(mri, pet_rot);
        
        if ismember(th, key_angles)
            key_hists{key_idx} = h2d;
            key_idx = key_idx + 1;
            status_tag = '';
            if th == 0, status_tag = '(PEAK)'; end
            fprintf('Δθ = %+3d° %-10s | %-12.4f | %-22.4f | %-10.4f | %-10.2f\n', ...
                th, status_tag, mi, h_fm, ncc, mse);
        end
        
        results{idx, 1} = th;
        results{idx, 2} = round(mi, 4);
        results{idx, 3} = round(h_fm, 4);
        results{idx, 4} = round(ncc, 4);
        results{idx, 5} = round(mse, 2);
    end
    
    t = cell2table(results, 'VariableNames', {'Delta_Theta_deg', 'Mutual_Information_MI', 'Joint_Entropy', 'Normalized_Cross_Corr_NCC', 'Mean_Squared_Error_MSE'});
    writetable(t, fullfile(tableDir, 'exp12_task_12_3_rotation_sweep_matlab.csv'));
    
    % Figure 1: Sweep Curves
    f1 = figure('Position', [100, 100, 1400, 500], 'Visible', 'off');
    subplot(1, 2, 1);
    yyaxis left;
    plot(angles, [results{:, 2}], 'b-o', 'LineWidth', 2.0, 'MarkerSize', 4);
    ylabel('Mutual Information (bits)');
    xline(0, 'g--', 'LineWidth', 1.5);
    yyaxis right;
    plot(angles, [results{:, 3}], 'r--s', 'LineWidth', 1.8, 'MarkerSize', 3);
    ylabel('Joint Entropy H(F,M)');
    xlabel('Rotation Misalignment \Delta\theta (degrees)');
    title('Mutual Information vs. Rotation Angle \Delta\theta', 'FontSize', 11, 'FontWeight', 'bold');
    grid on;
    
    subplot(1, 2, 2);
    yyaxis left;
    plot(angles, [results{:, 4}], 'm-^', 'LineWidth', 2.0, 'MarkerSize', 4);
    ylabel('Normalized Cross-Correlation');
    xline(0, 'g--', 'LineWidth', 1.5);
    yyaxis right;
    plot(angles, [results{:, 5}], 'k:d', 'LineWidth', 1.8, 'MarkerSize', 3);
    ylabel('Mean Squared Error (MSE)');
    xlabel('Rotation Misalignment \Delta\theta (degrees)');
    title('NCC & MSE Across Rotation Angle \Delta\theta', 'FontSize', 11, 'FontWeight', 'bold');
    grid on;
    
    saveas(f1, fullfile(outDir, 'exp12_matlab_task12_3_rotation_sweep.png'));
    close(f1);
    
    % Figure 2: Multi-Angle Histograms
    f2 = figure('Position', [100, 100, 1800, 380], 'Visible', 'off');
    for k = 1:5
        subplot(1, 5, k);
        imagesc(log1p(key_hists{k})); colormap(hot); axis image; set(gca, 'YDir', 'normal');
        title(sprintf('\\Delta\\theta = %+d°', key_angles(k)), 'FontSize', 11, 'FontWeight', 'bold');
        xlabel('MRI Intensity');
        if k == 1, ylabel('PET Intensity'); else, set(gca, 'YTickLabel', []); end
    end
    saveas(f2, fullfile(outDir, 'exp12_matlab_task12_3_joint_histograms_panels.png'));
    close(f2);
    
    fprintf('>>> Task 12.3 completed successfully.\n');
end

function [mi, ncc, mse, h_fm, h2d] = compute_metrics_task3(fixed, moving)
    fixedD = double(fixed); movingD = double(moving);
    bins = 64;
    f_idx = min(bins, floor(fixedD / 256 * bins) + 1);
    m_idx = min(bins, floor(movingD / 256 * bins) + 1);
    h2d = accumarray([f_idx(:), m_idx(:)], 1, [bins, bins]);
    pxy = h2d / sum(h2d(:));
    px = sum(pxy, 2);
    py = sum(pxy, 1);
    [Xb, Yb] = meshgrid(py, px);
    prod_p = Xb .* Yb;
    nz = (pxy > 0) & (prod_p > 0);
    
    h_f = -sum(px(px > 0) .* log2(px(px > 0)));
    h_m = -sum(py(py > 0) .* log2(py(py > 0)));
    h_fm = -sum(pxy(pxy > 0) .* log2(pxy(pxy > 0)));
    mi = h_f + h_m - h_fm;
    
    fc = fixedD - mean(fixedD(:));
    mc = movingD - mean(movingD(:));
    denom = sqrt(sum(fc(:).^2) * sum(mc(:).^2));
    if denom > 0, ncc = sum(fc(:) .* mc(:)) / denom; else, ncc = 0; end
    mse = mean((fixedD(:) - movingD(:)).^2);
end
