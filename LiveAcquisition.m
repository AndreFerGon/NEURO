%% Brainflow Setup

% board_shim.release_session(); 
clear, clc, close all

openBCI_serial_port = 'COM5'; % For Windows Operating System | Change the serial port accordingly

% Variables used to store the data and pass them into csv files (Hasbulla)
eeg_raw_arr = [];
eeg_filtered_arr = [];
file_name_raw = 'data/raw_eeg.xlsx';
file_name_processed = 'data/processed_eeg.xlsx';

fs = 250;
data_save = [];
window_size = 5.5; % in seconds
step_size = 1; % in seconds
threshold = 0.24;

filter_crop = 1.5;

addpath(genpath('brainflow'))
BoardShim.set_log_file('brainflow.log');
BoardShim.enable_dev_board_logger();
params = BrainFlowInputParams();
params.serial_port = openBCI_serial_port;
board_shim = BoardShim(0, params); % BoardIds.SYNTHETIC_BOARD (-1)  |  BoardIds.CYTON_BOARD (0)
preset = int32(BrainFlowPresets.DEFAULT_PRESET);

%% Initializing variables for using CCA;
refFreq = [7.2 8 9 9.6 12];
time = window_size-filter_crop; % Seconds;
classNum = length(refFreq); 
%trialNum = 1;
loss = 0;

ref_t = 0:1/fs:(time-1/fs);

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

%% Streaming Cycle

board_shim.prepare_session();
board_shim.start_stream(450000, '');
currentTime = datetime('now', 'Format', 'HH:mm:ss.SSS');
disp(['Stream start: ', char(currentTime)]);

host = 'localhost';  % Use 'localhost' or '127.0.0.1' if running on the same machine
port = 12345;         % Port number on which Python server is listening
% 
tto = tcpclient(host, port);

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

window_data = zeros(1, window_size*fs); % Initialize window data
filtered_window = zeros(1, (window_size-filter_crop)*fs);

i_segment = 0;
prev_ind = 0;
ind = 0;

cca_vector = [];

stopLoop = true;
while stopLoop
    i_segment = i_segment + 1;
    pause(step_size); % Wait for step_size seconds
    % 1: Signal Acquisition
    data = board_shim.get_board_data(board_shim.get_board_data_count(preset), preset);
    %size(data)

    % Save incoming raw data to raw_eeg_arr (Hasbulla)
    eeg_raw_arr = [eeg_raw_arr, data];
    % writematrix(eeg_raw_arr,file_name_raw);


    t = 0:1/fs:(size(data,2)-1)/fs;

    channel = 3;
    window_data = [window_data(length(data)+1:end), data(channel,:)];

    filtered_window = filter(low_b, low_a, window_data);
    filtered_window = filter(high_b, high_a, filtered_window);
    filtered_window = filter(notch_b, notch_a, filtered_window);

    filtered_window = filtered_window(250*filter_crop+1:end);


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
        [~, ~, corr] = canoncorr(filtered_window', Y{j}');
        r(j) = max(corr);
    end
    [m, ind] = max(r);

    cca_vector = [cca_vector; [t_segment(1) r]];

    if(m>threshold && prev_ind==ind)
        counter = counter+1;
    else
        counter = 0;
    end

    if(m>threshold)
     fprintf('SSVEP Frequency: %d Hz (canoncorr = %f) \n', refFreq(ind), m);
    end

    try
         if (counter == 4)                 
        % Send random integer numbers every second
            if refFreq(ind) == 7.2
                message = sprintf('%d', 0);                    
            elseif refFreq(ind) == 8
                message = sprintf('%d', 1);
            elseif refFreq(ind) == 9
                message = sprintf('%d', 2);
            elseif refFreq(ind) == 9.6
                message = sprintf('%d', 3);
            elseif refFreq(ind) == 12
                message = sprintf('%d', 4);
            end      
            fprintf('CLASS DETECTED: %d Hz  \n', refFreq(ind));

            counter = 0;
         end


            % Send the message over TCP/IP
            write(tto, message);  % Send as characters

            % Display the sent message (optional)
            %disp(['Frequency: ', num2str(message)]);



    catch ME
        %disp(['Error occurred: ', ME.message]);
        if exist('tto', 'var') && isvalid(tto)
            delete(tto);  % Close and delete the tcpclient object on error
        end
    end


end

board_shim.stop_stream();
board_shim.release_session();
sound(sin(0:1000)); % play stop beep sound for 3s
