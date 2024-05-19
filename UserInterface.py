import pygame
import sys
import threading
import time
from classToSound_neuro import *

# --- constants ---

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

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

def change_colored_squares(color_squares, received_integer):
    for color_square_data in color_squares:
        if color_square_data["id"] == str(received_integer):
            color_square_data["square"].set_permanent_green()

def display_icons(screen, screen_width, screen_height):
    icon_size = (screen_width / 15, screen_width / 15)
    icons = []
    positions = [
        (screen_width / 32.4 + screen_width / 5.1, screen_height / 20 + screen_width / (2 * 5.1)),
        (screen_width / 1.3 - screen_width / 15, screen_height / 1.5384 + screen_width / (2 * 5.1)),
        (screen_width / 32.4 + screen_width / 5, screen_height / 1.5384 + screen_width / (2 * 5.1)),
        (screen_width / 1.3 - screen_width / 15, screen_height / 20 + screen_width / (2 * 5.1))
        
    ]

    for i, position in enumerate(positions):
        icon = pygame.image.load(f'Icons/icon{i + 1}.png')
        icon = pygame.transform.scale(icon, icon_size)
        icons.append((icon, position))
        screen.blit(icon, position)

    return icons

def display_menu_icon(screen, screen_width, screen_height, label):
    icon_size = (screen_width/15, screen_width/15)
    icon_position = (screen_width / 2.49 + 100, screen_height / 2.857 - 150)

    icon = pygame.image.load(f'Icons/icon{label}.png')
    icon = pygame.transform.scale(icon, icon_size)
    screen.blit(icon, icon_position)

def display_play_icon(screen, screen_width, screen_height, sample):
    icon_size = (screen_width/15, screen_width/15)
    icon = pygame.image.load(f'Icons/play.png')
    icon = pygame.transform.scale(icon, icon_size)
    
    positions = [
        (screen_width / 32.4 + screen_width / 5.1, screen_height / 20 ),
        (screen_width / 1.3 - screen_width / 15, screen_height / 1.5384 ),
        (screen_width / 32.4 + screen_width / 5, screen_height / 1.5384 ),
        (screen_width / 1.3 - screen_width / 15, screen_height / 20 )
    ]

    screen.blit(icon, positions[sample-1])



# --- main ---

