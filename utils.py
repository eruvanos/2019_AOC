import math
from time import time
from typing import NamedTuple


class Timer:
    def __enter__(self):
        self.start = time()
        return self

    def __exit__(self, *args, **kwargs):
        self.end = time() - self.start

    def time(self):
        return self.end


class Vector(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        x, y = other
        return Vector(self.x + x, self.y + y)

    def __sub__(self, other):
        x, y = other
        return Vector(self.x - y, self.y - y)

    def manhattan(self, other: 'Vector'):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def distance(self, other: 'Vector'):
        x = self.x - other.x
        y = self.y - other.y
        return math.sqrt(x ** 2 + y ** 2)

    def angle(self, target: 'Vector'):
        """
        returns angle beween this point and the other, pointing to the east with 0 degree, running counter clockwise.
        """
        radian = math.atan2(target.y - self.y, target.x - self.x)
        degrees = math.degrees(radian)

        positive_degree = 360 + degrees
        return positive_degree


DIRECTIONS = {
    'R': Vector(0, 1),
    'L': Vector(0, -1),
    'U': Vector(1, 0),
    'D': Vector(-1, 0)
}

DIRECTION_ANGLES = {
    'R': 90,
    'L': 270,
    'U': 0,
    'D': 180
}
