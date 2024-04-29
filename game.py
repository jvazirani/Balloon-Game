"""
A game where you try to get down safely by popping the balloons

@author: Jaya Vazirani
@version: May 2024

edited from: https://i-know-python.com/computer-vision-game-using-mediapipe-and-python/
"""
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2
import random
import time 
from balloon import Balloon 
from balloonbundle import Balloonbundle

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
        self.score = 0
        self.level = 1  
        # TODO: Initialize the enemy

        self.balloon_bundle = Balloonbundle(4)
        # Create the hand detector
        base_options = BaseOptions(model_asset_path='data/hand_landmarker.task')
        options = HandLandmarkerOptions(base_options=base_options,
                                                num_hands=2)
        self.detector = HandLandmarker.create_from_options(options)

        # TODO: Load video
        self.video = cv2.VideoCapture(1)


    
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
        x_intercept = finger_x < balloon.x + 10 and finger_x > balloon.x - 10
        y_intercept = finger_y < balloon.y + 10 and finger_y > balloon.y - 10
        if(x_intercept and y_intercept): 
            # balloon.respawn()
            self.score += 1
            self.temp = True
        
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
            thumb = hand_landmarks[HandLandmarkPoints.THUMB_TIP.value]

            # Map the coordinates back to screen dimesnions 
            pixelCoord = DrawingUtil._normalized_to_pixel_coordinates(finger.x, finger.y, imageWidth, imageHeight)
            pixelCoord_thumb = DrawingUtil._normalized_to_pixel_coordinates(thumb.x, thumb.y, imageWidth, imageHeight)

            if pixelCoord:
                #Draw the circle 
                cv2.circle(image, (pixelCoord[0], pixelCoord[1]), 25, GREEN, 5)
                self.check_balloon_intercept(pixelCoord[0], pixelCoord[1], self.green_balloon, image)

            if pixelCoord_thumb:
                cv2.circle(image, (pixelCoord_thumb[0], pixelCoord_thumb[1]), 25, RED, 5)
                self.check_balloon_intercept(pixelCoord_thumb[0], pixelCoord_thumb[1], self.red_balloon, image)

            # elif (finger_intersect and thumb_intersect):
            #     self.green_enemy.respawn()
            #     self.red_enemy.respawn()

            # THUMB_TIP
            
    
    def run(self):
        """
        Main game loop. Runs until the 
        user presses "q".
        """    
        # TODO: Modify loop condition  
        while self.video.isOpened():
            # Get the current frame
            frame = self.video.read()[1]

            # Convert it to an RGB image
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Flip
            image = cv2.flip(image, 1)

            # Draw the enemy on the image
            self.green_balloon.draw(image)
            
            self.red_balloon.draw(image)
            
            # draw score
            cv2.putText(image, str(self.score), (50,50), fontFace= cv2.FONT_HERSHEY_COMPLEX, fontScale = 1, color = GREEN, thickness = 2)
            # Convert the image to a readable format and find the hands
            to_detect = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
            results = self.detector.detect(to_detect)

            self.check_balloon_pop(image, results)
            if(self.score == 10 and self.level == 0): 
                curr_time = time.time()    
                print(curr_time)
                break

            # Change the color of the frame back
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cv2.imshow('Hand Tracking', image)
            # Break the loop if the user presses 'q'
            if cv2.waitKey(50) & 0xFF == ord('q'):
                print(self.score)
                break
        self.video.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":        
    g = Game()
    g.run()


