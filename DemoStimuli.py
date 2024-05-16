import pygame
import sys
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

def main():
    pygame.init()

    screen_width = 800
    screen_height = 600

    color_squares = []

    square_info = [
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

if __name__ == "__main__":
    main()
