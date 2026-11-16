%% Experiment No. 2 Master Runner: Contrast Enhancement and Histogram Equalization
% Course: Medical Image Processing | Department of Biomedical Engineering, Riphah International University
% Faculty: Engr. Rana Talha Khalid

clear; close all; clc;
fprintf('================================================================================\n');
fprintf('EXPERIMENT NO. 02: MATLAB AUTOMATED SUITE\n');
fprintf('Histogram Computation and Histogram Equalization Techniques\n');
fprintf('================================================================================\n\n');

task_files = { ...
    'example_01_histogram_cdf.m', ...
    'example_02_ghe_vs_clahe.m', ...
    'task_2_1_manual_histogram.m', ...
    'task_2_2_dual_axis_cdf.m', ...
    'task_2_3_global_histogram_equalization.m', ...
    'task_2_4_clahe_clip_sensitivity.m', ...
    'task_2_5_multipanel_contrast_report.m' ...
};

for i = 1:numel(task_files)
    fprintf('>>> RUNNING: %s ...\n', task_files{i});
    try
        [~, funcName, ~] = fileparts(task_files{i});
        feval(funcName);
        fprintf('[PASS] %s completed successfully.\n\n', task_files{i});
    catch ME
        fprintf('[FAIL] Error in %s: %s\n\n', task_files{i}, ME.message);
    end
end

fprintf('================================================================================\n');
fprintf('ALL MATLAB EXPERIMENT 02 TASKS COMPLETED.\n');
fprintf('================================================================================\n');
