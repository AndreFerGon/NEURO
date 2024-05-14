# receive numeric class classLabel (4 classes, 1-4) from matlab signal processing
# and output a sound based on a modifier 5th class (0)

# import sys
import numpy as np
# import sounddevice as sd
import soundfile as sf
# import time
import pygame
import threading
import os
import queue

userInput = queue.Queue()

# Define a function to get user input
def getInput():

    while True:
        inputtings = input("Enter a command: ")
        if inputtings.isdigit():
            userInput.put(int(inputtings))
        else:
            print(f"Invalid command! (0 - 1 - 2 - 3 - 4)\n")

def playSounds(audioDict, delay):

     # Set to keep track of currently playing sounds
    playingSounds = {}

    # default values
    modifier = 0    # 0 - instrument choice mode / 1 - sample choice mode
    instrument = 1  # drums

    while True:
        
        if not userInput.empty():
            # TO RECEIVE CLASS classLabel FROM MATLAB
            classLabel = userInput.get(); print("classLabel: ", classLabel)
            print("classLabel: ", classLabel)

        # if the classLabel is a valid non modifier class
            if classLabel in audioDict:
            
            # change instrument
                if modifier == 0:
                    print("\n(Instrument choice mode) ")
                    instrument = classLabel; print("Instrument", instrument)
            # change sound
                elif modifier == 1:
                    print("\n(Sample choice mode) ")
                    audioToPlay = chooseSound(classLabel, instrument, modifier); print("Audio", audioToPlay)  # tuple (instrument, samplerate)
                

                # If the sound for this class is already playing, stop it
                    if audioToPlay in playingSounds:
                        playingSounds[audioToPlay].stop()
                        # print("here")
                        del playingSounds[audioToPlay]
                    else:
                # Otherwise, start playing the sound in a loop
                        choice = np.random.choice(audioDict[audioToPlay[0]][audioToPlay[1] - 1])
                        playingSounds[audioToPlay] = pygame.mixer.Sound(choice[0])

                        pygame.time.wait(delay) # align next beat

                        playingSounds[audioToPlay].play(1)  # -1 means loop indefinitely


        # if the classLabel is a modifier class
            if classLabel == 0: 
                modifier = 1 if modifier == 0 else 0
                print("Modifier: ", modifier)

        user_input = None


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

def loadsong(song, audioDict):
    
    print("loading song...\n")
# for each folder of instrument type
    for instrument in [1, 2, 3, 4]:
    # for each sound file in the folder
        instrumentPath = f"sounds/{song}/{instrument}/"
        for stem in os.listdir(instrumentPath):
            print(stem, flush=True)

            # index = stem[:-4].lstrip(str(instrument)) # remove the instrument name and the .wav extension
            # stems = {}

            # add tuples of sound file paths to the dictionary
            audioDict[instrument][int(stem[0])].append(sf.read(instrumentPath + stem))
    
    # print(audioDict)


def main(): # receive class classLabel and outputs in real time
    # load sound files, each intrument (class) has 4 sound samples
    # 1 - drums, 2 - bass, 3 - guitar, 4 - vocals
    # 0 - no sound (modifier class)

    # dictionary with class classLabels as keys and imported sound samples as values
    audioDict = audioDict = {
    1: {1: [], 2: [], 3: [], 4: []},
    2: {1: [], 2: [], 3: [], 4: []},
    3: {1: [], 2: [], 3: [], 4: []},
    4: {1: [], 2: [], 3: [], 4: []}
}


    song = "heartOfGlass"
    loadsong(song, audioDict)


    pygame.mixer.init()
    
    
    # sound = pygame.mixer.Sound(r"sounds/_archive/audioBeat.wav")
    # sound.set_volume(0.3)  # Adjust the volume (0.0 - 1.0)
    # sound.play(-1)  # -1 means loop indefinitely
    tempo = 115 # bpm for Heart of Glass
    delay = int(60000 / tempo)   # ms

    
    # have two threads, one for playing sounds and the other for receiving a real time input from the user

    # Start a new thread to get user input
    input_thread = threading.Thread(target=getInput)
    input_thread.start()

    # Start a new thread to play sounds
    sound_thread = threading.Thread(target=playSounds, args=(audioDict, delay))
    sound_thread.start()
    

        

if __name__ == "__main__":
    main()