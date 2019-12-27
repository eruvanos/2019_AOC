import json
from collections import namedtuple
from threading import Thread
from typing import Tuple

import arcade

from op_machine import Interpreter
from utils import Vector
from utils.data import PriorityQueue
from utils.gui import Canvas
from utils.path import SetGraph

WALL = 'X'
FREE = ' '
DIRECTIONS = 'NESW'
DIR_MAP = {
    'N': (1, Vector(0, 1),),
    'E': (4, Vector(1, 0),),
    'S': (2, Vector(0, -1),),
    'W': (3, Vector(-1, 0),),
}

key_map = {
    arcade.key.UP: 1,
    arcade.key.DOWN: 2,
    arcade.key.RIGHT: 4,
    arcade.key.LEFT: 3,
}
dir_map = {
    1: Vector(0, 1),
    2: Vector(0, -1),
    3: Vector(-1, 0),
    4: Vector(1, 0),
}

Entry = namedtuple('Entry', 'dir1 dir2 fdir')


class Algo:
    DIRS = {
        'N': Entry(*'ENW'),
        'E': Entry(*'SEN'),
        'S': Entry(*'WSE'),
        'W': Entry(*'NWS'),
    }

    def __init__(self):
        self.cd = 'N'

    def next(self, ship, cur_pos) -> Tuple['CMD', 'Vector']:
        strategy = self.DIRS[self.cd]

        cmd1, vec1 = DIR_MAP[strategy.dir1]
        cmd2, vec2 = DIR_MAP[strategy.dir2]

        if ship.get(cur_pos + vec1) is None:
            self.cd = strategy.dir1  # FIXME If we run against a wall this should not be executed
            return cmd1, vec1
        elif ship.get(cur_pos + vec2) is None:
            self.cd = strategy.dir2
            return cmd2, vec2
        else:
            self.cd = strategy.fdir
            return None, None


def run(canvas: Canvas):
    robot = Interpreter.from_file('input.txt')
    robot.start()

    cur_pos = Vector(0, 0)
    canvas.set(cur_pos, 1)
    # cur_dir = 'N'
    ship = dict()
    algo = Algo()
    oxygen_pos = None

    long_road = []

    while True:
        # walk
        old_cd = algo.cd
        cmd, vec = algo.next(ship, cur_pos)
        if cmd is None:
            continue
        next_pos = cur_pos + vec

        # manual
        # key = canvas.get_key_event()
        # while not (cmd := key_map.get(key)):
        #     pass
        # next_pos = cur_pos + dir_map[cmd]

        # sleep(0.1)
        robot.put(cmd)

        # process output
        result = robot.get()
        if result == 0:
            # hit wall, reset direction of algo
            ship[next_pos] = WALL
            canvas.add(next_pos)
            algo.cd = old_cd
        elif result in (1, 2):
            # moved
            canvas.set(next_pos, 1)
            canvas.remove(cur_pos)
            cur_pos = next_pos

            if oxygen_pos is None:  # record path
                if next_pos in set(long_road):
                    start_index = long_road.index(next_pos)
                    long_road = long_road[:start_index]

                long_road.append(next_pos)

        if result == 2:
            # found oxygen
            print(f'Found oxygen at {next_pos} {len(long_road)}')
            if oxygen_pos:
                break
            oxygen_pos = next_pos

    # calc distance
    # graph = SetGraph({key for key, value in ship.items() if value == WALL})
    # robot_path = a_star_search(graph, Vector(0, 0), oxygen_pos)
    # print(len(robot_path))
    print(long_road)

    with open('./mace.json', 'wt') as f:
        json.dump([(key.x, key.y) for key, value in ship.items() if value == WALL], f)


def solve1():
    canvas = ThisCanvas(debug=True)
    Thread(target=run, daemon=True, args=(canvas,)).start()
    arcade.run()


class ThisCanvas(Canvas):
    def create_new_sprite(self, vec: Vector):
        sprite = arcade.Sprite('wall.png', scale=0.5)
        sprite.append_texture(arcade.load_texture('robot.png', scale=0.5))
        sprite.append_texture(arcade.load_texture('bubble.png', scale=0.5))
        return sprite


def solve2():
    with open('./mace.json') as f:
        mace = json.load(f)
    mace = {Vector(x, y) for x, y in mace}

    graph = SetGraph(mace)

    queue = PriorityQueue()
    queue.put((0, Vector(16, 16)))

    max_distance = 0
    visited = set()
    while not queue.empty():
        distance, pos = queue.get()
        max_distance = max(max_distance, distance)

        visited.add(Vector(*pos))

        for n in graph.neighbors(pos):
            if n not in visited:
                queue.put((distance + 1, n))

    print(max_distance)

    canvas = ThisCanvas()


    for vec in mace:
        canvas.set(vec, 0)
    for vec in visited:
        canvas.set(vec, 2)

    arcade.run()






if __name__ == '__main__':
    # solve1()
    solve2()
