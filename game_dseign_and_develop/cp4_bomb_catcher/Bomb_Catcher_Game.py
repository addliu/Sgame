# Bomb Catcher Game
import sys
import pygame
import random
from pygame.locals import *


def print_text(font, x, y, text, color=(255, 255, 255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))

# main program begins
pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Bomb Catcher Game")

font1 = pygame.font.Font(None, 24)
white = 255, 255, 255
yellow = 230, 230, 0
red = 220, 50, 50
black = 0, 0, 0

lives = 3
score = 0
game_over = True
mouse_x = mouse_y = 0
pos_x, pos_y = 300, 460
bomb_x = random.randint(0, 500)
bomb_y = -50
vel_y = 0.7

#   repeating loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            move_x, move_y = event.rel
        elif event.type == pygame.MOUSEBUTTONUP:
            if game_over:
                game_over = False
                lives = 3
                score = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        sys.exit()
# clear the screen
    screen.fill((0, 0, 100))

    if game_over:
        print_text(font1, 100, 200, "<CLICK TO PLAY>")
    else:
        bomb_y += vel_y
# has the player missed the bomb?
    if bomb_y > 500:
        bomb_x = random.randint(0, 500)
        bomb_y = -50
        lives -= 1
        if lives == 0:
            game_over = True
# see if player caught the bomb
    elif bomb_y > pos_y:
        if pos_x < bomb_x < pos_x + 120:
            score += 10
            bomb_x = random.randint(0, 500)
            bomb_y = - 50
# draw the bomb
    pygame.draw.circle(screen, black, (bomb_x - 4, int(bomb_y) - 4), 30, 0)
    pygame.draw.circle(screen, yellow, (bomb_x, int(bomb_y)), 30, 0)
# set basket position
    pos_x = mouse_x
    if pos_x < 0:
        pos_x = 0
    elif pos_x > 500:
        pos_x = 500
# draw the basket
    pygame.draw.rect(screen, black, (pos_x - 4, pos_y - 4, 120, 40), 0)
    pygame.draw.rect(screen, red, (pos_x, pos_y, 120, 40), 0)
# print lives
    print_text(font1, 0, 0, "Lives: " + str(lives))
# print score
    print_text(font1, 500, 0, "SCORE: " + str(score))
    pygame.display.update()
__author__ = 'added new'
