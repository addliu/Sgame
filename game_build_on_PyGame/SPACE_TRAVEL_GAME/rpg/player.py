# coding:utf8
import mylibrary
import dungeon
import random
import pygame
from pygame.locals import *

player_image = r"D:\PythonRepository\game_build_on_PyGame\SPACE_TRAVEL_GAME\res\image\armorman.png"


class Player(mylibrary.gameSprite):
    def __init__(self):
        mylibrary.gameSprite.__init__(self)
        self.dun = dungeon.Dungeon()
        self.direction = mylibrary.Point(0, -1)
        self.vel = mylibrary.Point(0, -1)
        self.load(player_image, 32, 32, 4)

    def move(self):
        self.X += self.vel.x
        self.Y += self.vel.y

    def move_up(self):
        pos = self.get_next()
        self.first_frame = 0
        self.last_frame = 1
        self.direction = self.vel = mylibrary.Point(0, -1)
        if move_able:
            self.move()
        else:
            self.make_action(pos)

    def move_down(self):
        pos = self.get_next()
        self.first_frame = 2
        self.last_frame = 3
        self.direction = self.vel = mylibrary.Point(0, 1)
        if move_able:
            self.move()
        else:
            self.make_action(pos)

    def move_left(self):
        pos = self.get_next()
        self.first_frame = 4
        self.last_frame = 5
        self.direction = self.vel = mylibrary.Point(-1, 0)
        if move_able:
            self.move()
        else:
            self.make_action(pos)

    def move_right(self):
        pos = self.get_next()
        self.first_frame = 6
        self.last_frame = 7
        self.direction = self.vel = mylibrary.Point(1, 0)
        if move_able:
            self.move()
        else:
            self.make_action(pos)

    def get_next(self):
        global move_able
        self.X += self.vel.x
        self.Y += self.vel.y
        pos = self.dun.get_image_at(self.X, self.Y)
        if pos[1] != dungeon.DUNGEON:
            move_able = False
        else:
            move_able = True

        return pos

    def make_action(self, pos):
        if pos[0] == self.dun.treasurechest_sprite:
            if pos[1] == self.dun.CHEST_OFF:
                self.open_the_chest()

    def open_the_chest(self):
        things = random.randint(0, 2)
        if things == 0:
            print("YOU GET " + str(random.randint(5, 10)) + " GOLD!")
        elif things == 1:
            print("ATTACK UP " + str(random.randint(1, 2)) + " POINT! ")
        elif things == 2:
            print("DEFEND UP " + str(random.randint(1, 2)) + " POINT! ")
__author__ = 'added new'
