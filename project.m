%%  data import
close all, clear, clc
data16Hz = table2array(readtable('Protocol#1_202007965_21_Male_16Hz.csv'));
data16Hz = data16Hz(2:length(data16Hz), :);

%% pre-processing (filter design)
fs = 250;  
band = [1 40];   
order = 2; 
[b, a] = butter(order, band/(fs/2), 'bandpass');

% % Initialize the initial conditions of the filter
% z = zeros(max(length(a),length(b))-1,size(data16Hz,2)); 

% Apply the filter with initial conditions
filtered_signal = filter(b, a, data16Hz, [], 1);


figure
for i=1:8

signal=data16Hz(1:end,i);
subplot(8,2,2*i-1)
plot(signal)
title(['Channel ', num2str(i), ': Original Signal'])
xlabel('Time')
ylabel('Amplitude')
%axis([0 length(data16Hz) 2.75e4 3.25e4])

subplot(8,2,2*i)
plot(filtered_signal(1:end,i))
title(['Channel ', num2str(i), ': Filtered Signal with Bandpass 1-40 Hz'])
xlabel('Time')
ylabel('Amplitude')

end

%% 
figure
for i=1:8

signal=data16Hz(1:end,i);
filtered_signal = filter(b, a, signal);
filtered_signal = filtered_signal(400:end);
subplot(8,2,2*i-1)
plot(filtered_signal)
title(['Channel ', num2str(i), ': Original Signal'])
xlabel('Time')
ylabel('Amplitude')
%axis([0 length(data16Hz) 2.75e4 3.25e4])



window_size = 1024; 
overlap = window_size / 2; 
[pxx_filtered, f_filtered] = pwelch(filtered_signal, window_size, overlap, [], fs);

subplot(8,2,2*i)
plot(pxx_filtered(1:50))
title(['Channel ', num2str(i), ': Original Signal FFT'])
xlabel('Frequency');
ylabel('Amplitude')


end

%% signal crop
figure
for i=1:8

signal=data16Hz(7000:7500,i);
x=1:length(signal);
subplot(8,2,2*i-1)
plot(x, signal)
title(['Channel ', num2str(i), ': Original Signal'])
xlabel('Time')
ylabel('Amplitude')
%axis([0 length(data16Hz) 2.75e4 3.25e4])

filtered_signal = filter(b, a, signal);

window_size = length(filtered_signal)/15; 
overlap = window_size / 2; 
[pxx_filtered, f_filtered] = pwelch(filtered_signal, window_size, overlap, [], fs);

subplot(8,2,2*i)
plot(pxx_filtered(1:50))
%axis([6  0 400])
title(['Channel ', num2str(i), ': Original Signal FFT'])
xlabel('Frequency');
ylabel('Amplitude')


end

%% single signal split
signal=data16Hz(1:end,1);
filtered_signal=filter(b,a,signal);
filtered_signal=filtered_signal(400:end);
base_signal = filtered_signal(1:4600);
stim_signal = filtered_signal(4601:end);

window_size = fix(length(filtered_signal)/15); 
overlap = fix(window_size / 2); 
[pxx_original, f_original] = pwelch(signal, window_size, overlap, [], fs); 
[pxx_filtered, f_filtered] = pwelch(filtered_signal, window_size, overlap, [], fs);
figure
subplot(2,2,1)
plot(signal)
subplot(2,2,2)
plot(filtered_signal)
subplot(2,2,3)
plot(f_original, pxx_original)
xlim([2 60])
subplot(2,2,4)
plot(f_filtered, pxx_filtered)
xlim([2 60])

window_size = 1024;
overlap = fix(window_size / 2); 
[pxx_base, f_base] = pwelch(base_signal, window_size, overlap, [], fs); 
[pxx_stim, f_stim] = pwelch(stim_signal, window_size, overlap, [], fs);
figure
subplot(3,2,1)
plot(base_signal)
subplot(3,2,2)
plot(stim_signal)
subplot(3,2,3)
plot(f_base, pxx_base)
%xlim([2 40])
subplot(3,2,4)
plot(f_stim, pxx_stim)
%xlim([2 40])
subplot(3,2,6)
plot(f_base, pxx_stim-pxx_base)
xlim([2 40])

%%
w = kaiser(2048, 19);
figure
subplot(2,1,1)
spectrogram(data16Hz(:,1), w, [], [], fs, "yaxis")
colormap jet
subplot(2,1,2)
spectrogram(filtered_signal(:,1), w, [], [], fs, "yaxis")
colormap jet