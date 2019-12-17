from op_machine import Interpreter
from utils import Vector


def solve():
    robot = Interpreter.from_file('input.txt')
    robot.start()

    pos = Vector(0, 0)
    directions = 'NESW'
    cur_dir = 0
    ship = dict()

    dir_map = {
        'N': (1, Vector(0, 1),),
        'E': (4, Vector(1, 0),),
        'S': (2, Vector(0, -1),),
        'W': (3, Vector(-1, 0),),
    }

    while not robot.finished:
        # walk
        next_dir, vec = dir_map[directions[cur_dir]]
        robot.put(next_dir)

        # process output
        result = robot.get()
        if result == 0:
            # cur_dir = cur_dir % 4
            pass
        elif result == 1:
            pos += vec
        elif result == 2:
            pos += vec
            print('Found oxigen')

    pass


if __name__ == '__main__':
    solve()
