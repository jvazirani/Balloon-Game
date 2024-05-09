
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2
import random
import time
import turtle  
import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Balloon:
    """
    A class to represent a balloon that needs to be popped. It is represented by a cirle with a line 
    that is spawned within the boundries.
    """
    def __init__(self):
        self.radius = 70
        # Ranges for where balloons can be 
        self.count = 0
        self.temp = False
        self.respawn()
        self.image = pygame.image.load("balloon.png")
        self.image = pygame.transform.scale(self.image, (66, 156))
        self.dx = 0
        self.dy = -4

    def respawn(self):
        """
        Selects a random location on the screen to respawn
        """
        # change so it might not be off screen 
        # Respawn at the bottom of the screen
        self.y = random.randint(400, 1200)
        self.x = random.randint(0, 700)
        self.count += 1

    def move(self, score):
        self.dy = random.randint(-15, -1)
        self.dx = random.randint(-5, 5)
        self.x += self.dx
        self.y += self.dy
        if self.y < 0: 
            score = score - 1
            # self.respawn()
    
    def draw(self, screen):
        """
        Enemy is drawn as a circle onto the image

        Args:
            image (Image): The image to draw the enemy onto
        """
        # # change because right now just drawing cirlce 
        # cv2.circle(image, (self.x, self.y), self.radius, self.color, -1) 
        # for i in range(312): 
        #     for j in range(132):
        #         if sum(self.image[i, j]):
        #             image[self.y + i, self.x + j, :] = self.image[i, j , :]
        screen.blit(self.image, (self.x, self.y))

        # image[self.y: self.y + 312, self.x: self.x + 132, :] = self.image
        # cv2.line(image, (self.x, self.y), (self.x, self.y + 400), self.color, 10) 
        # cv2.circle(image, (self.x, self.y), 25, self.color, 5)

