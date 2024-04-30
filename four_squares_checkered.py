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

    delay_duration = 10000  # In milliseconds
    start_time = pygame.time.get_ticks()  # Start time at initialization
    elapsed_time = 0  # Initialize elapsed time
    delay_complete = False  # Flag to track completion of delay

    # Load font for displaying stopwatch
    font = pygame.font.Font(None, 36)

    frequency1 = 10
    frequency2 = 20
    frequency3 = 30
    frequency4 = 40

    delay1 = 1000 / frequency1
    delay2 = 1000 / frequency2
    delay3 = 1000 / frequency3
    delay4 = 1000 / frequency4

    # Create multiple checkerboard squares with different toggle intervals
    squares_info = [
        {"rect": pygame.Rect(250, 100, 300, 300), "num_rows": 16, "num_cols": 16, "toggle_interval": delay1},
        {"rect": pygame.Rect(250, 600, 300, 300), "num_rows": 16, "num_cols": 16, "toggle_interval": delay2},
        {"rect": pygame.Rect(1050, 100, 300, 300), "num_rows": 16, "num_cols": 16, "toggle_interval": delay3},
        {"rect": pygame.Rect(1050, 600, 300, 300), "num_rows": 16, "num_cols": 16, "toggle_interval": delay4}
    ]

    squares = []
    for info in squares_info:
        checkerboard = CheckerboardSquare(info["rect"], info["num_rows"], info["num_cols"], info["toggle_interval"])
        squares.append(checkerboard)

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check if delay duration has passed
        if not delay_complete and elapsed_time >= delay_duration:
            delay_complete = True

        screen.fill(GREY)

        # Display stopwatch during delay and after
        display_stopwatch(screen, font, elapsed_time)

        # Draw squares only after delay completion
        if delay_complete:
            for square in squares:
                square.update()
                square.draw(screen)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
