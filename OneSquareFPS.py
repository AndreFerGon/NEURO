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

def display_frame(screen, font, frames_counted):
    # Calculate seconds and milliseconds    

    frames_text = f"Frame Counter: {frames_counted}"
    text_surface = font.render(frames_text, True, BLACK)
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

   
    toggle_frame_interval = 1  # Toggles colors every 10 frames

    delay_duration = 5 #in seconds
    delay_frames = delay_duration * 60
    delay_complete = False

    # Load font for displaying stopwatch
    font = pygame.font.Font(None, 36)

    # Create checkerboard square
    checkerboard_rect = pygame.Rect(500, 200, 600, 600)
    checkerboard_square = CheckerboardSquare(checkerboard_rect, 8, 8, toggle_frame_interval)

    running = True
    frame_count = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(GREY)
        display_frame(screen,font,frame_count)

        if not delay_complete and delay_frames==frame_count:
            delay_complete = True

        # Update and draw the checkerboard square
        

        if delay_complete:
            checkerboard_square.update()
            checkerboard_square.draw(screen)           
        else:
            delay_complete = False
                
       
        # Increment frame count
        frame_count += 1
        clock.tick(fps)

        pygame.display.flip()
        

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
