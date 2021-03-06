from queue import Queue
from threading import Thread
from typing import Dict

import arcade
from arcade import SpriteList, Sprite, load_texture

from op_machine import Interpreter
from utils import Vector


class Canvas(arcade.Window):
    def __init__(self, world_state: Dict[Vector, int], queue: Queue):
        super().__init__()

        self.world_state = world_state
        self.key_queue = queue

        self._sprites = SpriteList()
        self._obj_sprite = dict()

        self.score = 0
        self.SCALE = 64

        # shoul_update
        self.UPS = 60
        self._last_update = 0

    def create_new_sprite(self, obj):
        sprite = Sprite('wall.png', scale=0.5)
        sprite.append_texture(load_texture('box.png', scale=0.5))
        sprite.append_texture(load_texture('paddle.png', scale=2))
        sprite.append_texture(load_texture('ball.png', scale=0.5))
        return sprite

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
            self.key_queue.put(-1)
        elif symbol == arcade.key.RIGHT:
            self.key_queue.put(1)
        elif symbol == arcade.key.DOWN:
            self.key_queue.put(0)
        elif symbol == arcade.key.SPACE:
            # auto play
            self.auto_turn()

    def auto_turn(self):
        ball = None
        paddle = None
        for vec, kind in self.world_state.items():
            if kind == 4:
                ball = vec
            if kind == 3:
                paddle = vec

            if None not in (ball, paddle):
                break
        else:
            self.key_queue.put(0)
            return

        if paddle.x < ball.x:
            self.key_queue.put(1)
        elif paddle.x > ball.x:
            self.key_queue.put(-1)
        else:
            self.key_queue.put(0)

    def on_update(self, delta_time: float):
        if self.should_update(delta_time):
            self.auto_turn()

        # Update sprites and viewport
        for vec, kind in list(self.world_state.items()):
            sprite = self._obj_sprite.get(vec)

            if sprite is None:
                sprite = self.create_new_sprite(vec)
                self._obj_sprite[vec] = sprite
                self._sprites.append(sprite)

            if kind == 0:
                sprite.alpha = 0
            else:
                sprite.alpha = 255
                if kind == 1:
                    sprite.set_texture(0)
                elif kind == 2:
                    sprite.set_texture(1)
                elif kind == 3:
                    sprite.set_texture(2)
                elif kind == 4:
                    sprite.set_texture(3)

            sprite.center_x = vec.x * self.SCALE
            sprite.center_y = vec.y * self.SCALE

        self.apply_margine()

    def should_update(self, dt):
        self._last_update += dt
        if self._last_update > 1 / self.UPS:
            self._last_update = 0
            return True
        else:
            return False

    def apply_margine(self):
        min_x, max_x = 0, 0
        min_y, max_y = 0, 0
        for sprite in self._sprites:
            min_x = min(sprite.center_x, min_x)
            max_x = max(sprite.center_x, max_x)
            min_y = min(sprite.center_y, min_y)
            max_y = max(sprite.center_y, max_y)
        margine = 100
        self.set_viewport(min_x - margine, max_x + margine, max_y + margine, min_y - margine)

    def on_draw(self):
        arcade.start_render()
        self._sprites.draw()


def solve():
    # Part 1
    def part_1():
        interpreter = Interpreter.from_file('input.txt')
        interpreter.start()

        game = {}
        while not interpreter.finished:
            x = interpreter.get()
            y = interpreter.get()
            tile_type = interpreter.get()

            game[Vector(x, y)] = tile_type
        print(len([x for x in game.values() if x == 2]))

    def part_2():
        # Part 2
        interpreter = Interpreter.from_file('input.txt')
        interpreter[0] = 2

        interpreter.start()
        game = {}
        canvas = Canvas(game, interpreter.stdin)
        score = 0

        def run():
            while not (interpreter.finished and interpreter.stdout.empty()):
                x = interpreter.get()
                y = interpreter.get()
                tile_type = interpreter.get()

                if x == -1:
                    score = tile_type
                    print('Score', score)

                vec = Vector(x, y)
                game[vec] = tile_type

        Thread(target=run, daemon=True).start()

        arcade.run()

        # play the game

    part_2()


if __name__ == '__main__':
    solve()
