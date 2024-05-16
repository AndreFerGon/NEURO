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
import time

userInput = queue.Queue()

# Define a function to get user input
def getInput():

    while True:
        inputtings = input("\n!!! Choose a label: ")
        if inputtings.isdigit():
            userInput.put(int(inputtings))
        else:
            print(f"Invalid command! (0 - 1 - 2 - 3 - 4)\n")

def playSounds():

    # receive class label and outputs in real time
    # load sound files, each intrument (class) has 4 sound samples
    # 1 - drums, 2 - bass, 3 - guitar, 4 - vocals
    # 0 - no sound (mode class)

    # print the rules of playing
    print("\n\n!!! Choose a label:\n1 - drums,\n2 - bass,\n3 - guitar,\n4 - vocals\n")
    print("!!! Press 0 to switch between instrument and sample choice modes\n")
    print("!!! Press Ctrl+C to exit\n\n")

    # sound = pygame.mixer.Sound(r"sounds/_archive/audioBeat.wav")
    # sound.set_volume(0.3)  # Adjust the volume (0.0 - 1.0)
    # sound.play(-1)  # -1 means loop indefinitely
    tempo = 115 # bpm for Heart of Glass
    tempoDelay = int(60000 / tempo)   # ms
    magnet = 4 # 16th notes per bar

    # dictionary with class labels as keys and imported sound samples as values
    audioDict = {
    1: {1: [], 2: [], 3: [], 4: []},
    2: {1: [], 2: [], 3: [], 4: []},
    3: {1: [], 2: [], 3: [], 4: []},
    4: {1: [], 2: [], 3: [], 4: []}
}   
    
    pygame.mixer.pre_init(48000, -16, 2, 1024)   # setup mixer to avoid sound lag
    pygame.mixer.init()

    song = "heartOfGlass"
    loadsong(song, audioDict, tempo)
    
    
     # Set to keep track of currently playing sounds
    playingSounds = {}

    # default values
    mode = 0    # 0 - instrument choice mode / 1 - sample choice mode
    instrument = 1  # drums

    timezero = time.time()  # s

    while True:
        
        if not userInput.empty():
            # TO RECEIVE CLASS label FROM MATLAB
            label = int(userInput.get()); 
            # print("label: ", label, '\n')


        # if the label is a valid non mode class
            if label in (1, 2, 3, 4):

                print("\nPLAYING SOUNDS\n", playingSounds.keys())
            
            # change instrument
                if mode == 0:
                    instrument = label;
                    # print("Instrument", instrument, '\n')
                    mode = switchModes(mode)

                
            # change sound
                elif mode == 1:

                    audioToPlay = (instrument, label); # tuple (instrument, samplerate)
                    # print("Audio", audioToPlay, '\n')  
                    soundchoice = random.choice(audioDict[instrument][label])   # choose a random sound from the list

                # If the sound for this class is already playing, stop it
                    if audioToPlay in playingSounds:
                        print("\nStopping sound", audioToPlay, '\n')
                        alignAction(timezero, magnet, tempoDelay)
                        playingSounds[audioToPlay].stop()

                        del playingSounds[audioToPlay]
                    # If a sound of this instrument is already playing, switch them
                    elif audioToPlay[0] in [i[0] for i in playingSounds]:
                        
                        playingSounds[audioToPlay] = soundchoice
                        playInstrument_key = [key for key in playingSounds if key[0] == audioToPlay[0]][0]
                        print(f"\nSwitching {playInstrument_key} for {audioToPlay}", '\n')

                        alignAction(timezero, magnet, tempoDelay)
                        playingSounds[playInstrument_key].stop()
                        playingSounds[audioToPlay].play(-1)
                        del playingSounds[playInstrument_key]
                # Otherwise, start playing the sound in a loop    
                    else:
                        print("\nPlaying sound", audioToPlay, '\n')
                        playingSounds[audioToPlay] = soundchoice

                        alignAction(timezero, magnet, tempoDelay)
                        playingSounds[audioToPlay].play(-1)  # -1 means loop indefinitely
                    
        # if the label is a mode class, switch between modes
            if label == 0: 
                mode = switchModes(mode)

def alignAction(timezero, magnet, tempoDelay):
    # calculate the delay to play the sound

    delayToPlay = tempoDelay * magnet - 1000 * (time.time() - timezero) % int(tempoDelay * magnet)
    print("\ndelayToPlay: ", delayToPlay, '\n')
    time.sleep(delayToPlay / 1000)
    # play a test beep
    sound = pygame.mixer.Sound(r"sounds/heartOfGlass/1/11.wav")
    sound.play(maxtime=300)

def switchModes(mode):  # switch between instrument and sample choice mode
    
    mode = 1 if mode == 0 else 0
    print(f"Mode changed to {'instrument (0)' if mode == 0 else 'sample (1)'}\n")
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

def loadsong(song, audioDict, tempo):
    
    print("\nloading song stems...")
# for each folder of instrument type
    for instrument in [1, 2, 3, 4]:
    # for each sound file in the folder
        instrumentPath = f"sounds/{song}/{instrument}/"
        for stem in os.listdir(instrumentPath):
            print(stem, end='\t')

            # index = stem[:-4].lstrip(str(instrument)) # remove the instrument name and the .wav extension
            # stems = {}
            sound = pygame.mixer.Sound(instrumentPath + stem)
            # soundBeats = int(sound.get_length() / (tempo / 60))  # get the length of the sound in beats
            # print("Beats:", soundBeats)

            # add tuples of sound file paths to the dictionary
            audioDict[instrument][int(stem[1])].append(sound)
    print('\n')
    # print(audioDict)


def main():
    

    # have two threads, one for playing sounds and the other for receiving a real time input from the user

    # Thread to play sounds
    sound_thread = threading.Thread(target=playSounds)
    sound_thread.start()

    # sleep using os for 3 seconds to allow the sound thread to start
    time.sleep(1)

    # Thread to get user input
    input_thread = threading.Thread(target=getInput)
    input_thread.start()

    

    
    

        

if __name__ == "__main__":
    main()