%%  data import and visualization
close all, clear, clc

flick_f = 36;
data = table2array(readtable(['Data/Protocol#1_202007965_21_Male_', num2str(flick_f), 'Hz.csv']));
data = data(100:end, :);

% data = table2array(readtable(['S202007965_21_Protocol#2_1SFT_7.5Hz_Trials3_7.csv']));
% data = data(50:end, :);

channel_labels = {'P7','O1','Oz','O2','P8','P3','Pz','P4'};


fs = 250;
t = 0:1/fs:(length(data)-1)/fs;


channel = 3;

figure

subplot(2,1,1)
plot(t, data(:, channel))
title(['Channel ', channel_labels{channel}, ': Raw Signal'])
xlabel('Time (s)')
ylabel('Amplitude (μV)')

signal=data(:, channel);

n = length(signal);
f = (0:n-1)*(fs/n); % Frequency range
s= fft(signal);
p = abs(s.^2);

subplot(2,1,2)
plot(f, 10*log10(p))
title(['Channel ', channel_labels{channel}, ': Raw Signal FFT in dB'])
xlabel('Frequency (Hz)')
xlim([0 fs/2])
ylabel('Power (dB)')

%% pre-processing (filter design)

close all
% % Band-pass Filter 1-40 Hz
% order = 6; 
% band = [1 40];  
% [b, a] = butter(order, band/(fs/2), 'bandpass');
% figure
% freqz(b,a);
% filtered_signal = filter(b, a, data, [], 1);
% 
% channel = 1;
% 
% figure
% filt_signal=filtered_signal(500:end, channel);
% 
% 
% t = 0:1/fs:(length(filt_signal)-1)/fs;
% subplot(2,1,1)
% plot(t, filt_signal)
% title(['Channel ', num2str(channel), ': Filtered Signal with Bandpass 1-40Hz'])
% xlabel('Time (s)')
% ylabel('Amplitude (μV)')
% 
% window=1024;
% noverlap=window/2;
% [filt_p, filt_f] = pwelch(filt_signal, [], [], 2^12, fs);
% 
% subplot(2,1,2)
% plot(filt_f, 10*log10(filt_p))
% title(['Channel ', num2str(channel), ': Filtered Signal FFT (in dB) with Bandpass 1-40Hz'])
% xlabel('Frequency (Hz)')
% ylabel('Power (dB)')


% Low-pass 60 Hz
order = 8; 
[low_b, low_a] = butter(order, 40/(fs/2), 'low');
% figure
% freqz(b,a)
% title('Frequency Response of Low-pass Filter (Butterworth, 40 Hz)')
% ylim([-100 5])

% filtered_signal = filter(b, a, data, [], 1);

% High-pass 1 Hz
order = 2; 
[high_b, high_a] = butter(order, 1/(fs/2), 'high');
% figure
% freqz(b,a)
% title('Frequency Response of High-pass Filter (Butterworth, 1 Hz)')
% ylim([-25 2])

% filtered_signal = filter(b, a, filtered_signal, [], 1);

% Notch-filter 50 Hz
order = 2; 
[notch_b, notch_a] = butter(order, [48 52]/(fs/2), 'stop');
% figure
% freqz(b,a)
% title('Frequency Response of Notch Filter (Butterworth, 50 Hz)')
% ylim([-60 5])

% filtered_signal = filter(b, a, filtered_signal, [], 1);


%filtered_signal = signal;

filt_t = 0:1/fs:(length(data)-351)/fs;

filtered_signal = filter(low_b, low_a, data);
filtered_signal = filter(high_b, high_a, filtered_signal);
filtered_signal = filter(notch_b, notch_a, filtered_signal);

% Remove the first 350 samples from all columns
filtered_signal = filtered_signal(351:end, :);

figure
for i=1:8
    % filtered_signal(:,i) = filter(low_b, low_a, data(:,i));
    % filtered_signal(:,i) = filter(high_b, high_a, filtered_signal(:,i));
    % filtered_signal(:,i) = filter(notch_b, notch_a, filtered_signal(:,i));
    % 
    % filtered_signal(:,i) = filtered_signal(350:end, :);

    filt_t = 0:1/fs:(length(filtered_signal)-1)/fs;

    subplot(8,2,2*i-1)
    plot(t, data(:,i))
    title(['Channel ', channel_labels{i}, ': Original Signal'])
    xlabel('Time (s)')
    ylabel('Amplitude (μV)')
    grid on

    subplot(8,2,2*i)
    plot(filt_t, filtered_signal(:,i))
    title(['Channel ', channel_labels{i}, ': Filtered Signal with Bandpass 1-40 Hz'])
    xlabel('Time (s)')
    ylabel('Amplitude (μV)')
    grid on
end

filtered_stim_36Hz = filtered_signal(:, 3);
save("filtered_stim_36Hz", "filtered_stim_36Hz")

%% 8-channel FFT analysis
close all




