%% ==============================================================================
%% EXPERIMENT 09: MASTER PIPELINE ORCHESTRATOR (MATLAB)
%% ==============================================================================
function experiment_09()
    tStart = tic;
    fprintf('==================================================================\n');
    fprintf('STARTING EXPERIMENT 09 MATLAB PIPELINE\n');
    fprintf('Department of Biomedical Engineering - Riphah International University\n');
    fprintf('==================================================================\n');

    fprintf('\n>>> STEP 1: Running Benchmark & Compound Morphological Operations...\n');
    example_01_morphology_benchmark();

    fprintf('\n>>> STEP 2: Running Task 9.1 (Structuring Element Geometry on Calvarium)...\n');
    task_9_1_se_geometry_comparison();

    fprintf('\n>>> STEP 3: Running Task 9.2 (SE Radius Sensitivity Sweep on Ventricles)...\n');
    task_9_2_radius_sensitivity_sweep();

    fprintf('\n>>> STEP 4: Running Task 9.3 (Order of Operations: Open-Close vs. Close-Open)...\n');
    task_9_3_order_of_operations();

    fprintf('\n>>> STEP 5: Running Task 9.4 (Morphological Boundary Extraction)...\n');
    task_9_4_morphological_boundaries();

    fprintf('\n>>> STEP 6: Running Task 9.5 (Automated Cortical Skull Stripping on Head CT)...\n');
    task_9_5_skull_stripping();

    elapsed = toc(tStart);
    fprintf('\n==================================================================\n');
    fprintf('EXPERIMENT 09 MATLAB PIPELINE COMPLETED IN %.2f SECONDS\n', elapsed);
    fprintf('All MAT-files, figures, and CSV tables successfully generated.\n');
    fprintf('==================================================================\n');
end
