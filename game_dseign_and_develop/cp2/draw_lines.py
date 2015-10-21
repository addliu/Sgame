import pygame
from pygame.locals import *
import sys
import random
__author__ = 'added new'

pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Draw Lines")
position = []
for each in range(1, 1001):
    pos_x = random.randint(0, 600)
    pos_y = random.randint(0, 500)
    position.append([pos_x, pos_y])

while True:
    for event in pygame.event.get():
        if event.type in (pygame.QUIT, pygame.KEYDOWN):
            sys.exit()

    color = 255, 255, 255
    screen.fill((0, 0, 0))
#   draw lines
    pygame.draw.lines(screen, color, False, position, 1)

    pygame.display.update()
