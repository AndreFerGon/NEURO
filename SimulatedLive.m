%% DATA IMPORT
clear, close all, clc

fs = 250;

% a mixed signal with 10s rest + 10s 8Hz sti + 10s rest + 10s 12Hz stim

<<<<<<< HEAD
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

=======
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
>>>>>>> cbcc04a0f60b4a6ae28dc0774c11d62abba3ae98

%% Initializing variables for using CCA;

refFreq = [7.2 8 9 9.6 12];
time = window_size - 1.5; % Seconds;

<<<<<<< HEAD
fs= 250;
=======
>>>>>>> cbcc04a0f60b4a6ae28dc0774c11d62abba3ae98
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


<<<<<<< HEAD

host = 'localhost';  % Use 'localhost' or '127.0.0.1' if running on the same machine
port = 12345;         % Port number on which Python server is listening
% 
tto = tcpclient(host, port);
=======
host = 'localhost';  % Use 'localhost' or '127.0.0.1' if running on the same machine
port = 12345;         % Port number on which Python server is listening
% 
try
    tto = tcpclient(host, port);
catch ME
    error('Failed to create TCP connection: %s', ME.message);
end
>>>>>>> cbcc04a0f60b4a6ae28dc0774c11d62abba3ae98


% Initialize figure for real-time plotting
figure;
subplot(1,2,1)
<<<<<<< HEAD
h1 = plot(zeros(1,2*fs)); % Initialize plot
title(['Filtered EEG Data (' num2str(window_size-1.5) 's time window)']);
xlabel('Time (s)');
ylabel('Amplitude');
=======
h1 = plot(zeros(1,2*fs), 'DisplayName', 'Channel O1'); % Initialize plot for Channel 1
hold on;
h2 = plot(zeros(1,2*fs) - 200, 'DisplayName', 'Channel Oz'); % Initialize plot for Channel 2 with offset
h3 = plot(zeros(1,2*fs) + 200, 'DisplayName', 'Channel O2'); % Initialize plot for Channel 3 with offset
hold off;
title(['Filtered EEG Data (' num2str(window_size-1.5) 's time window)']);
xlabel('Time (s)');
ylabel('Amplitude');
legend('show', 'Location','best');
>>>>>>> cbcc04a0f60b4a6ae28dc0774c11d62abba3ae98
%ylim([-100 100]);
%xlim([0 window_size]) % Set initial x-axis limits
%set(gca, 'XTick', 0:1:window_size) % Set x-axis ticks every second

subplot(1,2,2)
<<<<<<< HEAD
h2 = plot(zeros(1,2*fs)); % Initialize plot
=======
h4 = plot(zeros(1,2*fs), 'DisplayName', 'Channel O1'); % Initialize plot for PSD of Channel 1
hold on;
h5 = plot(zeros(1,2*fs), 'DisplayName', 'Channel Oz'); % Initialize plot for PSD of Channel 2
h6 = plot(zeros(1,2*fs), 'DisplayName', 'Channel O2'); % Initialize plot for PSD of Channel 3
hold off;
>>>>>>> cbcc04a0f60b4a6ae28dc0774c11d62abba3ae98
title('Raw EEG Data FFT');
xlabel('Frequency (Hz)');
ylabel('Power');
xlim([0 50]) % Set initial x-axis limits
<<<<<<< HEAD
=======
legend('show');
>>>>>>> cbcc04a0f60b4a6ae28dc0774c11d62abba3ae98

i_segment = 0;
filtered_window = zeros(1, 2*fs);

counter = 0;
<<<<<<< HEAD
=======
ind=0;
prev_ind=0;

cca_vector = [];
>>>>>>> cbcc04a0f60b4a6ae28dc0774c11d62abba3ae98

while true
    i_segment = i_segment + 1;
    pause(step_size) % Wait for step_size seconds
    
    % Generate data for the current window
<<<<<<< HEAD
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
=======
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
>>>>>>> cbcc04a0f60b4a6ae28dc0774c11d62abba3ae98
    xlim([4 28]);
    
    drawnow;

<<<<<<< HEAD
    for j = 1:classNum
        [~, ~, corr] = canoncorr(filtered_window', Y{j}');
        r(j) = max(corr);
    end

    [m, ind] = max(r);
    prev_ind = ind;

    if(m>0.24 && prev_ind==ind)
=======
    prev_ind = ind;
    for j = 1:classNum
        [~, ~, corr] = canoncorr(filtered_window, Y{j}');
        r(j) = max(corr);
    end

    c

    [m, ind] = max(r);
    
    if(m>threshold && prev_ind==ind)
>>>>>>> cbcc04a0f60b4a6ae28dc0774c11d62abba3ae98
        counter = counter+1;
    else
        counter = 0;
    end

<<<<<<< HEAD
    if(m>0.18)
     fprintf('SSVEP Frequency: %d Hz (canoncorr = %f) \n', refFreq(ind), m);

     counter = 0;

        try
                                 
            % Send random integer numbers every second
                if refFreq(ind) == 7.2
                    message = sprintf('%d\n', 1);
                elseif refFreq(ind) == 8
                    message = sprintf('%d\n', 2);
                elseif refFreq(ind) == 9
                    message = sprintf('%d\n', 3);
                elseif refFreq(ind) == 9.6
                    message = sprintf('%d\n', 4);
                elseif refFreq(ind) == 12
                    message = sprintf('%d\n', 5);
                end           

                
                % Send the message over TCP/IP
                write(tto, message);  % Send as characters
                
                % Display the sent message (optional)
                %disp(['Frequency: ', num2str(message)]);
                
                
        
        catch ME
            disp(['Error occurred: ', ME.message]);
            if exist('tto', 'var') && isvalid(t)
                delete(t);  % Close and delete the tcpclient object on error
            end
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
=======
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

>>>>>>> cbcc04a0f60b4a6ae28dc0774c11d62abba3ae98
