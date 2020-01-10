from typing import List

from utils import Vector


def solve(file):
    with open(file) as f:
        lines = f.readlines()

    cells = set()

    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell == '#':
                cells.add(Vector(x, y))

    def neighbors(cells, current: Vector) -> List:
        x, y = current
        pos_neighbors = [
            (x, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x, y + 1)
        ]
        return [(x, y) for x, y in pos_neighbors if (x, y) in cells]

    def round(cells):
        new_cells = set()

        for y in range(5):
            for x in range(5):
                cell = Vector(x, y)
                ns = neighbors(cells, cell)
                if cell in cells and len(ns) == 1:
                    new_cells.add(cell)
                elif cell not in cells and len(ns) in (1, 2):
                    new_cells.add(cell)

        return new_cells

    def print_cells(cells):
        diversity = sum(2 ** (y * 5 + x) for x, y in cells)

        for y in range(5):
            for x in range(5):
                print('#' if (x, y) in cells else '.', end='')
            print()
        print('Diversity of', diversity)
        print()

    print('Initial')
    print_cells(cells)

    history = list()
    history.append(cells)

    for r in range(4000):
        print('Round', r + 1)
        cells = round(cells)
        print_cells(cells)

        if cells in history:
            print('Restarting process')
            exit()
        history.append(cells)


if __name__ == '__main__':
    # solve('input_test_1.txt')
    solve('input.txt')
