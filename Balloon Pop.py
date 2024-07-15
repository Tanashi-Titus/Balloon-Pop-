import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
 
 
# Initialize
pygame.init()
 
# Create Window/Display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balloon Pop")
 
# Initialize Clock for FPS
fps = 30
clock = pygame.time.Clock()
 
# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height
 
# Images
imgBalloonRed = pygame.image.load('Resources/BalloonRed.png').convert_alpha()
rectBalloonRed = imgBalloonRed.get_rect()
rectBalloonRed.x, rectBalloonRed.y = 500, 300

imgBalloonBlue = pygame.image.load('Resources/BalloonBlue.png').convert_alpha()
rectBalloonBlue = imgBalloonBlue.get_rect()
rectBalloonBlue.x, rectBalloonBlue.y = 500, 300
# Variables
speedRed = 15
speedBlue = 10
score = 0
startTime = time.time()
totalTime = 20
 
# Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

def resetBalloonRed():
    rectBalloonRed.x = random.randint(100, width - 100)
    rectBalloonRed.y = height + 50

def resetBalloonBlue():
    rectBalloonBlue.x = random.randint(100, width - 100)
    rectBalloonBlue.y = height + 50
# Button replay game
def resetGame():
    global speed, score, startTime
    speed = 15
    score = 0
    startTime = time.time()
    resetBalloonRed()
    resetBalloonBlue()
# draw replay button
def drawButton(text, rect, color, text_color):
    pygame.draw.rect(window, color, rect)
    font = pygame.font.Font('Resources/Marcellus-Regular.ttf', 40)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    window.blit(text_surface, text_rect)


start_screen = True
start = False
while start_screen:
    window.fill((255, 255, 255))

    font = pygame.font.Font('Resources/Marcellus-Regular.ttf', 50)
    textTitle = font.render(f'Balloon Pop Game', True, (50, 50, 255))
    window.blit(textTitle, (450, 250))

    start_button = pygame.Rect(540, 350, 200, 50)

    mouse_pos = pygame.mouse.get_pos()
    if start_button.collidepoint(mouse_pos):
        drawButton("Start", start_button, (0, 150, 0), (255, 255, 255))
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        drawButton("Start", start_button, (0, 200, 0), (255, 255, 255))
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_screen = False
            pygame.quit()
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                start_screen = False
                start = True
                resetGame()

    pygame.display.update()
    clock.tick(fps)
# Main loop
while start:
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if replay_button.collidepoint(event.pos):
                resetGame()
            elif quit_button.collidepoint(event.pos):
                start = False
                pygame.quit()
                break
    # Apply Logic
    timeRemain = int(totalTime -(time.time()-startTime))
    if timeRemain < 0:
        window.fill((255,255,255))

        font = pygame.font.Font('Resources/Marcellus-Regular.ttf', 50)
        textScore = font.render(f'Your Score: {score}', True, (50, 50, 255))
        textTime = font.render(f'Time UP', True, (50, 50, 255))
        window.blit(textScore, (450, 350))
        window.blit(textTime, (530, 275))

        # Draw Replay Button
        replay_button = pygame.Rect(540, 450, 200, 50)
        quit_button = pygame.Rect(540, 520, 200, 50)
        # Change button color when hovering
        mouse_pos = pygame.mouse.get_pos()
        if replay_button.collidepoint(mouse_pos):
            drawButton("Replay", replay_button, (0, 150, 0), (255, 255, 255))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            drawButton("Replay", replay_button, (0, 200, 0), (255, 255, 255))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if quit_button.collidepoint(mouse_pos):
            drawButton("Quit", quit_button, (150, 0, 0), (255, 255, 255))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            drawButton("Quit", quit_button, (200, 0, 0), (255, 255, 255))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    else:
        # OpenCV
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        # Move the balloon up
        rectBalloonRed.y -= speedRed
        rectBalloonBlue.y -= speedBlue
        # check if balloon has reached the top without pop
        if rectBalloonRed.y < 0:
            resetBalloonRed()
            speedRed += 1
        if rectBalloonBlue.y < 0:
            resetBalloonBlue()
            speedBlue += 1

        if hands:
            hand = hands[0]
            x, y, z = hand['lmList'][8]
            if rectBalloonRed.collidepoint(x, y):
                resetBalloonRed()
                score += 10
                speedRed += 1
            if rectBalloonBlue.collidepoint(x, y):
                resetBalloonBlue()
                score += 5
                speedBlue += 1

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))
        window.blit(imgBalloonRed, rectBalloonRed)
        window.blit(imgBalloonBlue, rectBalloonBlue)

        font = pygame.font.Font('Resources/Marcellus-Regular.ttf', 50)
        textScore = font.render(f'Score: {score}', True, (50, 50, 255))
        textTime = font.render(f'Time: {timeRemain}', True, (50, 50, 255))
        window.blit(textScore, (35, 35))
        window.blit(textTime, (1000, 35))

    # Update Display
    pygame.display.update()
    # Set FPS
    clock.tick(fps)