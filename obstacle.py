import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import random
import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

OBSTACLE_RADIUS = 50

class Obstacle:
    """
    A class to represent an obstacle that is bad if you hit it in the game. 
    """
    def __init__(self):
        self.radius = OBSTACLE_RADIUS
        self.respawn()
        self.image = pygame.image.load("bomb.png")
        self.image = pygame.transform.scale(self.image, (66, 66))
        self.dx = 0
        self.dy = -4

    def respawn(self):
        """
        Selects a somewhat random location on the screen to respawn
        """
        self.y = random.randint(400, 1200)
        self.x = random.randint(0, 700)

    def move(self, score):
        self.dy = random.randint(-15, -1)
        self.dx = random.randint(-5, 5)
        self.x += self.dx
        self.y += self.dy
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
