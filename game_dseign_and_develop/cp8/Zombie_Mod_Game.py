import itertools
import sys
import time
import random
import math
import pygame
from pygame.locals import *
from MyLibrary import *


def calc_velocity(direction, vel=2.0):
    velocity = Point(0, 0)
    if direction == 0:  # north
        velocity.y = -vel
    elif direction == 2:  # east
        velocity.x = vel
    elif direction == 4:  # south
        velocity.y = vel
    elif direction == 6:  # west
        velocity.x = -vel
    return velocity


def reverse_direction(sprite):
    if sprite.direction == 0:
        sprite.direction = 4
    elif sprite.direction == 2:
        sprite.direction = 6
    elif sprite.direction == 4:
        sprite.direction = 0
    elif sprite.direction == 6:
        sprite.direction = 2


def create_zombie(zombie_group):
    zombie = MySprite()
    zombie.load(zombie_image, 96, 96, 8)
    zombie.position = random.randint(0, 700), random.randint(0, 500)
    zombie.direction = random.randint(0, 3) * 2
    zombie_group.add(zombie)

# main program begins
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Collision Demo")
font = pygame.font.Font(None, 36)
timer = pygame.time.Clock()

# create sprite group
player_group = pygame.sprite.Group()
zombie_group = pygame.sprite.Group()
health_group = pygame.sprite.Group()

# create the player sprite
player = MySprite()
player.load(r"D:\9806-MorePython\resources\code\chap08\farmer walk.png", 96, 96, 8)
player.position = 80, 80
player.direction = 4
player_group.add(player)

# create the zombie sprite
clock = 0
zombie_image = r"D:\9806-MorePython\resources\code\chap08\zombie walk.png"
for n in range(0, 10):
    create_zombie(zombie_group)

# create health sprite
for n in range(0, 3):
    health = MySprite()
    health.load(r"D:\9806-MorePython\resources\code\chap08\health.png", 32, 32, 1)
    health.position = random.randint(0, 700), random.randint(0, 500)
    health_group.add(health)

# draw background
# background = pygame.image.load(r"D:\bitmaps\cp8background.png").convert_alpha()


game_over = False
player_moving = False
player_health = 100


# repeating loop
while True:
    timer.tick(10)
    framerate = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        sys.exit()
    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        player.direction = 0
        player_moving = True
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.direction = 2
        player_moving = True
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.direction = 4
        player_moving = True
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.direction = 6
        player_moving = True
    else:
        player_moving = False

    # these things should not happen when the game is over
    if not game_over:
        # set animation frames based on player's direction
        player.first_frame = player.direction * player.columns
        player.last_frame = player.first_frame + player.columns - 1
        if player.frame < player.first_frame:
            player.frame = player.first_frame
        if not player_moving:
            # stop animation when player is not pressing a key
            player.frame = player.first_frame = player.last_frame
        else:
            # move player in direction
            player.velocity = calc_velocity(player.direction)
            player.velocity.x *= 3.0
            player.velocity.y *= 3.0

        # update player sprite
        player_group.update(framerate)

        # manually move the player
        if player_moving:
            player.X += player.velocity.x
            player.Y += player.velocity.y

            # player become hungry when moving
            player_health -= 0.1

            if player.X < 0:
                player.X = 0
            if player.X > 700:
                player.X = 700
            if player.Y < 0:
                player.Y = 0
            if player.Y > 500:
                player.Y = 500

        # update zombie sprites
        if framerate - clock >= 10000:
            create_zombie(zombie_group)
            clock = framerate
            print(len(zombie_group))
        zombie_group.update(framerate)

        # manually iterate through all the zombies
        for z in zombie_group:
            # set the zombie's animation range
            z.first_frame = z.direction * z.columns
            z.last_frame = z.first_frame + z.columns - 1
            if z.frame < z.first_frame + 1:  # replace if z.frame < z.first_frame#
                z.frame = z.first_frame
                z.velocity = calc_velocity(z.direction)

            # keep the zombie on the screen
            z.X += z.velocity.x
            z.Y += z.velocity.y
            if z.X < 0 or z.X > 700 or z.Y < 0 or z.Y > 500:
                reverse_direction(z)
                z.velocity = calc_velocity(z.direction)

            # check for collision with zombies
            attacker = None
            attacker = pygame.sprite.spritecollideany(player, zombie_group)
            if attacker is not None:
                # We got a hit, now do more precise check
                if pygame.sprite.collide_rect_ratio(0.5)(player, attacker):
                    player_health -= 10
                    if attacker.X < player.X:
                        player.X += 10
                    elif attacker.X > player.X:
                        player.X -= 10
                    else:
                        attacker = None


        # update the health drop
        health_group.update(framerate)

        # check for collision with health
        health_eat = None
        for h in health_group:
            health_eat = pygame.sprite.spritecollideany(player, health_group)
            if health_eat is not None:
                if pygame.sprite.collide_rect_ratio(0.5)(player, health_eat):
                    player_health += 30
                    health_eat.X = random.randint(0, 700)
                    health_eat.Y = random.randint(0, 500)
                    if player_health > 100:
                        player_health = 100
                else:
                    health_eat = None

        # is player dead?
        if player_health <= 0:
            game_over = True

    # clean the screen
    screen.fill((50, 50, 100))
    # screen.blit(background, (0, 0))

    # draw sprites
    health_group.draw(screen)
    player_group.draw(screen)
    zombie_group.draw(screen)

    # draw energy bar
    pygame.draw.rect(screen, (50, 150, 50, 180), Rect(300, 570, player_health * 2, 25))
    pygame.draw.rect(screen, (100, 200, 100, 180), Rect(300, 570, 200, 25), 2)

    if game_over:
        print_text(font, 300, 100, "G A M E O V E R")

    pygame.display.update()

__author__ = 'added new'
