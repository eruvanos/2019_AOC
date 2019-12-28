from collections import Counter

from op_machine import Interpreter


def solve(file):
    interpreter = Interpreter.from_file(file)
    interpreter.run()

    field = ''
    while data := interpreter.get():
        field += chr(data)

    print(field)

    matrix = field.splitlines()[:-1]

    intersections = []
    for y in range(1, len(matrix) - 1):
        row = matrix[y]
        for x in range(1, len(row) - 1):
            cell = row[x]

            if cell == '#':
                ns = (
                    matrix[y - 1][x],
                    matrix[y + 1][x],
                    matrix[y][x + 1],
                    matrix[y][x - 1],
                )
                if Counter(ns)['#'] > 2:
                    intersections.append((x, y))

    for inter in intersections:
        print(inter)

    print('Sum', sum(map(lambda e: e[0] * e[1], intersections)))


if __name__ == '__main__':
    solve('input.txt')
    # solve('input.txt')
