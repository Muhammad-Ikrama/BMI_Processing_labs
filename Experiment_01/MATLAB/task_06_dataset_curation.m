function task_06_dataset_curation()
% Experiment 01 - Task 6: Multi-Modal and Longitudinal Patient Dataset Identification & Curation
% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
% Faculty: Engr. Rana Talha Khalid | Department of Biomedical Engineering, Riphah International University

baseDir = fileparts(fileparts(mfilename('fullpath')));
dataDir = fullfile(baseDir, 'lab 1 dataset');

dcmFiles = [dir(fullfile(dataDir, '*.dcm')); dir(fullfile(dataDir, '*.DCM'))];

fprintf('================================================================================\n');
fprintf('STUDENT LAB TASK 6: MULTI-MODAL & LONGITUDINAL PATIENT DATASET CURATION (MATLAB)\n');
fprintf('================================================================================\n');
fprintf('Scanning DICOM Dataset Directory: %s\n\n', dataDir);
fprintf('%-20s %-15s %-10s %-12s %-12s %-15s\n', 'Filename', 'PatientID', 'Modality', 'Dimensions', 'PixelSpacing', 'StudyDate');
fprintf('%s\n', repmat('-', 1, 90));

for i = 1:length(dcmFiles)
    fname = dcmFiles(i).name;
    fpath = fullfile(dataDir, fname);
    try
        info = dicominfo(fpath);

        pid = 'N/A'; if isfield(info, 'PatientID'), pid = char(info.PatientID); end
        mod = 'Unknown'; if isfield(info, 'Modality'), mod = char(info.Modality); end
        sdate = 'N/A'; if isfield(info, 'StudyDate'), sdate = char(info.StudyDate); end
        dims = sprintf('%dx%d', info.Rows, info.Columns);
        
        spacing = 'N/A';
        if isfield(info, 'PixelSpacing')
            spacing = sprintf('[%.3f,%.3f]', info.PixelSpacing(1), info.PixelSpacing(2));
        end

        fprintf('%-20s %-15s %-10s %-12s %-12s %-15s\n', fname, pid, mod, dims, spacing, sdate);
    catch ME
        fprintf('%-20s ERROR: %s\n', fname, ME.message);
    end
end

fprintf('%s\n', repmat('-', 1, 90));

fprintf('\n=== CLINICAL ANALYSIS & OPEN DATA REPOSITORIES ===\n');
fprintf('1. Patient Identity Verification:\n');
fprintf('   Header tags (PatientID, PatientName) verify multi-modality alignment for identical clinical subjects.\n');
fprintf('2. Open Repositories for Longitudinal & Multi-Modal Imaging:\n');
fprintf('   - TCIA (The Cancer Imaging Archive): Longitudinal CT/PET-CT datasets (RIDER, TCGA).\n');
fprintf('   - ADNI (Alzheimer''s Disease Neuroimaging Initiative): Long-term MRI & PET brain tracking.\n');
fprintf('   - BraTS: Multi-parametric MRI co-registered volumes (T1, T1-Gd, T2, FLAIR).\n');
fprintf('   - OASIS: Open Access Series of Imaging Studies for neurodevelopment & dementia.\n');
fprintf('3. Downstream Clinical Application:\n');
fprintf('   - Experiment 12: Spatial Image Registration (rigid / affine matrix transformation).\n');
fprintf('   - Experiment 16: Multi-Modal Fusion (overlaying functional PET onto anatomical CT/MRI).\n');
end
