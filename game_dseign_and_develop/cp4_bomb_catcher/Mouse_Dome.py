import sys
import pygame
from pygame.locals import *


def print_text(font, x, y, text, color=(255, 255, 255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))


# main program begins
pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Mouse Dome")
font1 = pygame.font.Font(None, 24)
white = 255, 255, 255
mouse_x = moues_y = 0
move_x = move_y = 0
mouse_down = mouse_up = 0
mouse_down_x = mouse_down_y = 0
mouse_up_x = mouse_up_y = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            move_x, move_y = event.rel
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = event.button
            mouse_down_x, mouse_down_y = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_up = event.button
            mouse_up_x, mouse_up_y = event.pos
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        sys.exit()
    screen.fill((0, 100, 0))

    print_text(font1, 0, 0, "Mouse Events")
    print_text(font1, 0, 20, "Mouse position: " + str(mouse_x) + "," + str(mouse_y))
    print_text(font1, 0, 40, "Mouse relative: " + str(move_x) + "," + str(move_x))
    print_text(font1, 0, 60, "Mouse button down:" + str(mouse_down) + "at" + str(mouse_down_x) + "," + str(mouse_down_y))
    print_text(font1, 0, 80, "Mouse button up: " + str(mouse_up) + "at" + str(mouse_up_x) + "," + str(mouse_up_y))
    print_text(font1, 0, 160, "Mouse Polling")
    x, y = pygame.mouse.get_pos()
    print_text(font1, 0, 180, "Mouse position: " + str(mouse_x) + "," + str(mouse_y))

    b1, b2, b3 = pygame.mouse.get_pressed()
    print_text(font1, 0, 300, "Mouse buttons: " + str(b1) + "," + str(b2) + "," + str(b3))
    pygame.display.update()
__author__ = 'added new'
