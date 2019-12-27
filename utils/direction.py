from utils import Vector

ARROW_DIR = {
    'R': Vector(0, 1),
    'L': Vector(0, -1),
    'U': Vector(1, 0),
    'D': Vector(-1, 0)
}
"""Right, Left, Up, Down"""

NESW_DIR = {
    'E': Vector(0, 1),
    'W': Vector(0, -1),
    'N': Vector(1, 0),
    'S': Vector(-1, 0)
}
"""North, East, South, West"""

NESW_ARROW = {
    'E': 'R',
    'W': 'L',
    'N': 'U',
    'S': 'D',
}
"""Convert NESW to Arrow"""

ARROW_NESW = {
    'R': 'E',
    'L': 'W',
    'U': 'N',
    'D': 'S',
}
"""Convert Arrow to NESW"""

ANGLES_DIR = {
    'R': 90,
    'L': 270,
    'U': 0,
    'D': 180
}
"""ARROW to Angle U = 0° """
