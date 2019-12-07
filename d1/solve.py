def calc_fuel_1(mass):
    return mass // 3 - 2


def calc_fuel_2(mass):
    total = 0
    add_fuel = mass
    while (add_fuel := add_fuel // 3 - 2) > 0:
        total += add_fuel
    return total


def solve_1():
    with open('./input_1.txt') as f:
        return sum(calc_fuel_1(int(row)) for row in f.readlines())


def solve_2():
    with open('./input_1.txt') as f:
        return sum(calc_fuel_2(int(row)) for row in f.readlines())


if __name__ == '__main__':
    assert calc_fuel_1(12) == 2
    assert calc_fuel_1(14) == 2
    assert calc_fuel_1(1969) == 654
    assert calc_fuel_1(100756) == 33583

    payload_fuel = solve_1()
    print('Part 1', payload_fuel)

    payload_fuel = solve_2()
    print('Part 2', payload_fuel)
