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
        return Vector(self.x + y, self.y + y)

    def __sub__(self, other):
        x, y = other
        return Vector(self.x - y, self.y - y)

    def manhattan(self, other: 'Vector'):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def distance(self, other: 'Vector'):
        x = self.x - other.x
        y = self.y - other.y
        return math.sqrt(x ** 2 + y ** 2)
