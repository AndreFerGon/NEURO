%%  data import
close all, clear, clc
data16Hz = table2array(readtable('Protocol#1_202007965_21_Male_16Hz.csv'));
data16Hz = data16Hz(250:length(data16Hz), :);

%% pre-processing (filter design)
fs = 250;  
band = [1 40];  

order = 6; 
[b, a] = butter(order, 60/(fs/2), 'low');
figure
freqz(b,a);
filtered_signal = filter(b, a, data16Hz, [], 1);

order = 2; 
[b, a] = butter(order, 1/(fs/2), 'high');
figure
freqz(b,a);
filtered_signal = filter(b, a, filtered_signal, [], 1);

order = 2; 
[b, a] = butter(order, [48 52]/(fs/2), 'stop');
figure
freqz(b,a);
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

%% Single channel visualization
close all, clc

channel = 1;

signal=data16Hz(220:end,channel);
filt_signal=filtered_signal(220:end, channel);

[p, f] = pwelch(signal, [], [], 2^12, fs);
[filt_p, filt_f] = pwelch(filt_signal, [], [], 2^12, fs);


subplot(2,2,1)
plot(signal)
title(['Channel ', num2str(channel), ': Original Signal'])
xlabel('Time')
ylabel('Amplitude')
%axis([0 length(data16Hz) 2.75e4 3.25e4])

subplot(2,2,3)
plot(filt_signal)
title(['Channel ', num2str(channel), ': Filtered Signal with Bandpass 1-40 Hz'])
xlabel('Time')
ylabel('Amplitude')

subplot(2,2,2)
plot(f, 10*log10(p))
title(['Channel ', num2str(channel), ': Signal FFT Power in dB'])
xlabel('Frequency')
ylabel('Amplitude')

subplot(2,2,4)
plot(filt_f, 10*log10(filt_p))
title(['Channel ', num2str(channel), ': Filtered Signal FFT Power in dB'])
xlabel('Frequency')
ylabel('Amplitude')

figure
plot(filt_f, filt_p)
title(['Channel ', num2str(channel), ': Filtered Signal FFT Power'])
xlabel('Frequency')
ylabel('Amplitude')
xlim([0 35])

%% pre-stim vs stim

pre_stim = filt_signal(1:4700);
stim = filt_signal(4701:end);

[pre_p, pre_f] = pwelch(pre_stim, [], [], 2^12, fs);
[stim_p, stim_f] = pwelch(stim, [], [], 2^12, fs);

figure

subplot(2,1,1)
plot(pre_f, 10*log10(pre_p))
title(['Channel ', num2str(channel), ': Filtered Signal FFT Power (Pre-Stimulus)'])
xlabel('Frequency')
ylabel('Amplitude')
%xlim([0 35])

subplot(2,1,2)
plot(stim_f, 10*log10(stim_p))
title(['Channel ', num2str(channel), ': Filtered Signal FFT Power (During Stimulus)'])
xlabel('Frequency')
ylabel('Amplitude')
%xlim([0 35])
ylim([0 200])

%% Stim split and averaging

n=length(stim)
resto = rem(n, 8)
cropstim=stim(1:end-4);
n=length(cropstim)
resto = rem(n, 8)

split = reshape(cropstim, [n/8, 8]);
avg_stim = mean(split, 2);
[avg_p, avg_f] = pwelch(avg_stim, [], [], 2^12, fs);

plot(avg_f, avg_p)
title(['Channel ', num2str(channel), ': Average Signal FFT Power (During Stimulus)'])
xlabel('Frequency')
ylabel('Amplitude')
% xlim([0 35])
% ylim([0 200])
