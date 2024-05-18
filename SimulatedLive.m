%% DATA IMPORT
clear, close all, clc

fs = 250;

% a mixed signal with 10s rest + 10s 8Hz sti + 10s rest + 10s 12Hz stim

% load("mixed_signal_16_24.mat");
% eeg_data = mixed_signal;
% t = 0:1/fs:(length(eeg_data)/250 - 1/fs);

% load("S202007965_21_Protocol#3_Trial3.csv")
% eeg_data = S202007965_21_Protocol_3_Trial3(250*0.5:end, 3);
% t = 0:1/fs:(length(eeg_data)/250 - 1/fs);

% Plot the simulated EEG data
figure;
plot(t, eeg_data);
xlabel('Time (s)');
ylabel('Amplitude');
title('EEG Data from Oz electrode');

window_size = 6.5; % in seconds
step_size = 1; % in seconds


%% Initializing variables for using CCA;

refFreq = [7.2 8 9 9.6 12];
time = window_size - 1.5; % Seconds;

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
h1 = plot(zeros(1,2*fs)); % Initialize plot
title(['Filtered EEG Data (' num2str(window_size-1.5) 's time window)']);
xlabel('Time (s)');
ylabel('Amplitude');
%ylim([-100 100]);
%xlim([0 window_size]) % Set initial x-axis limits
%set(gca, 'XTick', 0:1:window_size) % Set x-axis ticks every second

subplot(1,2,2)
h2 = plot(zeros(1,2*fs)); % Initialize plot
title('Raw EEG Data FFT');
xlabel('Frequency (Hz)');
ylabel('Power');
xlim([0 50]) % Set initial x-axis limits

i_segment = 0;
filtered_window = zeros(1, 2*fs);

counter = 0;

while true
    i_segment = i_segment + 1;
    pause(step_size) % Wait for step_size seconds
    
    % Generate data for the current window
    start_idx = max(1, 1 + (i_segment-1)*step_size*fs);
    end_idx = min(length(eeg_data), start_idx + window_size*fs);
    segment_data = eeg_data(start_idx:end_idx);
    t_segment = t(start_idx+1.5*fs:end_idx);


    filtered_window = filter(low_b, low_a, segment_data);
    filtered_window = filter(high_b, high_a, filtered_window);
    filtered_window = filter(notch_b, notch_a, filtered_window);

    filtered_window = filtered_window(250*1.5+1:end);

    % Update plot 
     %set(gca, 'XTick', t_segment(1):1:t_segment(end)) % Update x-axis ticks

    set(h1, 'XData', t_segment, 'YData', filtered_window);
    xlim([t_segment(1) t_segment(end)])
    

    [p, f] = periodogram(filtered_window, [], [], fs);

    set(h2, 'XData', f, 'YData', p);
    xlim([4 28]);
    
    drawnow;

    for j = 1:classNum
        [~, ~, corr] = canoncorr(filtered_window', Y{j}');
        r(j) = max(corr);
    end

    [m, ind] = max(r);
    prev_ind = ind;

    if(m>0.24 && prev_ind==ind)
        counter = counter+1;
    else
        counter = 0;
    end

    if(m>0.24)
     fprintf('SSVEP Frequency: %d Hz (canoncorr = %f) \n', refFreq(ind), m);
    end


        try
             if (counter == 4)                 
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
                fprintf(message)
                if isvalid(tto)
                    write(tto, message);  % Send as characters
                else
                    error('TCP connection is no longer valid.');
                end

                counter = 0;
             end
                
        
    catch ME
        disp(['Error occurred: ', ME.message]);
        if exist('tto', 'var') && isvalid(tto)
            delete(tto);  % Close and delete the tcpclient object on error
        end
        try
            tto = tcpclient(host, port);  % Attempt to reconnect
        catch recon_ME
            error('Failed to reconnect: %s', recon_ME.message);
        end
    end

    
    % % Check if the user pressed the escape key
    % if waitforbuttonpress == 1
    %     break;
    % end
end


%% Simulate EEG Data
clear, close all, clc

% Simulate EEG data
fs = 250; % Sampling frequency (Hz)
time = 60; % 10 seconds of data
t = 0:1/fs:(time - 1/fs);
freq_segments = [7.2 8 9 9.6 12]; % Frequencies for each segment (Hz)
amplitude = 50; % Amplitude of the simulated signal
window_size = 6.5; % in seconds
step_size = 1; % in seconds

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


% %% MATLAB Script: send_ssvep_data.m
% 
% % Set up TCP/IP client
% host = 'localhost';
% port = 12345;
% 
% try
%     % Create TCP/IP client object
%     tto = tcpclient(host, port);
%     
%     % Define SSVEP frequencies and corresponding messages
%     refFreq = [8, 12, 15];  % SSVEP frequencies in Hz
%     messages = {'1', '2', '3'};  % Messages to be sent corresponding to frequencies
% 
%     % Simulated SSVEP detection loop
%     while true
%         % Perform SSVEP frequency detection (replace with your actual logic)
%         detected_freq = detect_ssvep_frequency();  % Example function to detect SSVEP frequency
%         
%         % Find index of detected frequency
%         [~, ind] = ismember(detected_freq, refFreq);
%         
%         if ind > 0
%             % Send corresponding message over TCP/IP
%             message = messages{ind};
%             write(tto, message);  % Send message as characters
%             fprintf('Sent SSVEP Frequency: %d Hz (Message: %s)\n', detected_freq, message);
%         end
%         
%         pause(1);  % Pause for 1 second before next detection
%     end
%     
% catch ME
%     disp(['Error occurred: ', ME.message]);
%     if exist('tto', 'var') && isvalid(tto)
%         delete(tto);  % Close and delete the tcpclient object on error
%     end
% end
% 
% % Function to simulate SSVEP frequency detection (replace with actual detection logic)
% function detected_freq = detect_ssvep_frequency()
%     % Simulated detection logic (replace with your actual SSVEP detection algorithm)
%     detected_freq = randi([8, 15]);  % Simulate random frequency detection (8, 12, or 15 Hz)
% end
