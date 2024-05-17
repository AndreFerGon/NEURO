import pygame
import sys
import socket
import threading
from classToSound_neuro2 import *

# --- constants ---

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0,255,0)
RED = (255,0,0)

# --- classes ---

class Square:
    def __init__(self, rect, time, delay):
        self.rect = rect
        self.time = time
        self.delay = delay
        self.color = WHITE

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self, current_time):
        if current_time >= self.time:
            self.time = current_time + self.delay
            self.color = BLACK if self.color == WHITE else WHITE

class ColorSwitchingSquare:
    def __init__(self, rect, default_color):
        self.rect = rect
        self.default_color = default_color
        self.current_color = default_color
        self.timer_active = False
        self.timer_start_time = 0

    def set_color(self, color):
        self.current_color = color

    def set_permanent_green(self):
        self.current_color = GREEN
        self.timer_active = True
        self.timer_start_time = pygame.time.get_ticks()  # Start timer

    def update(self):
        if self.timer_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.timer_start_time >= 300: 
                self.current_color = self.default_color
                self.timer_active = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect)


def change_colored_squares(color_squares,received_integer):
    for color_square_data in color_squares:
        if color_square_data["id"] == str(received_integer):
            color_square_data["square"].set_permanent_green()         



# --- main ---

def main():
    pygame.init()

    # have two threads, one for playing sounds and the other for receiving a real time input from the user

    # Thread to play sounds
    sound_thread = threading.Thread(target=playSounds)
    sound_thread.start()

    # sleep using os for 3 seconds to allow the sound thread to start
    time.sleep(1)

    # Thread to get user input
    input_thread = threading.Thread(target=getInput)
    input_thread.start()

    # Set up the screen
    screen_width = 800
    screen_height = 600
    fenetre = pygame.display.set_mode((screen_width, screen_height))

    current_time = pygame.time.get_ticks()

    # Start the socket communication in a separate thread
    
    default_colored_square_color = BLACK
    color_squares = []

    square_info = [
        {"rect": pygame.Rect(screen_width/32.4 - screen_width/530, screen_height/20 - screen_height/250, screen_width/5, screen_width/5), "default_color": default_colored_square_color, "id": "0"},
        {"rect": pygame.Rect(screen_width/32.4 - screen_width/530, screen_height/1.5384- screen_height/250, screen_width/5, screen_width/5), "default_color": default_colored_square_color, "id": "2"},
        {"rect": pygame.Rect(screen_width/1.3 - screen_width/530, screen_height/20- screen_height/250, screen_width/5, screen_width/5), "default_color": default_colored_square_color, "id": "3"},
        {"rect": pygame.Rect(screen_width/1.3 - screen_width/530, screen_height/1.5384- screen_height/250, screen_width/5, screen_width/5), "default_color": default_colored_square_color, "id": "1"},
        {"rect": pygame.Rect(screen_width/2.49 - screen_width/530, screen_height/2.857- screen_height/250, screen_width/5, screen_width/5), "default_color": default_colored_square_color, "id": "4"}
    ]
    
    for info in square_info:
        color_square = ColorSwitchingSquare(info["rect"], info["default_color"])
        color_squares.append({"square": color_square, "id": info["id"]})



    # Frequency of square show/hide (seconds)
    # Frequency of square show/hide (seconds)
    frequency = [8, 9.6, 12, 14.4, 16]
    delays = [500 / f for f in frequency]

    # Positions and sizes for each square
    square_params = [
        {"position": (screen_width / 32.4, screen_height / 20), "delay": delays[0]},
        {"position": (screen_width / 32.4, screen_height / 1.5384), "delay": delays[1]},
        {"position": (screen_width / 1.3, screen_height / 20), "delay": delays[2]},
        {"position": (screen_width / 1.3, screen_height / 1.5384), "delay": delays[3]},
        {"position": (screen_width / 2.49, screen_height / 2.857), "delay": delays[4]}
    ]

    squares = []
    for params in square_params:
        rect = pygame.Rect(params["position"][0], params["position"][1], screen_width / 5.1, screen_width / 5.1)
        square = Square(rect, current_time, params["delay"])
        squares.append(square)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update current time
        current_time = pygame.time.get_ticks()

        # Update each square
        for square in squares:
            square.update(current_time)

        for cs in color_squares:
            cs["square"].update() 

        while not labelQueue.empty():
            label = labelQueue.get()
            change_colored_squares(color_squares, label)

        # Draw on the screen
        fenetre.fill(BLACK)

        for cs in color_squares:
            cs["square"].draw(fenetre)

        for square in squares:
            square.draw(fenetre)


        pygame.display.update()

      

        


if __name__ == "__main__":
    main()
