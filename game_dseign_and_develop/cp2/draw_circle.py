import pygame
from pygame.locals import *
import sys
__author__ = 'added new'

#   initialise pygame
pygame.init()
#   get screen size
screen = pygame.display.set_mode((600, 500))
#   set caption
pygame.display.set_caption("draw circle")

#   set exit condition
while True:
    for event in pygame.event.get():
        if event.type in (pygame.QUIT, pygame.KEYDOWN):
            sys.exit()

#   set screen color
    screen.fill((0, 252, 0))
#   set circle position
    position = 300, 250
#   set circle color
    color = 255, 255, 255
#   set circle width
    width = 10
#   set radius
    radius = 100
#   draw circle
    pygame.draw.circle(screen, color, position, radius, width)
#   update screen
    pygame.display.update()
