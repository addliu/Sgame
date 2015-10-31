"""
player.py：将玩家加入到地下城中
属性：
player_image：玩家素材图像的绝对路径
Player类：生成玩家
"""
# coding:utf8
import mylibrary
import dungeon
import random
import pygame
from pygame.locals import *

player_image = r"D:\PythonRepository\game_build_on_PyGame\SPACE_TRAVEL_GAME\res\image\armorman.png"


class Player(mylibrary.gameSprite):
    """
    Player类：
    方法：
    __init__(self, dungeon):初始化Player
    put_player_at(self, room):将玩家放在地下城的一个房间里
    move(self):朝给定方向移动玩家
    move_up(self):把移动方向设置为向上，设置人物帧图像
    move_down(self):把移动方向设置为向下，设置人物帧图像
    move_left(self):把移动方向设置为向左，设置人物帧图像
    move_right(self):把移动方向设置为向右，设置人物帧图像
    get_next(self):获得当前方向下一个位置的图像
    make_action(self, pos):根据下一个位置的图像，来让玩家完成特定动作
    open_the_chest(self):完成打开宝箱动作
    """
    def __init__(self, dungeon):
        mylibrary.gameSprite.__init__(self)
        # 获取正在使用的地下城
        self.dungeon = dungeon
        self.direction = mylibrary.Point(0, -1)
        self.vel = mylibrary.Point(0, -1)
        self.load(player_image, 32, 32, 4)
        self.put_player_at(self.dungeon.rooms[0])
        self.gold = 100
        self.attack = 5
        self.defence = 5

    def put_player_at(self, room):
        self.X = room.x + random.randint(0, room.width - 1)
        self.Y = room.x + random.randint(0, room.height - 1)
        print(self.X, self.Y)

    def draw_player(self, surface):
        surface.blit(self.image, (self.X * self.frame_width, self.Y * self.frame_height))

    def move(self):
        self.X += self.vel.x
        self.Y += self.vel.y

    def move_up(self):
        self.direction = mylibrary.Point(0, -1)
        self.vel = mylibrary.Point(0, -1)
        pos = self.get_next()
        self.frame = 0
        self.first_frame = 0
        self.last_frame = 1
        if move_able:
            self.move()
        else:
            self.make_action(pos)

    def move_down(self):
        self.direction = mylibrary.Point(0, 1)
        self.vel = mylibrary.Point(0, 1)
        pos = self.get_next()
        self.frame = 2
        self.first_frame = 2
        self.last_frame = 3
        if move_able:
            self.move()
        else:
            self.make_action(pos)

    def move_left(self):
        self.direction = mylibrary.Point(-1, 0)
        self.vel = mylibrary.Point(-1, 0)
        pos = self.get_next()
        self.frame = 4
        self.first_frame = 4
        self.last_frame = 5
        if move_able:
            self.move()
        else:
            self.make_action(pos)

    def move_right(self):
        self.direction = mylibrary.Point(1, 0)
        self.vel = mylibrary.Point(1, 0)
        pos = self.get_next()
        self.frame = 6
        self.first_frame = 6
        self.last_frame = 7
        if move_able:
            self.move()
        else:
            self.make_action(pos)

    def get_next(self):
        global move_able
        X = self.X + self.vel.x
        Y = self.Y + self.vel.y
        pos = self.dungeon.get_image_at(X, Y)
        if pos[1] != dungeon.DUNGEON:
            move_able = False
        else:
            move_able = True
        return pos

    def make_action(self, pos):
        if pos[0] == self.dungeon.treasurechest_sprite:
            if pos[1] == 0:
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