figure
for channel = 1:8
    signal=data(1:end,channel);
    filt_signal=filtered_signal(1:end, channel);
    
    [p, f] = pwelch(signal, [], [], 2^12, fs);
    [filt_p, filt_f] = pwelch(filt_signal, [], [], 2^12, fs);
    
    if (channel == 5)
        figure
    end
    
    if channel <= 4
        subplot(4,1,channel)
    else
        subplot(4,1,channel-4)
    end
    
    plot(filt_f, filt_p)
    title(['Channel ', channel_labels{channel}, ': Filtered Signal FFT Power in dB (Flickering f: ', num2str(flick_f), ' Hz)'])
    xlabel('Frequency (Hz)')
    ylabel('Amplitude (dB)')
    xlim([5 40])
end



%% Single channel visualization
close all, clc

channel = 3;
signal=data(220:end, channel);
filt_signal=filtered_signal(220:end, channel);
[p, f] = pwelch(signal, [], [], 2^12, fs);
[filt_p, filt_f] = pwelch(filt_signal, [], [], 2^12, fs);

t = 0:1/fs:(length(filt_signal)-1)/fs;

subplot(2,2,1)
plot(t, signal)
title(['Channel ', channel_labels{channel}, ': Raw Signal'])
xlabel('Time (s)')
ylabel('Amplitude (μV)')
%axis([0 length(data16Hz) 2.75e4 3.25e4])

subplot(2,2,3)
plot(t, filt_signal)
title(['Channel ', channel_labels{channel}, ': Filtered Signal with Low-Pass, High-Pass and Notch'])
xlabel('Time (s)')
ylabel('Amplitude (μV)')

subplot(2,2,2)
plot(f, 10*log10(p))
title(['Channel ', channel_labels{channel}, ': Raw Signal FFT Power in dB'])
xlabel('Frequency (Hz)')
ylabel('Power (dB)')

subplot(2,2,4)
plot(filt_f, 10*log10(filt_p))
title(['Channel ', channel_labels{channel}, ': Filtered Signal FFT Power in dB'])
xlabel('Frequency (Hz)')
ylabel('Power (dB)')

figure
plot(filt_f, filt_p)
title(['Channel ', channel_labels{channel}, ': Filtered Signal FFT Power'])
xlabel('Frequency')
ylabel('Amplitude')
xlim([5 40])

%% pre-stim vs stim
close all


pre_stim = filt_signal(1:4700);
stim = filt_signal(4701:end);

[pre_p, pre_f] = pwelch(pre_stim, [], [], 2^14, fs);
[stim_p, stim_f] = pwelch(stim, [], [], 2^14, fs);

figure

subplot(2,1,1)
plot(pre_f, pre_p)
title(['Channel ', channel_labels{channel}, ': Filtered Signal FFT Power (Pre-Stimulus)'])
xlabel('Frequency')
ylabel('Amplitude')
xlim([0 35])

subplot(2,1,2)
plot(stim_f, stim_p)
title(['Channel ', channel_labels{channel}, ': Filtered Signal FFT Power (During Stimulus)'])
xlabel('Frequency')
ylabel('Amplitude')
xlim([0 35])
%ylim([0 200])

%% Stim split and averaging
close all 

n = length(stim);
resto = rem(n, 8);
cropstim = stim(1:end-resto);
n = length(cropstim);
resto = rem(n, 8);

split = reshape(cropstim, [n/8, 8]);

% Single trial analysis
for trial = 1:8
    signal = split(:, trial);
    
    [p, f] = pwelch(signal, [], [], 2^12, fs);

    if (trial == 8) % Save trials with 4 s long
           trial_signal = signal(1:1000);
           save('stim_36Hz_trial8_Oz_data.mat', 'trial_signal');
    end

    if (trial == 5)
        figure
    end

    subplot(4, 1, rem(trial, 4) + 1)
    plot(f, p)
    title(['Trial ', num2str(trial), ': FFT Power'])
    xlabel('Frequency')
    ylabel('Amplitude')
    xlim([6 40])

end

% avg_stim = mean(split, 2);
% [avg_p, avg_f] = pwelch(avg_stim, [], [], 2^12, fs);

% figure
% plot(avg_f, avg_p)
% title(['Channel ', num2str(channel), ': Average Signal FFT Power (During Stimulus)'])
% xlabel('Frequency')
% ylabel('Amplitude')
% xlim([0 35])
% ylim([0 200])

%% Average of 8 channels

avg_signal = mean(filtered_signal(500:end, :), 2);
%plot(filtered_signal(500:end, :))

[avg_p, avg_f] = pwelch(avg_signal, [], [], 2^12, fs);
plot(avg_f, 10*log10(avg_p))

%% Single frequency power during time

target_f = [flick_f/2, flick_f];

n = length(filt_signal);
spectrogram(filt_signal, fix(n/20), fix(n/40), 2^14, fs);
xlim([4 20])

[s, f, t, ps] = spectrogram(filt_signal, fix(n/20), fix(n/40), 2^14, fs);

target_f_vector = [];
for i = 1:length(target_f)
    target_f_vector = [target_f_vector; find(f > target_f(i)-0.01 & f < target_f(i)+0.01)];
end

total_ps = sum(ps, 1);

target_ps = sum(ps(target_f_vector, :), 1);
percentage = (target_ps ./ total_ps) * 100;

figure

plot(t, percentage)
title(['Channel ', num2str(channel), ': Target Frequency Power Percentage'])
xlabel('Time')
ylabel('Percentage')

