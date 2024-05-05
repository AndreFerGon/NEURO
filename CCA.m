%% Initializing variables for using CCA;
refFreq = [60/5, 60/7, 60/9, 60/11];
time = 4; % Seconds;
classNum = 5; % Add one more class for "rest"
trialNum = 1;
loss = 0;

t = 0:1/fs:time;

Y = cell(1, classNum);
r = zeros(1, classNum);

% Generate reference signals for each class
for i = 1:classNum
    if i <= classNum - 1
        ref = 2*pi*refFreq(i)*t;
        Y{i} = [sin(ref); cos(ref); sin(ref*2); cos(ref*2)];
    else
        % For the "rest" class, the reference signal can be anything, like random noise
        Y{i} = randn(4, length(t));
    end
end

%% Analysing SSVEP using CCA in single trials
for i = 1:trialNum
    data = squeeze(smt.x(:, i, :));
    for j = 1:classNum
        [~, ~, corr] = canoncorr(data, Y{j}');
        r(j) = max(corr);
    end
    [~, ind] = max(r);
    
    if ind == classNum
        fprintf('Trial %d: No control\n', i);
    else
        fprintf('Trial %d: Class %d\n', i, ind);
    end
    
    if ~smt.y_logic(ind, i)
        loss = loss + 1;
    end
end
