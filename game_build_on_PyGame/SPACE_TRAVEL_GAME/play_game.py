import pygame
from pygame.locals import *

def play():
    pygame.init()
    SCREEN = pygame.display.set_mode((800, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("SPACE TRAVEL")

__author__ = 'liuchuang'
