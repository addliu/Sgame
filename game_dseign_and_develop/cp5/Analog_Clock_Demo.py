import sys
import random
import math
import pygame
from pygame.locals import *
from datetime import datetime, date, time


def print_text(font, x, y, text, color=(255, 255, 255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))


def wrap_angle(angle):
    return abs(angle % 360)

# main program begins
pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Analog Clock Demo")

font = pygame.font.Font(None, 36)
orange = 255, 102, 255
white = 0, 0, 204
yellow = 255, 255, 0
pink = 150, 0, 0

pos_x = 300
pos_y = 250
radius = 250
angle = 360

# repeating loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        sys.exit()

    screen.fill((82, 255, 212))
    # draw one step around the circle
    pygame.draw.circle(screen, white, (pos_x, pos_y), radius, 6)
    # draw the clock number 1-12
    for n in range(1, 13):
        angle = math.radians(n * 30 - 90)
        x = math.cos(angle) * (radius - 20) - 10
        y = math.sin(angle) * (radius - 20) - 10
        print_text(font, pos_x + x, pos_y + y, str(n))

    # get the time of day
    today = datetime.today()
    hours = today.hour % 12
    minutes = today.minute
    second = today.second
    hours += minutes / 60.0

    # draw the hours hand
    hour_angle = wrap_angle(hours * 30 - 90)
    hour_angle = math.radians(hour_angle)
    hour_x = math.cos(hour_angle) * (radius - 80)
    hour_y = math.sin(hour_angle) * (radius - 80)
    target = (pos_x + hour_x, pos_y + hour_y)
    pygame.draw.line(screen, pink, (pos_x, pos_y), target, 25)

    # draw the minutes hand
    min_angle = wrap_angle(minutes * 6 - 90)
    min_angle = math.radians(min_angle)
    min_x = math.cos(min_angle) * (radius - 60)
    min_y = math.sin(min_angle) * (radius - 60)
    target = (pos_x + min_x, pos_y + min_y)
    pygame.draw.line(screen, orange, (pos_x, pos_y), target, 12)

    # draw the second hand
    sec_angle = wrap_angle(second * 6 - 90)
    sec_angle = math.radians(sec_angle)
    sec_x = math.cos(sec_angle) * (radius - 40)
    sec_y = math.sin(sec_angle) * (radius - 40)
    target = (pos_x + sec_x, pos_y + sec_y)
    pygame.draw.line(screen, yellow, (pos_x, pos_y), target, 6)

    # cover the center
    pygame.draw.circle(screen, (255, 255, 255), (pos_x, pos_y), 20)
    print_text(font, 0, 0, str("{:.0f}".format(hours)) + ":" + str(minutes) + ":" + str(second))
    pygame.display.update()


__author__ = 'added new'
