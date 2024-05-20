import numpy as np
import soundfile as sf
import pygame
import threading
import os
import queue
import random
import time

labelQueue = queue.Queue()

def playSounds(labelQueue):
    tempo = 115  # bpm for Heart of Glass
    tempoDelay = int(60000 / tempo)  # ms
    magnet = 4  # 16th notes per bar

    audioDict = {
        1: {1: None},
        2: {1: None},
        3: {1: None},
        4: {1: None}
    }

    pygame.mixer.pre_init(48000, -16, 2, 1024)
    pygame.mixer.init()

    song = "heartOfGlass"
    loadsong(song, audioDict)

    playingSounds = {}
    mode = 0
    timezero = time.time()

    while True:
        label = labelQueue.get()
        if label in (1, 2, 3, 4):
            audioToPlay = (label, 1)  # Play sample 1 from the selected instrument
            soundchoice = audioDict[label][1]
            if audioToPlay in playingSounds:
                print("\nStopping sound", audioToPlay, '\n')
                alignAction(timezero, magnet, tempoDelay)
                playingSounds[audioToPlay].stop()
                del playingSounds[audioToPlay]
            else:
                print("\nPlaying sound", audioToPlay, '\n')
                playingSounds[audioToPlay] = soundchoice
                alignAction(timezero, magnet, tempoDelay)
                playingSounds[audioToPlay].play(-1)
        else:
            print("Invalid input. Please enter 1, 2, 3, or 4.")

def alignAction(timezero, magnet, tempoDelay):
    delayToPlay = tempoDelay * magnet - 1000 * (time.time() - timezero) % int(tempoDelay * magnet)
    time.sleep(delayToPlay / 1000)
    sound = pygame.mixer.Sound(r"sounds/heartOfGlass/1/11.wav")
    sound.play(maxtime=300)

def loadsong(song, audioDict):
    for instrument in [1, 2, 3, 4]:
        instrumentPath = f"sounds/heartOfGlassDemo/"
        sound = pygame.mixer.Sound(instrumentPath + str(instrument) +".wav")
        audioDict[instrument][1] = sound

def input_thread(labelQueue):
    while True:
        user_input = input("Enter a number (1, 2, 3, or 4) to play the corresponding sound: ")
        try:
            label = int(user_input)
            if label not in (1, 2, 3, 4):
                print("Invalid input. Please enter 1, 2, 3, or 4.")
                continue
            labelQueue.put(label)
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    input_thread_ = threading.Thread(target=input_thread, args=(labelQueue,))
    input_thread_.start()
    
    playSounds(labelQueue)


if __name__ == "__main__":
    main()
