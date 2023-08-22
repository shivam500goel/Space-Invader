import pygame
import random
import math
from pygame import mixer


# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
backg = pygame.image.load("back.png")

#background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load("player.png")
playerx = 370
playery = 480
playerx_chan = 0
# playery_chan = 0

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_chan = []
enemyy_chan = []
num_enemy = 6

for i in range(num_enemy):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(50, 150))
    enemyx_chan.append(3)
    enemyy_chan.append(32)

# flame
# ready state - you cant see the flame on screen
# fire state - you can see the flame moving
flameimg = pygame.image.load("flame.png")
flamex = 0
flamey = 480
# flamex_chan = 2
flamey_chan = 10
flame_s = "ready"

#score
score_v = 0
font = pygame.font.Font("freesansbold.ttf",32)

textx=10
texty=10

#gameiver text
over_font=pygame.font.Font("freesansbold.ttf",64)

def show_sr(x,y):
    score=font.render("score : " + str(score_v),True,(255,255,255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_flame(x, y):
    global flame_s
    flame_s = "fire"
    screen.blit(flameimg, (x + 16, y + 10))


def iscollision_ef(x1, y1, x2, y2):
    distance = math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))
    if distance < 27:
        return True
    else:
        return False

def game_over():
    over_text=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))


# game loop
running = True
while running:

    # RGB=red,green,blue
    screen.fill((0, 0, 0))
    # background image
    screen.blit(backg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is presse check wheter is right or left
        if event.type == pygame.KEYDOWN:
            # print("a keystroke is pressed")
            if event.key == pygame.K_LEFT:
                # print("left arrow is pressed")
                playerx_chan = -3.5
            if event.key == pygame.K_RIGHT:
                # print("right arrow is pressed")
                playerx_chan = 3.5

            if flame_s == "ready":
                # get the current x cordinate of spaceship
                if event.key == pygame.K_SPACE:
                    flame_sou = mixer.Sound("laser.wav")
                    flame_sou.play()
                    flamex = playerx
                    fire_flame(flamex, flamey)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("keystroke has been released")
                playerx_chan = 0

    # checking for boundaries movement

    # player
    playerx += playerx_chan
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    # enemy
    for i in range(num_enemy):
        #game over
        if enemyy[i]>440:
            for j in range(num_enemy):
                enemyy[j]=2000
            game_over()
            break
        enemyx[i] += enemyx_chan[i]
        if enemyx[i] <= 0:
            enemyx_chan[i] = 3
            enemyy[i] += enemyy_chan[i]
        elif enemyx[i] >= 736:
            enemyx_chan[i] = -3
            enemyy[i] += enemyy_chan[i]

        # collision
        collision = iscollision_ef(enemyx[i], enemyy[i], flamex, flamey)
        if collision:
            explosion_sou = mixer.Sound("explosion.wav")
            explosion_sou.play()
            flamey = 480
            flame_s = "ready"
            score_v += 5
            # print(score)
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(50, 150)

        enemy(enemyx[i], enemyy[i], i)

    # bullet movement
    if flamey <= 0:
        flamey = 480
        flame_s = "ready"

    if flame_s == "fire":
        fire_flame(flamex, flamey)
        flamey -= flamey_chan

    player(playerx, playery)
    show_sr(textx,texty)
    pygame.display.update()
