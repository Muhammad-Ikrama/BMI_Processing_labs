%% Task 13.3: Directional Anisotropy Analysis on Chest X-Ray
% Experiment 13: Texture Feature Extraction from Medical Images Using GLCM
% Author: Muhammad Ikrama (Reg ID: 60140)

function results = task_13_3_directional_anisotropy()
    fprintf('================================================================================\n');
    fprintf('TASK 13.3: DIRECTIONAL ANISOTROPY ANALYSIS ON CHEST X-RAY (MATLAB)\n');
    fprintf('================================================================================\n');
    
    xray = imread(fullfile('..', 'Inputs', 'images', 'Chest_Xray.png'));
    if size(xray, 3) == 3; xray = rgb2gray(xray); end
    
    % Extract 64x64 ROIs
    roiRib = xray(141:204, 81:144);
    roiLung = xray(261:324, 281:344);
    
    % Offsets for 0 deg and 90 deg at d=1
    offset0 = [0 1];
    offset90 = [-1 0];
    
    % Rib GLCM
    glcmRib0 = graycomatrix(roiRib, 'NumLevels', 16, 'GrayLimits', [0 255], 'Offset', offset0, 'Symmetric', true);
    glcmRib90 = graycomatrix(roiRib, 'NumLevels', 16, 'GrayLimits', [0 255], 'Offset', offset90, 'Symmetric', true);
    sRib0 = graycoprops(glcmRib0, {'Contrast', 'Homogeneity', 'Correlation'});
    sRib90 = graycoprops(glcmRib90, {'Contrast', 'Homogeneity', 'Correlation'});
    
    % Lung GLCM
    glcmLung0 = graycomatrix(roiLung, 'NumLevels', 16, 'GrayLimits', [0 255], 'Offset', offset0, 'Symmetric', true);
    glcmLung90 = graycomatrix(roiLung, 'NumLevels', 16, 'GrayLimits', [0 255], 'Offset', offset90, 'Symmetric', true);
    sLung0 = graycoprops(glcmLung0, {'Contrast', 'Homogeneity', 'Correlation'});
    sLung90 = graycoprops(glcmLung90, {'Contrast', 'Homogeneity', 'Correlation'});
    
    ratioRib = sRib90.Contrast / sRib0.Contrast;
    ratioLung = sLung90.Contrast / sLung0.Contrast;
    
    fprintf('%-38s | %-8s | %-9s | %-9s | %-8s\n', 'Anatomical ROI', 'Angle', 'Contrast', 'Homogen.', 'Correl.');
    fprintf('---------------------------------------------------------------------------\n');
    fprintf('%-38s | %-8s | %-9.4f | %-9.4f | %-8.4f\n', 'Posterior Ribs ROI (Directional Bone)', '0 deg', sRib0.Contrast, sRib0.Homogeneity, sRib0.Correlation);
    fprintf('%-38s | %-8s | %-9.4f | %-9.4f | %-8.4f\n', 'Posterior Ribs ROI (Directional Bone)', '90 deg', sRib90.Contrast, sRib90.Homogeneity, sRib90.Correlation);
    fprintf('  --> Directional Anisotropy Ratio (C90 / C0): %.2fx\n\n', ratioRib);
    
    fprintf('%-38s | %-8s | %-9.4f | %-9.4f | %-8.4f\n', 'Lung Parenchyma ROI (Isotropic Tissue)', '0 deg', sLung0.Contrast, sLung0.Homogeneity, sLung0.Correlation);
    fprintf('%-38s | %-8s | %-9.4f | %-9.4f | %-8.4f\n', 'Lung Parenchyma ROI (Isotropic Tissue)', '90 deg', sLung90.Contrast, sLung90.Homogeneity, sLung90.Correlation);
    fprintf('  --> Directional Anisotropy Ratio (C90 / C0): %.2fx\n', ratioLung);
    
    results = struct('sRib0', sRib0, 'sRib90', sRib90, 'sLung0', sLung0, 'sLung90', sLung90, 'ratioRib', ratioRib, 'ratioLung', ratioLung);
    fprintf('>>> Task 13.3 Analysis Complete.\n');
end
