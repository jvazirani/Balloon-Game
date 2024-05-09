"""
A game where you try to pop as many balloons as possible before they fly away into the sky

@author: Jaya Vazirani
@version: May 2024

edited from: https://i-know-python.com/computer-vision-game-using-mediapipe-and-python/
"""
# Imports
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2
import pygame
import sys
from balloon import Balloon 
from obstacle import Obstacle
class Color: 
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

# Library Constants
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkPoints = mp.solutions.hands.HandLandmark
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
DrawingUtil = mp.solutions.drawing_utils
      
class Game:
    def __init__(self):
        # Load game elements (balloons and obstacles)
        self.balloons = []
        self.initialize_balloons(50)
        self.obstacles = []
        self.initialize_obstacles(5)

        # Initialize score
        self.score = 0
        # cirlcle on fingers radius
        self.finger_radius = 25

        # Create the hand detector
        base_options = BaseOptions(model_asset_path='data/hand_landmarker.task')
        options = HandLandmarkerOptions(base_options=base_options,
                                                num_hands=2)
        self.detector = HandLandmarker.create_from_options(options)

        # Load video
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

        # Initialize popper image
        self.popper = pygame.image.load("pin.png")
        self.popper = pygame.transform.scale(self.popper, (100, 100))
        self.explode = pygame.image.load("explode.png")


    def initialize_balloons(self, num_balloons): 
        for i in range(num_balloons): 
            self.balloons.append(Balloon())

    def initialize_obstacles(self, num_obstacles): 
        for i in range(num_obstacles): 
            self.obstacles.append(Obstacle())

    def display_neg_screen(self):
        explode = pygame.image.load("explode.png")
        explode = pygame.transform.scale(explode, (self.width, self.height))  # Resize image
        print("Image loaded successfully:", explode.get_rect())
        # Display screen with giant -1
        self.screen.fill(Color.WHITE)
        self.draw_text(str(-1), 'Arial', 30, Color.RED, self.screen, 50, 50) 
        self.screen.blit(explode, (self.width/2 - explode.get_width()/2, self.height/2 - explode.get_height()/2))  # Center the image
        pygame.display.flip()

        # Wait for one second
        pygame.time.delay(1000)  # 1000 milliseconds = 1 second

    
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
        """
        x_balloon = balloon.x + balloon.radius
        y_balloon = balloon.y + balloon.radius
        x_finger = finger_x 
        y_finger = finger_y
        if (balloon.radius + self.finger_radius)**2 > (x_finger - x_balloon)**2 + (y_finger - y_balloon)**2:
            return True
            # balloon.respawn()
        return False
    def check_obstacle_intercept(self, ifinger_x, ifinger_y, obstacle, image):
        """
        Determines if the finger position overlaps with the 
        enemy's position. Respawns and draws the enemy and 
        increases the score accordingly.
        """
        x_obstacle = obstacle.x + obstacle.radius
        y_obstacle = obstacle.y + obstacle.radius
        x_finger = ifinger_x 
        y_finger = ifinger_y
        if (obstacle.radius + self.finger_radius)**2 > (x_finger - x_obstacle)**2 + (y_finger - y_obstacle)**2:
            print("obstacle colided")
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
            safe_obstacles = []
            if pixelCoord:
               # Draws the popper image on screen
                self.screen.blit(self.popper, (pixelCoord[0], pixelCoord[1]))
                for balloon in self.balloons:
                    popped = self.check_balloon_intercept(pixelCoord[0], pixelCoord[1], balloon, image)
                    if popped: 
                        self.score +=1
                    else: 
                        safe_balloons.append(balloon) 
                self.balloons = safe_balloons 

                for obstacle in self.obstacles:
                    exploded = self.check_obstacle_intercept(pixelCoord[0], pixelCoord[1], obstacle, image)
                    if exploded: 
                        # We want to subtract score
                        # We want to change the imag
                        self.score = self.score - 1
                        self.display_neg_screen()
                    else: 
                        safe_obstacles.append(obstacle) 
                self.obstacles = safe_obstacles         

    def draw_text(self, text, font_name, font_size, color, surface, x, y):
        font = pygame.font.SysFont(font_name, font_size)
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_obj, text_rect)

    def main_menu(self):
        while True:
            self.screen.fill(Color.WHITE)
            self.draw_text("Welcome to Balloon slicer", 'Arial', 50, Color.GREEN, self.screen, self.width/2, self.height/3)
            
            # Draw Start Button
            start_button = pygame.Rect(300, 300, 200, 50)
            pygame.draw.rect(self.screen, Color.GREEN, start_button)
            self.draw_text("Start", 'Arial', 30, Color.WHITE, self.screen, start_button.centerx, start_button.centery)
            
            # Get mouse position and check for click
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            if start_button.collidepoint(mouse_pos):
                if mouse_click[0] == 1:  # Left mouse button clicked
                    return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    
    def run(self):
        # Main game loop
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
            
            self.screen.blit(self.background_image, self.background_rect)

            # Draw and move the balloons
            for balloon in self.balloons: 
                balloon.draw(self.screen)
                balloon.move(self.score)
            # Draw and move the obstacles
            for obstacle in self.obstacles: 
                obstacle.draw(self.screen)
                obstacle.move(self.score)

            # Draw score
            self.draw_text(str(self.score), 'Arial', 30, Color.GREEN, self.screen, 50, 50) 
            self.check_balloon_pop(image, results)

            # Update the display
            pygame.display.flip()
            if cv2.waitKey(50) & 0xFF == ord('q'):
                print(self.score)
                break
        self.video.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":        
    g = Game()
    g.main_menu()
    g.run()


