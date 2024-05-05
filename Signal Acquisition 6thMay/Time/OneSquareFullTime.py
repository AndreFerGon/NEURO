import pygame
import sys

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

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
                    #print("change")
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

def display_stopwatch(screen, font, elapsed_time):
    # Calculate seconds and milliseconds
    seconds = elapsed_time // 1000
    milliseconds = elapsed_time % 1000

    stopwatch_text = f"Elapsed Time: {seconds}.{milliseconds:03d} seconds"
    text_surface = font.render(stopwatch_text, True, BLACK)
    screen.blit(text_surface, (10, 10))

def main():
    pygame.init()

    # Set up the screen
    screen_width = 1620
    screen_height = 1000
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Checkerboards with Different Intervals")

    clock = pygame.time.Clock()
    fps = 60

    delay_duration = 3000  # In milliseconds
    stimuli_duration = 7000
    start_time = pygame.time.get_ticks()  # Start time at initialization
    start_time_beginning = pygame.time.get_ticks()
    elapsed_time = 0  # Initialize elapsed time
    delay_complete = False  # Flag to track completion of delay

    # Load font for displaying stopwatch
    font = pygame.font.Font(None, 20)

    frequency = 30
    #frequency = 20
    #frequency = 15
    #frequency = 12
    #frequency = 10
    #frequency = 60/7
    #frequency = 7.5

    delay = 1000 / frequency

    # Create multiple checkerboard squares with different toggle intervals
    squares_info = [
        {"rect": pygame.Rect(500, 200, 600, 600), "num_rows": 1, "num_cols": 1, "toggle_interval": delay},
        
    ]

    squares = []
    for info in squares_info:
        checkerboard = CheckerboardSquare(info["rect"], info["num_rows"], info["num_cols"], info["toggle_interval"])
        squares.append(checkerboard)

    running = True
    
    while running:
        elapsed_time = pygame.time.get_ticks() - start_time
        total_time = pygame.time.get_ticks() - start_time_beginning
        #print(elapsed_time)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(GREY)
        display_stopwatch(screen, font, total_time)

        if not delay_complete and elapsed_time >= delay_duration:
            delay_complete = True
            start_time = pygame.time.get_ticks()

        if delay_complete:
            # Draw squares for a limited time after delay completion
            if elapsed_time <= stimuli_duration:  # Adjust this duration as needed
                for square in squares:
                    square.update()
                    square.draw(screen)
                    
            else:
                # Reset delay state and start time
                delay_complete = False
                start_time = pygame.time.get_ticks()
                
        pygame.display.flip()
        clock.tick(fps)


    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()