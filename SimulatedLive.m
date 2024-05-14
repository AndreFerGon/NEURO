%% Simulate EEG Data
clear, close all, clc

% Simulate EEG data
fs = 250; % Sampling frequency (Hz)
time = 5; % 10 seconds of data
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

load("mixed_signal_16_24.mat");
eeg_data = mixed_signal;
t = 0:1/fs:(length(eeg_data)/250 - 1/fs);

% Plot the simulated EEG data
figure;
plot(t, eeg_data);
xlabel('Time (s)');
ylabel('Amplitude');
title('Simulated EEG Data');


%% Initializing variables for using CCA;
refFreq = [8 12 18];
time = 5; % Seconds;
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

window_size = 5; % in seconds
step_size = 1; % in seconds

host = 'localhost';  % Use 'localhost' or '127.0.0.1' if running on the same machine
port = 12345;         % Port number on which Python server is listening

tto = tcpclient(host, port);


% Initialize figure for real-time plotting
figure;
subplot(1,2,1)
h1 = plot(zeros(1,2*fs)); % Initialize plot
title('Raw EEG Data');
xlabel('Time (s)');
ylabel('Amplitude');
ylim([-100 100]);
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
    t_segment = t(start_idx:end_idx);


    filtered_window = filter(low_b, low_a, segment_data);
    filtered_window = filter(high_b, high_a, filtered_window);
    filtered_window = filter(notch_b, notch_a, filtered_window);

    %filtered_window = filtered_window(250*1+1:end);

    % Update plot 
     %set(gca, 'XTick', t_segment(1):1:t_segment(end)) % Update x-axis ticks

    set(h1, 'XData', t_segment, 'YData', segment_data);
    xlim([t_segment(1) t_segment(end)])
    

    [p, f] = periodogram(segment_data, [], [], fs);

    set(h2, 'XData', f, 'YData', p);
    xlim([0 50]);
    
    drawnow;

    for j = 1:classNum
        [~, ~, corr] = canoncorr(filtered_window, Y{j}');
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

     counter = 0;


        try
                                 
            % Send random integer numbers every second
           
                
                % Format the message to send (convert random_integer to string)
                message = sprintf('%d\n', refFreq(ind));
                
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


%% MATLAB Script: send_random_data.m

% % Define parameters
% host = 'localhost';  % Use 'localhost' or '127.0.0.1' if running on the same machine
% port = 12345;         % Port number on which Python server is listening
% 
% try
%     % Create TCP/IP client object
%     t = tcpclient(host, port);
%     
%     % Send random integer numbers every second
%     while true
%         % Generate a random integer between 1 and 100 (adjust range as needed)
%         random_integer = randi([1, 100]);  % Random integer between 1 and 100
%         
%         % Format the message to send (convert random_integer to string)
%         message = sprintf('%d\n', random_integer);
%         
%         % Send the message over TCP/IP
%         write(t, message, 'char');  % Send as characters
%         
%         % Display the sent message (optional)
%         disp(['Sent random integer: ', num2str(random_integer)]);
%         
%         % Pause for 1 second before sending the next random number
%         pause(1);  
%     end
%     
% catch ME
%     disp(['Error occurred: ', ME.message]);
%     if exist('t', 'var') && isvalid(t)
%         delete(t);  % Close and delete the tcpclient object on error
%     end
%end
