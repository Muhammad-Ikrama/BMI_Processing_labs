%% Experiment 05 - Task 5.1: Discrete Gradient Kernel Construction & Directional Sensitivity
%% Directional Sobel Decomposition and HSV Color-Coded Orientation Mapping
%% Course: Medical Image Processing (B.Sc. Biomedical Engineering)
%% Faculty: Engr. Rana Talha Khalid | Riphah International University

function results = task_5_1()
    fprintf('======================================================================\n');
    fprintf('EXPERIMENT 05 - TASK 5.1: DIRECTIONAL GRADIENTS & HSV MAPPING (MATLAB)\n');
    fprintf('======================================================================\n');

    % Setup paths
    scriptDir = fileparts(mfilename('fullpath'));
    expDir = fileparts(scriptDir);
    imgPath = fullfile(expDir, 'Inputs', 'images', 'CT.jpg');
    if ~exist(imgPath, 'file')
        imgPath = fullfile(expDir, '..', '..', 'images', 'CT.jpg');
    end

    img = imread(imgPath);
    if size(img, 3) == 3; img = rgb2gray(img); end
    imgD = double(img);

    % Sobel kernels
    % Gx detects vertical edges (horizontal intensity change df/dx)
    Gx_kernel = [-1, 0, 1; -2, 0, 2; -1, 0, 1];
    % Gy detects horizontal edges (vertical intensity change df/dy)
    Gy_kernel = [-1, -2, -1; 0, 0, 0; 1, 2, 1];

    Gx = imfilter(imgD, Gx_kernel, 'replicate');
    Gy = imfilter(imgD, Gy_kernel, 'replicate');

    mag = sqrt(Gx.^2 + Gy.^2);
    % Angle in radians [-pi, pi], map to [0, pi]
    theta = atan2(Gy, Gx);
    theta_deg = mod(rad2deg(theta), 180);

    % Build HSV direction map
    [H, W] = size(img);
    hsvMap = zeros(H, W, 3);
    hsvMap(:, :, 1) = theta_deg / 180.0; % Hue [0, 1]
    hsvMap(:, :, 2) = 1.0;               % Saturation

    % Value: normalized magnitude
    p98 = prctile(mag(:), 98);
    normMag = min(mag / p98, 1.0);
    hsvMap(:, :, 3) = normMag;

    rgbOrientation = hsv2rgb(hsvMap);

    % Save output images
    outDir = fullfile(expDir, 'Outputs', 'MATLAB');
    if ~exist(outDir, 'dir'); mkdir(outDir); end
    imwrite(uint8(min(abs(Gx), 255)), fullfile(outDir, 'exp05_task_5_1_Gx.png'));
    imwrite(uint8(min(abs(Gy), 255)), fullfile(outDir, 'exp05_task_5_1_Gy.png'));
    imwrite(uint8(min(mag, 255)), fullfile(outDir, 'exp05_task_5_1_magnitude.png'));
    imwrite(rgbOrientation, fullfile(outDir, 'exp05_task_5_1_hsv_orientation.png'));

    results.max_Gx = max(abs(Gx(:)));
    results.max_Gy = max(abs(Gy(:)));
    results.max_mag = max(mag(:));

    fprintf('[METRIC] Max Gx: %.2f | Max Gy: %.2f | Max Magnitude: %.2f\n', ...
        results.max_Gx, results.max_Gy, results.max_mag);
    fprintf('[CLINICAL ANATOMY INSIGHT]\n');
    fprintf(' - Gx highlights VERTICAL edges: Sagittal suture, lateral skull bone, falx cerebri.\n');
    fprintf(' - Gy highlights HORIZONTAL edges: Superior cranial vault, transverse sinuses, horizontal ventricles.\n');

    % 4-Panel Visualization
    fig = figure('Visible', 'off', 'Units', 'pixels', 'Position', [100, 100, 1200, 950]);

    % Gx
    subplot(2, 2, 1);
    imagesc(abs(Gx));
    colormap(gca, 'hot');
    colorbar;
    axis image off;
    title({'Horizontal Gradient |Gx|', '(Highlights Vertical Anatomical Edges)'}, ...
        'FontWeight', 'bold', 'FontSize', 11);

    % Gy
    subplot(2, 2, 2);
    imagesc(abs(Gy));
    colormap(gca, 'hot');
    colorbar;
    axis image off;
    title({'Vertical Gradient |Gy|', '(Highlights Horizontal Anatomical Edges)'}, ...
        'FontWeight', 'bold', 'FontSize', 11);

    % Magnitude
    subplot(2, 2, 3);
    imagesc(mag);
    colormap(gca, 'parula');
    colorbar;
    axis image off;
    title({'Combined Gradient Magnitude |\\nabla f|', '|\\nabla f| = \\surd(Gx^2 + Gy^2)'}, ...
        'FontWeight', 'bold', 'FontSize', 11);

    % HSV Orientation
    subplot(2, 2, 4);
    imshow(rgbOrientation);
    axis image off;
    title({'HSV Color-Coded Gradient Orientation Map', 'Hue: Direction \\theta (0-180°) | Value: Magnitude'}, ...
        'FontWeight', 'bold', 'FontSize', 11);

    sgtitle({'Task 5.1: Directional Gradient Decomposition & Orientation Mapping in Head CT', ...
             'Differential Spatial Calculus with Orthogonal Sobel Operators (MATLAB)'}, ...
        'FontWeight', 'bold', 'FontSize', 13);

    figDir = fullfile(expDir, 'Figures');
    if ~exist(figDir, 'dir'); mkdir(figDir); end
    figPath = fullfile(figDir, 'exp05_task_5_1_directional_gradients_m.png');
    exportgraphics(fig, figPath, 'Resolution', 300);
    close(fig);
    fprintf('[SUCCESS] Figure saved to %s\n', figPath);
end