def main():
    pygame.init()

    # Thread to play sounds
    sound_thread = threading.Thread(target=playSounds)
    sound_thread.start()

    # Allow the sound thread to start
    time.sleep(1)

    # Set up the screen
    screen_width = 800
    screen_height = 600
    fenetre = pygame.display.set_mode((screen_width, screen_height))

    current_time = pygame.time.get_ticks()

    default_colored_square_color = BLACK
    color_squares = []

    square_info = [
        {"rect": pygame.Rect(screen_width / 32.4 - screen_width / 530, screen_height / 20 - screen_height / 250, screen_width / 5, screen_width / 5), "default_color": default_colored_square_color, "id": "1"},
        {"rect": pygame.Rect(screen_width / 32.4 - screen_width / 530, screen_height / 1.5384 - screen_height / 250, screen_width / 5, screen_width / 5), "default_color": default_colored_square_color, "id": "3"},
        {"rect": pygame.Rect(screen_width / 1.3 - screen_width / 530, screen_height / 20 - screen_height / 250, screen_width / 5, screen_width / 5), "default_color": default_colored_square_color, "id": "4"},
        {"rect": pygame.Rect(screen_width / 1.3 - screen_width / 530, screen_height / 1.5384 - screen_height / 250, screen_width / 5, screen_width / 5), "default_color": default_colored_square_color, "id": "2"},
        {"rect": pygame.Rect(screen_width / 2.49 - screen_width / 530, screen_height / 2.857 - screen_height / 250, screen_width / 5, screen_width / 5), "default_color": default_colored_square_color, "id": "0"}
    ]

    for info in square_info:
        color_square = ColorSwitchingSquare(info["rect"], info["default_color"])
        color_squares.append({"square": color_square, "id": info["id"]})

    # Frequency of square show/hide (seconds)
    frequency = [1, 2, 4, 8, 16]
    delays = [500 / f for f in frequency]

    # Positions and sizes for each square
    square_params = [
        {"position": (screen_width / 32.4, screen_height / 20), "delay": delays[1]},
        {"position": (screen_width / 32.4, screen_height / 1.5384), "delay": delays[3]},
        {"position": (screen_width / 1.3, screen_height / 20), "delay": delays[4]},
        {"position": (screen_width / 1.3, screen_height / 1.5384), "delay": delays[2]},
        {"position": (screen_width / 2.49, screen_height / 2.857), "delay": delays[0]}
    ]

    squares = []
    for params in square_params:
        rect = pygame.Rect(params["position"][0], params["position"][1], screen_width / 5.1, screen_width / 5.1)
        square = Square(rect, current_time, params["delay"])
        squares.append(square)

    previous_instrument = 1
    mode = 0 #instrument choosing
    sample = -1
    playing_instrument_1_sample_1 = False
    playing_instrument_1_sample_2 = False
    playing_instrument_1_sample_3= False
    playing_instrument_1_sample_4 = False
    
    playing_instrument_2_sample_1 = False
    playing_instrument_2_sample_2 = False
    playing_instrument_2_sample_3= False
    playing_instrument_2_sample_4 = False

    playing_instrument_3_sample_1 = False
    playing_instrument_3_sample_2 = False
    playing_instrument_3_sample_3= False
    playing_instrument_3_sample_4 = False
    
    playing_instrument_4_sample_1 = False
    playing_instrument_4_sample_2 = False
    playing_instrument_4_sample_3= False
    playing_instrument_4_sample_4 = False

    display_icons_flag = True
    show_menu_icon = False
    playing = True

    playing_instrument_1 = False
    playing_instrument_2 = False
    playing_instrument_3 = False
    playing_instrument_4 = False

    instrument_menu = 0

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

            if mode == 0:                            #choosing instrument mode
                display_icons_flag = True
                show_menu_icon = False
                if label == 0:                       #go to previous intrument
                    mode = 1
                    display_icons_flag = False
                    show_menu_icon = True
                    instrument_menu = previous_instrument
                elif label != 0:                     #go to new instrument
                    mode = 1
                    previous_instrument = label
                    display_icons_flag = False
                    show_menu_icon = True
                    instrument_menu = label
                

            elif mode == 1:                          #instrument mode
                display_icons_flag = False
                show_menu_icon = True
                if label == 0:                       #go back to choosing instrument
                    mode = 0
                    display_icons_flag = True
                    show_menu_icon = False
                    instrument_menu = label                  
                  
                if instrument_menu == 1 and label != 0:
                    playing_instrument_1 = True
                    if label == 1 and playing_instrument_1_sample_1 == False:          #play sample 1
                        if playing_instrument_1_sample_2 == True:
                            playing_instrument_1_sample_2 = False
                        elif playing_instrument_1_sample_3 == True:
                            playing_instrument_1_sample_3 = False
                        elif playing_instrument_1_sample_4 == True:
                            playing_instrument_1_sample_4 = False
                        playing_instrument_1_sample_1 = True
       
                    elif label == 2 and playing_instrument_1_sample_2 == False:          #play sample 2
                        if playing_instrument_1_sample_1 == True:
                            playing_instrument_1_sample_1 = False
                        elif playing_instrument_1_sample_3 == True:
                            playing_instrument_1_sample_3 = False
                        elif playing_instrument_1_sample_4 == True:
                            playing_instrument_1_sample_4 = False
                        playing_instrument_1_sample_2 = True
                    
                    elif label == 3 and playing_instrument_1_sample_3 == False:          #play sample 3
                        if playing_instrument_1_sample_2 == True:
                            playing_instrument_1_sample_2 = False
                        elif playing_instrument_1_sample_1 == True:
                            playing_instrument_1_sample_1 = False
                        elif playing_instrument_1_sample_4 == True:
                            playing_instrument_1_sample_4 = False
                        playing_instrument_1_sample_3 = True
                    
                    elif label == 4 and playing_instrument_1_sample_4 == False:          #play sample 4 and stop other
                        if playing_instrument_1_sample_2 == True:
                            playing_instrument_1_sample_2 = False
                        elif playing_instrument_1_sample_3 == True:
                            playing_instrument_1_sample_3 = False
                        elif playing_instrument_1_sample_1 == True:
                            playing_instrument_1_sample_1 = False
                        playing_instrument_1_sample_4 = True 
                    
                    elif label == 1 and playing_instrument_1_sample_1 == True:           #stop playing sample 1 
                        playing_instrument_1_sample_1 = False
                        playing_instrument_1 = False
                    elif label == 2 and playing_instrument_1_sample_2 == True:           #stop playing sample 2
                        playing_instrument_1_sample_2 = False
                        playing_instrument_1 = False
                    elif label == 3 and playing_instrument_1_sample_3 == True:           #stop playing sample 3
                        playing_instrument_1_sample_3 = False
                        playing_instrument_1 = False
                    elif label == 4 and playing_instrument_1_sample_4 == True:           #stop playing sample 4
                        playing_instrument_1_sample_4 = False
                        playing_instrument_1 = False
           
                if instrument_menu == 2 and label != 0:
                    playing_instrument_2 = True
                    if label == 1 and playing_instrument_2_sample_1 == False:  # play sample 1
                        if playing_instrument_2_sample_2 == True:
                            playing_instrument_2_sample_2 = False
                        elif playing_instrument_2_sample_3 == True:
                            playing_instrument_2_sample_3 = False
                        elif playing_instrument_2_sample_4 == True:
                            playing_instrument_2_sample_4 = False
                        playing_instrument_2_sample_1 = True

                    elif label == 2 and playing_instrument_2_sample_2 == False:  # play sample 2
                        if playing_instrument_2_sample_1 == True:
                            playing_instrument_2_sample_1 = False
                        elif playing_instrument_2_sample_3 == True:
                            playing_instrument_2_sample_3 = False
                        elif playing_instrument_2_sample_4 == True:
                            playing_instrument_2_sample_4 = False
                        playing_instrument_2_sample_2 = True

                    elif label == 3 and playing_instrument_2_sample_3 == False:  # play sample 3
                        if playing_instrument_2_sample_2 == True:
                            playing_instrument_2_sample_2 = False
                        elif playing_instrument_2_sample_1 == True:
                            playing_instrument_2_sample_1 = False
                        elif playing_instrument_2_sample_4 == True:
                            playing_instrument_2_sample_4 = False
                        playing_instrument_2_sample_3 = True

                    elif label == 4 and playing_instrument_2_sample_4 == False:  # play sample 4 and stop other
                        if playing_instrument_2_sample_2 == True:
                            playing_instrument_2_sample_2 = False
                        elif playing_instrument_2_sample_3 == True:
                            playing_instrument_2_sample_3 = False
                        elif playing_instrument_2_sample_1 == True:
                            playing_instrument_2_sample_1 = False
                        playing_instrument_2_sample_4 = True

                    elif label == 1 and playing_instrument_2_sample_1 == True:  # stop playing sample 1
                        playing_instrument_2_sample_1 = False
                        playing_instrument_2 = False
                    elif label == 2 and playing_instrument_2_sample_2 == True:  # stop playing sample 2
                        playing_instrument_2_sample_2 = False
                        playing_instrument_2 = False
                    elif label == 3 and playing_instrument_2_sample_3 == True:  # stop playing sample 3
                        playing_instrument_2_sample_3 = False
                        playing_instrument_2 = False
                    elif label == 4 and playing_instrument_2_sample_4 == True:  # stop playing sample 4
                        playing_instrument_2_sample_4 = False
                        playing_instrument_2 = False

                if instrument_menu == 3 and label != 0:
                    playing_instrument_3 = True
                    if label == 1 and playing_instrument_3_sample_1 == False:  # play sample 1
                        if playing_instrument_3_sample_2 == True:
                            playing_instrument_3_sample_2 = False
                        elif playing_instrument_3_sample_3 == True:
                            playing_instrument_3_sample_3 = False
                        elif playing_instrument_3_sample_4 == True:
                            playing_instrument_3_sample_4 = False
                        playing_instrument_3_sample_1 = True

                    elif label == 2 and playing_instrument_3_sample_2 == False:  # play sample 2
                        if playing_instrument_3_sample_1 == True:
                            playing_instrument_3_sample_1 = False
                        elif playing_instrument_3_sample_3 == True:
                            playing_instrument_3_sample_3 = False
                        elif playing_instrument_3_sample_4 == True:
                            playing_instrument_3_sample_4 = False
                        playing_instrument_3_sample_2 = True

                    elif label == 3 and playing_instrument_3_sample_3 == False:  # play sample 3
                        if playing_instrument_3_sample_2 == True:
                            playing_instrument_3_sample_2 = False
                        elif playing_instrument_3_sample_1 == True:
                            playing_instrument_3_sample_1 = False
                        elif playing_instrument_3_sample_4 == True:
                            playing_instrument_3_sample_4 = False
                        playing_instrument_3_sample_3 = True

                    elif label == 4 and playing_instrument_3_sample_4 == False:  # play sample 4 and stop other
                        if playing_instrument_3_sample_2 == True:
                            playing_instrument_3_sample_2 = False
                        elif playing_instrument_3_sample_3 == True:
                            playing_instrument_3_sample_3 = False
                        elif playing_instrument_3_sample_1 == True:
                            playing_instrument_3_sample_1 = False
                        playing_instrument_3_sample_4 = True

                    elif label == 1 and playing_instrument_3_sample_1 == True:  # stop playing sample 1
                        playing_instrument_3_sample_1 = False
                        playing_instrument_3 = False
                    elif label == 2 and playing_instrument_3_sample_2 == True:  # stop playing sample 2
                        playing_instrument_3_sample_2 = False
                        playing_instrument_3 = False
                    elif label == 3 and playing_instrument_3_sample_3 == True:  # stop playing sample 3
                        playing_instrument_3_sample_3 = False
                        playing_instrument_3 = False
                    elif label == 4 and playing_instrument_3_sample_4 == True:  # stop playing sample 4
                        playing_instrument_3_sample_4 = False
                        playing_instrument_3 = False

                if instrument_menu == 4 and label != 0:
                    playing_instrument_4 = True
                    if label == 1 and playing_instrument_4_sample_1 == False:  # play sample 1
                        if playing_instrument_4_sample_2 == True:
                            playing_instrument_4_sample_2 = False
                        elif playing_instrument_4_sample_3 == True:
                            playing_instrument_4_sample_3 = False
                        elif playing_instrument_4_sample_4 == True:
                            playing_instrument_4_sample_4 = False
                        playing_instrument_4_sample_1 = True

                    elif label == 2 and playing_instrument_4_sample_2 == False:  # play sample 2
                        if playing_instrument_4_sample_1 == True:
                            playing_instrument_4_sample_1 = False
                        elif playing_instrument_4_sample_3 == True:
                            playing_instrument_4_sample_3 = False
                        elif playing_instrument_4_sample_4 == True:
                            playing_instrument_4_sample_4 = False
                        playing_instrument_4_sample_2 = True

                    elif label == 3 and playing_instrument_4_sample_3 == False:  # play sample 3
                        if playing_instrument_4_sample_2 == True:
                            playing_instrument_4_sample_2 = False
                        elif playing_instrument_4_sample_1 == True:
                            playing_instrument_4_sample_1 = False
                        elif playing_instrument_4_sample_4 == True:
                            playing_instrument_4_sample_4 = False
                        playing_instrument_4_sample_3 = True

                    elif label == 4 and playing_instrument_4_sample_4 == False:  # play sample 4 and stop other
                        if playing_instrument_4_sample_2 == True:
                            playing_instrument_4_sample_2 = False
                        elif playing_instrument_4_sample_3 == True:
                            playing_instrument_4_sample_3 = False
                        elif playing_instrument_4_sample_1 == True:
                            playing_instrument_4_sample_1 = False
                        playing_instrument_4_sample_4 = True

                    elif label == 1 and playing_instrument_4_sample_1 == True:  # stop playing sample 1
                        playing_instrument_4_sample_1 = False
                        playing_instrument_4 = False
                    elif label == 2 and playing_instrument_4_sample_2 == True:  # stop playing sample 2
                        playing_instrument_4_sample_2 = False
                        playing_instrument_4 = False
                    elif label == 3 and playing_instrument_4_sample_3 == True:  # stop playing sample 3
                        playing_instrument_4_sample_3 = False
                        playing_instrument_4 = False
                    elif label == 4 and playing_instrument_4_sample_4 == True:  # stop playing sample 4
                        playing_instrument_4_sample_4 = False
                        playing_instrument_4 = False

            if instrument_menu == 1:
                if playing_instrument_1 == True:
                    if playing_instrument_1_sample_1 == True:
                        sample = 1
                    elif playing_instrument_1_sample_2 == True:
                        sample = 2
                    elif playing_instrument_1_sample_3 == True:
                        sample = 3
                    elif playing_instrument_1_sample_4 == True:
                        sample = 4                
                else:
                    sample = -1                
            elif instrument_menu == 2:
                if playing_instrument_2 == True:
                    if playing_instrument_2_sample_1 == True:
                        sample = 1
                    elif playing_instrument_2_sample_2 == True:
                        sample = 2
                    elif playing_instrument_2_sample_3 == True:
                        sample = 3
                    elif playing_instrument_2_sample_4 == True:
                        sample = 4                
                else:
                    sample = -1                
            elif instrument_menu == 3:
                if playing_instrument_3 == True:
                    if playing_instrument_3_sample_1 == True:
                        sample = 1
                    elif playing_instrument_3_sample_2 == True:
                        sample = 2
                    elif playing_instrument_3_sample_3 == True:
                        sample = 3
                    elif playing_instrument_3_sample_4 == True:
                        sample = 4                
                else:
                    sample = -1   
            elif instrument_menu == 4:
                if playing_instrument_4 == True:
                    if playing_instrument_4_sample_1 == True:
                        sample = 1
                    elif playing_instrument_4_sample_2 == True:
                        sample = 2
                    elif playing_instrument_4_sample_3 == True:
                        sample = 3
                    elif playing_instrument_4_sample_4 == True:
                        sample = 4                
                else:
                    sample = -1   
            elif instrument_menu == 0:
                sample = -1         

        # Draw on the screen
        fenetre.fill(BLACK)

        # Draw the icons onto the window surface if the input is 0
        if display_icons_flag:
            display_icons(fenetre, screen_width, screen_height)

        if show_menu_icon:
            display_menu_icon(fenetre, screen_width, screen_height,previous_instrument)

        if playing and sample != -1:
            display_play_icon(fenetre, screen_width, screen_height,sample)

        for cs in color_squares:
            cs["square"].draw(fenetre)

        for square in squares:
            square.draw(fenetre)

        pygame.display.update()

if __name__ == "__main__":
    main()
