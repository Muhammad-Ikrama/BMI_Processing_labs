%% Task 14.3: Multi-Modality Rate-Distortion Curve Benchmarking
% Experiment 14: Medical Image Compression and Quality Evaluation
% Author: Muhammad Ikrama (Reg ID: 60140)

function results = task_14_3_rate_distortion_curves()
    fprintf('================================================================================\n');
    fprintf('TASK 14.3: MULTI-MODALITY RATE-DISTORTION CURVE BENCHMARKING (MATLAB)\n');
    fprintf('================================================================================\n');
    
    mri = imread(fullfile('..', 'Inputs', 'images', 'Brain_MRI.png'));
    if size(mri, 3) == 3; mri = rgb2gray(mri); end
    
    xray = imread(fullfile('..', 'Inputs', 'images', 'Chest_Xray.png'));
    if size(xray, 3) == 3; xray = rgb2gray(xray); end
    
    modalities = {'Brain MRI', mri; 'Chest X-Ray', xray};
    qualities = [95, 85, 70, 50, 30, 15, 5];
    
    fprintf('%-14s | %-9s | %-6s | %-7s | %-10s | %-6s\n', 'Modality', 'Q Factor', 'CR', 'MSE', 'PSNR (dB)', 'SSIM');
    fprintf('--------------------------------------------------------------\n');
    
    for m = 1:size(modalities, 1)
        mName = modalities{m, 1};
        img = modalities{m, 2};
        rawB = numel(img);
        
        for q = qualities
            tempJ = sprintf('temp_m_%d_q%d.jpg', m, q);
            imwrite(img, tempJ, 'jpg', 'Quality', q);
            infoJ = imfinfo(tempJ);
            decJ = imread(tempJ);
            delete(tempJ);
            
            cr = rawB / infoJ.FileSize;
            mseVal = mean((double(img) - double(decJ)).^2, 'all');
            psnrVal = psnr(decJ, img);
            ssimVal = ssim(decJ, img);
            
            fprintf('%-14s | %-9d | %-5.2fx | %-7.2f | %-10.2f | %-6.4f\n', mName, q, cr, mseVal, psnrVal, ssimVal);
        end
    end
    fprintf('>>> Task 14.3 Multi-Modality RD Evaluation Complete.\n');
end
