from threading import Thread

from op_machine import Interpreter


class Robot(Thread):
    def __init__(self, interpreter: Interpreter):
        super().__init__()
        self._interpreter = interpreter

    def run(self):
        self._interpreter.run()

    def put(self, value: int):
        self._interpreter.put(value)

    def get(self):
        return self._interpreter.get()

class Ship:
    def __init__(self):
        self._hull = {}


def solve():
    robot = Robot(Interpreter.from_file('input.txt'))
    robot.start()

    # 0 paint black
    # 1 paint white
    # 0 left, 1 right

    




if __name__ == '__main__':
    solve()
