import pygame
import sys
import socket
import threading


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



# --- main ---

def main():
    pygame.init()

    # Set up the screen
    screen_width = 800
    screen_height = 600
    fenetre = pygame.display.set_mode((screen_width, screen_height))

    current_time = pygame.time.get_ticks()

    # Start the socket communication in a separate thread
    
    default_colored_square_color = BLACK
    color_squares = []

    square_info = [
        {"rect": pygame.Rect(screen_width/32.4 - screen_width/530, screen_height/20 - screen_height/250, screen_width/5, screen_width/5), "default_color": default_colored_square_color, "id": "1"},
        {"rect": pygame.Rect(screen_width/32.4 - screen_width/530, screen_height/1.5384- screen_height/250, screen_width/5, screen_width/5), "default_color": default_colored_square_color, "id": "3"},
        {"rect": pygame.Rect(screen_width/1.3 - screen_width/530, screen_height/20- screen_height/250, screen_width/5, screen_width/5), "default_color": default_colored_square_color, "id": "4"},
        {"rect": pygame.Rect(screen_width/1.3 - screen_width/530, screen_height/1.5384- screen_height/250, screen_width/5, screen_width/5), "default_color": default_colored_square_color, "id": "2"},
        {"rect": pygame.Rect(screen_width/2.49 - screen_width/530, screen_height/2.857- screen_height/250, screen_width/5, screen_width/5), "default_color": default_colored_square_color, "id": "5"}
    ]
    
    for info in square_info:
        color_square = ColorSwitchingSquare(info["rect"], info["default_color"])
        color_squares.append({"square": color_square, "id": info["id"]})

    socket_thread = threading.Thread(target=handle_socket_communication, args=(color_squares,), daemon=True)
    socket_thread.start()


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

        # Draw on the screen
        fenetre.fill(BLACK)

        for cs in color_squares:
            cs["square"].draw(fenetre)

        for square in squares:
            square.draw(fenetre)


        pygame.display.update()

if __name__ == "__main__":
    main()
