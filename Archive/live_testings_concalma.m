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

end

board_shim.stop_stream();
board_shim.release_session();
sound(sin(0:1000)); % play stop beep sound for 3s

%% 