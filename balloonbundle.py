import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2
import random
import time
from balloon import Balloon
class Color: 
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

class Balloonbundle: 

    def __init__(self, num_balloons, screen_width=600, screen_height=400):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.num_balloons = num_balloons
        self.balloons = []
        self.speed = 30
        self.initialize_balloons()

    def initialize_balloons(self): 
        for i in range(self.num_balloons): 
            self.balloons.append(Balloon(Color.RED))

    # def slow_speed():
    #     # if balloon popped
            # adjust speed


    def draw(self):
        for balloon in self.balloons:
            balloon.draw()
        


