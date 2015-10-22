import sys
import random
import math
import pygame
from pygame.locals import *

# main program begins
pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Circle Dome")
screen.fill((235, 235, 235))

pos_x = 300
pos_y = 250
radius = 200
angle = 360
# repeating loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        sys.exit()
        # increment angle
    angle += 1
    if angle >= 360:
        angle = 0
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = r, g, b
    # calculate coordinates
    x = math.cos(math.radians(angle)) * radius
    y = math.sin(math.radians(angle)) * radius
    # draw one step around the circle
    pos = (int(pos_x + x), int(pos_y + y))
    if angle % 3 == 0:
        pygame.draw.circle(screen, color, pos, 10, 0)
    elif angle % 3 == 1:
        pygame.draw.rect(screen, color, (pos[0], pos[1], 10, 10), 0)
    else:
        pygame.draw.ellipse(screen, color, (pos[0], pos[1], 10, 10), 0)

    pygame.display.update()

__author__ = 'added new'
