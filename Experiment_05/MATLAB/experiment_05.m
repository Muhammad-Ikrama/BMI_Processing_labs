%% Experiment 05: Master Execution Script (MATLAB)
%% Edge Detection in Medical Images Using Sobel, Prewitt, and Canny Operators: Implementation and Comparative Analysis
%% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
%% Faculty: Engr. Rana Talha Khalid | Riphah International University

function experiment_05()
    tStart = tic;
    fprintf('================================================================================\n');
    fprintf('STARTING FULL EXECUTION: EXPERIMENT 05 (MATLAB PIPELINE)\n');
    fprintf('Course: Medical Image Processing | Instructor: Engr. Rana Talha Khalid\n');
    fprintf('================================================================================\n');

    % Ensure script directory is on path
    scriptDir = fileparts(mfilename('fullpath'));
    addpath(scriptDir);

    % 1. Example 01
    fprintf('\n>>> Running Example 01: Medical Edge Detection Benchmark...\n');
    resEx01 = example_01();

    % 2. Task 5.1
    fprintf('\n>>> Running Task 5.1: Discrete Gradient Kernel Construction & Directional Sensitivity...\n');
    resT51 = task_5_1();

    % 3. Task 5.2
    fprintf('\n>>> Running Task 5.2: Prewitt vs. Sobel Noise Sensitivity Benchmarking...\n');
    resT52 = task_5_2();

    % 4. Task 5.3
    fprintf('\n>>> Running Task 5.3: Manual Implementation of Non-Maximum Suppression (NMS)...\n');
    resT53 = task_5_3();

    % 5. Task 5.4
    fprintf('\n>>> Running Task 5.4: Canny Hysteresis Threshold Tuning & Broken Contour Analysis...\n');
    resT54 = task_5_4();

    % 6. Task 5.5
    fprintf('\n>>> Running Task 5.5: Multi-Operator Quantitative Diagnostic Evaluation Report...\n');
    resT55 = task_5_5();

    elapsed = toc(tStart);
    fprintf('\n================================================================================\n');
    fprintf('[COMPLETE] All Experiment 05 MATLAB tasks completed successfully in %.2f seconds.\n', elapsed);
    fprintf('Generated 6 publication figures in Figures/ and outputs in Outputs/MATLAB/.\n');
    fprintf('================================================================================\n');
end
