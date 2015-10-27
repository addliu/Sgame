import sys
import time
import random
import math
import pygame
from pygame.locals import *
from MyLibrary import *

levels = (
    (1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1,),

    (2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
     2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2,
     2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2,
     2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
     2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
     2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
     2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
     2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2,
     2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2,
     2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,),

    (3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
     3, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 3,
     3, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 3,
     3, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 3,
     3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
     3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
     3, 3, 0, 0, 0, 3, 3, 0, 0, 0, 3, 3,
     3, 3, 0, 0, 0, 3, 3, 0, 0, 0, 3, 3,
     3, 3, 0, 0, 0, 3, 3, 0, 0, 0, 3, 3,
     3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,),

    (0, 0, 0, 1, 5, 1, 4, 1, 6, 0, 0, 0,
     0, 0, 2, 1, 2, 4, 5, 3, 1, 7, 0, 0,
     0, 3, 4, 2, 5, 3, 1, 5, 2, 7, 6, 0,
     7, 1, 2, 1, 2, 1, 3, 1, 3, 1, 4, 1,
     1, 3, 5, 6, 5, 2, 6, 1, 7, 4, 5, 3,
     6, 1, 4, 1, 7, 2, 2, 5, 4, 6, 2, 1,
     5, 7, 6, 4, 2, 3, 5, 2, 1, 4, 3, 5,
     0, 3, 1, 5, 1, 6, 1, 3, 2, 5, 1, 0,
     0, 0, 3, 2, 3, 5, 6, 4, 5, 2, 0, 0,
     0, 0, 0, 4, 1, 4, 1, 7, 1, 0, 0, 0,),
)


# this function increments the level
def goto_next_level():
    global level, levels
    level += 1
    if level > len(levels) - 1:
        level = 0
    load_level()


# this function updates the blocks in play
def update_block():
    global block_group, waiting
    if len(block_group) == 0:
        goto_next_level()
        waiting = True
    block_group.update(ticks, 50)


# this function sets up the blocks for the levels
def load_level():
    global level, block_image, block_group, levels, block
    block_image = pygame.image.load(r"image/blocks.png").convert_alpha()
    block_group.empty()  # reset block group
    for bx in range(0, 12):
        for by in range(0, 10):
            block = MySprite()
            block.set_image(block_image, 58, 28, 4)
            x = 40 + bx * (block.frame_width + 1)
            y = 60 + by * (block.frame_height + 1)
            block.position = x, y
            # read blocks from levels data
            num = levels[level][by*12+bx]
            # give blocks differently color
            if num is not 0:
                num = random.randint(1, 8)
            block.first_frame = num - 1
            block.last_frame = num - 1
            if num > 0:  # 0 is blank
                block_group.add(block)


# this function initializes the game
def game_init():
    global screen, font, timer
    global paddle_group, block_group, ball_group
    global paddle, block_image, block, ball

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Block Breaker Game")
    font = pygame.font.Font(None, 36)
    pygame.mouse.set_visible(False)
    timer = pygame.time.Clock()

    # create sprite group
    paddle_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()
    ball_group = pygame.sprite.Group()

    # create the paddle sprite
    paddle = MySprite()
    paddle.load(r"image/paddle.png")
    paddle.position = 400, 540
    paddle_group.add(paddle)

    # create the ball sprite
    ball = MySprite()
    ball.load(r"image/ball.png")
    ball.position = 400, 300
    ball_group.add(ball)


# this function moves the paddle
def move_paddle():
    global movex, movey, keys, waiting
    paddle_group.update(ticks, 50)
    if keys[pygame.K_ESCAPE]:
        if waiting:
            waiting = False
            reset_ball()
    elif keys[pygame.K_LEFT]:
        paddle.velocity.x = -10.0
    elif keys[pygame.K_RIGHT]:
        paddle.velocity.x = 10
    else:
        if movex < -2:
            paddle.velocity.x = movex
        elif movex > 2:
            paddle.velocity.x = movex
        else:
            paddle.velocity.x = 0
    paddle.X += paddle.velocity.x
    if paddle.X < 0:
        paddle.X = 0
    elif paddle.X > 710:
        paddle.X = 710


# this function reset the ball's velocity
def reset_ball():
    ball.velocity = Point(4.5, -7.0)


# this function moves the ball
def move_ball():
    global waiting, ball, game_over, lives
    # move the ball
    ball_group.update(ticks, 50)
    if waiting:
        ball.X = paddle.X + 40
        ball.Y = paddle.Y - 20
    ball.X += ball.velocity.x
    ball.Y += ball.velocity.y
    if ball.X < 0:
        ball.X = 0
        ball.velocity.x *= -1
    elif ball.X > 780:
        ball.X = 780
        ball.velocity.x *= -1
    elif ball.Y < 0:
        ball.Y = 0
        ball.velocity.y *= -1
    elif ball.Y > 580:  # missed paddle
        waiting = True
        lives -= 1
        if lives < 1:
            game_over = True


