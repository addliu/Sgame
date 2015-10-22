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
        return "{X:" + str(self.x) + ", y:" + str(self.y) + "}"


class Ellipse(Point):
    wr = 0.0
    hr = 0.0

    def __init__(self, x, y, wr, hr):
        super(Ellipse, self).__init__(x, y)
        self.wr = wr
        self.hr = hr
        print("Ellipse Point constructor")

    def ToString(self):
        return super().ToString() + "{WR:" + str(self.wr) + \
            ", HR:" + str(self.hr) + "}"


class Size(object):
    width = 0.0
    height = 0.0

    def __init__(self, width, height):
        self.width = width
        self.height = height
        print("Size constructor")

    def tostring(self):
        return "{WIDTH:" + str(self.width) + ", HEIGHT:" + str(self.height) + "}"


class Rectangle(Point,Size):

    def __init__(self, x, y, width, height):
        Point.__init__(self, x, y)
        Size.__init__(self, width, height)
        print("Rectangle constructor")

    def tostring(self):
        return Point.ToString(self) + Size.tostring(self)

    def calcarea(self):
        return "AREA=" + str(self.height * self.width)

r = Rectangle(10, 10, 10, 10)
print(r.tostring())
print(r.calcarea())
