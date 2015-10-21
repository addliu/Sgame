import math
__author__ = 'added new'


class Point(object):
    x = 0.0
    y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        print("Point constructor")

    def ToString(self):
        return "{X:" + str(self.x) + "," + "y:" + str(self.y) + "}"


class Circle(Point):
    radius = 0.0

    def __init__(self, x, y, radius):
        super(Circle, self).__init__(x, y)
        self.radius = radius
        print("Circle constructor")

    def ToString(self):
        return super(Circle, self).ToString() + \
            "{RADIUS=" + str(self.radius) + "}"

    def calccircum(self):
        return "CIRCUM=" + str(2 * math.pi * self.radius)

p = Point(10, 20)
c = Circle(100, 100, 25)

print(p.ToString())
print(c.ToString())
print(c.calccircum())
