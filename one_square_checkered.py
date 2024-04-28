import pygame
import sys

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128,128,128)

# Checkerboard Square Class
class CheckerboardSquare:
    def __init__(self, rect, num_rows, num_cols):
        self.rect = rect
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.colors = self.create_initial_colors()
        frequency = 10
        self.toggle_interval = 1000 / frequency  
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

# Main Function
def main():
    pygame.init()

    # Set up the screen
    screen_width = 1600
    screen_height = 1000
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Alternating Checkerboard")

    clock = pygame.time.Clock()
    fps = 60

    # Create the checkerboard square
    checkerboard_rect = pygame.Rect(500, 200, 600, 600)
    num_rows = 4
    num_cols = 4
    checkerboard = CheckerboardSquare(checkerboard_rect, num_rows, num_cols)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the checkerboard (toggle colors)
        checkerboard.update()

        # Fill the screen with black
        screen.fill(GREY)

        # Draw the checkerboard
        checkerboard.draw(screen)

        # Update the display
        pygame.display.flip()

        clock.tick(fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
