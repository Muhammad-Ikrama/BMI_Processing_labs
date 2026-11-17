%% Master Orchestrator: Experiment 11 - Active Contour (Snake) Based Segmentation
% Course: Medical Image Processing (BMI-701) | Riphah International University
% Student: Muhammad Ikrama (Reg ID: 60140)
% Instructor: Engr. Rana Talha Khalid

function experiment_11()
    clc;
    fprintf('================================================================================\n');
    fprintf('STARTING COMPLETE MASTER EXECUTION: EXPERIMENT 11 (MATLAB)\n');
    fprintf('================================================================================\n');
    tStart = tic;
    
    % 1. Benchmark
    example_01_snake_benchmark();
    
    % 2. Task 11.1
    task_11_1_alpha_beta_sensitivity();
    
    % 3. Task 11.2
    task_11_2_capture_range_radius();
    
    % 4. Task 11.3
    task_11_3_broken_boundary_bridging();
    
    % 5. Task 11.4
    task_11_4_edge_vs_chan_vese_noise();
    
    % 6. Task 11.5
    task_11_5_head_ct_skull_extraction();
    
    tElapsed = toc(tStart);
    fprintf('\n================================================================================\n');
    fprintf('[SUCCESS] ALL EXPERIMENT 11 MATLAB MODULES COMPLETED IN %.2fs\n', tElapsed);
    fprintf('================================================================================\n');
end
