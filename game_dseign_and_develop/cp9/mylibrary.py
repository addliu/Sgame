# coding:utf8
import pygame
from pygame.locals import *


# 使用提供的字体在屏幕上打印文字
def print_text(font, x, y, text, color=(255, 255, 255)):
    imgText = font.render(text, True, color)
    screen = pygame.display.get_surface()
    screen.blit(imgText, (x, y))


# MySprite 类 继承 pygame.sprite.Sprite
class MySprite(pygame.sprite.Sprite):
    def __init__(self):
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
        self.direction = 0
        self.velocity = Point(0, 0)

    # X 属性
    def _getx(self):
        return self.rect.x

    def _setx(self, value):
        self.rect.x = value

    X = property(_getx, _setx)

    # Y 属性
    def _gety(self):
        return self.rect.y

    def _sety(self, value):
        self.rect.y = value

    Y = property(_gety, _sety)

    # 位置属性
    def _getpos(self):
        return self.rect.topleft

    def _setpos(self, pos):
        self.rect.topleft = pos

    position = property(_getpos, _setpos)

    # 从文件中读取精灵的图像
    def load(self, filename, width=0, height=0, columns=1):
        self.monster_image = pygame.image.load(filename).convert_alpha()
        self.set_image(self.monster_image, width, height, columns)

    # 设置精灵的属性
    def set_image(self, image, width=0, height=0, columns=1):
        self.monster_image = image
        if width == 0 and height == 0:
            self.frame_width = image.get_width()
            self.frame_height = image.get_height()
        else:
            self.frame_width = width
            self.frame_height = height
            rect = self.monster_image.get_rect()
            self.last_frame = (rect.width // width) * (rect.height // height) - 1
        self.rect = Rect(0, 0, self.frame_width, self.frame_height)
        self.columns = columns

    # 更新精灵动画
    def update(self, current_time, rate=30):
        if self.last_frame > self.first_frame:
            # 更新动画帧
            if current_time > self.last_time + rate:
                self.frame += 1
                if self.frame > self.last_frame:
                    self.frame = self.first_frame
                self.last_time = current_time
        else:
            self.frame = self.first_frame

        # 仅在当前帧改变时更新帧
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.monster_image.subsurface(rect)
            self.old_frame = self.frame

    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + "," + \
               str(self.last_frame) + "," + str(self.frame_width) + "," + \
               str(self.frame_height) + "," + str(self.columns) + "," + \
               str(self.rect)


# Point 类继承 object
class Point(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    # X 属性
    def getx(self): return self.__x

    def setx(self, value): self.__x = value

    x = property(getx, setx)

    # Y 属性
    def gety(self): return self.__y

    def sety(self, value): self.__y = value

    y = property(gety, sety)

    def __str__(self):
        return "{X: " + "{:.0f}".format(self.__x) + \
               ",Y:" + "{:.0f}".format(self.__y) + "}"


__author__ = 'added new'
