%% ==============================================================================
%% EXPERIMENT 08: TASK 8.2 - ITERATIVE ISODATA CONVERGENCE (MATLAB)
%% ==============================================================================
function df = task_8_2_isodata_convergence()
    baseDir = fileparts(fileparts(mfilename('fullpath')));
    imgDir = fullfile(baseDir, 'Inputs', 'images');
    outDir = fullfile(baseDir, 'Outputs', 'MATLAB');
    tabDir = fullfile(baseDir, 'Tables');
    if ~exist(outDir, 'dir'); mkdir(outDir); end
    if ~exist(tabDir, 'dir'); mkdir(tabDir); end

    modalities = {
        'Brain MRI', fullfile(imgDir, 'Brain_MRI.png');
        'Chest X-ray', fullfile(imgDir, 'Chest_Xray.png')
    };

    t0Guesses = [20, 128, 230];
    tol = 0.05;
    maxIter = 50;

    modList = {};
    t0List = [];
    tIsoList = [];
    tOtsuList = [];
    iterList = [];
    deltaList = [];
    diceList = [];

    f = figure('Visible', 'off', 'Position', [100, 100, 1400, 700]);
    colors = {[0.15, 0.39, 0.92], [0.09, 0.64, 0.29], [0.86, 0.15, 0.15]};

    fprintf('==================================================================\n');
    fprintf('TASK 8.2: ITERATIVE ISODATA VS. OTSU CONVERGENCE BENCHMARK (MATLAB)\n');
    fprintf('==================================================================\n');

    for m = 1:size(modalities, 1)
        modName = modalities{m, 1};
        imgPath = modalities{m, 2};

        img = imread(imgPath);
        if size(img, 3) == 3; img = rgb2gray(img); end
        if size(img, 1) ~= 512 || size(img, 2) ~= 512
            img = imresize(img, [512, 512]);
        end

        % Otsu reference
        levelOtsu = graythresh(img);
        tOtsu = double(round(levelOtsu * 255));
        maskOtsu = imbinarize(img, levelOtsu);

        fprintf('\n--- %s (Otsu T* = %.1f) ---\n', modName, tOtsu);
        fprintf('%-12s | %-12s | %-11s | %-13s | %-10s\n', 'Initial T0', 'Final T_iso', 'Iterations', 'Diff vs Otsu', 'Dice (DSC)');
        fprintf('-----------------------------------------------------------------\n');

        subplot(2, 3, (m - 1) * 3 + 1); hold on;

        for g = 1:length(t0Guesses)
            T0 = t0Guesses(g);
            T = double(T0);
            traj = T;

            for it = 1:maxIter
                bg = img(img <= T);
                fg = img(img > T);
                muBg = mean(double(bg)); if isempty(bg); muBg = 0; end
                muFg = mean(double(fg)); if isempty(fg); muFg = 255; end
                TNext = 0.5 * (muBg + muFg);
                traj(end+1) = TNext; %#ok<AGROW>
                if abs(TNext - T) < tol
                    T = TNext;
                    numIters = it;
                    break;
                end
                T = TNext;
                numIters = it;
            end

            maskIso = img > T;
            inter = sum(maskIso(:) & maskOtsu(:));
            denom = sum(maskIso(:)) + sum(maskOtsu(:));
            dsc = (2.0 * inter) / denom;
            diffOtsu = abs(T - tOtsu);

            fprintf('%-12d | %-12.2f | %-11d | %-13.2f | %-10.4f\n', T0, T, numIters, diffOtsu, dsc);

            modList{end+1} = modName; %#ok<AGROW>
            t0List(end+1, 1) = T0; %#ok<AGROW>
            tIsoList(end+1, 1) = round(T, 2); %#ok<AGROW>
            tOtsuList(end+1, 1) = round(tOtsu, 2); %#ok<AGROW>
            iterList(end+1, 1) = numIters; %#ok<AGROW>
            deltaList(end+1, 1) = round(diffOtsu, 2); %#ok<AGROW>
            diceList(end+1, 1) = round(dsc, 4); %#ok<AGROW>

            plot(0:(length(traj)-1), traj, '-o', 'Color', colors{g}, 'LineWidth', 1.5, ...
                'DisplayName', sprintf('T0=%d (%d iters)', T0, numIters));
        end

        yline(tOtsu, '--k', sprintf('Otsu T*=%.1f', tOtsu), 'LineWidth', 1.8);
        title(sprintf('%s: Isodata Convergence', modName), 'FontWeight', 'bold');
        xlabel('Iteration k'); ylabel('Threshold T_k');
        legend('Location', 'best'); grid on;

        subplot(2, 3, (m - 1) * 3 + 2);
        imshow(img); title(sprintf('%s (Input)', modName), 'FontWeight', 'bold');

        subplot(2, 3, (m - 1) * 3 + 3);
        imshow(img > tIsoList(end)); title(sprintf('%s Mask (T=%.1f)', modName, tIsoList(end)), 'FontWeight', 'bold');
    end

    df = table(modList', t0List, tIsoList, tOtsuList, iterList, deltaList, diceList, ...
        'VariableNames', {'Modality', 'T0_Guess', 'Final_T_iso', 'Otsu_T_star', 'Iterations', 'Delta_T', 'Dice_vs_Otsu'});
    csvPath = fullfile(tabDir, 'exp08_task_8_2_isodata_convergence_matlab.csv');
    writetable(df, csvPath);
    fprintf('\n[SAVED] Task 8.2 table: %s\n', csvPath);

    figPath = fullfile(outDir, 'exp08_task_8_2_isodata_convergence_m.png');
    saveas(f, figPath);
    close(f);
    fprintf('[SAVED] Task 8.2 figure: %s\n', figPath);
end
