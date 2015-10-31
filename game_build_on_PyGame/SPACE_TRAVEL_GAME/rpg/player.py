import mylibrary
import dungeon
import pygame
from pygame.locals import *


class Player(mylibrary.gameSprite):
    def __init__(self):
        mylibrary.gameSprite.__init__(self)
        self.dun = dungeon.Dungeon()

    def move(self, x, y):
        self.X += x
        self.Y += y

    # def move_up(self):

__author__ = 'added new'
