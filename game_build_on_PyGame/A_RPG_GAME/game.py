# coding:utf-8
# class game
# mods: print_text(), new SysFont
import sys
import time
import random
import math
import pygame
from pygame.locals import *
from mylibrary import *
from dungeon import *
from player import *

screen_width = 800
screen_height = 608


def game_init():
    global screen, back_buffer, font1, font2, timer
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    back_buffer = pygame.Surface((screen_width, screen_height))
    pygame.display.set_caption("Dungeon Game")
    font1 = pygame.font.SysFont("Ubuntu Mono", size=18, bold=True)
    font2 = pygame.font.SysFont("Ubuntu Mono", size=14, bold=True)
    timer = pygame.time.Clock()


def player_collision(step_x, step_y):
    global player, level
    yellow = (220, 220, 0)
    green = (0, 220, 0)

    # get object at location
    image = dungeon.get_image_at(player.x + step_x, player.y + step_y)

    if image == entry_image:
        message("portal up")
    elif image == exit_image:
        message("portal down")
    elif image == empty_image:
        message("You ran into the wall--ouch!", yellow)
    elif image == gold_image:
        gold = random.randint(1, level)
        player.gold += gold
        dungeon.set_image_at(player.x + step_x, player.y + step_y, room_image)
    elif image == weapon_image:
        weapon = random.randint(1, level + 2)
        # low levels get crappy stuff
        if level <= 5:
            temp = random.randint(0, 2)
        else:
            temp = random.randint(3, 6)
        if temp == 0:
            name = "Dagger"
        elif temp == 1:
            name = "Short Sword"
        elif temp == 2:
            name = "Wooden Club"
        elif temp == 3:
            name = "Long Sword"
        elif temp == 4:
            name = "War Hammer"
        elif temp == 5:
            name = "Battle Axe"
        elif temp == 6:
            name = "Halberd"
        if weapon >= player.weapon:
            player.weapon = weapon
            player.weapon_name = name
            message("You found a" + name + " +" + str(weapon) + "!", yellow)
        else:
            player.gold += 1
            message("You discarded a worthless" + name + ".")
        dungeon.set_image_at(player.x + step_x, player.y + step_y, room_image)
    elif image == armor_image:
        armor = random.randint(1, level + 2)
        # low levels get crappy stuff
        if level <= 5:
            temp = random.randint(0, 2)
        else:
            temp = random.randint(3, 7)
        if temp == 0:
            name = "Cloth"
        elif temp == 1:
            name = "Patchwork"
        elif temp == 2:
            name = "Leather"
        elif temp == 3:
            name = "Chain"
        elif temp == 4:
            name = "Scale"
        elif temp == 5:
            name = "Plate"
        elif temp == 6:
            name = "Mithril"
        elif temp == 7:
            name = "Adamantium"
        if armor >= player.armor:
            player.armor = armor
            player.armor_name = name
            message("You found a" + name + " +" + str(armor) + "!", yellow)
        else:
            player.gold += 1
            message("You discarded a worthless" + name + ".")
        dungeon.set_image_at(player.x + step_x, player.y + step_y, room_image)
    elif image == health_image:
        heal = 0
        for n in range(0, level):
            heal += Die(6)
        player.add_health(heal)
        dungeon.set_image_at(player.x + step_x, player.y + step_y, room_image)
        message("You drank a healing potion worth " + str(heal) + "points!", green)
    elif image == monster_image:
        attack_monster(player.x + step_x, player.y + step_y, monster_image)


