%% Task 14.2: Shannon First-Order Entropy & Redundancy Comparison Across Modalities
% Experiment 14: Medical Image Compression and Quality Evaluation
% Author: Muhammad Ikrama (Reg ID: 60140)

function results = task_14_2_entropy_redundancy()
    fprintf('================================================================================\n');
    fprintf('TASK 14.2: SHANNON ENTROPY & REDUNDANCY COMPARISON (MATLAB)\n');
    fprintf('================================================================================\n');
    
    files = {
        'Brain MRI', fullfile('..', 'Inputs', 'images', 'Brain_MRI.png');
        'Head CT', fullfile('..', 'Inputs', 'images', 'Head_CT.png');
        'Chest X-Ray', fullfile('..', 'Inputs', 'images', 'Chest_Xray.png')
    };
    
    fprintf('%-16s | %-12s | %-10s | %-12s | %-17s | %-10s | %-7s\n', ...
            'Medical Modality', 'Dimensions', 'Raw Bytes', 'Entropy H', 'Max 1st-Order CR', 'PNG Bytes', 'PNG CR');
    fprintf('--------------------------------------------------------------------------------------------\n');
    
    results = struct();
    for k = 1:size(files, 1)
        name = files{k, 1};
        path = files{k, 2};
        im = imread(path);
        if size(im, 3) == 3; im = rgb2gray(im); end
        
        rawBytes = numel(im);
        hCounts = imhist(im);
        p = hCounts(hCounts > 0) / rawBytes;
        H = -sum(p .* log2(p));
        crShannon = 8.0 / H;
        
        tempName = sprintf('temp_p_%d.png', k);
        imwrite(im, tempName, 'png');
        infoP = imfinfo(tempName);
        crPng = rawBytes / infoP.FileSize;
        delete(tempName);
        
        fprintf('%-16s | %-12s | %-10d | %-12.3f | %-17.2fx | %-10d | %.2fx\n', ...
                name, sprintf('%dx%d', size(im, 1), size(im, 2)), rawBytes, H, crShannon, infoP.FileSize, crPng);
    end
    fprintf('>>> Task 14.2 Shannon Entropy Evaluation Complete.\n');
end
