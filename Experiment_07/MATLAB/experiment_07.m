%% ==============================================================================
%% EXPERIMENT 07 - MASTER PIPELINE EXECUTION SCRIPT (MATLAB)
%% Image Sharpening of Medical Images Using High-Boost Filtering and Unsharp Masking
%% Course: Medical Image Processing | Riphah International University
%% Faculty: Engr. Rana Talha Khalid
%% ==============================================================================

function experiment_07()
    tStart = tic;
    fprintf('================================================================================\n');
    fprintf('STARTING EXPERIMENT 07: IMAGE SHARPENING & HIGH-BOOST MASTER MATLAB PIPELINE\n');
    fprintf('Riphah International University | Department of Biomedical Engineering\n');
    fprintf('================================================================================\n\n');

    fprintf('>>> STEP 1: Running Example 01 (Baseline Sharpening & Gradient Benchmark)...\n');
    t0 = tic;
    example_01();
    fprintf('    Completed in %.2f s\n\n', toc(t0));

    fprintf('>>> STEP 2: Running Task 7.1 (High-Boost Sweep & Dynamic Range Clipping)...\n');
    t0 = tic;
    task_7_1();
    fprintf('    Completed in %.2f s\n\n', toc(t0));

    fprintf('>>> STEP 3: Running Task 7.2 (Smoothing Kernel Blur & Mask Bandwidth)...\n');
    t0 = tic;
    task_7_2();
    fprintf('    Completed in %.2f s\n\n', toc(t0));

    fprintf('>>> STEP 4: Running Task 7.3 (1D Transect & Mach Band Measurements)...\n');
    t0 = tic;
    task_7_3();
    fprintf('    Completed in %.2f s\n\n', toc(t0));

    fprintf('>>> STEP 5: Running Task 7.4 (Noise Amplification in Low-Dose Scans)...\n');
    t0 = tic;
    task_7_4();
    fprintf('    Completed in %.2f s\n\n', toc(t0));

    fprintf('>>> STEP 6: Running Task 7.5 (Clinical ROIs & Master Diagnostic Report)...\n');
    t0 = tic;
    task_7_5();
    fprintf('    Completed in %.2f s\n\n', toc(t0));

    total_time = toc(tStart);
    fprintf('================================================================================\n');
    fprintf('EXPERIMENT 07 MASTER MATLAB PIPELINE COMPLETED SUCCESSFULLY IN %.2f s\n', total_time);
    fprintf('All figures (_m.png), tables, and sharpened outputs generated and verified.\n');
    fprintf('================================================================================\n');
end
