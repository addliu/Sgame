# coding:utf8
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
            self.tiles.append(EMPTY)
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
                    self.set_image_at(x, y)

    def create_hall(self, start_room, end_room):
        start_x, start_y = start_room.x + start_room.width // 2, start_room.y + start_room.height // 2
        print(start_x, start_y)
        end_x, end_y = end_room.x + end_room.width // 2, end_room.y + end_room.height // 2
        print(end_x, end_y)
        scentre_x, scentre_y = start_x, (start_y + end_y) // 2
        print(scentre_x, scentre_y)
        ecentre_x, ecentre_y = end_x, scentre_y
        print(ecentre_x, ecentre_y)
        self._create_hall(start_x, start_y, scentre_x, scentre_y)
        self._create_hall(scentre_x, scentre_y, ecentre_x, ecentre_y)
        self._create_hall(ecentre_x, ecentre_y, end_x, end_y)

    def _create_hall(self, x1, y1, x2, y2):
        if x1 == x2:
            while (y1 > y2):
                self.set_image_at(x1, y1)
                y1 -= 1
            while (y2 > y1):
                self.set_image_at(x1, y1)
                y1 += 1
        elif y1 == y2:
            while (x1 > x2):
                self.set_image_at(x1, y1)
                x1 -= 1
            while (x1 < x2):
                self.set_image_at(x1, y1)
                x1 += 1

    def set_image_at(self, x, y, image=DUNGEON):
        if x < 0 or x > 50 - 1 or y < 0 or y > 50 - 1:
            print("error: x, y = ", x, y)
            return
        index = y * 50 + x
        if index < 0 or index > 50 * 50:
            print("error: index = ", index)
            return
        self.tiles[index] = image

    def get_image_at(self, x, y):
        if x < 0 or x > 50 - 1 or y < 0 or y > 50 - 1:
            print("error: x, y = ", x, y)
            return
        index = y * 50 + x
        if index < 0 or index > 50 * 50:
            print("error: index = ", index)
            return
        return self.tiles[index]

    def draw(self, surface):
        for x in range(0, 50):
            for y in range(0, 50):
                image = self.get_image_at(x, y)
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
