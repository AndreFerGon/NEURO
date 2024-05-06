%% Brainflow Setup

openBCI_serial_port = 'COM3'; % For Windows Operating System | Change the serial port accordingly
file_name = 'data/raw_data.csv';
fs = 256;
data_save = [];
window_size = 2; % in seconds
total_trial = 30;

addpath(genpath('brainflow'))
BoardShim.set_log_file('brainflow.log');
BoardShim.enable_dev_board_logger();
params = BrainFlowInputParams();
params.serial_port = openBCI_serial_port;
board_shim = BoardShim(0, params); % BoardIds.SYNTHETIC_BOARD (-1)  |  BoardIds.CYTON_BOARD (0)
preset = int32(BrainFlowPresets.DEFAULT_PRESET);

%% Initializing variables for using CCA;
refFreq = [16 24 36];
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

%% Streaming cycle

board_shim.prepare_session();
board_shim.start_stream(450000, '');

figure;

for i_segment = 1:total_trial
        sound(sin(0:300)); % play beep sound for 300ms at the beginning of each 5 seconds window
        pause(window_size);
        disp(strcat('Elapsed: ', num2str(i_segment*window_size), ' Seconds'));

        window_detected_freqs = [];
        window_data_filtered = [];


        % 1: Signal Acquisition
        data = board_shim.get_board_data(board_shim.get_board_data_count(preset), preset);
        data_save = [data_save data];

        % 2: Filtering

        for chan_i = 1:size(data,1)

            chan_i_data = data(chan_i,:);

            % Low-pass 60 Hz
            order = 8; 
            [b, a] = butter(order, 40/(fs/2), 'low');     
            chan_i_filtered = filter(b, a, chan_i_data, [], 1);
            
            % High-pass 1 Hz
            order = 2; 
            [b, a] = butter(order, 1/(fs/2), 'high');        
            chan_i_filtered = filter(b, a, chan_i_filtered, [], 1);
    
            % Notch-filter 50 Hz
            order = 2; 
            [b, a] = butter(order, [48 52]/(fs/2), 'stop');
            chan_i_filtered = filter(b, a, chan_i_filtered, [], 1);

            data_filtered = [data_filtered, chan_i_filtered];

            % % Detrend, PSD and save power for each frequency bin
            % detrended = DataFilter.detrend(chan_i_filtered, int32(DetrendOperations.LINEAR));
            % [ampls, freqs] = DataFilter.get_psd_welch(detrended, nfft, nfft / 2, fs, int32(WindowOperations.HANNING));
            % 
            % chan_i_bandPower_XXHz = DataFilter.get_band_power(ampls, freqs, 8.0, 13.0); %use this line to create the frequency "bins" 
            % chan_i_bandPower_YYHz = DataFilter.get_band_power(ampls, freqs, 8.0, 13.0); %use this line to create the frequency "bins" 
            % chan_i_bandPower_WWHz = DataFilter.get_band_power(ampls, freqs, 8.0, 13.0); %use this line to create the frequency "bins" 
            % chan_i_bandPower_ZZHz = DataFilter.get_band_power(ampls, freqs, 8.0, 13.0); %use this line to create the frequency "bins"
            % 
            % chan_i_freq_bins = [chan_i_bandPower_XXHz, chan_i_bandPower_YYHz, chan_i_bandPower_WWHz, chan_i_bandPower_ZZHz]
            % freq_bins = [freq_bins chan_i_freq_bins]

            % CCA implementation

            for j = 1:classNum
                [~, ~, corr] = canoncorr(data_filtered, Y{j}');
                r(j) = max(corr);
            end
            [~, ind] = max(r);

            chan_i_detected_freq = refFreq(ind);
            window_detected_freqs = [window_detected_freqs chan_i_detected_freq];

        end

        window_main_freq = mode(window_detected_freqs);
        fprintf('Window SSVEP Frequency: %d Hz\n', window_main_freq);

        window_data_filtered = [window_data_filtered data_filtered]
        % window_freq_bins = [window_freq_bins freq_bins]

end

board_shim.stop_stream();
board_shim.release_session();
sound(sin(0:1000)); % play stop beep sound for 1s
DataFilter.write_file(data_save, file_name, 'w');
DataFilter.write_file(windows_data_filtered, 'data/Windows_data_filtered.csv', 'w');
disp('---Data Collection Completed---');