# -*- coding:utf-8 -*-
# failed
import pygame
import sys
from pygame.locals import *
from PIL import Image

pygame.init()
screen = pygame.display.set_mode((255, 255))
pygame.display.set_caption("Gif Background")

background = pygame.image.load(r"D:\bitmaps\Chain.gif").convert_alpha()

while True:
    for event in pygame.event.get():
        if event.type in (pygame.QUIT, pygame.KEYUP):
            sys.exit()
    screen.blit(background, (0, 0))
    pygame.display.update()


__author__ = 'added new'
