from typing import List

from op_machine import Interpreter, read_input


def solve():
    # Part 1
    # interpreter = Interpreter.from_file('input.txt')
    #
    # interpreter.put(1)
    # interpreter.run()
    #
    # for out in interpreter.stream():
    #     print(out)

    # Part 2
    interpreter = Interpreter.from_file('input.txt')

    interpreter.put(5)
    interpreter.run()

    for out in interpreter.stream():
        print(out)


if __name__ == '__main__':
    solve()