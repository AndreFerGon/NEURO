import pygame
import sys
import threading
import time
import socket

# --- constants ---

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255 ,0)

# --- classes ---

class Square():
    def __init__(self, color, rect, time, delay):
        self.color = color
        self.rect = rect
        self.time = time
        self.delay = delay
        self.show = True  # Always show the square
        self.last_color_change = time  # Track the last time the color was changed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self, current_time,showing):
        if current_time - self.last_color_change >= self.delay:
            if showing == True:
                self.color = WHITE if self.color == BLACK else BLACK
                self.last_color_change = current_time
            else:
                self.color = BLACK    



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

def change_colored_squares(color_squares,correct_guess):
    for color_square_data in color_squares:
        if color_square_data["correct_guess"] != correct_guess:
            color_square_data["square"].set_permanent_green()

def client_handler(client_socket, input_queue):
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                input_queue.append(data.decode().strip())
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

# --- main ---

def main():
    pygame.init()

    # Set up the screen
    screen_width = 800
    screen_height = 600
    fenetre = pygame.display.set_mode((screen_width, screen_height))

    # Set up the font for the stopwatch
    font = pygame.font.SysFont(None, 55)

    # Start time for the stopwatch
    start_time = pygame.time.get_ticks()

    current_time = pygame.time.get_ticks()
    last_display_time = current_time  # Track the last time the square was displayed
    frequency_index = 0  # Track the current frequency index
    frequency_change_time = current_time  # Track the time of the last frequency change

    # Frequency array (Hz)
    frequencies = [1,2,4,8]

    # Initial frequency
    frequency = frequencies[frequency_index]
    delay = 500 // frequency

    correct_guess = False
    showing = False

    # Create the square
    rect_center = Square(WHITE, pygame.Rect(screen_width/3, screen_height/2-screen_width/6, screen_width/3, screen_width/3), current_time, delay)
    default_colored_square_color = BLACK

    color_squares = []

    square_info = [
        {"rect": pygame.Rect(screen_width/3-5, screen_height/2-screen_width/6-5, screen_width/2.9, screen_width/2.9), "default_color": default_colored_square_color,"correct_guess": correct_guess},
    ]

    for info in square_info:
        color_square = ColorSwitchingSquare(info["rect"], info["default_color"])
        color_squares.append({"square": color_square, "correct_guess": info["correct_guess"]})

    # Load icons for each frequency
    icon_paths = ["Icons/icon1.png", "Icons/icon2.png", "Icons/icon3.png", "Icons/icon4.png"]
    icons = [pygame.image.load(path) for path in icon_paths]

    # Scale the icons to desired size
    icon_size = (50, 50)  # Adjust size as needed
    icons = [pygame.transform.scale(icon, icon_size) for icon in icons]

    show_icon = False

    input_queue = []

    def setup_server():
        host = 'localhost'
        port = 12345
        # Create server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)  # Listen for incoming connections
        print(f"Server listening on {host}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            # Start a new thread to handle client communication
            client_thread = threading.Thread(target=client_handler, args=(client_socket, input_queue))
            client_thread.start()

    server_thread = threading.Thread(target=setup_server)
    server_thread.start()

 
   
    while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            
                # Update current time
                current_time = pygame.time.get_ticks()

                # Calculate the elapsed time for the stopwatch
                elapsed_time = current_time - start_time
                minutes = elapsed_time // 60000
                seconds = (elapsed_time % 60000) // 1000
                milliseconds = (elapsed_time % 1000) // 10
                stopwatch_text = f"{minutes:02}:{seconds:02}:{milliseconds:02}"
                stopwatch_surface = font.render(stopwatch_text, True, WHITE)

                # If 10 seconds have passed since last display time, switch to the next frequency
                if current_time - last_display_time >= 10000:
                    # Move to the next frequency
                    frequency_index = (frequency_index + 1) % len(frequencies)
                    frequency = frequencies[frequency_index]
                    delay = 500 // frequency
                    rect_center.delay = delay
                    last_display_time = current_time  # Update the last display time
                    frequency_change_time = current_time  # Update the frequency change time
                    show_icon = False
                    showing = False
                    #print(f"Frequency changed to {frequency} Hz with delay {delay} ms")

                # Update the square
                if current_time - frequency_change_time >= 5000:
                    showing = True
                    current_time = pygame.time.get_ticks()
                    
                    show_icon = True

                if input_queue:
                    user_input = input_queue.pop(0)
                    try:
                        user_index = int(user_input)
                        
                        
                        if showing == True:
                            if user_index - 1 == frequency_index:
                                print("Correct frequency")
                                correct_guess = True
                            else:
                                print("Wrong frequency")
                                correct_guess = False    
                                
                            change_colored_squares(color_squares, correct_guess)
                    except ValueError:
                        print("Invalid input. Please enter a number between 0 and 3.")

                rect_center.update(current_time,showing)
                for cs in color_squares:
                        cs["square"].update()
                
                # Draw on the screen
                fenetre.fill(BLACK)

                for cs in color_squares:
                    cs["square"].draw(fenetre)
                # Draw the square
                rect_center.draw(fenetre)

                # Blit the icon in the top-left corner
                if show_icon == True:
                    fenetre.blit(icons[frequency_index], (10, 10))

                # Draw the stopwatch on the screen
                fenetre.blit(stopwatch_surface, (screen_width - 200, 10))  # Adjust position as needed

                pygame.display.update()

if __name__ == "__main__":
    main()
