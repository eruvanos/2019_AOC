from op_machine import Interpreter


def solve(file):
    inter = Interpreter.from_file('input.txt')
    inter.start()

    with open(file) as f:
        instructions = f.readlines()

    for instruction in instructions:
        instruction = instruction.strip()
        if len(instruction) == 0 or instruction[0] == '#':
            continue

        for char in instruction:
            inter.put(ord(char))
        inter.put(10)

    while not inter.finished or not inter.stdout.empty():

        value = inter.get()
        if value is not None:
            if value <= 128:
                print(chr(value), end='')
            else:
                print(value)





if __name__ == '__main__':
    solve('part1.txt')
    solve('part2.txt')
