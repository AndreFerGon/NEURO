import pygame
import sys

# --- constants ---

BLACK = (0, 0, 0)
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
    screen_width = 1000
    screen_height = 800
    fenetre = pygame.display.set_mode((screen_width, screen_height))

    current_time = pygame.time.get_ticks()

    # Frequency of square show/hide (seconds)
    frequency1 = 10    
    frequency2 = 15   
    frequency3 = 25
    frequency4 = 31
    
    delay1 = 1000 // frequency1
    delay2 = 1000 // frequency2 
    delay3 = 1000 // frequency3
    delay4 = 1000 // frequency4

    # Create squares for each corner
    rect_top_left = Square(WHITE, pygame.Rect(150, 150, 200, 200), current_time, delay1)
    rect_top_right = Square(WHITE, pygame.Rect(150, 500, 200, 200), current_time, delay2)
    rect_bottom_left = Square(WHITE, pygame.Rect(screen_width - 350, 150, 200, 200), current_time, delay3)
    rect_bottom_right = Square(WHITE, pygame.Rect(screen_width - 350, 500, 200, 200), current_time, delay4)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

if __name__ == "__main__":
    main()
