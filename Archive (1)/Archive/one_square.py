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
    screen_width = 1200
    screen_height = 800
    fenetre = pygame.display.set_mode((screen_width, screen_height))

    current_time = pygame.time.get_ticks()

    # Frequency of square show/hide (seconds)
    frequency1 =  36
   
    delay1 = 1000 // frequency1
    
    # Create squares for each corner
    rect_center = Square(WHITE, pygame.Rect(350, 100, 600, 600), current_time, delay1)
    #rect_ldr =  Square(WHITE, pygame.Rect( 200, 350, 200, 200), current_time, 0 )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update current time
        current_time = pygame.time.get_ticks()

        # Update each square
        rect_center.update(current_time)
        #rect_ldr.update(current_time)
 

        # Draw on the screen
        fenetre.fill(BLACK)

        rect_center.draw(fenetre)
        #rect_ldr.draw(fenetre)


        pygame.display.update()

if __name__ == "__main__":
    main()
