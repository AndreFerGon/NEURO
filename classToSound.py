# receive numeric class classLabel (4 classes, 1-4) from matlab signal processing
# and output a sound based on a modifier 5th class (0)

import sys
import numpy as np
# import sounddevice as sd
import soundfile as sf
import time
import pygame




# load sound files, each intrument (class) has 4 sound samples
# 1 - drums, 2 - bass, 3 - guitar, 4 - vocals
# 0 - no sound (modifier class)

# dictionary with class classLabels as keys and imported sound samples as values
audioDict = {1: [], 2: [], 3: [], 4: []}
# midiDict = {1: [], 2: [], 3: [], 4: []}

for i in ['drums', 'bass', 'guitar', 'vocals']:
    try:
        audioDict[i].append((sf.read(r'sounds/' + i + f"/{i}{str(n)}{letter}" + '.wav') for n in range(1, 5) for letter in ['', 'a', 'b', 'c', 'd']))
    except:
        continue


# Set to keep track of currently playing sounds
playingSounds = {}

def chooseMode(classLabel, modifier):  # choose between instrument and sample choice mode
    
    if classLabel == 0:
        modifier = 1 if modifier == 0 else 0    # switch between modes
    return modifier

def chooseSound(classLabel, instrument, modifier):   # choose the sound to play

    if classLabel not in range(0, 5):
        print("Invalid class classLabel")
        return

    # if in instrument choice mode, choose it and play the default sample (first one)
    if modifier == 0:
        instrument = classLabel
        return (instrument, 1)
    
    # if in sample choice mode, choose the sample to play
    if modifier == 1:
        return (instrument, classLabel)

'''
def playMidi(midiToPlay):
    # Load the MIDI file
    pygame.mixer.music.load(midiDict[midiToPlay])

    # Play the MIDI file
    pygame.mixer.music.play()
'''

def main(): # receive class classLabel and outputs in real time
    end = False

    pygame.mixer.init()

    # default values
    modifier = 0    # 0 - instrument choice mode / 1 - sample choice mode
    instrument = 1  # drums
    
    print(audioDict)

    testBusclassLabel = [2, 1, 0, 3, 1, 0, 4, 1, 0, 2, 1, 0, 3, 1, 0]

    
    sound = pygame.mixer.Sound(r"sounds/_archive/audioBeat.wav")
    sound.set_volume(0.3)  # Adjust the volume (0.0 - 1.0)
    # sound.play(-1)  # -1 means loop indefinitely
    tempo = 115 # bpm for Heart of Glass
    delay = int(60000 / tempo)   # ms

    index = 0
    while not end:
        print()
        # TO RECEIVE CLASS classLabel FROM MATLAB
        classLabel = testBusclassLabel[index]; print("classLabel: ", classLabel)
    
    # if the classLabel is a valid non modifier class
        if classLabel in audioDict:
        
        # change instrument
            if modifier == 0:
                print("Instrument choice mode")
                instrument = classLabel; print("Instrument", instrument)
        # change sound
            elif modifier == 1:
                print("Sample choice mode")
                audioToPlay = chooseSound(classLabel, instrument, modifier); print("Audio", audioToPlay)  # tuple (instrument, samplerate)
            

            # If the sound for this class is already playing, stop it
                if audioToPlay in playingSounds:
                    playingSounds[audioToPlay].stop()
                    # print("here")
                    del playingSounds[audioToPlay]
                else:
            # Otherwise, start playing the sound in a loop
                    playingSounds[audioToPlay] = pygame.mixer.Sound(audioDict[audioToPlay[0]][audioToPlay[1] - 1])

                    pygame.time.wait(delay) # align next beat

                    playingSounds[audioToPlay].play(1)  # -1 means loop indefinitely

        # end if ESC key is pressed
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    end = True

    # if the classLabel is a modifier class
        if classLabel == 0: 
            modifier = 1 if modifier == 0 else 0
            print("Modifier: ", modifier)

        # temporary testing ending condition
        end = input("Next? (y/n): ") == 'n'
        index += 1
        if index == len(testBusclassLabel):
            end = True
        

if __name__ == "__main__":
    main()