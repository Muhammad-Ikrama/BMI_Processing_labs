%% Master Orchestrator: Experiment 10 - Region-Based Segmentation Using Seeded Region Growing and Watershed Transform
%% Author: Muhammad Ikrama (Reg ID: 60140)
%% Department of Biomedical Engineering, Riphah International University, Lahore
%% Instructor: Engr. Rana Talha Khalid

function experiment_10()
    fprintf('================================================================================\n');
    fprintf('STARTING COMPLETE MASTER EXECUTION: EXPERIMENT 10 (MATLAB)\n');
    fprintf('================================================================================\n');
    tStart = tic;
    
    % 1. Benchmark
    example_01_region_growing_watershed_benchmark();
    
    % 2. Task 10.1
    task_10_1_connectivity_4_vs_8();
    
    % 3. Task 10.2
    task_10_2_fixed_vs_running_mean();
    
    % 4. Task 10.3
    task_10_3_seed_perturbation();
    
    % 5. Task 10.4
    task_10_4_distance_transform_sweep();
    
    % 6. Task 10.5
    task_10_5_chest_xray_lung_watershed();
    
    tElapsed = toc(tStart);
    fprintf('\n================================================================================\n');
    fprintf('[SUCCESS] ALL EXPERIMENT 10 MATLAB MODULES COMPLETED IN %.2f SECONDS\n', tElapsed);
    fprintf('================================================================================\n');
end
