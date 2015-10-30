# coding:utf-8
# Player/Monster classes
from dungeon import *


# this function get a random number range in (1, faces)
def Die(faces):
    roll = random.randint(1, faces)
    return roll


# class Player
class Player(object):
    def __init__(self, dungeon, level, name):
        self.dungeon = dungeon
        self.level = level
        self.alive = True
        self.x = 0
        self.y = 0
        self.name = name
        self.gold = 0
        self.experience = 0
        self.weapon = level
        self.weapon_name = "Club"
        self.armor = level
        self.armor_name = "Rags"
        self.roll()
        self.sprite = MySprite()
        self.sprite.load(r"GAME_ARGUMENTS/player.png", frame_width, frame_height, 12)

    # 随机设置玩家初始能力值
    def roll(self):
        # 力量
        self.strength = 6 + Die(6) + Die(6)
        # 敏捷
        self.dexterous = 6 + Die(6) + Die(6)
        # 体质
        self.constitution = 6 + Die(6) + Die(6)
        # 智力
        self.intelligence = 6 + Die(6) + Die(6)
        # 魅力
        self.charm = 6 + Die(6) + Die(6)
        # 最大生命值
        self.max_health = 10 + Die(self.constitution)
        # 生命值
        self.health = self.max_health

    # 等级提升，玩家能力随机增加
    def levelUp(self):
        self.strength += Die(6)
        self.dexterous += Die(6)
        self.constitution += Die(6)
        self.intelligence += Die(6)
        self.charm += Die(6)
        self.max_health += Die(6)
        self.health = self.max_health

    def draw(self, surface, image):
        self.dungeon.draw_image(surface, self.sprite, self.x, self.y, image)

    # 移动玩家角色
    def move(self, movex, movey):
        image = self.dungeon.get_image_at(self.x + movex, self.y + movey)
        if image not in (self.dungeon.room_image, self.dungeon.hall_image):
            return False
        else:
            self.x += movex
            self.y += movey
            return True

    def moveUp(self):
        return self.move(0, -1)

    def moveDown(self):
        return self.move(0, 1)

    def moveLeft(self):
        return self.move(-1, 0)

    def moveRight(self):
        return self.move(1, 0)

    # 获得血瓶，血量增加
    def add_health(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        elif self.health < 0:
            self.health = 0

    # 获得经验
    def add_experience(self, xp):
        cap = math.pow(10, self.level)
        self.experience += xp
        if self.experience > cap:
            self.levelUp()

    # 计算初始攻击伤害，还应减去防守减伤来得到真实伤害
    def get_attack(self):
        attack = self.strength + Die(20)
        return attack

    # 计算防守值带来的减伤效果
    def get_defense(self):
        defense = self.dexterous + self.armor
        return defense

    # 真实伤害
    def get_damage(self, defence):
        damage = Die(8) + self.strength + self.weapon - defence
        return damage

# class Monster extend Player
class Monster(Player):
    def __init__(self, dungeon, level, name):
        Player.__init__(self, dungeon, level, name)
        self.gold = random.randint(1, 4) * level
        self.strength = 1 + Die(6) + Die(6)
        self.dexterous = 1 + Die(6) + Die(6)
        self.sprite = MySprite()
        self.sprite.load(r"GAME_ARGUMENTS/robot.png", frame_width, frame_height, 12)

    def draw(self, surface, image):
        self.dungeon.draw_image(surface, self.sprite, self.x, self.y, image)

__author__ = 'liuchuang'
