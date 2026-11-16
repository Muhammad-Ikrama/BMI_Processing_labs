%% ==============================================================================
%% EXPERIMENT 09: TASK 9.1 - STRUCTURING ELEMENT GEOMETRY COMPARISON (MATLAB)
%% ==============================================================================
function df = task_9_1_se_geometry_comparison()
    baseDir = fileparts(fileparts(mfilename('fullpath')));
    imgPath = fullfile(baseDir, 'Inputs', 'images', 'Head_CT.png');
    outDir = fullfile(baseDir, 'Outputs', 'MATLAB');
    tabDir = fullfile(baseDir, 'Tables');
    if ~exist(outDir, 'dir'); mkdir(outDir); end
    if ~exist(tabDir, 'dir'); mkdir(tabDir); end

    ct = imread(imgPath);
    if size(ct, 3) == 3; ct = rgb2gray(ct); end
    if size(ct, 1) ~= 512 || size(ct, 2) ~= 512
        ct = imresize(ct, [512, 512]);
    end

    skullRaw = ct > 118;

    % 7x7 Structuring Elements
    seSquare = strel('square', 7);
    seCross = strel('diamond', 3); % 7x7 cross/diamond
    seDisk = strel('disk', 3, 0);  % 7x7 disk

    elements = {
        'Square (8-connected Box)', seSquare, 'Square';
        'Cross (4-connected Diamond)', seCross, 'Cross';
        'Disk (Isotropic Ellipse)', seDisk, 'Disk'
    };

    fprintf('==================================================================\n');
    fprintf('TASK 9.1: STRUCTURING ELEMENT GEOMETRY COMPARISON (MATLAB)\n');
    fprintf('==================================================================\n');
    fprintf('%-28s | %-9s | %-11s | %-11s | %-11s\n', 'SE Geometry', 'Active Px', 'Opened Area', 'Closed Area', 'Perimeter Px');
    fprintf('----------------------------------------------------------------------------------\n');

    names = {};
    shapes = {};
    activeList = [];
    opAreaList = [];
    clAreaList = [];
    perimList = [];
    openedMasks = cell(3, 1);

    for i = 1:size(elements, 1)
        name = elements{i, 1};
        se = elements{i, 2};
        tag = elements{i, 3};

        opMask = imopen(skullRaw, se);
        clMask = imclose(skullRaw, se);
        openedMasks{i} = opMask;

        % Morphological gradient for perimeter
        grad = imdilate(opMask, se) & ~imerode(opMask, se);
        perim = sum(grad(:));

        activePx = sum(se.Neighborhood(:));
        opArea = sum(opMask(:));
        clArea = sum(clMask(:));

        fprintf('%-28s | %-9d | %-11d | %-11d | %-11d\n', name, activePx, opArea, clArea, perim);

        names{end+1} = name; %#ok<AGROW>
        shapes{end+1} = tag; %#ok<AGROW>
        activeList(end+1, 1) = activePx; %#ok<AGROW>
        opAreaList(end+1, 1) = opArea; %#ok<AGROW>
        clAreaList(end+1, 1) = clArea; %#ok<AGROW>
        perimList(end+1, 1) = perim; %#ok<AGROW>
    end

    df = table(names', shapes', activeList, opAreaList, clAreaList, perimList, ...
        'VariableNames', {'SE_Geometry', 'SE_Shape', 'Active_Pixels_KxK', 'Opened_Area_Px', 'Closed_Area_Px', 'Boundary_Perimeter_Px'});
    csvPath = fullfile(tabDir, 'exp09_task_9_1_se_geometry_matlab.csv');
    writetable(df, csvPath);
    fprintf('\n[SAVED] Task 9.1 table: %s\n', csvPath);

    % Save Visual Figure with 80x80 zoom
    f = figure('Visible', 'off', 'Position', [100, 100, 1300, 700]);
    r = 71:150; c = 361:440;

    subplot(2, 4, 1); imshow(skullRaw); title('Raw Skull Mask', 'FontWeight', 'bold');
    subplot(2, 4, 2); imshow(openedMasks{1}); title('Opened: Square (7x7)', 'FontWeight', 'bold');
    subplot(2, 4, 3); imshow(openedMasks{2}); title('Opened: Cross (7x7)', 'FontWeight', 'bold');
    subplot(2, 4, 4); imshow(openedMasks{3}); title('Opened: Disk (7x7)', 'FontWeight', 'bold');

    subplot(2, 4, 5); imshow(skullRaw(r, c)); title('Raw Boundary Crop', 'FontWeight', 'bold');
    subplot(2, 4, 6); imshow(openedMasks{1}(r, c)); title('Square: Blocky Facets', 'FontWeight', 'bold', 'Color', [0.8, 0, 0]);
    subplot(2, 4, 7); imshow(openedMasks{2}(r, c)); title('Cross: Diamond Points', 'FontWeight', 'bold', 'Color', [0.8, 0, 0]);
    subplot(2, 4, 8); imshow(openedMasks{3}(r, c)); title('Disk: Smooth Curvature', 'FontWeight', 'bold', 'Color', [0, 0.6, 0]);

    figPath = fullfile(outDir, 'exp09_task_9_1_se_geometry_m.png');
    saveas(f, figPath);
    close(f);
    fprintf('[SAVED] Task 9.1 figure: %s\n', figPath);
end
