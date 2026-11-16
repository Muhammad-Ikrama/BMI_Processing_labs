%% ==============================================================================
%% EXPERIMENT 06: MASTER MATLAB PIPELINE EXECUTION SCRIPT
%% Frequency-Domain Filtering of Medical Images Using the 2-D Fourier Transform
%% Course: Medical Image Processing | Riphah International University
%% Faculty: Engr. Rana Talha Khalid
%% ==============================================================================

function experiment_06()
    t_start = tic;
    fprintf('================================================================================\n');
    fprintf('STARTING EXPERIMENT 06: FREQUENCY-DOMAIN FILTERING MASTER PIPELINE (MATLAB)\n');
    fprintf('Riphah International University | Department of Biomedical Engineering\n');
    fprintf('================================================================================\n\n');

    fprintf('>>> STEP 1: Running Example 01 (Baseline Frequency Filtering Pipeline)...\n');
    example_01();

    fprintf('\n>>> STEP 2: Running Task 6.1 (2-D DFT & Centered Magnitude Spectrum)...\n');
    task_6_1();

    fprintf('\n>>> STEP 3: Running Task 6.2 (Gibbs Ringing & ILPF Sensitivity Sweep)...\n');
    task_6_2();

    fprintf('\n>>> STEP 4: Running Task 6.3 (Butterworth LP Filter Order Sweep)...\n');
    task_6_3();

    fprintf('\n>>> STEP 5: Running Task 6.4 (Gaussian Low-Pass vs High-Pass Contrast)...\n');
    task_6_4();

    fprintf('\n>>> STEP 6: Running Task 6.5 (Multi-Filter Benchmarking & Diagnostic Report)...\n');
    task_6_5();

    elapsed = toc(t_start);
    fprintf('\n================================================================================\n');
    fprintf('EXPERIMENT 06 MASTER MATLAB PIPELINE COMPLETED SUCCESSFULLY IN %.2f SECONDS\n', elapsed);
    fprintf('All figures, tables, and filtered outputs generated and verified.\n');
    fprintf('================================================================================\n');
end
