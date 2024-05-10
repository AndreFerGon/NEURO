%% Load trials
clear, clc, close all

load('stim_16Hz_trial1_Oz_data.mat');
signal_16Hz_trial1 = trial_signal;

load('stim_16Hz_trial3_Oz_data.mat');
signal_16Hz_trial3 = trial_signal;

load('stim_16Hz_trial7_Oz_data.mat');
signal_16Hz_trial7 = trial_signal;
       
load('stim_24Hz_trial1_Oz_data.mat');
signal_24Hz_trial1 = trial_signal;

load('stim_24Hz_trial2_Oz_data.mat');
signal_24Hz_trial2 = trial_signal;

load('stim_24Hz_trial3_Oz_data.mat');
signal_24Hz_trial3 = trial_signal;

load('stim_24Hz_trial8_Oz_data.mat');
signal_24Hz_trial8 = trial_signal;

load('stim_36Hz_trial5_Oz_data.mat');
signal_36Hz_trial5 = trial_signal;

load('stim_36Hz_trial7_Oz_data.mat');
signal_36Hz_trial7 = trial_signal;

load('stim_36Hz_trial8_Oz_data.mat');
signal_36Hz_trial8 = trial_signal;

clear trial_signal


%% Initializing variables for using CCA;
refFreq = [8 12 18];
time = 4; % Seconds;
fs= 250;
classNum = 3; 
trialNum = 1;
loss = 0;

t = 0:1/fs:(time - 1/fs);

Y = cell(1, classNum);
r = zeros(1, classNum);

% Generate reference signals for each class
for i = 1:classNum
    ref = 2*pi*refFreq(i)*t;
    Y{i} = [sin(ref); cos(ref); sin(ref*2); cos(ref*2)];
end

%% Analysing SSVEP using CCA in single trials
for i = 1:trialNum
    data = signal_36Hz_trial8;
    for j = 1:classNum
        [~, ~, corr] = canoncorr(data, Y{j}');
        r(j) = max(corr);
    end
    [~, ind] = max(r);
    

    fprintf('Trial %d: SSVEP Frequency: %d Hz\n', i, refFreq(ind));

    
    % if ~smt.y_logic(ind, i)
    %     loss = loss + 1;
    % end
end
