%% Task 13.1: Hand-Verified 4x4 GLCM Construction & Probability Normalization
% Experiment 13: Texture Feature Extraction from Medical Images Using GLCM
% Author: Muhammad Ikrama (Reg ID: 60140)

function P = task_13_1_synthetic_glcm()
    fprintf('================================================================================\n');
    fprintf('TASK 13.1: HAND-VERIFIED 4x4 GLCM CONSTRUCTION & NORMALIZATION (MATLAB)\n');
    fprintf('================================================================================\n');
    
    % Synthetic 4x4 image with Ng = 4 (values 0..3)
    I = [0 0 1 1;
         0 0 1 1;
         0 2 2 2;
         2 2 3 3];
    
    glcm_raw = graycomatrix(I, 'NumLevels', 4, 'GrayLimits', [0 3], 'Offset', [0 1], 'Symmetric', false);
    glcm_sym = graycomatrix(I, 'NumLevels', 4, 'GrayLimits', [0 3], 'Offset', [0 1], 'Symmetric', true);
    
    total_pairs = sum(glcm_sym, 'all');
    P = double(glcm_sym) / total_pairs;
    
    fprintf('\n1. Synthetic 4x4 Input Image (Ng = 4):\n');
    disp(I);
    fprintf('2. Raw Horizontal Count Matrix C (d=1, theta=0 deg, Non-Symmetric, Sum = %d):\n', sum(glcm_raw, 'all'));
    disp(glcm_raw);
    fprintf('3. Symmetric Count Matrix C_sym = C + C'' (Sum = %d):\n', sum(glcm_sym, 'all'));
    disp(glcm_sym);
    fprintf('4. Normalized Probability Matrix P(i,j) (Sum = %.6f):\n', sum(P, 'all'));
    disp(P);
    
    stats = graycoprops(glcm_sym, {'Contrast', 'Homogeneity', 'Energy', 'Correlation'});
    fprintf('Haralick Features:\n');
    fprintf('  Contrast: %.4f\n', stats.Contrast);
    fprintf('  Homogeneity: %.4f\n', stats.Homogeneity);
    fprintf('  Energy: %.4f\n', stats.Energy);
    
    % Entropy
    nz = P > 0;
    entropyVal = -sum(P(nz) .* log2(P(nz)));
    fprintf('  Entropy: %.4f bits\n', entropyVal);
    
    assert(abs(sum(P, 'all') - 1.0) < 1e-6, 'Normalization check failed!');
    fprintf('>>> Task 13.1 Verification Passed: Probability Matrix sums to 1.000000.\n');
end
