import pygame
from pygame import mixer
from pygame import joystick
import random
import os
import json
# Test 2
# Initialize the pygame
pygame.init()

# Initialize Controller
joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(joystick.Joystick(i))
for joystick in joysticks:
    joystick.init()
with open(os.path.join("keys.json"), 'r+') as file:
    button_keys = json.load(file)

# 0: Left analog horizontal, 1: Left Analog Vertical, 2: Left Trigger
# 3: Right Analog Horizontal, 4: Right Analog Vertical, 5: Right Trigger
analog_keys = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1}

# Create a 800x800px screen
screenX = 800
screenY = 800
screen = pygame.display.set_mode((screenX, screenY))

# Background
# background = pygame.image.load("background1.png")

# Background Music
mixer.music.load("8-bit Throne Room.wav")
mixer.music.set_volume(0.35)
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("deathstar1.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("xwing2.png")
playerSize = 128
playerX = (screenX / 2) - (playerSize / 2)
playerY = (screenY / 5) * 4
playerX_change = 0
playerY_change = 0
playerSpeed = 0.8  # pixels to move

# Enemy
enemyImg = []
enemySize = 128
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemySpeed = []
enemy_count = 3

for i in range(enemy_count):
    enemyImg.append(pygame.image.load("tie2.png"))
    enemyX.append(random.randint(0, screenX - enemySize))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.6)
    enemyY_change.append(40)
    enemySpeed.append(0.6)  # pixels to move

# Lasers
# States: ready = waiting to be fired , fire = moving
laserImg = pygame.image.load("lasers.png")
laserSize = 128
laserX = 0
laserY = playerY - 32
laserX_change = 0
laserY_change = 1.2
laser_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('Starjedi.ttf', 32)
textX = 10
textY = 10

isOver = False


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 232, 80))
    screen.blit(score, (x, y))


def game_over_text():
    game_over = pygame.image.load("vader.png")
    screen.blit(game_over, (130, 60))
    mixer.music.stop()
    game_over_sound = mixer.Sound("8-bit Emperor's Throne Room.wav")
    game_over_sound.play()


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, index):
    screen.blit(enemyImg[index], (x, y))


def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x, y - 32))


def is_collision(enemy_x, enemy_y, laser_x, laser_y):
    if abs(enemy_x - laser_x) < 64 and abs(enemy_y - laser_y) < 32:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    screen.fill((18, 14, 20))

    # Background
    # screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -playerSpeed
            if event.key == pygame.K_RIGHT:
                playerX_change = playerSpeed
            if event.key == pygame.K_UP:
                playerY_change = -playerSpeed
            if event.key == pygame.K_DOWN:
                playerY_change = playerSpeed
            if event.key == pygame.K_SPACE:
                if laser_state == "ready":
                    laser_sound = mixer.Sound('laser sound.wav')
                    laser_sound.play()
                    laserX = playerX
                    laserY = playerY
                    fire_laser(laserX, laserY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

        # Handles analog inputs
        if event.type == pygame.JOYAXISMOTION:
            analog_keys[event.axis] = event.value
            # print(analog_keys)
            # Horizontal Analog
            if abs(analog_keys[0]) > .4:
                if analog_keys[0] < -.5:
                    playerX_change = -playerSpeed
                if analog_keys[0] > .5:
                    playerX_change = playerSpeed
            else:
                playerX_change = 0
            # Vertical Analog
            if abs(analog_keys[1]) > .4:
                if analog_keys[1] < -.5:
                    playerY_change = -playerSpeed
                if analog_keys[1] > .5:
                    playerY_change = playerSpeed
            else:
                playerY_change = 0
            # Triggers
            if analog_keys[4] > 0 or analog_keys[5] > 0:  # Left or Right trigger
                if laser_state == "ready":
                    laser_sound = mixer.Sound('laser sound.wav')
                    laser_sound.play()
                    laserX = playerX
                    laserY = playerY
                    fire_laser(laserX, laserY)

    # Ensure player is in bounds
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= screenX - playerSize:
        playerX = screenX - playerSize

    if playerY <= 0:
        playerY = 0
    elif playerY >= screenY - playerSize:
        playerY = screenY - playerSize
    # Enemy Movement
    for i in range(enemy_count):

        # Game Over
        if enemyY[i] >= playerY - (playerSize / 1.5):
            for j in range(enemy_count):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = enemySpeed[i]
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= screenX - enemySize:
            enemyX_change[i] = -enemySpeed[i]
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = is_collision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.set_volume(0.2)
            explosion_sound.play()
            laserY = playerY
            laser_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, screenX - enemySize)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Laser Movement
    if laserY <= -128:
        laserY = playerY
        laser_state = "ready"

    if laser_state == "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
