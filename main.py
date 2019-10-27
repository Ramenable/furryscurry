# new python file
import pygame
import os
from pygame.locals import *
import sys
import math
import random
os.chdir("/Users/sophi/Documents/COLLEGE/Fall 2019/COMPSCI/hackGT")
# Initialize Python
pygame.init()
# Create canvas variable named window
window = pygame.display.set_mode((900,405))
# Title and Icon
pygame.display.set_caption("Furry Scurry")
icon = pygame.image.load("BunnyIcon.png")
pygame.display.set_icon(icon)

title = pygame.transform.scale(pygame.image.load('FurryScurry.png'), (520, 200))
#titleDesc = pygame.transform.scale(pygame.image.load('start.png'), (300, 100))
gameOver = pygame.transform.scale(pygame.image.load('GameOver.png'), (400, 150))

pygame.mixer.music.load("ToyDay.mp3")
pygame.mixer.music.play(-1, 0.0)

rabbit = pygame.image.load('2.png')
bg = pygame.image.load('Sky.png').convert() # BackGround
rd = pygame.image.load('SkyRoad.png').convert() # Road
bgX = 0
bgX2 = bg.get_width()
rdX = 0
rdX2 = rd.get_width()

# SNOW
white = [255, 255, 255]
transparent = (0, 0, 0, 0)
# Create an empty array
star_list = []
# Loop 10 times and add a star in a random x,y position
for i in range(10):
    x = random.randrange(0, 900)
    y = random.randrange(0, 405)
    star_list.append([x, y])

clock = pygame.time.Clock()
running = True
pause = 0
fallSpeed = 0

#Rabbit
class player(object):
    run = [pygame.image.load(str(x) + '.png') for x in range(1,4)]
    jump = [pygame.image.load('2.png')]
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.isJump = False
        self.jumpCount = 10 # this should not be 0
        self.runCount = 0
        self.falling = False

    def draw(self, window):
        # Jumping mechanics
        if not self.isJump:
            if keys[pygame.K_SPACE]:
                self.isJump = True
            self.hitbox = (self.x + 3, self.y + 10, self.width - 10, self.height - 10)
        else:
            title.fill(transparent)
            #titleDesc.fill(transparent)
            if self.jumpCount >= -10:
                # jumping follows the quadratic formula (jumpCount moves up and down)
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= (self.jumpCount ** 2) * 0.3 * neg
                self.jumpCount -= 1
            # ends and resets jump
            else:
                self.isJump = False
                self.jumpCount = 10
            self.hitbox = (self.x + 3, self.y + 10, self.width - 10, self.height - 10)

        if self.runCount > 42:
            self.runCount = 0
        window.blit(self.run[self.runCount//15], (self.x, self.y))
        #speed of bunny (how fast it looks)
        self.runCount += 3
        #pygame.draw.rect(window, (255,0,0), self.hitbox, 2  )


#Obstacle
class carrot(object):
    img = pygame.image.load("carrot.png")
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y,width, height)
        self.count = 0

    def draw(self, window):
        self.hitbox = (self.x + 47, self.y + 28, 24, 60)
        window.blit(self.img,(self.x, self.y))
        #pygame.draw.rect(window, (255,0,0), self.hitbox, 2) #(location, color, item, thickness of hitbox)
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False


def redrawGameWindow():
    # makes it grey and lets the circle move
    window.fill((255,255,255))
    window.blit(bg, (bgX, 0))
    window.blit(bg, (bgX2, 0))
    window.blit(rd, (rdX, 367))
    window.blit(rd, (rdX2, 367))
    window.blit(title, (100, -10))
    #window.blit(titleDesc, (250, 150))
    bunny.draw(window)
    for item in obstacles:
        item.draw(window)
    # updates displays
    pygame.display.update()

def endScreen():
    global pause, score, speed, obstacles
    pause = 0
    speed = 30
    obstacles = []
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                run = False
                bunny.falling = False
                bunny.jumping = False
        end = pygame.transform.scale(pygame.image.load('FurryScurry.png'), (500,220))
        window.blit(gameOver, (250, 150))
        pygame.display.update()
# main
bunny = player(50, 340, 34, 34)
speed = 30
obstacles = []
pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2, random.randrange(800, 1500))

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

#MAIN GAME LOOP
while running:
    for item in obstacles:
        if item.collide(bunny.hitbox):
            title.fill(transparent)
            #titleDesc.fill(transparent)
            bunny.falling = True
            if pause == 0:
                endScreen()
        item.x -= 6
        if item.x < item.width * -1:    #if the item is off the screen it is removed
            obstacles.pop(obstacles.index(item))
    clock.tick(speed)

    # SNOW
    # Process each star in the list
    for i in range(len(star_list)):
        # Draw the star
        g = random.randint(1, 2)
        pygame.draw.circle(window, white, star_list[i], g)
        # Move the star down one pixel
        star_list[i][1] += random.randrange(3, 5)
        #star_list[1][i] -= 1
        # If the star has moved off the bottom of the screen
        if star_list[i][1] > 405:
            # Reset it just above the top
            y = random.randrange(-50, -10)
            star_list[i][1] = y
            # Give it a new x position
            x = random.randrange(0, 1000)
            star_list[i][0] = x
    pygame.display.flip()

    bgX -= 2
    bgX2 -= 2
    rdX -= 6
    rdX2 -= 6

    if bgX < bg.get_width() * -1:  # If our bg is at the -width then reset its position
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()
    if rdX < rd.get_width() * -1:  # If our rd is at the -width then reset its position
        rdX = rd.get_width()
    if rdX2 < rd.get_width() * -1:
        rdX2 = rd.get_width()


    i = 1
    # gets a list of all events that are happening
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == USEREVENT+1: # Checks if timer goes off
            speed += .5 # Increases speed
        if event.type == USEREVENT+2:
            pygame.time.set_timer(USEREVENT+2, random.randrange(700, 2000))
        keys = pygame.key.get_pressed()
        if i == 1:
            if event.type == USEREVENT + 2:
                obstacles.append(carrot(1000, 280, 40, 78))
    # a list of key presses, if statements do whatever if their keys are pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if not(bunny.jumping):
            bunny.jumping = True

    redrawGameWindow()
