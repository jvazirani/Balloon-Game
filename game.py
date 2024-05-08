"""
A game where you try to pop as many balloons as possible before they fly away into the sky

@author: Jaya Vazirani
@version: May 2024

edited from: https://i-know-python.com/computer-vision-game-using-mediapipe-and-python/
"""
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2
import pygame
import sys
import time 
from balloon import Balloon 
from balloonbundle import Balloonbundle
class Color: 
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

# Library Constants
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkPoints = mp.solutions.hands.HandLandmark
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
DrawingUtil = mp.solutions.drawing_utils
      
class Game:
    def __init__(self):
        # Load game elements
        self.balloons = []
        self.initialize_balloons(4)
        self.score = 0
        # cirlcle on fingers radius
        self.finger_radius = 25
        # Create the hand detector
        base_options = BaseOptions(model_asset_path='data/hand_landmarker.task')
        options = HandLandmarkerOptions(base_options=base_options,
                                                num_hands=2)
        self.detector = HandLandmarker.create_from_options(options)

        # TODO: Load video
        self.video = cv2.VideoCapture(1)

        # Pygame stuff
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Balloon Game")
        self.background_image = pygame.image.load("background.png")
        self.background_rect = self.background_image.get_rect()
        self.background_rect = self.background_rect.move((0, 0))  
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

        self.popper = pygame.image.load("pin.png")


    def initialize_balloons(self, num_balloons): 
        for i in range(num_balloons): 
            self.balloons.append(Balloon(Color.RED))

    
    def draw_landmarks_on_hand(self, image, detection_result):
        """
        Draws all the landmarks on the hand
        Args:
            image (Image): Image to draw on
            detection_result (HandLandmarkerResult): HandLandmarker detection results
        """
        # Get a list of the landmarks
        hand_landmarks_list = detection_result.hand_landmarks
        
        # Loop through the detected hands to visualize.
        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx]

            # Save the landmarks into a NormalizedLandmarkList
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
            ])

            # Draw the landmarks on the hand
            DrawingUtil.draw_landmarks(image,
                                       hand_landmarks_proto,
                                       solutions.hands.HAND_CONNECTIONS,
                                       solutions.drawing_styles.get_default_hand_landmarks_style(),
                                       solutions.drawing_styles.get_default_hand_connections_style())

    
    def check_balloon_intercept(self, finger_x, finger_y, balloon, image):
        """
        Determines if the finger position overlaps with the 
        enemy's position. Respawns and draws the enemy and 
        increases the score accordingly.
        Args:
            finger_x (float): x-coordinates of index finger
            finger_y (float): y-coordinates of index finger
            image (_type_): The image to draw on

        """
        # is this righ

        x_balloon = balloon.x + balloon.radius
        y_balloon = balloon.y + balloon.radius
        x_finger = finger_x 
        y_finger = finger_y

        if (balloon.radius + self.finger_radius)**2 > (x_finger - x_balloon)**2 + (y_finger - y_balloon)**2:
            return True
            # balloon.respawn()
        return False
        
    def check_balloon_pop(self, image, detection_result):
        """
        Draws a green circle on the index finger 
        and calls a method to check if we've intercepted
        with the enemy
        Args:
            image (Image): The image to draw on
            detection_result (HandLandmarkerResult): HandLandmarker detection results
        """
        # Get image details
        imageHeight, imageWidth = image.shape[:2]
         # Get a list of the landmarks
        hand_landmarks_list = detection_result.hand_landmarks
        
        # Loop through the detected hands to visualize.
        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx]
            # Get the coordinates of just the index finger 
            finger = hand_landmarks[HandLandmarkPoints.INDEX_FINGER_TIP.value]
            # Map the coordinates back to screen dimesnions 
            pixelCoord = DrawingUtil._normalized_to_pixel_coordinates(finger.x, finger.y, imageWidth, imageHeight)
            safe_balloons = []
            if pixelCoord:
                # cv2.circle(image, (pixelCoord[0], pixelCoord[1]), self.finger_radius, Color.GREEN, 5)
                self.screen.blit(self.popper, (pixelCoord[0], pixelCoord[1]))
                for balloon in self.balloons:
                    popped = self.check_balloon_intercept(pixelCoord[0], pixelCoord[1], balloon, image)
                    if popped: 
                        self.score +=1
                    else: 
                        safe_balloons.append(balloon) 
                self.balloons = safe_balloons      
    
    def run(self):
        """
        Main game loop. Runs until the 
        user presses "q".
        """    
        # TODO: Modify loop condition  
        running = True
        while self.video.isOpened() and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Get the current frame
            frame = self.video.read()[1]

            # Convert it to an RGB image
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Flip
            image = cv2.flip(image, 1)

            
            # Convert the image to a readable format and find the hands
            to_detect = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
            results = self.detector.detect(to_detect)
            cv2.putText(image, str(self.score), (50,50), fontFace= cv2.FONT_HERSHEY_COMPLEX, fontScale = 1, color = Color.GREEN, thickness = 2)

            # Draw the balloon on the image
            
            self.screen.blit(self.background_image, self.background_rect)

            for balloon in self.balloons: 
                balloon.draw(self.screen)

            for balloon in self.balloons:
                balloon.move()

            self.check_balloon_pop(image, results)

            # Draw the balloon image on top of the background

            # Update the display
            pygame.display.flip()

            # Change the color of the frame back
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # cv2.imshow('Hand Tracking', image)
            # Break the loop if the user presses 'q'
            if cv2.waitKey(50) & 0xFF == ord('q'):
                print(self.score)
                break
        self.video.release()
        cv2.destroyAllWindows()
        # Fill the screen with the background image



if __name__ == "__main__":        
    g = Game()
    g.run()


