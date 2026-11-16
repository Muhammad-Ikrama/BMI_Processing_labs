%% ==============================================================================
%% EXPERIMENT 08: MASTER PIPELINE ORCHESTRATOR (MATLAB)
%% ==============================================================================
function experiment_08()
    tStart = tic;
    fprintf('==================================================================\n');
    fprintf('STARTING EXPERIMENT 08 MATLAB PIPELINE\n');
    fprintf('Department of Biomedical Engineering - Riphah International University\n');
    fprintf('==================================================================\n');

    fprintf('\n>>> STEP 1: Running Benchmark & Clinical Comparison...\n');
    example_01_global_adaptive_benchmark();

    fprintf('\n>>> STEP 2: Running Task 8.1 (Custom Otsu from First Principles)...\n');
    task_8_1_custom_otsu();

    fprintf('\n>>> STEP 3: Running Task 8.2 (Iterative Isodata vs. Otsu Convergence)...\n');
    task_8_2_isodata_convergence();

    fprintf('\n>>> STEP 4: Running Task 8.3 (MRI RF Bias-Field Shading Failure)...\n');
    task_8_3_rf_bias_failure();

    fprintf('\n>>> STEP 5: Running Task 8.4 (Adaptive Parameter Sensitivity Sweep)...\n');
    task_8_4_adaptive_param_sweep();

    fprintf('\n>>> STEP 6: Running Task 8.5 (Multi-Otsu 3-Class Tissue Classification)...\n');
    task_8_5_multi_otsu();

    elapsed = toc(tStart);
    fprintf('\n==================================================================\n');
    fprintf('EXPERIMENT 08 MATLAB PIPELINE COMPLETED IN %.2f SECONDS\n', elapsed);
    fprintf('All MAT-files, figures, and CSV tables successfully generated.\n');
    fprintf('==================================================================\n');
end
