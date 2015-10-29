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
width, height = int(pygame.display.Info().current_w), int(pygame.display.Info().current_h)
SCREEN = pygame.display.set_mode((width, height))
pygame.display.set_caption(CAPTION)
big_font = pygame.font.SysFont("Ubuntu Mono", 72, True)
font = pygame.font.SysFont("Ubuntu Mono", 36, bold=True)
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
        for x in range(0, width / home_background.get_rect().width + 1):
            for y in range(0, height / home_background.get_rect().height + 1):
                SCREEN.blit(home_background, (x * home_background.get_rect().width,
                                              y * home_background.get_rect().height))
        print_text(big_font, 200, 158, "SPACE TRAVEL")
        print_text(font, 200, 300, "PRESS RETURN TO CONTINUE", (220, 20, 20))
    pygame.display.update()

__author__ = 'liuchuang'
