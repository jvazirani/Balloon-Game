import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balloon Game")

# Load the background image
background_image = pygame.image.load("background.png")  # Replace "background.jpg" with your background image path
background_rect = background_image.get_rect()
background_rect = background_rect.move((0, 0))  # Move the background rectangle to cover the entire screen

# Load the balloon image
balloon_image = pygame.image.load("balloon.png")  # Replace "balloon.png" with your balloon image path
balloon_rect = balloon_image.get_rect()
background_image = pygame.transform.scale(background_image, (width, height))

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fill the screen with the background image
    screen.blit(background_image, background_rect)

    # Draw the balloon image on top of the background
    screen.blit(balloon_image, ((width - balloon_rect.width) // 2, (height - balloon_rect.height) // 2))

    # Update the display
    pygame.display.flip()
