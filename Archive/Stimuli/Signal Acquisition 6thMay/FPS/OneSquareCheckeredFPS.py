import pygame
import sys

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

# Checkerboard Square Class
class CheckerboardSquare:
    def __init__(self, rect, num_rows, num_cols, toggle_frame_interval):
        self.rect = rect
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.colors = self.create_initial_colors()
        self.toggle_frame_interval = toggle_frame_interval

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

    def update(self, frame_count):
        if frame_count % self.toggle_frame_interval == 0:
            # Toggle colors (switch between black and white)
            for row in range(self.num_rows):
                for col in range(self.num_cols):
                    self.colors[row][col] = WHITE if self.colors[row][col] == BLACK else BLACK

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

def display_frame(screen, font, frames_counted, frames_counted_stimuli, elapsed_time):
    # Calculate seconds and milliseconds    
    seconds = elapsed_time // 1000
    milliseconds = elapsed_time % 1000

    frames_text_1 = f"Frame Counter: {frames_counted}; " 
    frames_text_2 = f"Stimuli Frame: {frames_counted_stimuli}; " 
    frames_text_3 = f"Elapsed Time: {seconds}.{milliseconds:03d} seconds"

    text_surface = font.render(frames_text_1, True, BLACK)
    screen.blit(text_surface, (10, 10))
    text_surface = font.render(frames_text_2, True, BLACK)
    screen.blit(text_surface, (10, 25))
    text_surface = font.render(frames_text_3, True, BLACK)
    screen.blit(text_surface, (10, 40))

def main():
    pygame.init()

    # Set up the screen
    screen_width = 1620
    screen_height = 1000
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Checkerboards with Different Intervals")

    clock = pygame.time.Clock()
    fps = 60;   
   
    #toggle_frame_interval = 2 #30Hz
    #toggle_frame_interval = 3 #20Hz
    #toggle_frame_interval = 4 #15Hz
    toggle_frame_interval = 5 #12Hz
    #toggle_frame_interval = 6 #10Hz
    #toggle_frame_interval = 7 #8.57Hz
    #toggle_frame_interval = 8 #7.5Hz

    delay_duration = 3 #in seconds
    delay_frames = delay_duration * 60
    delay_complete = False

    stimuli_duration = 100 #in seconds
    stimuli_frames = stimuli_duration * 60

    start_time = pygame.time.get_ticks()  # Start time at initialization
    elapsed_time = 0  # Initialize elapsed time

    # Load font for displaying stopwatch
    font = pygame.font.Font(None, 20)

    squares_info = [
        {"rect": pygame.Rect(500, 200, 600, 600), "num_rows": 8, "num_cols": 8, "toggle_interval": toggle_frame_interval},
        
    ]

    squares = []
    for info in squares_info:
        checkerboard = CheckerboardSquare(info["rect"], info["num_rows"], info["num_cols"], info["toggle_interval"])
        squares.append(checkerboard)

    running = True
    frame_count_stimuli = 0
    frame_count = 0

    while running:

        elapsed_time = pygame.time.get_ticks() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(GREY)
        display_frame(screen, font, frame_count , frame_count_stimuli, elapsed_time)

        if not delay_complete and frame_count_stimuli >= delay_frames:
            delay_complete = True
            frame_count_stimuli = 0  # Reset frame count after delay is complete

        if delay_complete:
            if frame_count_stimuli <= stimuli_frames:
                checkerboard.update(frame_count_stimuli)
                checkerboard.draw(screen)
            else:
                delay_complete = False
                frame_count_stimuli = 0

        frame_count_stimuli += 1
        frame_count += 1
        clock.tick(fps)
        pygame.display.flip()
        

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
