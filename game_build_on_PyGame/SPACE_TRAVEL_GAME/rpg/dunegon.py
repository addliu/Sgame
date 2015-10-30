# coding:utf8
"""
dunegon.py:自动生成地下城文件
属性：
DUNGEON: 地板图形所处的位置，用于绘制地板
EMPTY: 空图像所处位置，用于绘制背景
STAIRS_DOWN: 楼梯（下）图像所处的位置，用于进入下一层
STAIRS_UP: 楼梯（上）图像所处的位置，用于进入上一层
CHEST_OFF: 宝箱（未开）图像所处的位置
CHEST_ON:  宝箱（已开）图像所处的位置
floor_image: 地板图像的绝对路径
stairs_image: 楼梯图像的绝对路径
chest_image: 宝箱图像的绝对路径
Dungeon类: 完成自动生成地下城地图列表
方法：
move_up(x, y): 因为画布要比屏幕大，所以必须移动画布来使屏幕间接显示整个背景画布，move_up为向下移动画布
move_down(x, y):向上移动画布
move_left(x, y):向右移动画布
move_right(x, y):向左移动画布
"""
import pygame
import random
import sys
import mylibrary
from pygame.locals import *

DUNGEON = 71
EMPTY = 69
STAIRS_DOWN = 0
STAIRS_UP = 1
CHEST_OFF = 0
CHEST_ON = 1
floor_image = r"D:\PythonRepository\game_build_on_PyGame\SPACE_TRAVEL_GAME\res\image\tileset3.png"
stairs_image = r"D:\PythonRepository\game_build_on_PyGame\SPACE_TRAVEL_GAME\res\image\stairs.png"
chest_image = r"D:\PythonRepository\game_build_on_PyGame\SPACE_TRAVEL_GAME\res\image\treasurechest.png"

"""
Dungeon类：主要功能是自动生成地下城
该类一共有3个精灵对象，分别为：floor_sprite（地板）、stairs_sprite（楼梯）、treasurechest_sprite（宝箱）
方法：
__init__(self): 构造方法，用于初始化第地下城和精灵
create_room(self, x, y): 在（x， y）处创建一个随机大小的房间
create_dungeon(self, level=1):将完整的地图信息储存在一个tile列表中
create_hall(self, start_room, end_room):获取两个房间的位置信息，用以创建走廊
_create_hall(self, x1, y1, x2, y2):用走廊将给定的两点连接起来
set_image_at(self, x, y, image=DUNGEON):设置x，y处的地图信息
get_image_at(self, x, y):获取x，y处的地图信息
draw(self, surface):获取所有地图信息，通过调用draw_image()完成地图的绘制
draw_image(self, x, y, surface, image):在surface上绘制地图
"""


