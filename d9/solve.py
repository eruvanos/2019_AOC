from op_machine import Interpreter


def solve():
    subject = Interpreter.from_file('input.txt')
    subject.put(1)
    subject.run()
    print('Part 1:', subject.get())

    subject = Interpreter.from_file('input.txt')
    subject.put(2)
    subject.run()
    print('Part 2:', subject.get())


if __name__ == '__main__':
    solve()
