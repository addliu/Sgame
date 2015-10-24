# coding:utf8
"""
该文件含有两个类，gameSprite 是游戏精灵类，Point为向量类
gameSprite 主要负责完成游戏中精灵的更新以及动画效果
Point类可以控制精灵的速度大小以及方向
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
_getx(self): 获取精灵x坐标
_setx(self, value): 设置精灵x坐标
X: 设置，获取精灵的x坐标
_gety(self): 获取精灵的y坐标
_ sety(self, value): 设置精灵的y坐标
Y: 设置，获取精灵的y坐标
_getpos(self): 获取精灵的位置值
_setpos(self, topleft): 设置精灵的位置值
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
        self.master_image = pygame.image.load(filename).covent_alpha()
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

    def _getx(self):
        return  self.rect.x

    def _setx(self, value):
        self.rect.x = value
    X = property(_getx, _setx)

    def _gety(self):
        return  self.rect.y

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
"""
class Point(object):
    def __init__(self):
        self.x = 0
        self.y = 0

    def __str__(self):
        return "X: " + str(self.x) + ", Y: " + str(self.y)
__author__ = 'liuchuang'
