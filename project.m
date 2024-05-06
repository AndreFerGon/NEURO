%%  data import and visualization
close all, clear, clc

flick_f = 24;
data = table2array(readtable(['Protocol#1_202007965_21_Male_', num2str(flick_f), 'Hz.csv']));
data = data(250:end, :);


channel_labels = {'P7','O1','Oz','O2','P8','P3','Pz','P4'};


fs = 250;
t = 0:1/fs:(length(data)-1)/fs;

channel = 1;

figure

subplot(2,1,1)
plot(t, data(:, channel))
title(['Channel ', channel_labels{channel}, ': Raw Signal'])
xlabel('Time (s)')
ylabel('Amplitude (μV)')

signal=data(:, channel);
window=1024;
noverlap=window/2;
[p, f] = pwelch(signal, window, noverlap, 2^14, fs);

subplot(2,1,2)
plot(f, 10*log10(p))
title(['Channel ', channel_labels{channel}, ': Raw Signal FFT in dB'])
xlabel('Frequency (Hz)')
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
[b, a] = butter(order, 40/(fs/2), 'low');
figure
freqz(b,a)
title('Frequency Response of Low-pass Filter (Butterworth, 40 Hz)')
ylim([-100 5])

filtered_signal = filter(b, a, data, [], 1);

% High-pass 1 Hz
order = 2; 
[b, a] = butter(order, 1/(fs/2), 'high');
figure
freqz(b,a)
title('Frequency Response of High-pass Filter (Butterworth, 1 Hz)')
ylim([-25 2])

filtered_signal = filter(b, a, filtered_signal, [], 1);

% Notch-filter 50 Hz
order = 2; 
[b, a] = butter(order, [48 52]/(fs/2), 'stop');
figure
freqz(b,a)
title('Frequency Response of Notch Filter (Butterworth, 50 Hz)')
ylim([-60 5])

filtered_signal = filter(b, a, filtered_signal, [], 1);




% figure
% for i=1:8
% 
% signal=data16Hz(1:end,i);
% subplot(8,2,2*i-1)
% plot(signal)
% title(['Channel ', num2str(i), ': Original Signal'])
% xlabel('Time')
% ylabel('Amplitude')
% %axis([0 length(data16Hz) 2.75e4 3.25e4])
% 
% subplot(8,2,2*i)
% plot(filtered_signal(6000:6250,i))
% title(['Channel ', num2str(i), ': Filtered Signal with Bandpass 1-40 Hz'])
% xlabel('Time')
% ylabel('Amplitude')
% 
% end

%% 8-channel analysis
close all




figure
for channel = 1:8
    signal=data(220:end,channel);
    filt_signal=filtered_signal(220:end, channel);
    
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
    xlim([8 40])
end



%% Single channel visualization
close all, clc

channel = 1;
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
xlim([8 40])

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

n=length(stim)
resto = rem(n, 8)
cropstim=stim(1:end-resto);
n=length(cropstim)
resto = rem(n, 8)

split = reshape(cropstim, [n/8, 8]);

figure
%Single trial analysis
for trial = 1:8
    signal=split(:,trial);
    
    [p, f] = pwelch(signal, [], [], 2^12, fs);

    if (trial == 5)
        figure
    end

    subplot(4,1,rem(trial,4) +1)
    plot(f, p)
    title(['TRial ', num2str(trial), ': FFT Power'])
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

target_f = flick_f;

n = length(filt_signal);
spectrogram(filt_signal, fix(n/20), fix(n/40), 2^14, fs);
xlim([4 20])

[s, f, t, ps]=spectrogram(filt_signal, fix(n/20), fix(n/40), 2^14, fs);

target_f_vector = find(f > target_f-0.01 & f<target_f+0.01);
target_ps = sum(ps(target_f_vector, :), 1);

figure
plot(t, target_ps)
title(['peta'])
