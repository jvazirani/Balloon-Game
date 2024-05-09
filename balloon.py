
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import random
import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BALLOON_RADIUS = 70

class Balloon:
    """
    A class to represent a balloon that needs to be popped. It has coordinates and a speed and is represented 
    by a balloon image
    """
    def __init__(self):
        self.radius = BALLOON_RADIUS
        self.respawn()
        self.image = pygame.image.load("balloon.png")
        # TODO: make take away constants
        self.image = pygame.transform.scale(self.image, (66, 156))
        # Balloon speeds
        self.dx = 0
        self.dy = -4

    def respawn(self):
        """
        Selects a somewhat random location on the screen to respawn (towards the bottom of the screen and not too far left or right)
        """
        self.y = random.randint(400, 1200)
        self.x = random.randint(0, 700)

    def move(self, score):
        # Selects a somewhat random speed
        self.dy = random.randint(-15, -1)
        self.dx = random.randint(-5, 5)
        self.x += self.dx
        self.y += self.dy
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

