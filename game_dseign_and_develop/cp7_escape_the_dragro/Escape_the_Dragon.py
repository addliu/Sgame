# -*- coding:utf-8 -*-
# 还需获取按键长按事件；完成背景往后移动(finished in 9.27,2015)
import sys
import time
import pygame
import random
import math
from pygame.locals import *


class MySprite(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        self.monster_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0

    # X property
    def _getx(self): return self.rect.x

    def _setx(self, value): self.rect.x = value

    x = property(_getx, _setx)

    # y property
    def _gety(self): return self.rect.y

    def _sety(self, value): self.rect.y = value

    y = property(_gety, _sety)

    # position property
    def _getpos(self): return self.rect.topleft

    def _setpos(self, pos): self.rect.topleft = pos

    position = property(_getpos, _setpos)

    def load(self, filename, width, height, columns):
        self.monster_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0, 0, width, height)
        self.columns = columns
        # try to auto-calculate total frames
        rect = self.monster_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=0):
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
        self.last_time = current_time
        # build current frame only if it changed
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.monster_image.subsurface(rect)
            self.old_frame = self.frame

    def __str__(self):
        return str(self.frame) + " , " + str(self.first_frame) +\
            " , " + str(self.last_frame) + " , " + str(self.frame_width) +\
            " , " + str(self.frame_height) + " , " + str(self.columns) +\
            " , " + str(self.rect)


def print_text(font, x, y, text, color=(255, 255, 255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x, y))


def reset_arrow():
    y = random.randint(250, 350)
    arrow.position = 800, y


# main program begins
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Escape the Dragon")
font = pygame.font.Font(None, 18)
framerate = pygame.time.Clock()

# load bitmaps
bg = pygame.image.load(r"D:\bitmaps\background.png").convert_alpha()
# set bg_vel
bg_vel = -7
bg_x = 0

# set cloud vel
cloud_vel = 5.0

# create a sprite group
group = pygame.sprite.Group()

# create the dragon sprite
dragon = MySprite(screen)
dragon.load(r"D:\bitmaps\dragon.png", 260, 150, 3)
dragon.position = 100, 250
group.add(dragon)

# create the player sprite
player = MySprite(screen)
player.load(r"D:\bitmaps\caveman.png", 50, 64, 8)
player.first_frame = 1
player.last_frame = 7
player.position = 400, 303
group.add(player)

# create the arrow size
arrow = MySprite(screen)
arrow.load(r"D:\bitmaps\flame.png", 40, 16, 1)
arrow.position = 800, 320
group.add(arrow)

# create the cloud
cloud1 = MySprite(screen)
cloud1.load(r"D:\bitmaps\cloud1.png", 128, 71, 1)
cloud1.position = 400, 100
group.add(cloud1)
cloud2 = MySprite(screen)
cloud2.load(r"D:\bitmaps\cloud2.png", 128, 71, 1)
cloud2.position = 10, 10
group.add(cloud2)
cloud3 = MySprite(screen)
cloud3.load(r"D:\bitmaps\cloud3.png", 128, 71, 1)
cloud3.position = 150, 65
group.add(cloud3)

arrow_vel = 8.0
game_over = False
you_win = False
player_jumping = False
# recode the score
score = 0
high_score = 0
jump_vel = 0.0

player_start_y = player.y

# repeating loop
while True:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        elif keys[pygame.K_SPACE]:
            if not player_jumping:
                player_jumping = True
                jump_vel = -8.0

    # update the arrow
    if not game_over:
        arrow.x -= arrow_vel
        if arrow.x < -40:
            reset_arrow()

    # did arrow hit player?
    if pygame.sprite.collide_rect_ratio(0.75)(arrow, player):
        reset_arrow()
        player.x -= 8

    # did arrow hit dragon?
    if pygame.sprite.collide_rect(arrow, dragon):
        reset_arrow()
        dragon.x -= 10

    # did the dragon eat the player?
    if pygame.sprite.collide_rect(dragon, player):
        game_over = True

    # did the dragon get defeated?
    if dragon.x < -100:
        you_win = True
        game_over = True

    # get score
    if arrow.x == player.x and not pygame.sprite.collide_rect(arrow, player):
        score += 10
    high_score = max(high_score, score)
    # is the player jumping?
    if player_jumping:
        player.y += jump_vel
        jump_vel += 0.5
        if player.y > player_start_y:
            player_jumping = False
            player.y = player_start_y
            jump_vel = 0.0

    # move the background
    bg_x += bg_vel
    if bg_x < -400:
        bg_x = 0
    screen.blit(bg, (bg_x, 0))

    # update sprites
    if not game_over:
        # move the cloud
        cloud1.x -= (cloud_vel + cloud1.y//50)
        if cloud1.x < -120:
            cloud1.x = 800
        cloud2.x -= (cloud_vel + cloud2.y//50)
        if cloud2.x < -120:
            cloud2.x = 800
        cloud3.x -= (cloud_vel + cloud3.y//20)
        if cloud3.x < -120:
            cloud3.x = 800
        group.update(ticks)

    # draw sprites
    group.draw(screen)

    print_text(font, 350, 560, "Press SPACE to jump!")

    # show score and high_score
    print_text(font, 600, 0, "SCORE: " + str(score))
    print_text(font, 600, 10, "HIGH_SCORE: " + str(high_score))

    if game_over:
        player_jumping = True
        bg_vel = 0
        print_text(font, 360, 100, "G A M E O V E R")
        if you_win:
            print_text(font, 330, 130, "YOU  BEAT  THE  DRAGON!")
        else:
            print_text(font, 330, 130, "THE  DRAGON  GOT  YOU!")

    pygame.display.update()

__author__ = 'added new'
