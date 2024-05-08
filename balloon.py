
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
    def __init__(self, color, screen_width=1920, screen_height=1080):
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = 70
        # Ranges for where balloons can be 
        self.count = 0
        self.temp = False
        self.respawn()
        self.image = pygame.image.load("balloon.png")
        self.rect = self.image.get_rect()
        self.dx = 0
        self.dy = -4

    def respawn(self):
        """
        Selects a random location on the screen to respawn
        """
        # change so it might not be off screen 
        self.y = random.randint(0, 400)
        self.x = random.randint(0, 600)
        self.count += 1

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x < 0 or self.x > self.screen_width - 132 or self.y < 0 or self.y >  self.screen_height - 312: 
            self.respawn()
    
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

