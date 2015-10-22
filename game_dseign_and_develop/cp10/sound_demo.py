import pygame
import sys
from pygame.locals import *

pygame.init()
pygame.mixer.init()
audio_clip = pygame.mixer.Sound(r"E:\oggfile\VO_CS2_121_Play_01.ogg")
channel = pygame.mixer.find_channel(True)
channel.set_volume(1)
channel.play(audio_clip)
while True:
    for event in pygame.event.get():
        if event.type in [pygame.QUIT, pygame.KEYUP]:
            sys.exit()
    screen = pygame.display.set_mode((600, 500))
    pygame.display.set_caption("Sound Demo")
    screen.fill((50, 50, 100))
    pygame.display.update()

__author__ = 'added new'
