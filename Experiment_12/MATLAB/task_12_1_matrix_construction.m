%% Task 12.1: 2D Homogeneous Rigid Transformation Matrix Construction
% Course: Medical Image Processing (BMI-701) | Riphah International University
% Student: Muhammad Ikrama (Reg ID: 60140)
% Instructor: Engr. Rana Talha Khalid

function task_12_1_matrix_construction()
    fprintf('\n==========================================================================================\n');
    fprintf('TASK 12.1: 2D HOMOGENEOUS RIGID TRANSFORMATION MATRIX CONSTRUCTION (MATLAB)\n');
    fprintf('==========================================================================================\n');
    
    scriptDir = fileparts(mfilename('fullpath'));
    inDir = fullfile(scriptDir, '..', 'Inputs', 'images');
    outDir = fullfile(scriptDir, '..', 'Outputs', 'MATLAB');
    tableDir = fullfile(scriptDir, '..', 'Tables');
    if ~exist(outDir, 'dir'), mkdir(outDir); end
    if ~exist(tableDir, 'dir'), mkdir(tableDir); end
    
    ct = imread(fullfile(inDir, 'Head_CT.png'));
    if size(ct, 3) == 3, ct = rgb2gray(ct); end
    [H, W] = size(ct);
    cx = W / 2.0; cy = H / 2.0;
    
    tx = -15.0; ty = 12.0; theta_deg = 22.0;
    rad = deg2rad(theta_deg);
    
    T_to_orig = [1, 0, -cx; 0, 1, -cy; 0, 0, 1];
    R = [cos(rad), -sin(rad), 0; sin(rad), cos(rad), 0; 0, 0, 1];
    T_back = [1, 0, cx + tx; 0, 1, cy + ty; 0, 0, 1];
    T_forward = T_back * R * T_to_orig;
    T_inv = inv(T_forward);
    
    % In MATLAB, affine2d takes transpose of standard [x, y, 1] matrix
    tformFwd = affine2d(T_forward');
    tformInv = affine2d(T_inv');
    
    ct_fwd = imwarp(ct, tformFwd, 'OutputView', imref2d(size(ct)), 'InterpolationMethod', 'linear');
    ct_rec = imwarp(ct_fwd, tformInv, 'OutputView', imref2d(size(ct)), 'InterpolationMethod', 'linear');
    
    % Intracranial parenchyma evaluation mask
    brain_mask = (ct > 20) & (ct < 180);
    se = strel('disk', 18);
    eval_mask = imerode(brain_mask, se);
    num_eval = sum(eval_mask(:));
    
    orig_px = double(ct(eval_mask));
    rec_px = double(ct_rec(eval_mask));
    diff_px = abs(orig_px - rec_px);
    
    mae = mean(diff_px);
    mse = mean(diff_px.^2);
    max_err = max(diff_px);
    psnr_val = 10.0 * log10((255.0^2) / (mse + 1e-12));
    
    T_ident = T_forward * T_inv;
    frob_norm = norm(T_ident - eye(3), 'fro');
    
    fprintf('%-25s | %-14s | %-10s | %-10s | %-10s | %-10s\n', ...
        'Evaluation Region', 'Evaluated Px', 'MAE (Int)', 'MSE', 'Max Error', 'PSNR (dB)');
    fprintf('------------------------------------------------------------------------------------------\n');
    fprintf('%-25s | %-14d | %-10.4f | %-10.4f | %-10.2f | %-10.2f dB\n', ...
        'Intracranial Parenchyma', num_eval, mae, mse, max_err, psnr_val);
    fprintf('>>> Forward-Inverse Matrix Verification: ||T_fwd * T_inv - I|| = %.2e\n', frob_norm);
    
    results = {
        'Rigid (tx=-15, ty=+12, theta=22 deg)', round(det(T_forward), 6), frob_norm, num_eval, round(mae, 4), round(mse, 4), round(max_err, 2), round(psnr_val, 2)
    };
    t = cell2table(results, 'VariableNames', {'Transformation_Type', 'Matrix_Determinant', 'Identity_Deviation', 'Evaluated_Parenchyma_Pixels', 'Mean_Absolute_Error_MAE', 'Mean_Squared_Error_MSE', 'Max_Intensity_Error', 'Parenchyma_PSNR_dB'});
    writetable(t, fullfile(tableDir, 'exp12_task_12_1_matrix_error_matlab.csv'));
    
    % Multi-panel figure
    f = figure('Position', [100, 100, 1600, 420], 'Visible', 'off');
    subplot(1, 4, 1);
    imagesc(ct); colormap(gray); axis image; title('1. Original Reference Head CT', 'FontSize', 11, 'FontWeight', 'bold');
    
    subplot(1, 4, 2);
    imagesc(ct_fwd); colormap(gray); axis image; title('2. Forward Transformed (\theta=22°)', 'FontSize', 11, 'FontWeight', 'bold');
    
    subplot(1, 4, 3);
    imagesc(ct_rec); colormap(gray); axis image; title(sprintf('3. Inverse Recovered T^{-1}\nPSNR = %.2f dB', psnr_val), 'FontSize', 11, 'FontWeight', 'bold');
    
    subplot(1, 4, 4);
    diff_map = zeros(H, W);
    diff_map(eval_mask) = abs(double(ct(eval_mask)) - double(ct_rec(eval_mask)));
    imagesc(diff_map, [0, 15]); colormap(hot); axis image; colorbar;
    title(sprintf('4. Parenchyma Error Map\nMAE = %.2f', mae), 'FontSize', 11, 'FontWeight', 'bold');
    
    saveas(f, fullfile(outDir, 'exp12_matlab_task12_1_homogeneous_matrix.png'));
    close(f);
    fprintf('>>> Task 12.1 completed successfully.\n');
end
