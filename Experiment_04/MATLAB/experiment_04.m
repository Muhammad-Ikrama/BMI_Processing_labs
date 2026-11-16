%% ==============================================================================
%% SCRIPT: experiment_04.m
%% Experiment 04 Master Orchestration Script (MATLAB)
%% Noise Modeling and Removal in Medical Images Using Median and Adaptive Filtering
%% Course: Medical Image Processing | Riphah International University
%% Instructor: Engr. Rana Talha Khalid
%% ==============================================================================

function experiment_04()
    tStart = tic;
    fprintf('================================================================================\n');
    fprintf('RIPHAH INTERNATIONAL UNIVERSITY - DEPARTMENT OF BIOMEDICAL ENGINEERING\n');
    fprintf('EXPERIMENT NO. 04: NOISE MODELING AND REMOVAL USING MEDIAN & ADAPTIVE FILTERING\n');
    fprintf('Instructor: Engr. Rana Talha Khalid\n');
    fprintf('================================================================================\n');

    fprintf('\n>>> EXECUTING EXAMPLE 01: NOISE RESTORATION BENCHMARK...\n');
    example_01();

    fprintf('\n>>> EXECUTING TASK 4.1: NOISE MODELING & PDF ANALYSIS...\n');
    task_4_1();

    fprintf('\n>>> EXECUTING TASK 4.2: LINEAR FILTER FAILURE ANALYSIS ON IMPULSE NOISE...\n');
    task_4_2();

    fprintf('\n>>> EXECUTING TASK 4.3: MEDIAN WINDOW SENSITIVITY [3x3, 5x5, 7x7]...\n');
    task_4_3();

    fprintf('\n>>> EXECUTING TASK 4.4: ADAPTIVE MEDIAN (AMF) HIGH-DENSITY STRESS TEST...\n');
    task_4_4();

    fprintf('\n>>> EXECUTING TASK 4.5: DIAGNOSTIC RESTORATION REPORT...\n');
    task_4_5();

    elapsed = toc(tStart);
    fprintf('\n================================================================================\n');
    fprintf('[SUCCESS] ALL EXPERIMENT 04 MATLAB TASKS COMPLETED IN %.2f SECONDS!\n', elapsed);
    fprintf('================================================================================\n');
end
