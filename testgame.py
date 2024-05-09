import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("One Second Screen")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 50)

def display_screen_for_one_second():
    # Display screen
    screen.fill(WHITE)
    draw_text("Hello!", font, BLACK, screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    pygame.display.flip()

    # Wait for one second
    pygame.time.delay(3000)  # 1000 milliseconds = 1 second

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def main():
    display_screen_for_one_second()

    # Continue with your game logic or exit
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
