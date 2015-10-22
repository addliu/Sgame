import pygame
from pygame.locals import *
import sys

pygame.init()
window_width = 600
window_height = 500
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Drawing Rectangles")
pos_x = 300.0
pos_y = 250.0
vel_x = 0.1
vel_y = 0.1
color1 = 255, 255, 0
color2 = 255, 0, 255
color3 = 0, 255, 255
color_list = [color1, color2, color3]
now_site = 0
color = color_list[now_site]
while True:
    for event in pygame.event.get():
        if event.type in (pygame.QUIT, pygame.KEYDOWN):
            sys.exit()

    screen.fill((0, 0, 200))
    pos_x += vel_x
    pos_y += vel_y
    if pos_x < 0 or pos_x > 500:
        vel_x = -vel_x
        color = color_list[(now_site + 1) % len(color_list)]
        now_site += 1
    if pos_y < 0 or pos_y > 400:
        vel_y = -vel_y
        color = color_list[(now_site + 1) % len(color_list)]
        now_site += 1
    pygame.draw.rect(screen, color, (int(pos_x), int(pos_y), 100, 100))
    pygame.display.update()
