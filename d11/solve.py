from threading import Thread
from time import sleep

import arcade

from op_machine import Interpreter
from utils import Vector
from utils.direction import ARROW_DIR


class Robot(Thread):
    def __init__(self, interpreter: Interpreter):
        super().__init__()
        self.pos = Vector(0, 0)
        self._interpreter = interpreter
        self._direction = 0
        self._directions = 'URDL'

    def direction(self):
        return self._directions[self._direction % 4]

    def turn_left(self):
        self._direction -= 1

    def turn_right(self):
        self._direction += 1

    def move(self):
        self.pos += ARROW_DIR[self.direction()]

    def finished(self):
        return self._interpreter.finished

    def run(self):
        self._interpreter.run()

    def put(self, value: int):
        self._interpreter.put(value)

    def get(self):
        return self._interpreter.get()


class Canvas(arcade.Window):
    def __init__(self, robot):
        super().__init__(800, 800)

        self.sprites: arcade.SpriteList = arcade.SpriteList()
        self.shapes = arcade.ShapeElementList()

        self.rob = arcade.Sprite('robot.png', 25 / 115)

        self.sprites.append(self.rob)
        self.robot = robot
        self.new_paintings = []
        self.set_viewport(-400, 400, -400, 400)
        self.delay = 0.001
        self._last_update = 0

        self.draw_sprites = True

    def on_update(self, delta_time: float):
        self._last_update += delta_time

        CELL = 5
        self.rob.center_x = self.robot.pos.x * CELL
        self.rob.center_y = self.robot.pos.y * CELL

        # self.rob.angle = DIRECTION_ANGLES[self.robot.direction()]

        for paint in self.new_paintings[:]:
            pos, color = paint
            self.shapes.append(arcade.create_rectangle_filled(pos.x * CELL, pos.y * CELL, CELL, CELL, color))

            self.new_paintings.remove(paint)

    def on_key_press(self, symbol: int, modifiers: int):
        if self._last_update > 500:
            self._last_update = 0
            if symbol == arcade.key.NUM_ADD:
                self.delay *= 10
                print(self.delay)

            if symbol == arcade.key.NUM_SUBTRACT:
                self.delay *= 0.1
                print(self.delay)

    def on_draw(self):
        arcade.start_render()
        self.shapes.draw()

        if self.draw_sprites:
            self.sprites.draw()


def solve():
    COLORS = {0: arcade.color.BLACK, 1: arcade.color.WHITE, }

    # for
    # 0 paint black
    # 1 paint white
    # 0 left, 1 right

    robot = Robot(Interpreter.from_file('input.txt'))
    canvas = Canvas(robot)

    def rob_controller():
        robot.start()
        ship = {
            Vector(0, 0): 1  # Part 2
        }

        while not robot.finished():
            robot.put(ship.get(robot.pos, 0))

            color = robot.get()
            turn = robot.get()

            # Painting

            canvas.new_paintings.append(
                (robot.pos, COLORS[color])
            )
            ship[robot.pos] = color

            # Turn
            if turn == 0:
                robot.turn_left()
            elif turn == 1:
                robot.turn_right()

            robot.move()
            sleep(canvas.delay)

        print(len(ship))
        canvas.draw_sprites = False

    Thread(target=rob_controller, daemon=True).start()
    arcade.run()


if __name__ == '__main__':
    solve()
