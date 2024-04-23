data16Hz = table2array(readtable('Protocol#1_202007965_21_Male_16Hz.csv'));
data16Hz = data16Hz(250:length(data16Hz), :);
x=1:length(data16Hz);
x2=5000:length(data16Hz);

fs = 250;  
band = [1 40];   
order = 2; 
[b, a] = butter(order, band/(fs/2), 'bandpass');

figure
for i=1:8

signal=data16Hz(1:end,i);
subplot(8,2,2*i-1)
plot(x, signal)
title(['Channel ', num2str(i), ': Original Signal'])
xlabel('Time')
ylabel('Amplitude')
%axis([0 length(data16Hz) 2.75e4 3.25e4])

filtered_signal = filter(b, a, signal);

window_size = 1024; 
overlap = window_size / 2; 
[pxx_filtered, f_filtered] = pwelch(filtered_signal, window_size, overlap, [], fs);

subplot(8,2,2*i)
plot(pxx_filtered(1:50))
title(['Channel ', num2str(i), ': Original Signal FFT'])
xlabel('Frequency');
ylabel('Amplitude')


end
