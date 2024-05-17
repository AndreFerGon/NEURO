openBCI_serial_port = 'COM5'; % For Windows Operating System | Change the serial port accordingly
file_name = 'data/EyesRealTimeSubject1Session1.csv';
fs = 256;
data_save = [];
window_size = 5; % in seconds
total_trial = 12;
addpath(genpath('data'))
addpath(genpath('brainflow'))
BoardShim.set_log_file('brainflow.log');
BoardShim.enable_dev_board_logger();
params = BrainFlowInputParams();
params.serial_port = openBCI_serial_port;
board_shim = BoardShim(0, params); % BoardIds.SYNTHETIC_BOARD (-1)  |  BoardIds.CYTON_BOARD (0)
preset = int32(BrainFlowPresets.DEFAULT_PRESET);

board_shim.prepare_session();
board_shim.start_stream(450000, '');

for i_segment = 1:total_trial
        sound(sin(0:300)); % play beep sound for 300ms at the beginning of each 5 seconds window
        pause(window_size);
        disp(strcat('Elapsed: ', num2str(i_segment*window_size), ' Seconds'));
        % 1: Signal Acquisition
        data = board_shim.get_board_data(board_shim.get_board_data_count(preset), preset);
end

board_shim.stop_stream();
board_shim.release_session();
sound(sin(0:3000)); % play stop beep sound for 3s