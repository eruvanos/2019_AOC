from typing import NamedTuple


class Vector(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        x, y = other
        return Vector(self.x + y, self.y + y)

    def __sub__(self, other):
        x, y = other
        return Vector(self.x - y, self.y - y)


def trace_route(path):
    x, y = 0, 0
    trace = []

    vectors = {
        'R': (0, 1),
        'L': (0, -1),
        'U': (1, 0),
        'D': (-1, 0)
    }

    for direction, *steps in path:
        steps = int(''.join(steps))
        vx, vy = vectors[direction]

        for _ in range(steps):
            x += vx
            y += vy

            trace.append((x, y))

    return trace


def intersects(route1, route2):
    return set(route1).intersection(set(route2))


def manhattan(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1 - x2) + abs(y1 - y2)


def part_1(_input1, _input2):
    path1 = _input1.split(',')
    path2 = _input2.split(',')

    r1 = trace_route(path1)
    r2 = trace_route(path2)

    return min([manhattan((0, 0), inter) for inter in intersects(r1, r2)])


def part_2(_input1, _input2):
    path1 = _input1.split(',')
    path2 = _input2.split(',')

    r1 = trace_route(path1)
    r2 = trace_route(path2)

    return min([r1.index(inter) + r2.index(inter) + 2 for inter in intersects(r1, r2)])


def solve():
    with open('input.txt') as f:
        d_path1 = f.readline()
        d_path2 = f.readline()

    print(part_1('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83'))
    print('Part 1:', part_1(d_path1, d_path2))

    assert part_2('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7') == 410
    print('Part 2:', part_2(d_path1, d_path2))


if __name__ == '__main__':
    solve()
