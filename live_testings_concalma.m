%% Brainflow Setup

% board_shim.release_session(); 
clear

openBCI_serial_port = 'COM5'; % For Windows Operating System | Change the serial port accordingly
file_name = 'data/raw_data.csv';
fs = 250;
data_save = [];
window_size = 5; % in seconds
total_trial = 30;

addpath(genpath('brainflow'))
BoardShim.set_log_file('brainflow.log');
BoardShim.enable_dev_board_logger();
params = BrainFlowInputParams();
params.serial_port = openBCI_serial_port;
board_shim = BoardShim(0, params); % BoardIds.SYNTHETIC_BOARD (-1)  |  BoardIds.CYTON_BOARD (0)
preset = int32(BrainFlowPresets.DEFAULT_PRESET);

%% Streaming Cycle

board_shim.prepare_session();
board_shim.start_stream(450000, '');

figure;


for i_segment = 1:total_trial
        % sound(sin(0:300)); % play beep sound for 300ms at the beginning of each 5 seconds window
        pause(window_size);
        disp(strcat('Elapsed: ', num2str(i_segment*window_size), ' Seconds'));
        % 1: Signal Acquisition
        data = board_shim.get_board_data(board_shim.get_board_data_count(preset), preset);

        t = 0:1/fs:(size(data,2)-1)/fs;
        channel = 4;

        data_chan3 = data(channel,:);


        % Low-pass 40 Hz
        order = 8; 
        [b, a] = butter(order, 40/(fs/2), 'low');     
        data_chan3_filtered = filter(b, a, data_chan3, [], 1);
            
        % High-pass 1 Hz
        order = 2; 
        [b, a] = butter(order, 1/(fs/2), 'high');        
        data_chan3_filtered = filter(b, a, data_chan3_filtered, [], 1);

        % Notch-filter 50 Hz
        order = 2; 
        [b, a] = butter(order, [48 52]/(fs/2), 'stop');
        data_chan3_filtered = filter(b, a, data_chan3_filtered, [], 1);

        % Detrend and PSD!!!
        subplot(3,2,1)
        plot(data_chan3)
        title("Raw Signal")

        window = 256;
        noverlap = window/2;

        subplot(3,2,2)
        [p, f] = pwelch(data_chan3, window, noverlap, [], fs);
        plot(f,p)
        title("Raw Signal PSD")
        xlim([4 40])

        subplot(3,2,3)
        plot(data_chan3_filtered)
        title("Filtered Signal")

        subplot(3,2,4)
        [filt_p, filt_f] = pwelch(data_chan3_filtered, [], [], 2^12, fs);
        plot(filt_f,filt_p)
        title("Filtered Signal PSD")
        xlim([4 40])

        detrended = DataFilter.detrend(data_chan3_filtered, int32(DetrendOperations.LINEAR));

        subplot(3,2,5)
        plot(detrended)
        title("Detrended Signal")

        subplot(3,2,6)
        [d_p, d_f] = pwelch(data_chan3_filtered, [], [], 2^12, fs);
        plot(d_f,d_p)
        title("Detrended Signal PSD")
        xlim([4 40])


        % title(['Channel ', channel, ': PSD of the Signal'])
        % xlabel('Frequency (Hz)')
        % ylabel('Amplitude (?)')

end

board_shim.stop_stream();
board_shim.release_session();
sound(sin(0:1000)); % play stop beep sound for 3s

%% 