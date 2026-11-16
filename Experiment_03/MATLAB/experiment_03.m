%% ==============================================================================
%% SCRIPT: experiment_03.m
%% Experiment 03 Master Orchestration Script (MATLAB)
%% Image Smoothing of Medical Images Using Spatial Domain Mean & Gaussian Filters
%% Course: Medical Image Processing | Riphah International University
%% Instructor: Engr. Rana Talha Khalid
%% ==============================================================================

function experiment_03()
    tStart = tic;
    fprintf('================================================================================\n');
    fprintf('RIPHAH INTERNATIONAL UNIVERSITY - DEPARTMENT OF BIOMEDICAL ENGINEERING\n');
    fprintf('EXPERIMENT NO. 03: IMAGE SMOOTHING USING SPATIAL DOMAIN MEAN & GAUSSIAN FILTERS\n');
    fprintf('Instructor: Engr. Rana Talha Khalid\n');
    fprintf('================================================================================\n');

    fprintf('\n>>> EXECUTING EXAMPLE 01: FILTERING BENCHMARK (MEAN VS GAUSSIAN)...\n');
    example_01();

    fprintf('\n>>> EXECUTING TASK 3.1: 2D DISCRETE CONVOLUTION & BOUNDARY PADDING...\n');
    task_3_1();

    fprintf('\n>>> EXECUTING TASK 3.2: MEAN FILTER KERNEL SWEEP [3x3 to 9x9]...\n');
    task_3_2();

    fprintf('\n>>> EXECUTING TASK 3.3: 2D GAUSSIAN KERNEL GENERATION & SIGMA SWEEP...\n');
    task_3_3();

    fprintf('\n>>> EXECUTING TASK 3.4: QUANTITATIVE BENCHMARKING (PSNR, SSIM, CNR)...\n');
    task_3_4();

    fprintf('\n>>> EXECUTING TASK 3.5: 1D ANATOMICAL EDGE GRADIENT PROFILES...\n');
    task_3_5();

    elapsed = toc(tStart);
    fprintf('\n================================================================================\n');
    fprintf('[SUCCESS] ALL EXPERIMENT 03 MATLAB TASKS COMPLETED IN %.2f SECONDS!\n', elapsed);
    fprintf('================================================================================\n');
end
