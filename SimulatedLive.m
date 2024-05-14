%% Simulate EEG Data

% Simulate EEG data
fs = 250; % Sampling frequency (Hz)
time = 10; % 10 seconds of data
t = 0:1/fs:(time - 1/fs);
freq_segments = [8.57, 12, 15, 10, 8.57]; % Frequencies for each segment (Hz)
amplitude = 50; % Amplitude of the simulated signal

% Initialize EEG data
eeg_data = zeros(size(t));

% Generate EEG signal with different frequencies for different segments
start_idx = 1;
for i = 1:length(freq_segments)
    freq = freq_segments(i);
    segment_t = t(start_idx:start_idx+length(t)/length(freq_segments)-1);
    segment_eeg_data = amplitude * sin(2*pi*freq*segment_t);
    eeg_data(start_idx:start_idx+length(segment_t)-1) = segment_eeg_data;
    start_idx = start_idx + length(segment_t);
end

% Add noise to the simulated EEG data
eeg_data = eeg_data + randn(size(eeg_data)) * 10;

% Plot the simulated EEG data
figure;
plot(t, eeg_data);
xlabel('Time (s)');
ylabel('Amplitude');
title('Simulated EEG Data');


%% Initializing variables for using CCA;
refFreq = [8.57 10 12 15];
time = 2; % Seconds;
fs= 250;
classNum = length(refFreq); 
%trialNum = 1;
loss = 0;

ref_t = 0:1/fs:(time);

Y = cell(1, classNum);
r = zeros(1, classNum);

% Generate reference signals for each class
for i = 1:classNum
    ref = 2*pi*refFreq(i)*ref_t;
    Y{i} = [sin(ref); cos(ref); sin(ref*2); cos(ref*2)];
end

%% Pre-processing filters

% Low-pass 40 Hz
order = 4; 
[low_b, low_a] = butter(order, 40/(fs/2), 'low');

% High-pass 1 Hz
order = 2; 
[high_b, high_a] = butter(order, 1/(fs/2), 'high');

% Notch-filter 50 Hz
order = 2; 
[notch_b, notch_a] = butter(order, [48 52]/(fs/2), 'stop');

%% Simulate Data Acquisition and Real-time Plotting

% Set parameters
window_size = 3; % in seconds
step_size = 0.2; % in seconds


% Initialize figure for real-time plotting
figure;
subplot(1,2,1)
h1 = plot(zeros(1,2*fs)); % Initialize plot
title('Raw EEG Data');
xlabel('Time (s)');
ylabel('Amplitude');
ylim([-100 100]);

subplot(1,2,2)
h2 = plot(zeros(1,2*fs)); % Initialize plot
title('Raw EEG Data FFT');
xlabel('Frequency (Hz)');
ylabel('Power');


i_segment = 0;
filtered_window = zeros(1, 2*fs);
while true
    i_segment = i_segment + 1;
    pause(step_size) % Wait for step_size seconds
    
    % Generate data for the current window
    start_idx = max(1, 1 + (i_segment-1)*step_size*fs);
    end_idx = min(length(eeg_data), start_idx + window_size*fs);
    segment_data = eeg_data(start_idx:end_idx);
    t_segment = t(start_idx:end_idx);

    filtered_window = filter(low_b, low_a, segment_data);
    filtered_window = filtfilt(high_b, high_a, filtered_window);
    filtered_window = filtfilt(notch_b, notch_a, filtered_window);

    filtered_window = filtered_window(250*1+1:end);

    % Update plot 
    set(h1, 'XData', t_segment, 'YData', segment_data);
    xlim([t_segment(1) t_segment(end)]);

    [p, f] = periodogram(segment_data, [], [], fs);
    set(h2, 'YData', p);
    xlim([0 50]);
    

    drawnow;

    for j = 1:classNum
        [~, ~, corr] = canoncorr(filtered_window', Y{j}');
        r(j) = max(corr);
    end
    [m, ind] = max(r);

    if(m>0.24)
     fprintf('SSVEP Frequency: %d Hz (canoncorr = %f) \n', refFreq(ind), m);
    end
    
    % % Check if the user pressed the escape key
    % if waitforbuttonpress == 1
    %     break;
    % end
end
