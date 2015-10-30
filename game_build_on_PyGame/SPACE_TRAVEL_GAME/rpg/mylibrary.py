# coding:utf8
"""
mylibrary.py
该文件主要为以后开发带来便利
含有两个类，gameSprite 是游戏精灵类，Point为向量类
gameSprite 主要负责完成游戏中精灵的更新以及动画效果
Point类可以控制精灵的速度大小以及方向
含有四个方法：
wrap_angle(angle): 将角度控制在０～３６０之间
angular_velocity(angle): 根据角度不同来设置速度大小和方向
target_angle(x1, y1, x2, y2): 算出两点相对于原点之间的角度
print_text(font, x, y, text, color): 将字体打印到屏幕上的相应位置
"""
import pygame
import sys
import time
import math
import random
from pygame.locals import *

"""
gameSprite类:
__init__(self): 初始化精灵
load(self, filename, width, height, columns): 为游戏精灵添加位图
update(self, current_time, rate): 更新游戏精灵的帧图像
draw(self, surface): 该方法需精灵组调用，将该组中的精灵全部绘制在surface上
_getx(self): 获取精灵x坐标
_setx(self, value): 设置精灵x坐标
X: 设置，获取精灵的x坐标
_gety(self): 获取精灵的y坐标
_ sety(self, value): 设置精灵的y坐标
Y: 设置，获取精灵的y坐标
_getpos(self): 获取精灵的位置值
_setpos(self, pos): 设置精灵的位置值
position: 设置， 获取精灵的位置值
"""


class gameSprite(pygame.sprite.Sprite):
    # 初始化游戏参数
    def __init__(self):
        # 调用父类的构造方法
        pygame.sprite.Sprite.__init__(self)
        # master_image 为精灵的全部帧图像
        self.master_image = None
        # 游戏运行时精灵图像的帧图像
        self.frame = 0
        # 精灵的第一个帧图像
        self.first_frame = 0
        # 精灵的最后一个帧图像
        self.last_frame = -1
        # 精灵帧图像的宽度
        self.frame_width = 1
        # 精灵帧图像的长度
        self.frame_height = 1
        # 上一帧的时间
        self.old_time = 0
        # 上一帧的帧图像
        self.old_frame = 0
        # master_image 的列数
        self.columns = 1

    def load(self, filename, width, height, columns):
        # 设置精灵所有帧的位图
        self.master_image = pygame.image.load(filename).convert_alpha()
        # 当长宽都是１６时，将其改为３２
        if width != 32:
            temp_width, temp_height = self.master_image.get_size()
            self.master_image = pygame.transform.smoothscale(self.master_image, temp_width * 2, temp_height * 2)
        width = height = 32
        self.frame_width = width
        self.frame_height = height
        self.columns = columns
        self.rect = Rect(0, 0, width, height)
        rect = self.master_image.get_rect()
        # 获取精灵的最后一帧
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=0):  # current_time 为每帧播放的时间
        # 只在游戏运行一帧时刷屏
        if current_time > self.old_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            # 记录当前游戏时间
            self.old_time = current_time
        # 只在当前帧不等于上一帧时更新帧图像
        if self.frame is not self.old_frame:
            # frame_x, frame_y, rect　三个临时变量分别用于求当前帧的ｘ坐标、ｙ坐标和记录当前帧的位置
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = (frame_x, frame_y, self.frame_width, self.frame_height)
            # 设置游戏精灵的帧图像
            self.image = self.master_image.subsurface(rect)
            # 记录当前游戏帧图像
            self.old_frame = self.frame

    def draw(self, surface):
        surface.blit(self.image, (self.X, self.Y))

    def _getx(self):
        return self.rect.x

    def _setx(self, value):
        self.rect.x = value

    X = property(_getx, _setx)

    def _gety(self):
        return self.rect.y

    def _sety(self, value):
        self.rect.y = value

    Y = property(_gety, _sety)

    def _getpos(self):
        return self.rect.topleft

    def _setpos(self, pos):
        self.rect.topleft = pos

    position = property(_getpos, _setpos)


"""
Point类：
__init__(self): 初始化
__str__(self): 按照规定输出Point信息
_getx(self): 获得ｘ
_setx(self, value):　设置ｘ
x: 获得，设置ｘ
_gety(self):获得ｙ
_sety(self, value):设置ｙ
y: 获得，　设置ｙ
"""


class Point(object):
    def __init__(self):
        self.x = 0
        self.y = 0

    def _setx(self, value):
        self.x = value

    def _getx(self):
        return self.x

    x = property(_getx, _setx)

    def _gety(self):
        return self.y

    def _sety(self, value):
        self.y = value

    y = property(_gety, _sety)

    def __str__(self):
        return "X: " + str(self.x) + ", Y: " + str(self.y)


def warp_angle(angle):
    return angle % 360


def angular_velocity(angle):
    vel = Point(0.0, 0.0)
    vel.x = math.cos(math.radians(warp_angle(angle)))
    vel.y = math.sin(math.radians(warp_angle(angle)))
    return vel


def target_angle(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1
    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees


def print_text(font, x, y, text, color=(255, 255, 255)):
    screen = pygame.display.get_surface()
    text_image = font.render(text, True, color)
    font_rect = text_image.get_rect()
    font_rect.centerx = screen.get_rect().centerx
    font_rect.centery = y
    screen.blit(text_image, font_rect)
