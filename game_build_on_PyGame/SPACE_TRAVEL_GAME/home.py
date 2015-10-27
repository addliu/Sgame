# coding:utf8

import pygame
import sys
from pygame.locals import *
from mylibrary import *
from main_menu import *

CAPTION = "SPACE TRAVEL"
HOME_BACKGROUND = r"res/image/space.png"
MAIN_MENU_FLAG = False

pygame.init()
SCREEN = pygame.display.set_mode((800, 608))
pygame.display.set_caption(CAPTION)
font1 = pygame.font.SysFont("Ubuntu Mono", 72, True)
font2 = pygame.font.SysFont("Ubuntu Mono", 36, bold=True)

home_background = pygame.image.load(HOME_BACKGROUND).convert_alpha()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    if keys[K_RETURN] or MAIN_MENU_FLAG:
        MAIN_MENU_FLAG = True
        main_menu(SCREEN)

    else:
        SCREEN.blit(home_background, (0, 0))
        print_text(font1, 200, 158, "SPACE TRAVEL")
        print_text(font2, 200, 300, "PRESS RETURN TO CONTINUE", (220, 20, 20))
    pygame.display.update()

__author__ = 'liuchuang'
