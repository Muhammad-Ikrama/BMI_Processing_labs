%% Task 12.2: Interpolation Method Comparison (Nearest vs. Bilinear vs. Bicubic)
% Course: Medical Image Processing (BMI-701) | Riphah International University
% Student: Muhammad Ikrama (Reg ID: 60140)
% Instructor: Engr. Rana Talha Khalid

function task_12_2_interpolation_modes()
    fprintf('\n==========================================================================================\n');
    fprintf('TASK 12.2: INTERPOLATION METHOD COMPARISON (NEAREST VS. BILINEAR VS. BICUBIC) (MATLAB)\n');
    fprintf('==========================================================================================\n');
    
    scriptDir = fileparts(mfilename('fullpath'));
    inDir = fullfile(scriptDir, '..', 'Inputs', 'images');
    outDir = fullfile(scriptDir, '..', 'Outputs', 'MATLAB');
    tableDir = fullfile(scriptDir, '..', 'Tables');
    if ~exist(outDir, 'dir'), mkdir(outDir); end
    if ~exist(tableDir, 'dir'), mkdir(tableDir); end
    
    mri = imread(fullfile(inDir, 'Brain_MRI.png'));
    if size(mri, 3) == 3, mri = rgb2gray(mri); end
    [H, W] = size(mri);
    
    theta = 15.0;
    modes = {'nearest', 'bilinear', 'bicubic'};
    modeNames = {'Nearest-Neighbor', 'Bilinear', 'Bicubic'};
    
    brain_mask = mri > 25;
    se = strel('disk', 18);
    eval_mask = imerode(brain_mask, se);
    
    fprintf('%-22s | %-12s | %-10s | %-10s | %-10s | %-25s\n', ...
        'Interpolation Mode', 'PSNR (dB)', 'SSIM', 'MSE', 'MAE', 'Visual Quality');
    fprintf('------------------------------------------------------------------------------------------\n');
    
    results = cell(3, 7);
    recs = cell(3, 1);
    
    for k = 1:3
        m_flag = modes{k};
        m_name = modeNames{k};
        
        fwd = imrotate(mri, theta, m_flag, 'crop');
        bwd = imrotate(fwd, -theta, m_flag, 'crop');
        recs{k} = bwd;
        
        orig_px = double(mri(eval_mask));
        bwd_px = double(bwd(eval_mask));
        diff_px = abs(orig_px - bwd_px);
        
        mse = mean(diff_px.^2);
        mae = mean(diff_px);
        psnr_val = 10.0 * log10((255.0^2) / (mse + 1e-12));
        ssim_val = ssim(bwd, mri);
        
        if k == 1
            desc = '0th-Order Step Discontinuities (Jagged Edges)';
        elseif k == 2
            desc = '1st-Order Linear Weighting (Smooth, Standard)';
        else
            desc = '3rd-Order Spline (Sharp, High-Fidelity)';
        end
        
        fprintf('%-22s | %-12.2f | %-10.4f | %-10.2f | %-10.2f | %-25s\n', ...
            m_name, psnr_val, ssim_val, mse, mae, desc);
            
        results{k, 1} = m_name;
        results{k, 2} = 'Intracranial Parenchyma';
        results{k, 3} = round(psnr_val, 2);
        results{k, 4} = round(ssim_val, 4);
        results{k, 5} = round(mse, 2);
        results{k, 6} = round(mae, 2);
        results{k, 7} = desc;
    end
    
    t = cell2table(results, 'VariableNames', {'Interpolation_Method', 'Evaluation_Region', 'PSNR_dB', 'SSIM', 'MSE', 'MAE', 'Observed_Artifact'});
    writetable(t, fullfile(tableDir, 'exp12_task_12_2_interpolation_metrics_matlab.csv'));
    
    % Figure: Multi-panel comparison with zoomed crops
    f = figure('Position', [100, 100, 1500, 850], 'Visible', 'off');
    rx = 281; ry = 211; rw = 80; rh = 80;
    
    for k = 1:3
        subplot(2, 3, k);
        imagesc(recs{k}); colormap(gray); axis image; hold on;
        rectangle('Position', [rx, ry, rw, rh], 'EdgeColor', 'y', 'LineWidth', 1.8);
        title(sprintf('%s (Full Scan)\nPSNR = %.2f dB', modeNames{k}, results{k, 3}), 'FontSize', 11, 'FontWeight', 'bold');
        
        subplot(2, 3, k + 3);
        crop = recs{k}(ry:ry+rh, rx:rx+rw);
        imagesc(crop); colormap(gray); axis image;
        title(sprintf('Zoomed Crop (Sulci Detail)\nSSIM = %.4f', results{k, 4}), 'FontSize', 10, 'FontWeight', 'bold');
    end
    
    saveas(f, fullfile(outDir, 'exp12_matlab_task12_2_interpolation_comparison.png'));
    close(f);
    fprintf('>>> Task 12.2 completed successfully.\n');
end
