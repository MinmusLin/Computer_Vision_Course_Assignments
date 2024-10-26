% Define points as (x, y) pairs
points = [-2, 0; 0, 0.9; 2, 2.0; 3, 6.5; 4, 2.9; 5, 8.8; 6, 3.95; 8, 5.03; 10, 5.97; 12, 7.1; 13, 1.2; 14, 8.2; 16, 8.5; 18, 10.1];

% Parameters for RANSAC
maxIter = 5000;       % Maximum number of iterations
threshold = 0.5;      % Distance threshold for inliers
bestFit = [];         % Best line model found
bestInliersCount = 0; % Number of inliers for the best model

% RANSAC algorithm
for i = 1:maxIter
    % Randomly select 2 points to create a line model
    sampleIdx = randperm(size(points, 1), 2);
    x1 = points(sampleIdx(1), 1);
    y1 = points(sampleIdx(1), 2);
    x2 = points(sampleIdx(2), 1);
    y2 = points(sampleIdx(2), 2);

    % Skip iteration if the two points have the same x-value (vertical line)
    if x2 - x1 == 0
        continue;
    end

    % Calculate the slope (m) and y-intercept (b) of the line
    m = (y2 - y1) / (x2 - x1);
    b = y1 - m * x1;

    % Compute distances of all points from the line
    distances = abs(m * points(:, 1) - points(:, 2) + b) / sqrt(m^2 + 1);

    % Identify inliers as points whose distances are below the threshold
    inliers = distances < threshold;
    inliersCount = sum(inliers);

    % Update the best model if more inliers are found
    if inliersCount > bestInliersCount
        bestInliersCount = inliersCount;
        bestFit = [m, b];
    end
end

% Output the best line model found
fprintf('Best fit line: y = %.2fx + %.2f\n', bestFit(1), bestFit(2));

% Visualization of the points and the fitted line
figure;
plot(points(:, 1), points(:, 2), 'bo', 'MarkerSize', 8, 'DisplayName', 'Data Points');
hold on;

% Generate line points using the best fit model
xFit = linspace(min(points(:, 1)), max(points(:, 1)), 100);
yFit = bestFit(1) * xFit + bestFit(2);
plot(xFit, yFit, 'r-', 'LineWidth', 2, 'DisplayName', 'Fitted Line (RANSAC)');

% Label the axes and add title and legend
xlabel('x');
ylabel('y');
title('RANSAC Line Fitting');
legend('show');
grid on;
hold off;