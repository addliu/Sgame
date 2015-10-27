import pygame
from pygame.locals import *
from mylibrary import *


def main_menu(surface):
    font = pygame.font.SysFont("Ubuntu Mono", 36, bold=True)
    surface.blit(pygame.image.load(r"res/image/space.png"), (0, 0))
    print_text(font, 100, 100, "PRESS UP, DOWN, LEFT, RIGHT TO MOVE")
    print_text(font, 200, 300, "PRESS SPACE TO SELECT", (220, 220, 20))
    print_text(font, 200, 500, "PRESS RETURN TO SHOW MENU", (20, 20, 220))

    keys = pygame.key.get_pressed()
    # if keys[K_RETURN]:

__author__ = 'liuchuang'
