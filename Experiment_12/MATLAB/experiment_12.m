%% Master Orchestrator: Experiment 12 - Rigid Registration of Multi-Modal Medical Images
% Course: Medical Image Processing (BMI-701) | Riphah International University
% Student: Muhammad Ikrama (Reg ID: 60140)
% Instructor: Engr. Rana Talha Khalid

function experiment_12()
    clc;
    fprintf('================================================================================\n');
    fprintf('STARTING COMPLETE MASTER EXECUTION: EXPERIMENT 12 (MATLAB)\n');
    fprintf('================================================================================\n');
    tStart = tic;
    
    % 1. Benchmark
    example_01_rigid_registration_benchmark();
    
    % 2. Task 12.1
    task_12_1_matrix_construction();
    
    % 3. Task 12.2
    task_12_2_interpolation_modes();
    
    % 4. Task 12.3
    task_12_3_joint_histogram_rotation_sweep();
    
    % 5. Task 12.4
    task_12_4_why_mse_fails_multimodal();
    
    % 6. Task 12.5
    task_12_5_pet_mri_fusion_checkerboard();
    
    tElapsed = toc(tStart);
    fprintf('\n================================================================================\n');
    fprintf('[SUCCESS] ALL EXPERIMENT 12 MATLAB MODULES COMPLETED IN %.2fs\n', tElapsed);
    fprintf('================================================================================\n');
end
