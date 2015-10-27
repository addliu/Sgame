# coding:utf8
import sys
import time
import random
import math
import pygame
from pygame.locals import *
from mylibrary import *

# 关卡信息
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


# 进入下一关
def goto_next_level():
    global level, levels
    level += 1
    if level > len(levels) - 1:
        level = 0
    load_level()


# 更新砖块UI
def update_block():
    global block_group, waiting
    if len(block_group) == 0:
        goto_next_level()
        waiting = True
    block_group.update(ticks, 50)


# 设置新关卡的UI
def load_level():
    global level, block_image, block_group, levels, block
    block_image = pygame.image.load(r"image/blocks.png").convert_alpha()
    # 重置砖块精灵组
    block_group.empty()
    for bx in range(0, 12):
        for by in range(0, 10):
            block = MySprite()
            block.set_image(block_image, 58, 28, 4)
            x = 40 + bx * (block.frame_width + 1)
            y = 60 + by * (block.frame_height + 1)
            block.position = x, y
            # 从关卡信息中读取砖块信息
            num = levels[level][by*12+bx]
            # 为砖块设置不同的颜色
            if num is not 0:
                num = random.randint(1, 8)
            block.first_frame = num - 1
            block.last_frame = num - 1
            # num = 0的位置不设置砖块
            if num > 0:
                block_group.add(block)


# 初始化游戏参数
def game_init():
    global screen, font, timer, background
    global paddle_group, block_group, ball_group
    global paddle, block_image, block, ball

    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Block Breaker Game")
    font = pygame.font.Font(None, 36)
    pygame.mouse.set_visible(False)
    timer = pygame.time.Clock()
    background = pygame.image.load("image/space.png").convert_alpha()

    # 创建游戏精灵组
    paddle_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()
    ball_group = pygame.sprite.Group()

    # 创建挡板精灵
    paddle = MySprite()
    paddle.load(r"image/paddle.png")
    paddle.position = 400, 540
    paddle_group.add(paddle)

    # 创建球精灵
    ball = MySprite()
    ball.load(r"image/ball.png")
    ball.position = 400, 300
    ball_group.add(ball)


# 移动挡板
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


# 重置球的速度以及位置
def reset_ball():
    ball.velocity = Point(4.5, -7.0)


# 移动球
def move_ball():
    global waiting, ball, game_over, lives
    # 移动球
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
    elif ball.Y > 580:  # 挡板没有接住球
        waiting = True
        lives -= 1
        if lives < 1:
            game_over = True


# 处理挡板与球的碰撞
def collision_ball_paddle():
    if pygame.sprite.collide_rect(ball, paddle):
        play_sound(coinflip)
        ball.velocity.y = -abs(ball.velocity.y)
        bx = ball.X + 8
        px = paddle.X + paddle.frame_width/2
        if bx < px:  # 球落在挡板左半部分
            ball.velocity.x = -abs(ball.velocity.x) - 0.1
        else:  # 球落在挡板右半部分
            ball.velocity.x = abs(ball.velocity.x) + 0.1


# 处理球与砖块碰撞
def collision_ball_blocks():
    global score, block_group, ball
    hit_block = pygame.sprite.spritecollideany(ball, block_group)
    if hit_block is not None:
        score += 10
        play_sound(hit)
        block_group.remove(hit_block)
        bx = ball.X + 8
        by = ball.Y + 8

        # 球从上面还是下面击中砖块
        if hit_block.X + 5 < bx < hit_block.X + hit_block.frame_width - 5:
            if by < hit_block.Y + hit_block.frame_height/2:  # 球击中砖块上方
                ball.velocity.y = -abs(ball.velocity.y)
            else:  # 球击中砖块下方
                ball.velocity.y = abs(ball.velocity.y)

        # 球击中砖块左边
        elif bx < hit_block.X + 5:
            ball.velocity.x = -abs(ball.velocity.x)

        # 球击中砖块右边
        elif bx > hit_block.X + hit_block.frame_width - 5:
            ball.velocity.x = abs(ball.velocity.x)

        # 球击中砖块别的位置
        else:
            ball.velocity.y *= -1


# 初始化游戏声音
def audio_init():
    global coinflip, hit, bgm
    pygame.mixer.init()
    coinflip = pygame.mixer.Sound(r"auido/coinflip.wav")
    hit = pygame.mixer.Sound(r"auido/hit.wav")
    bgm = pygame.mixer.Sound(r"auido/flowerdance.ogg")


# 播放音乐
def play_sound(sound):
    channel = pygame.mixer.find_channel(True)
    channel.set_volume(0.5)
    channel.play(sound)


# 改变背景颜色
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

# 主程序
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

# 主循环
while True:
    timer.tick(30)
    ticks = pygame.time.get_ticks()

    # 处理事件
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

    # 处理键盘事件
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
            sys.exit()

    # 更新画面
    if not game_over:
        update_block()
        move_paddle()
        move_ball()
        collision_ball_paddle()
        collision_ball_blocks()
        change_color(alpha)
    screen.fill((alpha[0], alpha[1], alpha[2], alpha[3]))
    screen.blit(background, (0, 0))
    pygame.draw.line(screen, (0, 0, 0), (800, 0), (800, 600), 2)
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
