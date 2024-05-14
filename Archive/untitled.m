% Add Psychtoolbox to the path
addpath(genpath('/path/to/Psychtoolbox'));

% Parameters
num_freq = 12;
freq_range = [9.25, 14.75];
freq_interval = 0.5;
phase_diff = 0.5 * pi;
RefreshRate = 60;
num_frames = 120; % Number of frames to generate

% Generate frequencies
frequencies = freq_range(1):freq_interval:freq_range(2);

% Generate phase angles
phases = 0:phase_diff:(num_freq-1)*phase_diff;

% Open a PTB window
win = Screen('OpenWindow', max(Screen('Screens')));

% Generate stimulus sequence
for i = 1:num_freq
    for j = 1:num_frames
        % Calculate stimulus intensity
        intensity = 1 + sin(2*pi*frequencies(i)*(j/RefreshRate) + phases(i));
        
        % Draw stimulus
        Screen('FillRect', win, intensity, [0 0 100 100]); % Change [0 0 100 100] to your desired position
        Screen('Flip', win);
    end
end

% Close PTB window
Screen('CloseAll');
