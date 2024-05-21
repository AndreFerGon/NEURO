%% DATA IMPORT
clear, close all, clc

fs = 250;

% a mixed signal with 10s rest + 10s 8Hz sti + 10s rest + 10s 12Hz stim

% load("Data/mixed_signal_16_24.mat");
% eeg_data = mixed_signal;

% load("Data/S202007965_21_Protocol#3_Trial3.csv");
% eeg_data = S202007965_21_Protocol_3_Trial3(:, 2:4);

flick_f = 16;
data = table2array(readtable(['Data/Protocol#1_202007965_21_Male_', num2str(flick_f), 'Hz.csv']));
data16Hz = data(15*250:25*250, 2:4);

flick_f = 24;
data = table2array(readtable(['Data/Protocol#1_202007965_21_Male_', num2str(flick_f), 'Hz.csv']));
data24Hz = data(15*250:25*250, 2:4);

eeg_data = [data16Hz; data24Hz; data16Hz; data24Hz; data16Hz; data24Hz];

% load("lastAcquisition.mat")
% % eeg_data = eeg_raw_arr(2:9, :);
% eeg_data = eeg_raw_arr(3:5, :)'; % 10s rest, 13s 7.2Hz, 28s rest, 
% % 20s 8Hz, 20s rest, 26s 9Hz, 24s rest, 20s 9.6Hz, 20s rest, 20s 12Hz, 9s rest

t = 0:1/fs:(size(eeg_data, 1)/250 - 1/fs);

% % Plot the simulated EEG data
% figure;
% plot(t, eeg_data);
% xlabel('Time (s)');
% ylabel('Amplitude');
% title('EEG Data from Oz electrode');

window_size = 5.5; % in seconds
step_size = 1; % in seconds
threshold = 0.24;
filter_crop = 1.5;

%% Initializing variables for using CCA;

refFreq = [7.2 8 9 9.6 12];
time = window_size - 1.5; % Seconds;

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


host = 'localhost';  % Use 'localhost' or '127.0.0.1' if running on the same machine
port = 12345;         % Port number on which Python server is listening
% 
try
    tto = tcpclient(host, port);
catch ME
    error('Failed to create TCP connection: %s', ME.message);
end


% Initialize figure for real-time plotting
figure;
subplot(1,2,1)
h1 = plot(zeros(1,2*fs), 'DisplayName', 'Channel O1'); % Initialize plot for Channel 1
hold on;
h2 = plot(zeros(1,2*fs) - 200, 'DisplayName', 'Channel Oz'); % Initialize plot for Channel 2 with offset
h3 = plot(zeros(1,2*fs) + 200, 'DisplayName', 'Channel O2'); % Initialize plot for Channel 3 with offset
hold off;
title(['Filtered EEG Data (' num2str(window_size-1.5) 's time window)']);
xlabel('Time (s)');
ylabel('Amplitude');
legend('show', 'Location','best');
%ylim([-100 100]);
%xlim([0 window_size]) % Set initial x-axis limits
%set(gca, 'XTick', 0:1:window_size) % Set x-axis ticks every second

subplot(1,2,2)
h4 = plot(zeros(1,2*fs), 'DisplayName', 'Channel O1'); % Initialize plot for PSD of Channel 1
hold on;
h5 = plot(zeros(1,2*fs), 'DisplayName', 'Channel Oz'); % Initialize plot for PSD of Channel 2
h6 = plot(zeros(1,2*fs), 'DisplayName', 'Channel O2'); % Initialize plot for PSD of Channel 3
hold off;
title('Raw EEG Data FFT');
xlabel('Frequency (Hz)');
ylabel('Power');
xlim([0 50]) % Set initial x-axis limits
legend('show');

i_segment = 0;
filtered_window = zeros(1, 2*fs);

counter = 0;
ind=0;
prev_ind=0;

cca_vector = [];

while true
    i_segment = i_segment + 1;
    pause(step_size) % Wait for step_size seconds
    
    % Generate data for the current window
    start_idx = fix(max(1, 1 + (i_segment-1)*step_size*fs));
    end_idx = fix(min(length(eeg_data), start_idx + window_size*fs));
    segment_data = eeg_data(start_idx:end_idx, :);
    t_segment = t(start_idx:end_idx-1.5*fs);

    % Apply filters
    filtered_window = filter(low_b, low_a, segment_data, [], 1);
    filtered_window = filter(high_b, high_a, filtered_window, [], 1);
    filtered_window = filter(notch_b, notch_a, filtered_window, [], 1);
    filtered_window = filtered_window(250*filter_crop+1:end, :);

    % Update plot with offsets
    set(h1, 'XData', t_segment, 'YData', filtered_window(:, 1));
    set(h2, 'XData', t_segment, 'YData', filtered_window(:, 2) - 200);
    set(h3, 'XData', t_segment, 'YData', filtered_window(:, 3) + 200);
    xlim([t_segment(1) t_segment(end)]);
    
    % Calculate PSD
    [p1, ~] = periodogram(filtered_window(:, 1), [], [], fs);
    [p2, ~] = periodogram(filtered_window(:, 2), [], [], fs);
    [p3, f] = periodogram(filtered_window(:, 3), [], [], fs);

    % Update PSD plot
    set(h4, 'XData', f, 'YData', p1);
    set(h5, 'XData', f, 'YData', p2);
    set(h6, 'XData', f, 'YData', p3);
    xlim([4 28]);
    
    drawnow;

    prev_ind = ind;
    for j = 1:classNum
        [~, ~, corr] = canoncorr(filtered_window, Y{j}');
        r(j) = max(corr);
    end

    c

    [m, ind] = max(r);
    
    if(m>threshold && prev_ind==ind)
        counter = counter+1;
    else
        counter = 0;
    end

    if(m>threshold)
     % fprintf('SSVEP Frequency: %d Hz (canoncorr = %f) \n', refFreq(ind), m);
    else
     %fprintf('Rest state \n');
    end

    try
        if (counter == 3)                 
            % Send random integer numbers every second

            if refFreq(ind) == 7.2
                message = sprintf('%i', 0);                    
            elseif refFreq(ind) == 8
                message = sprintf('%i', 1);
            elseif refFreq(ind) == 9
                message = sprintf('%i', 2);
            elseif refFreq(ind) == 9.6
                message = sprintf('%i', 3);
            elseif refFreq(ind) == 12
                message = sprintf('%i', 4);
            end      
            fprintf('CLASS DETECTED: %d Hz  \n', refFreq(ind));
            currentTime = datetime('now', 'Format', 'HH:mm:ss.SSS');
            disp(['Current time: ', char(currentTime)]);

            counter = 0;
        end

        % Send the message over TCP/IP
        % write(tto, message);  % Send as characters
        
        % Display the sent message (optional)
        % disp(['Frequency: ', num2str(message)]);

    catch ME
        disp(['Error occurred: ', ME.message]);
        % if exist('tto', 'var') && isvalid(tto)
        %     delete(tto);  % Close and delete the tcpclient object on error
        % end

    end

end

