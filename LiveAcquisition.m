%% Brainflow Setup

% board_shim.release_session(); 
clear

openBCI_serial_port = 'COM5'; % For Windows Operating System | Change the serial port accordingly
file_name = 'data/raw_data.csv';
fs = 250;
data_save = [];
window_size = 3; % in seconds
step_size = 0.2; % in seconds

addpath(genpath('brainflow'))
BoardShim.set_log_file('brainflow.log');
BoardShim.enable_dev_board_logger();
params = BrainFlowInputParams();
params.serial_port = openBCI_serial_port;
board_shim = BoardShim(0, params); % BoardIds.SYNTHETIC_BOARD (-1)  |  BoardIds.CYTON_BOARD (0)
preset = int32(BrainFlowPresets.DEFAULT_PRESET);

%% Initializing variables for using CCA;
refFreq = [8.57 10 12 15];
time = 2; % Seconds;
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

%% Streaming Cycle

board_shim.prepare_session();
board_shim.start_stream(450000, '');

% Initialize figure for real-time plotting
figure;
subplot(2,1,1)
h1 = plot(zeros(1,2*fs)); % Initialize plot
title('Raw EEG Data');
xlabel('Time (s)');
ylabel('Amplitude');
ylim([-100 100]);

subplot(2,1,2)
h2 = plot(linspace(0,fs/2,fs), zeros(1,fs/2+1)); % Initialize plot
title('Raw EEG Data PSD');
xlabel('Frequency (Hz)');
ylabel('Power');

window_data = zeros(1, window_size*fs); % Initialize window data
filtered_window = zeros(1, window_size*fs);

i_segment = 0;
while true
    i_segment = i_segment + 1;
    pause(step_size); % Wait for step_size seconds
    % 1: Signal Acquisition
    data = board_shim.get_board_data(board_shim.get_board_data_count(preset), preset);

    t = 0:1/fs:(size(data,2)-1)/fs;

    channel = 3;
    window_data = [window_data(length(data)+1:end), data(channel,:)];

    filtered_window = filter(low_b, low_a, window_data);
    filtered_window = filtfilt(high_b, high_a, filtered_window);
    filtered_window = filtfilt(notch_b, notch_a, filtered_window);

    filtered_window = filtered_window(250*1+1:end);

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
    set(h1, 'XData', (0:1/fs:2-1/fs), 'YData', filtered_window);
    xlim([0 window_size]);

    subplot(2,1,2);
    [f,p] = periodogram(filtered_window,[],[],fs);
    set(h2, 'XData', f, 'YData', 10*log10(p));
    xlim([0 fs/2]);
    drawnow;
    
    for j = 1:classNum
        [~, ~, corr] = canoncorr(filtered_window', Y{j}');
        r(j) = max(corr);
    end
    [m, ind] = max(r);

    if(m>0.26)
     fprintf('SSVEP Frequency: %d Hz (canoncorr = %f) \n', refFreq(ind), m);
    end

    % Check if the escape key is pressed
    if waitforbuttonpress == 1
        break;
    end
end

board_shim.stop_stream();
board_shim.release_session();
sound(sin(0:1000)); % play stop beep sound for 3s
