import pygame
from pygame.locals import *
import sys
__author__ = 'added new'

pygame.init()
screen = pygame.display.set_mode((600, 500))
myfont = pygame.font.Font(None, 60)
textImage = myfont.render("Hello python", True, (255, 255, 255))
pygame.display.set_caption("blit textimg")

while True:
    for event in pygame.event.get():
        if event.type in (pygame.QUIT, pygame.KEYDOWN):
            sys.exit()

    screen.fill((0, 200, 0))
    screen.blit(textImage, (100, 100))
    pygame.display.update()
