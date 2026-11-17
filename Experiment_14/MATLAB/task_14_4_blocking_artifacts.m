%% Task 14.4: 8x8 DCT Blocking Artifact & Residual Error Map Visualization
% Experiment 14: Medical Image Compression and Quality Evaluation
% Author: Muhammad Ikrama (Reg ID: 60140)

function results = task_14_4_blocking_artifacts()
    fprintf('================================================================================\n');
    fprintf('TASK 14.4: 8x8 DCT BLOCKING ARTIFACT VISUALIZATION (MATLAB)\n');
    fprintf('================================================================================\n');
    
    mri = imread(fullfile('..', 'Inputs', 'images', 'Brain_MRI.png'));
    if size(mri, 3) == 3; mri = rgb2gray(mri); end
    
    qualities = [85, 25, 5];
    fprintf('%-14s | %-18s | %-18s | %-12s\n', 'JPEG Quality', 'Mean Absolute Err', 'Max Absolute Err', 'Root MSE');
    fprintf('--------------------------------------------------------------------\n');
    
    for q = qualities
        tempJ = sprintf('temp_ba_q%d.jpg', q);
        imwrite(mri, tempJ, 'jpg', 'Quality', q);
        decJ = imread(tempJ);
        delete(tempJ);
        
        diff = abs(double(mri) - double(decJ));
        mae = mean(diff(:));
        maxErr = max(diff(:));
        rmse = sqrt(mean(diff(:).^2));
        
        fprintf('JPEG Q=%-8d | %-18.3f | %-18.2f | %-12.3f\n', q, mae, maxErr, rmse);
    end
    fprintf('>>> Task 14.4 Artifact Evaluation Complete.\n');
end
