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
step_size = 0.5; % in seconds
threshold = 0.16;

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

host = 'localhost';  % Use 'localhost' or '127.0.0.1' if running on the same machine
port = 12345;         % Port number on which Python server is listening
% 
tto = tcpclient(host, port);

% Initialize figure for real-time plotting
figure;
subplot(2,1,1)
h1 = plot(zeros(1,2*fs)); % Initialize plot
title('Filtered EEG Data');
xlabel('Time (s)');
ylabel('Amplitude');
ylim([-100 100]);

subplot(2,1,2)
h2 = plot(linspace(0,fs/2,fs/2+1), zeros(1,fs/2+1)); % Initialize plot
title('Filtered EEG Data PSD');
xlabel('Frequency (Hz)');
ylabel('Power');

window_data = zeros(1, window_size*fs); % Initialize window data
filtered_window = zeros(1, (window_size-filter_crop)*fs);

i_segment = 0;
prev_ind = 0;
ind = 0;

while true
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

    % Save filtered eeg data from chann 3 to eeg_processed_arr (Hasbulla)
    % new_filtered_data = filtered_window(:,end-size(data, 2)+1:end);
    % eeg_filtered_arr = [eeg_filtered_arr, new_filtered_data];
    % writematrix(eeg_filtered_arr,file_name_processed);

    % % Update plot
    % subplot(2,1,1);
    % set(h1, 'XData', (0:1/fs:window_size-1/fs), 'YData', window_data);
    % xlim([0 window_size]);
    % 
    % subplot(2,1,2);
    % [f,p] = periodogram(window_data,[],[],fs);
    % set(h2, 'XData', f, 'YData', 10*log10(p));
    % xlim([0 fs/2]);


    % Update plot
    subplot(2,1,1);
    set(h1, 'XData', (0:1/fs:(window_size-filter_crop-1/fs)), 'YData', filtered_window);
    xlim([0 window_size]);

    subplot(2,1,2);
    [p, f] = periodogram(filtered_window,[],[],fs);
    set(h2, 'XData', f, 'YData', 10*log10(p));
    xlim([4 40]);

    drawnow;

    prev_ind = ind;
    for j = 1:classNum

        [~, ~, corr] = canoncorr(filtered_window', Y{j}');
        r(j) = max(corr);
    end
    [m, ind] = max(r);

   

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

    % % Check if the escape key is pressed
    % if waitforbuttonpress == 1
    %     break;
    % end
end

board_shim.stop_stream();
board_shim.release_session();
sound(sin(0:1000)); % play stop beep sound for 3s
