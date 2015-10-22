import pygame
from pygame.locals import *
import sys
__author__ = 'added new'

pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Draw Ellipse")

while True:
    for event in pygame.event.get():
        if event.type in (pygame.QUIT, pygame.KEYDOWN):
            sys.exit()

    screen.fill((0, 200, 0))
    pygame.draw.ellipse(screen, (255, 255, 255), (300, 250, 100, 120), 0)
    pygame.display.update()

