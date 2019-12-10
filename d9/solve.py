from op_machine import Interpreter
from utils import Timer


def solve():
    subject = Interpreter.from_file('input.txt')
    subject.put(1)
    subject.run()
    print('Part 1:', subject.get())

    subject = Interpreter.from_file('input.txt')
    subject.put(2)

    with Timer() as t:
        subject.run()
    print('Part 2:', subject.get(), f'finished in {t.time()} sec')


if __name__ == '__main__':
    solve()
