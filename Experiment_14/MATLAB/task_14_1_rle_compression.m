%% Task 14.1: Custom Run-Length Encoding (RLE) Compressor & Bit-Exact Verification
% Experiment 14: Medical Image Compression and Quality Evaluation
% Author: Muhammad Ikrama (Reg ID: 60140)

function results = task_14_1_rle_compression()
    fprintf('================================================================================\n');
    fprintf('TASK 14.1: CUSTOM RUN-LENGTH ENCODING (RLE) COMPRESSOR (MATLAB)\n');
    fprintf('================================================================================\n');
    
    mri = imread(fullfile('..', 'Inputs', 'images', 'Brain_MRI.png'));
    if size(mri, 3) == 3; mri = rgb2gray(mri); end
    
    % Otsu thresholding
    level = graythresh(mri);
    binMask = uint8(imbinarize(mri, level) * 255);
    
    % RLE encode binary mask
    [valsBin, countsBin] = rle_encode_mat(binMask);
    compBytesBin = length(valsBin) * 3;
    crBin = numel(binMask) / compBytesBin;
    decBin = rle_decode_mat(valsBin, countsBin, size(binMask));
    mseBin = mean((double(binMask) - double(decBin)).^2, 'all');
    
    % RLE encode grayscale MRI
    [valsGray, countsGray] = rle_encode_mat(mri);
    compBytesGray = length(valsGray) * 3;
    crGray = numel(mri) / compBytesGray;
    decGray = rle_decode_mat(valsGray, countsGray, size(mri));
    mseGray = mean((double(mri) - double(decGray)).^2, 'all');
    
    fprintf('%-38s | %-10s | %-7s | %-10s | %-6s | %-6s\n', 'Input Target', 'Raw Bytes', 'Runs', 'RLE Bytes', 'CR', 'MSE');
    fprintf('----------------------------------------------------------------------------------------\n');
    fprintf('%-38s | %-10d | %-7d | %-10d | %-5.2fx | %-6.4f\n', 'Binary Otsu Mask (High Redundancy)', numel(binMask), length(valsBin), compBytesBin, crBin, mseBin);
    fprintf('%-38s | %-10d | %-7d | %-10d | %-5.2fx | %-6.4f\n', 'Raw 8-bit Grayscale MRI (Noisy Pixels)', numel(mri), length(valsGray), compBytesGray, crGray, mseGray);
    
    assert(mseBin == 0, 'Binary RLE reconstruction failed!');
    assert(mseGray == 0, 'Grayscale RLE reconstruction failed!');
    fprintf('>>> Task 14.1 Complete: Bit-exact verification verified (MSE = 0.0000).\n');
    results = struct('crBin', crBin, 'crGray', crGray, 'mseBin', mseBin, 'mseGray', mseGray);
end

function [vals, counts] = rle_encode_mat(img)
    flat = img(:)';
    n = length(flat);
    if n == 0; vals = []; counts = []; return; end
    diffs = find(flat(1:end-1) ~= flat(2:end));
    idx = [0 diffs n];
    counts = diff(idx);
    vals = flat(idx(2:end));
end

function img = rle_decode_mat(vals, counts, sz)
    out = cell(1, length(vals));
    for k = 1:length(vals)
        out{k} = repmat(vals(k), 1, counts(k));
    end
    img = reshape([out{:}], sz);
end
