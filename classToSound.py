# receive numeric class label (4 classes, 1-4) from matlab signal processing
# and output a sound based on a modifier 5th class (0)

import sys
import numpy as np
import sounddevice as sd
import soundfile as sf
import time
import pygame




# load sound files, each intrument (class) has 4 sound samples
# 1 - drums, 2 - bass, 3 - guitar, 4 - vocals
# 0 - no sound (modifier class)

# dictionary with class labels as keys and imported sound samples as values
audioDict = {1: [], 2: [], 3: [], 4: []}
midiDict = {1: [], 2: [], 3: [], 4: []}

# for i in range(1, 5):
    # audioDict[i].append(sf.read(r'sounds/audio/' + str(i) + '.wav'))
# for i in range(1, 5):
    # midiDict[i].append(sf.read(r'sounds/midi/' + str(i) + '.mid'))
audioDict[1].append(r'sounds/audio/1/audio11.wav')
audioDict[1].append(r'sounds/audio/1/audio12.wav')
audioDict[1].append(r'sounds/audio/1/audio13.wav')
audioDict[1].append(r'sounds/audio/1/audio14.wav')
audioDict[2].append(r'sounds/audio/2/audio21.wav')
audioDict[2].append(r'sounds/audio/2/audio22.wav')
audioDict[2].append(r'sounds/audio/2/audio23.wav')
audioDict[2].append(r'sounds/audio/2/audio24.wav')


# Dictionary to keep track of currently playing sounds
playingSounds = {}

def chooseMode(label, modifier):  # choose between instrument and sample choice mode
    
    if label == 0:
        modifier = 1 if modifier == 0 else 0    # switch between modes
    return modifier

def chooseSound(label, instrument, modifier):   # choose the sound to play

    if label not in range(0, 5):
        print("Invalid class label")
        return

    # if in instrument choice mode, choose it and play the default sample (first one)
    if modifier == 0:
        instrument = label
        return (instrument, 1)
    
    # if in sample choice mode, choose the sample to play
    if modifier == 1:
        return (instrument, label)


def playMidi(midiToPlay):
    # Load the MIDI file
    pygame.mixer.music.load(midiDict[midiToPlay])

    # Play the MIDI file
    pygame.mixer.music.play()


def main(): # receive class label and outputs in real time
    end = False

    pygame.mixer.init()

    # default values
    modifier = 0    # 0 - instrument choice mode / 1 - sample choice mode
    instrument = 1  # drums
    
    testBusLabel = [2, 1, 0, 3, 1, 0, 4, 1, 0, 2, 1, 0, 3, 1, 0]

    pygame.mixer.Sound(r"sounds/audio/audioBeat.wav").play(-1)  # -1 means loop indefinitely
    tempo = 72 # bpm
    delay = int(60000 / tempo)   # ms

    index = 0
    while not end:
        print()
        

        label = testBusLabel[index]; print("Label: ", label)
    
        if label in audioDict:  # if the label is a valid non modifier class

            if modifier == 0:
                print("Instrument choice mode")
                instrument = label; print("Instrument", instrument)

            elif modifier == 1:
                print("Sample choice mode")
                audioToPlay = chooseSound(label, instrument, modifier); print("Audio", audioToPlay)  # tuple (instrument, sample)
            

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

        if label == 0:
            modifier = 1 if modifier == 0 else 0
            print("Modifier: ", modifier)

        # temporary testing ending condition
        end = input("Next? (y/n): ") == 'n'
        index += 1
        if index == len(testBusLabel):
            end = True
        

        

if __name__ == "__main__":
    main()