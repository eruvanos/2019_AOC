from op_machine import Interpreter


def new_inter():
    inter = Interpreter.from_file('input.txt')
    return inter


def test(x, y):
    if x < 0 or y < 0:
        result = 0
    else:
        inter = new_inter()
        inter.put(x)
        inter.put(y)
        inter.run()
        result = inter.get()

    # print(f'test {x}, {y} -> {result}')
    return result


def solve():
    y = 5
    max_x = 10
    while True:
        for x in range(max_x, 0, -1):
            right = test(x, y)
            print(f'test {x}, {y} -> {right}')
            if right:  # right corner

                if test(x - 99, y):  # left corner
                    if test(x - 99, y + 99):  # bottom left
                        return x - 99, y

                y += 1
                max_x = x + 2
                break


def print_ship(start_x, start_y):
    for y in range(start_y -1, start_y + 101):

        x = start_x - 110
        in_track = False
        print(f'{y:2} ', end='')
        while True:
            result = test(x, y)

            symbol = '#' if result else '.'
            if start_x <= x <= start_x + 99:
                if start_y <= y <= start_y + 99:
                    symbol = 'O'

            print(symbol, end='')
            x += 1

            if in_track and not result:
                print()
                break
            elif result:
                in_track = True


if __name__ == '__main__':
    # print('part1')
    # print_ship()

    print('part2')
    x, y = solve()
    print(f'{x=}, {y=}')
    print(f'solved part 2: {x * 10000 + y}')

    print_ship(x, y)
    # solve('input.txt')
