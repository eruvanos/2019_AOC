from itertools import permutations

from op_machine import Interpreter


def solve_part_1():
    def execute(phase, _in):
        interpreter = Interpreter.from_file('input.txt')
        interpreter.put(phase)
        interpreter.put(_in)
        interpreter.run()
        return list(interpreter.stream())[0]

    max_thrusters = 0

    for combination in permutations(range(5)):
        x = 0
        for phase in combination:
            x = execute(phase, x)
        max_thrusters = max(max_thrusters, x)
        print(combination, '>', x)

    print(f'{max_thrusters=}')


def solve_part_2():
    # setup
    def execute(combination):
        # create amplifier
        _in = [3, 26, 1001, 26, -4, 26,
               3, 27, 1002, 27, 2, 27,
               1, 27, 26, 27, 4, 27, 1001,
               28, -1, 28, 1005, 28, 6, 99,
               0, 0, 5]
        amplifiers = [
            Interpreter.from_file('input.txt'),
            Interpreter.from_file('input.txt'),
            Interpreter.from_file('input.txt'),
            Interpreter.from_file('input.txt'),
            Interpreter.from_file('input.txt'),

            # test data
            # Interpreter(_in[:]),
            # Interpreter(_in[:]),
            # Interpreter(_in[:]),
            # Interpreter(_in[:]),
            # Interpreter(_in[:]),
        ]

        # connect them
        for x in range(5):
            amplifiers[x - 1].stdout = amplifiers[x].stdin

        # fill phase input
        for phase, amp in zip(combination, amplifiers):
            amp.stdin.put(phase)

        # Add initial value
        amplifiers[0].put(0)

        for thread in [amp.start() for amp in amplifiers]:
            thread.join()

        return next(amplifiers[-1].stream())

    # RUN
    max_thrusters = 0

    for combination in permutations(range(5, 10)):
        x = execute(combination)
        max_thrusters = max(max_thrusters, x)
        print(combination, '>', x)

    print(f'{max_thrusters=}')


if __name__ == '__main__':
    # solve_part_1()
    solve_part_2()
