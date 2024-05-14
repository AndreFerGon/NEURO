import pygame
import sys

# --- constants ---

BLACK = (80, 80, 80)
WHITE = (255, 255, 255)

# --- classes ---

class Square():
    def __init__(self, color, rect, time, delay):
        self.color = color
        self.rect = rect
        self.time = time
        self.delay = delay
        self.show = False

    def draw(self, screen):
        if self.show:
            pygame.draw.rect(screen, self.color, self.rect)

    def update(self, current_time):
        if current_time >= self.time:
            self.time = current_time + self.delay
            self.show = not self.show

# --- main ---

def main():
    pygame.init()

    # Set up the screen
    screen_width = 1600
    screen_height = 1000
    fenetre = pygame.display.set_mode((screen_width, screen_height))

    clock = pygame.time.Clock()

    current_time = pygame.time.get_ticks()

    # Frequency of square show/hide (seconds)
    frequency1 = 1    
    frequency2 = 2   
    frequency3 = 4
    frequency4 = 8    
    delay1 = 1000 // frequency1
    delay2 = 1000 // frequency2 
    delay3 = 1000 // frequency3
    delay4 = 1000 // frequency4

    # Create squares for each corner
    rect_top_left = Square(WHITE, pygame.Rect(150, 100, 350, 350), current_time, delay1)
    rect_top_right = Square(WHITE, pygame.Rect(150, 550, 350, 350), current_time, delay2)
    rect_bottom_left = Square(WHITE, pygame.Rect(1100, 100, 350, 350), current_time, delay3)
    rect_bottom_right = Square(WHITE, pygame.Rect(1100, 550, 350, 350), current_time, delay4)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Update current time
        current_time = pygame.time.get_ticks()

        # Update each square
        rect_top_left.update(current_time)
        rect_top_right.update(current_time)
        rect_bottom_left.update(current_time)
        rect_bottom_right.update(current_time)

        # Draw on the screen
        fenetre.fill(BLACK)

        rect_top_left.draw(fenetre)
        rect_top_right.draw(fenetre)
        rect_bottom_left.draw(fenetre)
        rect_bottom_right.draw(fenetre)

        pygame.display.update()

        # Cap the frame rate at 60 FPS
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
