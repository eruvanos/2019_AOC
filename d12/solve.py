import itertools
import re
from dataclasses import dataclass
from itertools import count
from random import randint
from threading import Thread
from typing import Dict, List

import arcade
from arcade import SpriteList


@dataclass
class Moon:
    x: int
    y: int
    z: int

    vx = 0
    vy = 0
    vz = 0

    def __hash__(self):
        return id(self)

    def __str__(self):
        return f'{self.x=},{self.y=},{self.z=} vel: {self.vx=},{self.vy=},{self.vz=}'

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def pot(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def kin(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

    def __repr__(self):
        return str(self)

class Simulation(arcade.Window):
    def __init__(self):
        super().__init__()

        self.objects: List[Moon] = []
        self.obj_sprite: Dict[Moon, arcade.Sprite] = {}
        self.sprites = SpriteList()

        self.SCALE = 10

        self.UPS = 60
        self._last_update = 0

    def on_update(self, delta_time: float):
        self._last_update += delta_time
        if self._last_update > 1 / self.UPS:
            self._last_update = 0

            # Update sprites and viewport
            min_x, max_x = 0, 0
            min_y, max_y = 0, 0
            for obj in self.objects:
                sprite = self.obj_sprite.get(obj)

                if sprite is None:
                    sprite = self.new_sprite(obj)
                    self.obj_sprite[obj] = sprite
                    self.sprites.append(sprite)

                sprite.center_x = obj.x * self.SCALE
                sprite.center_y = obj.y * self.SCALE

                min_x = min(sprite.center_x, min_x)
                max_x = max(sprite.center_x, max_x)
                min_y = min(sprite.center_y, min_y)
                max_y = max(sprite.center_y, max_y)

            margine = 100
            self.set_viewport(min_x - margine, max_x + margine, min_y - margine, max_y + margine)

    def new_sprite(self, _: Moon):
        sprite = arcade.Sprite('meteorGrey_big1.png', scale=0.3)
        sprite.angle = randint(0, 360)
        return sprite

    def on_draw(self):
        arcade.start_render()
        self.sprites.draw()


def solve():
    # Part 1
    # file = 'input.txt'
    # STEPS = 1000

    # Test
    # file = 'input_test_1.txt'
    # STEPS = 10

    # Part 2 - tests
    # file = 'input_test_1.txt'
    file = 'input_test_2.txt'
    STEPS = None

    with open(file) as f:
        lines = f.readlines()

    moons = []
    for line in lines:
        match = re.match(r'^<x=(?P<x>-?\d*),\sy=(?P<y>-?\d*),\sz=(?P<z>-?\d*)>$', line)
        moon = Moon(int(match['x']), int(match['y']), int(match['z']))
        moons.append(moon)

    history = set()

    def gravity():
        for round in range(1, 1 + STEPS) if STEPS else count(1):
            for m1, m2 in itertools.combinations(moons, 2):

                if m1.x < m2.x:
                    m1.vx += 1
                    m2.vx -= 1
                elif m1.x > m2.x:
                    m1.vx -= 1
                    m2.vx += 1

                if m1.y < m2.y:
                    m1.vy += 1
                    m2.vy -= 1
                elif m1.y > m2.y:
                    m1.vy -= 1
                    m2.vy += 1

                if m1.z < m2.z:
                    m1.vz += 1
                    m2.vz -= 1
                elif m1.z > m2.z:
                    m1.vz -= 1
                    m2.vz += 1

            for moon in moons:
                moon.move()

            snapshot = str(moons)
            if snapshot in history:
                print(f'Same state after {round-1}')
                return
            else:
                history.add(snapshot)

            if round % 100_000 == 0:
                print(f'\r {round-1}', end='')


            # print()
            # print(f'Round {round}')
            # energy = 0
            # for moon in moons:
            #     print('\t', moon)
            #     energy += moon.pot() * moon.kin()
            # print(f'{energy=}')

            # sleep(1)

    Thread(target=gravity).start()

    # sim = Simulation()
    # sim.objects = moons
    # arcade.run()


if __name__ == '__main__':
    solve()
