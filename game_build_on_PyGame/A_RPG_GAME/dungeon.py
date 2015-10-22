# Dungeon class
import sys
import time
import random
import math
import pygame
from pygame.locals import *
from mylibrary import *

frame_width = 16
frame_height = 16
columns = 16
row_frame = 50
columns_frame = 38
pos_x = 1
pos_y = 2
size_min = 6
size_max = 9
# room width size
room_width = row_frame // 4
# room height size
room_height = columns_frame // 2

empty_image = 192
room_image = 96
hall_image = 96
# ------------ behind arguments has changed
entry_image = 29
exit_image = 30
gold_image = 70
weapon_image = 86
armor_image = 64
health_image = 71
player_image = 0
monster_image = 0


class Dungeon(object):
    def __init__(self, offset_x, offset_y):
        # create the font sprite
        self.sprite = MySprite()
        self.sprite.load("ascii8x12.png", frame_width, frame_height, columns)

        self.dun = MySprite()
        self.dun.load("dun_16.png", frame_width, frame_height, columns)

        # create the level list
        self.tiles = list()
        for n in range(0, row_frame * columns_frame):
            self.tiles.append(-1)

        self.offset_x = offset_x
        self.offset_y = offset_y

        self.generate(empty_image=empty_image, room_image=room_image, hall_image=hall_image)

    def generate(self, empty_image, room_image, hall_image):
        self.empty_image = empty_image
        self.room_image = room_image
        self.hall_image = hall_image

        # clear existing level
        for index in range(0, row_frame * columns_frame):
            self.tiles[index] = empty_image
        # create random rooms
        PL = pos_x
        PH = pos_y
        SL = size_min
        SH = size_max
        self.rooms = list()
        for j in range(0, 2):
            for i in range(0, 4):
                self.createRoom(i * room_width, j * room_height, PL, PH, SL, SH)

        # connect the rooms with halls
        self.createHallRight(self.rooms[0], self.rooms[1], hall_image)
        self.createHallRight(self.rooms[1], self.rooms[2], hall_image)
        self.createHallRight(self.rooms[2], self.rooms[3], hall_image)
        self.createHallRight(self.rooms[4], self.rooms[5], hall_image)
        self.createHallRight(self.rooms[5], self.rooms[6], hall_image)
        self.createHallRight(self.rooms[6], self.rooms[7], hall_image)

        # choose a random northern room to connect with the south
        choice = random.randint(0, 3)
        print("choice: " + str(choice) + ", " + str(choice + 4))
        self.createHallDown(self.rooms[choice], self.rooms[choice + 4], hall_image)
        # add rooms to level
        for room in self.rooms:
            for y in range(room.y, room.y + room.height):
                for x in range(room.x, room.x + room.width):
                    self.set_image_at(x, y, room_image)

        # add entrance portal
        choice = random.randint(0, 7)
        self.entrance_x = self.rooms[choice].x + self.rooms[choice].width // 2
        self.entrance_y = self.rooms[choice].y + self.rooms[choice].height // 2
        self.set_image_at(self.entrance_x, self.entrance_y, entry_image)
        print("entrance: ", choice, self.entrance_x, self.entrance_y)

        # add exit portals
        choice2 = random.randint(0, 7)
        while choice2 == choice:
            choice2 = random.randint(0, 7)
        x = self.rooms[choice2].x + self.rooms[choice2].width // 2
        y = self.rooms[choice2].y + self.rooms[choice2].height // 2
        self.set_image_at(x, y, exit_image)
        print("exit: ", choice2, x, y)

        # add random gold
        drops = random.randint(5, 20)
        for n in range(1, drops):
            self.put_image_in_random_room(room_image, gold_image)

        # add weapon, armor, and health
        self.put_image_in_random_room(room_image, weapon_image)
        self.put_image_in_random_room(room_image, armor_image)
        self.put_image_in_random_room(room_image, health_image)
        self.put_image_in_random_room(room_image, health_image)

        # add some monsters
        num = random.randint(5, 10)
        for n in range(0, num):
            self.put_image_in_random_room(room_image, monster_image)

    def put_image_in_random_room(self, target_image, item_image):
        tile = 0
        while tile != target_image:
            x = random.randint(0, row_frame - 1)
            y = random.randint(0, columns_frame - 1)
            tile = self.get_image_at(x, y)
        self.set_image_at(x, y, item_image)

    def createRoom(self, x, y, rposx, rposy, rsizel, rsizeh):
        room = Rect(x + random.randint(1, rposx),
                    y + random.randint(1, rposy),
                    random.randint(rsizel, rsizeh),
                    random.randint(rsizeh, rsizeh))
        self.rooms.append(room)

    def createHallRight(self, src, dst, hall):
        pathx = src.x + src.width
        pathy = src.y + random.randint(1, src.height )
        self.set_image_at(pathx, pathy, hall)
        if dst.y < pathy < dst.y + dst.height:
            while pathx < dst.x:
                pathx += 1
                self.set_image_at(pathx, pathy, hall)
        else:
            while pathx < dst.x + 1:
                pathx += 1
                self.set_image_at(pathx, pathy, hall)
            if pathy < dst.y + 1:
                self.set_image_at(pathx, pathy, hall)
                while pathy < dst.y:
                    pathy += 1
                    self.set_image_at(pathx, pathy, hall)
            else:
                self.set_image_at(pathx, pathy, hall)
                while pathy > dst.y + dst.height:
                    pathy -= 1
                    self.set_image_at(pathx, pathy, hall)

    def createHallDown(self, src, dst, hall_image):
        pathx = src.x + random.randint(1, src.width )
        pathy = src.y + src.height
        self.set_image_at(pathx, pathy, hall_image)
        if dst.x < pathx < dst.x + dst.width:
            while pathy < dst.y:
                pathy += 1
                self.set_image_at(pathx, pathy, hall_image)
        else:
            while pathy < dst.y + 1:
                pathy += 1
                self.set_image_at(pathx, pathy, hall_image)
            if pathx < dst.x + 1:
                self.set_image_at(pathx, pathy, hall_image)
                while pathx < dst.x:
                    pathx += 1
                    self.set_image_at(pathx, pathy, hall_image)
            else:
                self.set_image_at(pathx, pathy, hall_image)
                while pathx > dst.x + dst.width:
                    pathx -= 1
                    self.set_image_at(pathx, pathy, hall_image)

    def get_image_at(self, x, y):
        if x < 0 or x > row_frame - 1 or y < 0 or y > columns_frame - 1:
            print("error: x, y = ", x, y)
            return
        index = y * row_frame + x
        if index < 0 or index > row_frame * columns_frame:
            print("error: index = ", index)
            return
        return self.tiles[index]

    def set_image_at(self, x, y, image):
        if x < 0 or x > row_frame - 1 or y < 0 or y > columns_frame - 1:
            print("error: x, y = ", x, y)
            return
        index = y * row_frame + x
        if index < 0 or index > row_frame * columns_frame:
            print("error: index = ", index)
            return
        self.tiles[index] = image

    def draw(self, surface):
        for y in range(0, columns_frame):
            for x in range(0, row_frame):
                image = self.get_image_at(x, y)
                if 0 <= image <= columns_frame * row_frame:
                    self.draw_image(surface, self.dun, x, y, image)
                else:
                    pass  # empty tile

    def draw_radius(self, surface, rx, ry, radius):
        left = rx - radius
        right = rx + radius
        top = ry - radius
        bottom = ry + radius
        if left < 0:
            left = 0
        elif right > row_frame - 1:
            right = row_frame - 1
        if top < 0:
            top = 0
        elif bottom > columns_frame - 1:
            bottom = columns_frame

        for y in range(top, bottom):
            for x in range(left, right):
                image = self.get_image_at(x, y)
                if image >= 0 and image <= columns_frame * row_frame:
                    self.draw_image(surface, x, y, image)

    # def draw_image(self, surface, tilex, tiley, image):
    #     self.sprite.X = self.offset_x + tilex * frame_width
    #     self.sprite.Y = self.offset_y + tiley * frame_height
    #     self.sprite.frame = image
    #     self.sprite.last_frame = image
    #     self.sprite.update(0)
    #     self.sprite.draw(surface)
    def draw_image(self, surface, sprite, tilex, tiley, image):
        sprite.X = self.offset_x + tilex * frame_width
        sprite.Y = self.offset_y + tiley * frame_height
        sprite.frame = image
        sprite.last_frame = image
        sprite.update(0)
        sprite.draw(surface)


__author__ = 'liuchuang'
