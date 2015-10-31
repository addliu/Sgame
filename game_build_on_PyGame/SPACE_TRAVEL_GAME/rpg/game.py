import player
import dungeon
import pygame
from pygame.locals import *
import sys

CAPTION = "SPACE TRAVEL"


def game_init():
    global _player, _dungeon
    _dungeon = dungeon.Dungeon()
    _dungeon.create_dungeon()
    _player = player.Player(_dungeon)


def rpg_start():
    global screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
    buffer = pygame.Surface((1600, 1600))
    pygame.display.set_caption(CAPTION)
    game_init()
    timer = pygame.time.Clock()
    while True:
        timer.tick(5)
        ticks = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_UP or event.key == K_w:
                    _player.move_up()
                elif event.key == K_DOWN or event.key == K_s:
                    _player.move_down()
                elif event.key == K_LEFT or event.key == K_a:
                    _player.move_left()
                elif event.key == K_RIGHT or event.key == K_d:
                    _player.move_right()
        _dungeon.draw(buffer)
        _player.update(ticks)
        _player.draw_player(buffer)
        screen.fill((0, 0, 0))
        x = 400 - _player.X * _player.frame_width
        y = 300 - _player.Y * _player.frame_height
        screen.blit(buffer, (x, y))
        pygame.display.flip()


__author__ = 'added new'
