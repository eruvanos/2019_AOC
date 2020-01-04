from utils import Vector
LETTERS = 'abcdefghijklmnopqrstuvwxyz'

def solve(file):
    with open(file) as f:
        mace = f.readlines()

    walls = set()
    keys = dict()
    doors = dict()

    for x, row in enumerate(mace):
        for y, cell in enumerate(row):
            if cell == '#':
                walls.add(Vector(x,y))

            if cell in LETTERS.lower():
                keys[Vector(x,y)] = cell
            if cell in LETTERS.upper():
                doors[Vector(x,y)] = cell

if __name__ == '__main__':
    solve('input_test_1.txt')
    # solve('input.txt')
