import pygame
import home
from pygame.locals import *
from mylibrary import *


def main_menu():
    while True:
        pygame.init()
        SCREEN = pygame.display.set_mode((800, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("SPACE TRAVEL")
        font = pygame.font.SysFont("Ubuntu Mono", 36, bold=True)
        SCREEN.blit(pygame.image.load(r"res/image/space.png"), (0, 0))
        print_text(font, 100, 200, "PRESS ARROWS TO MOVE")
        print_text(font, 200, 300, "PRESS SPACE TO SELECT", (220, 220, 20))
        print_text(font, 200, 400, "PRESS RETURN TO SHOW MENU", (20, 20, 220))
        pygame.display.flip()


__author__ = 'liuchuang'