def attack_monster(x, y, image):
    global dungeon

    # player's attack
    defense = monster.get_defense()
    attack = player.get_attack()
    damage = player.get_damage(defense)
    battle_text = "You hit the " + monster.name + " for "
    # critical hit
    if attack == 20 + player.strength:
        damage *= 2
        battle_text += str(damage) + " CRIT points!"
        dungeon.set_image_at(x, y, gold_image)
        # to hit
    elif attack >= defense:
        if damage > 0:
            battle_text += str(damage) + " points!"
            dungeon.set_image_at(x, y, gold_image)
        else:
            battle_text += "no damage!"
            damage = 0
    else:
        battle_text += "no damage!"
        damage = 0

    # monster's attack
    defense = player.get_defense()
    attack = monster.get_attack()
    damage = monster.get_damage(defense)
    # to hit?
    if attack > defense:
        if damage > 0:
            # if damage is overwhelming , halve it
            if damage > player.max_health:
                damage /= 2
            battle_text += " It hit yoy for " + str(damage) + " points."
        else:
            battle_text += " It no damage to you."
    else:
        battle_text += " It missed you."

    # display battle results
    message(battle_text)
    # did the player survive?
    if player.health <= 0:
        player.alive = False


def move_monster():
    # find all monsters
    for y in range(0, columns_frame - 1):
        for x in range(0, row_frame - 1):
            tile = dungeon.get_image_at(x, y)
            # monster?
            if tile == monster_image:
                move_monsters(x, y, monster_image)


def move_monsters(x, y, image):
    movex = 0
    movey = 0
    dir = random.randint(1, 4)
    if dir == 1:
        movey = -1
    elif dir == 2:
        movey = 1
    elif dir == 3:
        movex = -1
    elif dir == 4:
        movex = 1
    # 获取当前位置
    temp = dungeon.get_image_at(x + movex, y + movey)
    if temp == room_image:
        # delete old  position
        dungeon.set_image_at(x, y, room_image)
        dungeon.set_image_at(x + movex, y + movey, image)


def print_stats():
    print_text(font2, 0, 0, "Test")


def message(text, color=(255, 255, 255)):
    global message_text, message_color
    message_text = text
    message_color = color

# event section
def event_section():
    global  draw_radius
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            elif event.key == K_TAB:
                # toggle map mode
                draw_radius = not draw_radius
            elif event.key == K_SPACE:
                dungeon.generate(empty_image, room_image, hall_image)
                player.x = dungeon.entrance_x + 1
                player.y = dungeon.entrance_y + 1
            elif event.key == K_UP or event.key == K_w:
                if player.moveUp() is False:
                    player_collision(0, -1)
                else:
                    move_monster()
            elif event.key == K_DOWN or event.key == K_s:
                if player.moveDown() is False:
                    player_collision(0, 1)
                else:
                    move_monster()

            elif event.key == K_RIGHT or event.key == K_d:
                if player.moveRight() is False:
                    player_collision(1, 0)
                else:
                    move_monster()

            elif event.key == K_LEFT or event.key == K_a:
                if player.moveLeft() is False:
                    player_collision(-1, 0)
                else:
                    move_monster()

# main program begins
game_init()
game_over = False
last_time = 0
dungeon = Dungeon(0, 0)
dungeon.generate(empty_image, room_image, hall_image)
player = Player(dungeon, 1, "Player")
monster = Monster(dungeon, 1, "Grue")
player.x = dungeon.entrance_x + 1
player.y = dungeon.entrance_y + 1
level = 1
message_text = "Welcome, brace adventurer!"
message_color = 0, 200, 50
draw_radius = False

# used to estimate attack damage
att = list(0 for n in range(0, 5))
att_low = 90
att_high = 0

# main loop
while True:
    timer.tick(30)
    ticks = pygame.time.get_ticks()

    event_section()

    # clear the background
    back_buffer.fill((20, 20, 20))

    # draw the dungeon
    if draw_radius:
        dungeon.draw_radius(back_buffer, player.x, player.y, 6)
    else:
        dungeon.draw(back_buffer)

    # draw the player's little dude
    player.draw(back_buffer, player_image)

    monster.draw(back_buffer, monster_image)
    # draw the back buffer
    screen.blit(back_buffer, (0, 0))

    print_stats()
    pygame.display.update()

__author__ = 'liuchuang'
