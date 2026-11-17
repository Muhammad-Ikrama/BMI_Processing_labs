%% Task 12.4: Why Mean Squared Error (MSE) Fails on Multi-Modal Scans
% Course: Medical Image Processing (BMI-701) | Riphah International University
% Student: Muhammad Ikrama (Reg ID: 60140)
% Instructor: Engr. Rana Talha Khalid

function task_12_4_why_mse_fails_multimodal()
    fprintf('\n==========================================================================================\n');
    fprintf('TASK 12.4: WHY MEAN SQUARED ERROR (MSE) FAILS ON MULTI-MODAL SCANS (GRID SWEEP) (MATLAB)\n');
    fprintf('==========================================================================================\n');
    
    scriptDir = fileparts(mfilename('fullpath'));
    inDir = fullfile(scriptDir, '..', 'Inputs', 'images');
    outDir = fullfile(scriptDir, '..', 'Outputs', 'MATLAB');
    tableDir = fullfile(scriptDir, '..', 'Tables');
    if ~exist(outDir, 'dir'), mkdir(outDir); end
    if ~exist(tableDir, 'dir'), mkdir(tableDir); end
    
    ct = imread(fullfile(inDir, 'Head_CT.png'));
    if size(ct, 3) == 3, ct = rgb2gray(ct); end
    ctD = double(ct);
    [H, W] = size(ct);
    
    % Simulate multi-modal inverted contrast MRI
    sim_mri = zeros(H, W);
    tissue = ctD > 15;
    sim_mri(tissue) = 235.0 - (ctD(tissue) * 0.85);
    brain_region = (ctD > 25) & (ctD < 170);
    sim_mri(brain_region) = 180.0 - (ctD(brain_region) - 70) * 0.4;
    sim_mri = uint8(max(0, min(255, sim_mri)));
    
    tx_range = -20:1:20;
    numT = length(tx_range);
    results = cell(numT, 4);
    
    for idx = 1:numT
        tx = tx_range(idx);
        % Shift sim_mri by tx
        shifted_mri = imtranslate(sim_mri, [tx, 0], 'FillValues', 0);
        
        mse = mean((ctD(:) - double(shifted_mri(:))).^2);
        mi = compute_mi_local(ct, shifted_mri);
        
        status = '';
        if tx == 0, status = 'True Alignment (Global MI Peak)'; end
        
        results{idx, 1} = tx;
        results{idx, 2} = round(mse, 2);
        results{idx, 3} = round(mi, 4);
        results{idx, 4} = status;
    end
    
    t = cell2table(results, 'VariableNames', {'Translation_tx_px', 'Mean_Squared_Error_MSE', 'Mutual_Information_MI', 'Alignment_Status'});
    writetable(t, fullfile(tableDir, 'exp12_task_12_4_mse_vs_mi_matlab.csv'));
    
    % Figure: Dual curves
    f = figure('Position', [100, 100, 1400, 500], 'Visible', 'off');
    subplot(1, 2, 1);
    yyaxis left;
    plot(tx_range, [results{:, 3}], 'g-o', 'LineWidth', 2.0, 'MarkerSize', 3);
    ylabel('Mutual Information (bits)');
    xline(0, 'g--', 'LineWidth', 1.5);
    yyaxis right;
    plot(tx_range, [results{:, 2}], 'r--s', 'LineWidth', 1.8, 'MarkerSize', 3);
    ylabel('Mean Squared Error (MSE)');
    xlabel('Horizontal Shift tx (pixels)');
    title('Mutual Information vs. Translation Offset', 'FontSize', 11, 'FontWeight', 'bold');
    grid on;
    
    subplot(1, 2, 2);
    comp = cat(3, sim_mri, ct, ct);
    imshow(comp);
    title('Multi-Modal Modality Contrast Inversion', 'FontSize', 11, 'FontWeight', 'bold');
    
    saveas(f, fullfile(outDir, 'exp12_matlab_task12_4_mse_vs_mi_failure.png'));
    close(f);
    
    fprintf('>>> Task 12.4 completed successfully.\n');
end

function mi = compute_mi_local(fixed, moving)
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
    mi = sum(pxy(nz) .* log2(pxy(nz) ./ prod_p(nz)));
end