class Dungeon(object):
    def __init__(self):
        # 创建地板精灵
        self.floor_sprite = mylibrary.gameSprite()
        # 创建楼梯精灵
        self.stairs_sprite = mylibrary.gameSprite()
        # 创建宝箱精灵
        self.treasurechest_sprite = mylibrary.gameSprite()

        self.floor_sprite.load(floor_image, 16, 16, 11)
        self.stairs_sprite.load(stairs_image, 16, 16, 2)
        self.treasurechest_sprite.load(chest_image, 32, 32, 2)
        # 地下城目前只设一帧
        self.floor_sprite.frame = DUNGEON
        self.floor_sprite.first_frame = DUNGEON
        self.floor_sprite.last_frame = DUNGEON
        # 0表示下楼梯，　１表示上楼梯
        self.stairs_sprite.frame = STAIRS_DOWN
        self.stairs_sprite.first_frame = STAIRS_DOWN
        self.stairs_sprite.last_frame = STAIRS_DOWN
        # 0表示宝箱未开启，　１表示宝箱已开启
        self.treasurechest_sprite.frame = CHEST_OFF
        self.treasurechest_sprite.first_frame = CHEST_OFF
        self.treasurechest_sprite.last_frame = CHEST_ON
        self.tiles = list()
        for i in range(0, 50 * 50):
            self.tiles.append([self.floor_sprite, EMPTY])
        self.rooms = list()

    def create_room(self, x, y):
        room = Rect(x + random.randint(1, 6), y + random.randint(1, 6),
                    random.randint(5, 10), random.randint(5, 10))
        self.rooms.append(room)

    def create_dungeon(self, level=1):
        for i in range(0, 3):
            for j in range(0, 3):
                # i * 16, j * 16分别为每个房间的开始位置
                self.create_room(i * 16, j * 16)
        self.create_hall(self.rooms[0], self.rooms[1])
        self.create_hall(self.rooms[1], self.rooms[2])
        self.create_hall(self.rooms[3], self.rooms[4])
        self.create_hall(self.rooms[4], self.rooms[5])
        self.create_hall(self.rooms[6], self.rooms[7])
        self.create_hall(self.rooms[7], self.rooms[8])
        choice = random.randint(0, 2)
        self.create_hall(self.rooms[choice], self.rooms[choice + 3])
        self.create_hall(self.rooms[4], self.rooms[7])
        # add
        for room in self.rooms:
            for y in range(room.y, room.y + room.height):
                for x in range(room.x, room.x + room.width):
                    self.set_image_at(x, y, self.floor_sprite)
        for chest in range(0, level + 1):
            choice = random.randint(0, 8)
            self.put_chest_in(self.rooms[choice])

    def create_hall(self, start_room, end_room):
        start_x, start_y = start_room.x + start_room.width // 2, start_room.y + start_room.height // 2
        end_x, end_y = end_room.x + end_room.width // 2, end_room.y + end_room.height // 2
        scentre_x, scentre_y = start_x, (start_y + end_y) // 2
        ecentre_x, ecentre_y = end_x, scentre_y
        self._create_hall(start_x, start_y, scentre_x, scentre_y)
        self._create_hall(scentre_x, scentre_y, ecentre_x, ecentre_y)
        self._create_hall(ecentre_x, ecentre_y, end_x, end_y)

    def _create_hall(self, x1, y1, x2, y2):
        if x1 == x2:
            while (y1 > y2):
                self.set_image_at(x1, y1, self.floor_sprite)
                y1 -= 1
            while (y2 > y1):
                self.set_image_at(x1, y1, self.floor_sprite)
                y1 += 1
        elif y1 == y2:
            while (x1 > x2):
                self.set_image_at(x1, y1, self.floor_sprite)
                x1 -= 1
            while (x1 < x2):
                self.set_image_at(x1, y1, self.floor_sprite)
                x1 += 1

    def set_image_at(self, x, y, sprite, image=DUNGEON):
        if x < 0 or x > 50 - 1 or y < 0 or y > 50 - 1:
            print("error: x, y = ", x, y)
            return
        index = y * 50 + x
        if index < 0 or index > 50 * 50:
            print("error: index = ", index)
            return
        self.tiles[index] = [sprite, image]

    def get_image_at(self, x, y):
        if x < 0 or x > 50 - 1 or y < 0 or y > 50 - 1:
            print("error: x, y = ", x, y)
            return
        index = y * 50 + x
        if index < 0 or index > 50 * 50:
            print("error: index = ", index)
            return
        return self.tiles[index]

    def put_chest_in(self, room):
        x, y = room.x + random.randint(0, room.width), room.y + random.randint(0, room.height)
        if self.get_image_at(x, y)[1] == DUNGEON:
            self.set_image_at(x, y, self.treasurechest_sprite, CHEST_OFF)
        else:
            self.put_chest_in(room)

    def draw(self, surface):
        for x in range(0, 50):
            for y in range(0, 50):
                sprite, image = self.get_image_at(x, y)[0], self.get_image_at(x, y)[1]
                self.draw_image(x, y, surface, image)

    def draw_image(self, x, y, surface, image):
        self.floor_sprite.X = x * self.floor_sprite.frame_width
        self.floor_sprite.Y = y * self.floor_sprite.frame_height
        self.floor_sprite.frame = image
        self.floor_sprite.last_frame = image
        self.floor_sprite.update(0)
        self.floor_sprite.draw(surface)


def move_down(x, y):
    if y > -1000:
        y -= 100
    return x, y


def move_up(x, y):
    if y < 0:
        y += 100
    return x, y


def move_right(x, y):
    if x > -800:
        x -= 100
    return x, y


def move_left(x, y):
    if x < 0:
        x += 100
    return x, y


pygame.init()
SCREEN = pygame.display.set_mode((800, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
buffer = pygame.Surface((1600, 1600))
pygame.display.set_caption("DUNGEON DEMO")

dun = Dungeon()
dun.create_dungeon()
x = y = 0
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                x, y = move_up(x, y)
            elif event.key == K_DOWN:
                x, y = move_down(x, y)
            elif event.key == K_LEFT:
                x, y = move_left(x, y)
            elif event.key == K_RIGHT:
                x, y = move_right(x, y)
    dun.draw(buffer)
    SCREEN.fill((20, 20, 220))
    SCREEN.blit(buffer, (x, y))
    pygame.display.flip()

__author__ = 'liuchuang'
