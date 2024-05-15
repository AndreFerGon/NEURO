# receive numeric class label (4 classes, 1-4) from matlab signal processing
# and output a sound based on a mode 5th class (0)

# import sys
import numpy as np
# import sounddevice as sd
import soundfile as sf
# import time
import pygame
import threading
import os
import queue
import random

userInput = queue.Queue()

# Define a function to get user input
def getInput():

    while True:
        inputtings = input("\n\n!!! Choose a label: ")
        if inputtings.isdigit():
            userInput.put(int(inputtings))
        else:
            print(f"Invalid command! (0 - 1 - 2 - 3 - 4)\n")

def playSounds(audioDict, delay):

    # choose the samplerate to play the sound
    pygame.mixer.pre_init(48000, -16, 2, 2048)  # 44100 Hz, 16-bit signed, stereo, buffer size 2048
    pygame.mixer.init()
    
     # Set to keep track of currently playing sounds
    playingSounds = {}

    # default values
    mode = 0    # 0 - instrument choice mode / 1 - sample choice mode
    instrument = 1  # drums

    while True:
        
        if not userInput.empty():
            # TO RECEIVE CLASS label FROM MATLAB
            label = int(userInput.get());
            # print("label: ", label, '\n')


        # if the label is a valid non mode class
            if label in (1, 2, 3, 4):
            
            # change instrument
                if mode == 0:
                    instrument = label;
                    mode = switchModes(mode)

            # change sound
                elif mode == 1:
                    audioToPlay = (instrument, label); print("Audio", audioToPlay, '\n')  # tuple (instrument, samplerate)
                

                # If the sound for this class is already playing, stop it
                    if audioToPlay in playingSounds:
                        playingSounds[audioToPlay].stop()
                        # print("here")
                        del playingSounds[audioToPlay]
                    else:
                # Otherwise, start playing the sound in a loop
                
                        soundchoice = random.choice(audioDict[audioToPlay[0]][audioToPlay[1]])
                        playingSounds[audioToPlay] = pygame.mixer.Sound(soundchoice[0])  # choice[0] is the sound data

                        pygame.time.wait(delay) # align next beat

                        playingSounds[audioToPlay].play(1)  # -1 means loop indefinitely


        # if the label is a mode class, switch between modes
            if label == 0: 
                mode = switchModes(mode)
                



def switchModes(mode):  # switch between instrument and sample choice mode
    
    mode = 1 if mode == 0 else 0
    print("New mode: ", mode, '\n')
    return mode

'''
def chooseSound(label, instrument, mode):   # choose the sound to play

# if in instrument choice mode, choose it and play the default sample (first one)
    if mode == 0:
        instrument = label
        return (instrument, 1)
    
# if in sample choice mode, choose the sample to play
    if mode == 1:
        return (instrument, label)
'''

'''
def playMidi(midiToPlay):
    # Load the MIDI file
    pygame.mixer.music.load(midiDict[midiToPlay])

    # Play the MIDI file
    pygame.mixer.music.play()
'''

def loadsong(song, audioDict):
    
    print("\nloading song stems...")
# for each folder of instrument type
    for instrument in [1, 2, 3, 4]:
    # for each sound file in the folder
        instrumentPath = f"sounds/{song}/{instrument}/"
        for stem in os.listdir(instrumentPath):
            print(stem, end='\t')

            # index = stem[:-4].lstrip(str(instrument)) # remove the instrument name and the .wav extension
            # stems = {}

            # add tuples of sound file paths to the dictionary
            audioDict[instrument][int(stem[1])].append(sf.read(instrumentPath + stem))
    print('\n')
    # print(audioDict)


def main(): # receive class label and outputs in real time
    # load sound files, each intrument (class) has 4 sound samples
    # 1 - drums, 2 - bass, 3 - guitar, 4 - vocals
    # 0 - no sound (mode class)

    # dictionary with class labels as keys and imported sound samples as values
    audioDict = audioDict = {
    1: {1: [], 2: [], 3: [], 4: []},
    2: {1: [], 2: [], 3: [], 4: []},
    3: {1: [], 2: [], 3: [], 4: []},
    4: {1: [], 2: [], 3: [], 4: []}
}


    song = "heartOfGlass"
    loadsong(song, audioDict)
    

    # sound = pygame.mixer.Sound(r"sounds/_archive/audioBeat.wav")
    # sound.set_volume(0.3)  # Adjust the volume (0.0 - 1.0)
    # sound.play(-1)  # -1 means loop indefinitely
    tempo = 115 # bpm for Heart of Glass
    delay = int(60000 / tempo)   # ms

    
    # have two threads, one for playing sounds and the other for receiving a real time input from the user

    # Thread to get user input
    input_thread = threading.Thread(target=getInput)
    input_thread.start()

    # Thread to play sounds
    sound_thread = threading.Thread(target=playSounds, args=(audioDict, delay))
    sound_thread.start()
    

        

if __name__ == "__main__":
    main()