# this function test for collision between ball and paddle, you can also set ball's velocity
def collision_ball_paddle():
    if pygame.sprite.collide_rect(ball, paddle):
        play_sound(coinflip)
        ball.velocity.y = -abs(ball.velocity.y)
        bx = ball.X + 8
        px = paddle.X + paddle.frame_width/2
        if bx < px:  # left side of paddle?
            ball.velocity.x = -abs(ball.velocity.x) - 0.1
        else:  # right side of paddle?
            ball.velocity.x = abs(ball.velocity.x) + 0.1


# this function tests for collision between ball and blocks
def collision_ball_blocks():
    global score, block_group, ball
    hit_block = pygame.sprite.spritecollideany(ball, block_group)
    if hit_block is not None:
        score += 10
        play_sound(hit)
        block_group.remove(hit_block)
        bx = ball.X + 8
        by = ball.Y + 8

        # hit middle of block from above or below?
        if hit_block.X + 5 < bx < hit_block.X + hit_block.frame_width - 5:
            if by < hit_block.Y + hit_block.frame_height/2:  # above?
                ball.velocity.y = -abs(ball.velocity.y)
            else:  # below?
                ball.velocity.y = abs(ball.velocity.y)

        # hit left side of block?
        elif bx < hit_block.X + 5:
            ball.velocity.x = -abs(ball.velocity.x)

        # hit right side of block?
        elif bx > hit_block.X + hit_block.frame_width - 5:
            ball.velocity.x = abs(ball.velocity.x)

        # handle any other situation
        else:
            ball.velocity.y *= -1


# this function initializes sound
def audio_init():
    global coinflip, hit, bgm
    pygame.mixer.init()
    coinflip = pygame.mixer.Sound(r"auido/coinflip.wav")
    hit = pygame.mixer.Sound(r"auido/hit.wav")
    bgm = pygame.mixer.Sound(r"auido/flowerdance.ogg")


# this function play the sound
def play_sound(sound):
    channel = pygame.mixer.find_channel(True)
    channel.set_volume(0.5)
    channel.play(sound)


# this function change the background color
def change_color(alpha):
    global vel_0, vel_1, vel_2
    alpha[0] += vel_0
    alpha[1] += vel_1
    alpha[2] += vel_2
    if alpha[0] < 0:
        alpha[0] = 0
        vel_0 *= -1
    elif alpha[0] > 255:
        alpha[0] = 255
        vel_0 *= -1
    if alpha[1] < 0:
        alpha[1] = 0
        vel_1 *= -1
    elif alpha[1] > 255:
        alpha[1] = 255
        vel_1 *= -1
    if alpha[2] < 0:
        alpha[2] = 0
        vel_2 *= -1
    elif alpha[2] > 255:
        alpha[2] = 255
        vel_2 *= -1

# main program begins
game_init()
audio_init()
play_sound(bgm)
game_over = False
waiting = True
score = 0
lives = 3
level = 0
vel_0 = 0.1
vel_1 = 0.2
vel_2 = 0.3
alpha = [50, 50, 100, 255]
# alpha_0 = 0.1
# alpha_1 = 0.2
# alpha_2 = 0.3
# alpha_vel = -0.1
load_level()

# repeating loop
while True:
    timer.tick(30)
    ticks = pygame.time.get_ticks()

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            movex, movey = event.rel
        elif event.type == pygame.MOUSEBUTTONUP:
            if waiting:
                waiting = False
                reset_ball()
        # elif event.type == pygame.KEYUP:
        #     if event.key == pygame.K_RETURN and game_over is False and waiting is True:
        #         goto_next_level()

    # handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        sys.exit()

    # do update
    if not game_over:
        update_block()
        move_paddle()
        move_ball()
        collision_ball_paddle()
        collision_ball_blocks()
        change_color(alpha)
    screen.fill((alpha[0], alpha[1], alpha[2], alpha[3]))
    block_group.draw(screen)
    ball_group.draw(screen)
    paddle_group.draw(screen)
    print_text(font, 0, 0, "SCORE: " + str(score))
    print_text(font, 200, 0, "LEVEL: " + str(level + 1))
    print_text(font, 400, 0, "BLOCKS: " + str(len(block_group)))
    print_text(font, 670, 0, "BALLS: " + str(lives))
    if game_over:
        print_text(font, 300, 380, "G  A  M  E  O  V  E  R ")
    pygame.display.update()

__author__ = 'added new'
