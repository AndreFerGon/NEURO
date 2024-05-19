import numpy as np
import soundfile as sf
import pygame
import threading
import os
import queue
import random
import time
import socket

labelQueue = queue.Queue()

def handle_socket_communication():
    host = 'localhost'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Listening on {host}:{port}...")

    try:
        client_socket, addr = server_socket.accept()
        print(f"Connection established from {addr}")
        return client_socket

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        server_socket.close()

def playSounds():
    tempo = 115  # bpm for Heart of Glass
    tempoDelay = int(60000 / tempo)  # ms
    magnet = 4  # 16th notes per bar

    audioDict = {
        1: {1: [], 2: [], 3: [], 4: []},
        2: {1: [], 2: [], 3: [], 4: []},
        3: {1: [], 2: [], 3: [], 4: []},
        4: {1: [], 2: [], 3: [], 4: []}
    }

    pygame.mixer.pre_init(48000, -16, 2, 1024)
    pygame.mixer.init()

    song = "heartOfGlass"
    loadsong(song, audioDict, tempo)

    playingSounds = {}
    mode = 0
    instrument = 1
    timezero = time.time()

    client_socket = handle_socket_communication()

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        received_message = data.decode().strip()
        label = int(received_message)
        print(f"Received integer: {label}")

        labelQueue.put(label)

        if label in (1, 2, 3, 4):
            print("\nPLAYING SOUNDS\n", playingSounds.keys())
            if mode == 0:
                instrument = label
                mode = switchModes(mode)
            elif mode == 1:
                audioToPlay = (instrument, label)
                soundchoice = random.choice(audioDict[instrument][label])
                if audioToPlay in playingSounds:
                    print("\nStopping sound", audioToPlay, '\n')
                    alignAction(timezero, magnet, tempoDelay)
                    playingSounds[audioToPlay].stop()
                    del playingSounds[audioToPlay]
                elif audioToPlay[0] in [i[0] for i in playingSounds]:
                    playingSounds[audioToPlay] = soundchoice
                    playInstrument_key = [key for key in playingSounds if key[0] == audioToPlay[0]][0]
                    print(f"\nSwitching {playInstrument_key} for {audioToPlay}", '\n')
                    alignAction(timezero, magnet, tempoDelay)
                    playingSounds[playInstrument_key].stop()
                    playingSounds[audioToPlay].play(-1)
                    del playingSounds[playInstrument_key]
                else:
                    print("\nPlaying sound", audioToPlay, '\n')
                    playingSounds[audioToPlay] = soundchoice
                    alignAction(timezero, magnet, tempoDelay)
                    playingSounds[audioToPlay].play(-1)
        elif label == 0:
            mode = switchModes(mode)

    client_socket.close()

def alignAction(timezero, magnet, tempoDelay):
    delayToPlay = tempoDelay * magnet - 1000 * (time.time() - timezero) % int(tempoDelay * magnet)
    print("\ndelayToPlay: ", delayToPlay, '\n')
    time.sleep(delayToPlay / 1000)
    sound = pygame.mixer.Sound(r"sounds/heartOfGlass/1/11.wav")
    sound.play(maxtime=300)

def switchModes(mode):
    mode = 1 if mode == 0 else 0
    print(f"Mode changed to {'instrument (0)' if mode == 0 else 'sample (1)'}\n")
    return mode

def loadsong(song, audioDict, tempo):
    print("\nloading song stems...")
    for instrument in [1, 2, 3, 4]:
        instrumentPath = f"sounds/{song}/{instrument}/"
        for stem in os.listdir(instrumentPath):
            print(stem, end='\t')
            sound = pygame.mixer.Sound(instrumentPath + stem)
            audioDict[instrument][int(stem[1])].append(sound)
    print('\n')

def main():
    sound_thread = threading.Thread(target=playSounds)
    sound_thread.start()

if __name__ == "__main__":
    main()
