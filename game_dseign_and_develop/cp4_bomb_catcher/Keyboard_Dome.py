#   time.time(),time.clock() both return 0
import sys
import random
import time
import pygame
from pygame.locals import *


def print_text(font, x, y, text, color=(255, 255, 255)):
    imageText = font.render(text, True, color)
    screen.blit(imageText, (x, y))

#   main program begins
pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Keyboard Dome")
font1 = pygame.font.Font(None, 24)
font2 = pygame.font.Font(None, 200)
white = 255, 255, 255
yellow = 255, 255, 0

key_flag = False
correct_answer = 97  # "a"
second = 11
score = 0
color_start = 0
game_over = True

#   repeating loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            key_flag = True
        elif event.type == pygame.KEYUP:
            key_flag = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sys.exit()

        if keys[pygame.K_RETURN]:
            if game_over:
                game_over = False
                score = 0
                second = 11

    clock_start = time.perf_counter()
    current = time.process_time() - clock_start
    print(current)
    speed = score * 6
    if second - current < 0:
        game_over = True
    elif current <= 10:
        if keys[correct_answer]:
            correct_answer = random.randint(97, 122)
            score += 1

    screen.fill((0, 100, 0))
    print_text(font1, 0, 0, "Let's see how fast you can type!")
    print_text(font1, 0, 20, "Try to keep up for 10 seconds...")

    if key_flag:
        print_text(font1, 500, 0, "<key>")
    if not game_over:
        print_text(font1, 0, 80, "Time: " + str(int(second - current)))
    print_text(font1, 0, 100, "Speed: " + str(speed) + "letters/min")

    if game_over:
        print_text(font1, 0, 160, "Press Enter to start...")
    print_text(font2, 0, 240, chr(correct_answer - 32), yellow)
#   update the display
    pygame.display.update()

__author__ = 'added new'
