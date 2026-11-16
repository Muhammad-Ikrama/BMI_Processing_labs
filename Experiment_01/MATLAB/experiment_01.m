%% Experiment No. 1 Master Runner: Digital Image Representation, Acquisition, and DICOM Data Handling
% Course: Medical Image Processing | Department of Biomedical Engineering, Riphah International University
% Faculty: Engr. Rana Talha Khalid

clear; close all; clc;
fprintf('================================================================================\n');
fprintf('EXPERIMENT NO. 1: MATLAB AUTOMATED SUITE\n');
fprintf('Digital Image Representation, Acquisition, and DICOM Data Handling\n');
fprintf('================================================================================\n\n');

task_files = { ...
    'task_01_matrix_analysis.m', ...
    'task_02_rgb_perceptual_luminance.m', ...
    'task_03_dicom_anonymization.m', ...
    'task_04_calibrated_measurement.m', ...
    'task_05_pacs_5x5_montage.m', ...
    'task_06_dataset_curation.m' ...
};

for i = 1:numel(task_files)
    fprintf('>>> RUNNING: %s ...\n', task_files{i});
    try
        run(task_files{i});
        fprintf('[PASS] %s completed successfully.\n\n', task_files{i});
    catch ME
        fprintf('[FAIL] Error in %s: %s\n\n', task_files{i}, ME.message);
    end
end

fprintf('================================================================================\n');
fprintf('ALL MATLAB EXPERIMENT 01 TASKS COMPLETED.\n');
fprintf('================================================================================\n');
