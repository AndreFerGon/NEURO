import numpy as np
from psychopy import visual, core

# Parameters
num_freq = 12
freq_range = [9.25, 14.75]
freq_interval = 0.5
phase_diff = 0.5 * np.pi
refresh_rate = 60
num_frames = 120  # Number of frames to generate

# Generate frequencies
frequencies = np.arange(freq_range[0], freq_range[1] + freq_interval, freq_interval)

# Generate phase angles
phases = np.arange(0, num_freq * phase_diff, phase_diff)

# Open a PsychoPy window
win = visual.Window([800, 600], monitor="testMonitor", units="pix")

# Generate stimulus sequence
stimuli = []
for i in range(num_freq):
    stim = visual.Circle(win, radius=100, fillColor=(1, 1, 1), lineColor=(-1, -1, -1))
    stimuli.append(stim)

for j in range(num_frames):
    for i in range(num_freq):
        # Calculate stimulus intensity
        intensity = 1 + np.sin(2 * np.pi * frequencies[i] * (j / refresh_rate) + phases[i])
        
        # Set stimulus intensity
        stimuli[i].fillColor = (intensity, intensity, intensity)
        
        # Draw stimulus
        stimuli[i].draw()
    
    # Flip window
    win.flip()

# Close PsychoPy window
win.close()
