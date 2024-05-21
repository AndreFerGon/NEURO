import pygame
import sys
<<<<<<< HEAD
import socket
import threading

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Checkerboard Square Class
class CheckerboardSquare:
    def __init__(self, rect, num_rows, num_cols, toggle_interval):
        self.rect = rect
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.colors = self.create_initial_colors()
        self.toggle_interval = toggle_interval
        self.last_toggle_time = 0

    def create_initial_colors(self):
        colors = []
        for row in range(self.num_rows):
            color_row = []
            for col in range(self.num_cols):
                if (row + col) % 2 == 0:
                    color_row.append(BLACK)
                else:
                    color_row.append(WHITE)
            colors.append(color_row)
        return colors

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_toggle_time >= self.toggle_interval:
            # Toggle colors (switch between black and white)
            for row in range(self.num_rows):
                for col in range(self.num_cols):
                    self.colors[row][col] = WHITE if self.colors[row][col] == BLACK else BLACK
            self.last_toggle_time = current_time

    def draw(self, screen):
        cell_width = self.rect.width // self.num_cols
        cell_height = self.rect.height // self.num_rows

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_rect = pygame.Rect(self.rect.left + col * cell_width,
                                        self.rect.top + row * cell_height,
                                        cell_width,
                                        cell_height)
                pygame.draw.rect(screen, self.colors[row][col], cell_rect)
=======
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


>>>>>>> cbcc04a0f60b4a6ae28dc0774c11d62abba3ae98

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
<<<<<<< HEAD
            if current_time - self.timer_start_time >= 300: 
=======
            if current_time - self.timer_start_time >= 300:
>>>>>>> cbcc04a0f60b4a6ae28dc0774c11d62abba3ae98
                self.current_color = self.default_color
                self.timer_active = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect)

<<<<<<< HEAD
def display_stopwatch(screen, font, elapsed_time):
    # Calculate seconds and milliseconds
    seconds = elapsed_time // 1000
    milliseconds = elapsed_time % 1000

    stopwatch_text = f"Elapsed Time: {seconds}.{milliseconds:03d} seconds"
    text_surface = font.render(stopwatch_text, True, BLACK)
    screen.blit(text_surface, (720, 980))

def handle_socket_communication(color_squares):
    host = 'localhost'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Listening on {host}:{port}...")

    try:
        client_socket, addr = server_socket.accept()
        print(f"Connection established from {addr}")

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            
            received_message = data.decode().strip()
            received_integer = int(received_message)
            print(f"Received integer: {received_integer}")
            
            # Set the corresponding square to green
            for color_square_data in color_squares:
                if color_square_data["id"] == str(received_integer):
                    color_square_data["square"].set_permanent_green()
                    break
            
    except Exception as e:
        print(f"Error occurred: {e}")
    
    finally:
        client_socket.close()
        server_socket.close()
=======
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
>>>>>>> cbcc04a0f60b4a6ae28dc0774c11d62abba3ae98

def main():
    pygame.init()

<<<<<<< HEAD
    screen_width = 800
    screen_height = 600
=======
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
>>>>>>> cbcc04a0f60b4a6ae28dc0774c11d62abba3ae98

    color_squares = []

    square_info = [
<<<<<<< HEAD
        {"rect": pygame.Rect(screen_width/32.4 - screen_width/324, screen_height/20- screen_height/200, screen_width/5, screen_width/5), "default_color": RED, "id": "1"},
        {"rect": pygame.Rect(screen_width/32.4 - screen_width/324, screen_height/1.5384- screen_height/200, screen_width/5, screen_width/5), "default_color": RED, "id": "2"},
        {"rect": pygame.Rect(screen_width/1.3 - screen_width/324, screen_height/20- screen_height/200, screen_width/5, screen_width/5), "default_color": RED, "id": "3"},
        {"rect": pygame.Rect(screen_width/1.3 - screen_width/324, screen_height/1.5384- screen_height/200, screen_width/5, screen_width/5), "default_color": RED, "id": "4"},
        {"rect": pygame.Rect(screen_width/2.49 - screen_width/324, screen_height/2.857- screen_height/200, screen_width/5, screen_width/5), "default_color": RED, "id": "5"}
    ]

    
    for info in square_info:
        color_square = ColorSwitchingSquare(info["rect"], info["default_color"])
        color_squares.append({"square": color_square, "id": info["id"]})

    # Start the socket communication in a separate thread
    socket_thread = threading.Thread(target=handle_socket_communication, args=(color_squares,), daemon=True)
    socket_thread.start()

    # Set up the screen
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Checkerboards with Different Intervals")

    clock = pygame.time.Clock()
    fps = 60

    start_time = pygame.time.get_ticks()
    elapsed_time = 0

    font = pygame.font.Font(None, 20)

    frequency5 = 15
    frequency4 = 12
    frequency3 = 10
    frequency2 = 60 / 7
    frequency1 = 7.5

    delay1 = 1000 / frequency1
    delay2 = 1000 / frequency2
    delay3 = 1000 / frequency3
    delay4 = 1000 / frequency4
    delay5 = 1000 / frequency5

    checkerboard_squares = []

    checkerboard_info = [
        {"rect": pygame.Rect(screen_width/32.4, screen_height/20, screen_width/5.1, screen_width/5.1), "num_rows": 8, "num_cols": 8, "toggle_interval": delay1},
        {"rect": pygame.Rect(screen_width/32.4, screen_height/1.5384, screen_width/5.1, screen_width/5.1), "num_rows": 8, "num_cols": 8, "toggle_interval": delay2},
        {"rect": pygame.Rect(screen_width/1.3, screen_height/20, screen_width/5.1, screen_width/5.1), "num_rows": 8, "num_cols": 8, "toggle_interval": delay3},
        {"rect": pygame.Rect(screen_width/1.3, screen_height/1.5384, screen_width/5.1, screen_width/5.1), "num_rows": 8, "num_cols": 8, "toggle_interval": delay4},
        {"rect": pygame.Rect(screen_width/2.49, screen_height/2.857, screen_width/5.1, screen_width/5.1), "num_rows": 8, "num_cols": 8, "toggle_interval": delay5}
    ]

    for info in checkerboard_info:
        checkerboard_square = CheckerboardSquare(info["rect"], info["num_rows"], info["num_cols"], info["toggle_interval"])
        checkerboard_squares.append(checkerboard_square)

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(GREY)
        display_stopwatch(screen, font, elapsed_time)
        
        for color_square_data in color_squares:
            color_square_data["square"].update()
            color_square_data["square"].draw(screen)
        
        for checkerboard_square in checkerboard_squares:
            checkerboard_square.update()
            checkerboard_square.draw(screen)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()
=======
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
>>>>>>> cbcc04a0f60b4a6ae28dc0774c11d62abba3ae98

if __name__ == "__main__":
    main()
