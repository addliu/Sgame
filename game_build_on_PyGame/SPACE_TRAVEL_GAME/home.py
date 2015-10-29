# coding:utf8

import pygame
import sys
from pygame.locals import *
from mylibrary import *
import main_menu


def launch():
    CAPTION = "SPACE TRAVEL"
    HOME_BACKGROUND = r"res/image/space.png"
    # MAIN_MENU_FLAG = False

    pygame.init()
    SCREEN = pygame.display.set_mode((800, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption(CAPTION)
    big_font = pygame.font.SysFont("Ubuntu Mono", 72, True)
    font = pygame.font.SysFont("Ubuntu Mono", 36, bold=True)
    home_background = pygame.image.load(HOME_BACKGROUND).convert_alpha()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN :
                    main_menu.main_menu()

        else:
            SCREEN.blit(home_background, (0, 0))
            print_text(big_font, 200, 158, "SPACE TRAVEL")
            print_text(font, 200, 300, "PRESS RETURN TO CONTINUE", (220, 20, 20))
        pygame.display.flip()


__author__ = 'liuchuang'
