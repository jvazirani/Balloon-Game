
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2
import random
import time
import turtle  

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Balloon:
    """
    A class to represent a balloon that needs to be popped. It is represented by a cirle with a line 
    that is spawned within the boundries.
    """
    def __init__(self, color, screen_width=600, screen_height=400):
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Ranges for where balloons can be 
        self.y_start = 50
        self.y_end = 200
        self.x_start = 300
        self.x_end = 400
        self.count = 0
        self.temp = False
        self.respawn()
    
    def respawn(self):
        """
        Selects a random location on the screen to respawn
        """
        self.y = random.randint(self.y_start, self.y_end)
        self.x = random.randint(self.x_start, self.x_end)
        self.count += 1
    
    def draw(self, image):
        """
        Enemy is drawn as a circle onto the image

        Args:
            image (Image): The image to draw the enemy onto
        """
        cv2.circle(image, (self.x, self.y), 70, self.color, -1) 
        cv2.line(image, (self.x, self.y), (self.x, self.y + 400), self.color, 10) 
        # cv2.circle(image, (self.x, self.y), 25, self.color, 5)