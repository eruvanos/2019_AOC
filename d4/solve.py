from typing import List


def is_valid(password):
    prev = int(password[0])
    found_double = False

    for x in map(int, password[1:]):
        if x < prev:
            return False
        if x == prev:
            found_double = True
        prev = x

    return found_double

def is_valid_v2(password):
    prev = int(password[0])
    groups = {}

    for x in map(int, password[1:]):
        if x < prev:
            return False
        if x == prev:
            groups.setdefault(x, 1)
            groups[x] += 1
        prev = x

    if 2 in list(groups.values()):
        return True
    else:
        return False


def solve():
    with open('input.txt') as f:
        _input: List = f.read()

    start, end = map(int, _input.split('-'))

    # Part 1
    valid_passwords = []
    for x in range(start, end):
        seed = str(x)
        if is_valid(seed):
            valid_passwords.append(seed)
    print(len(valid_passwords))

    # Part 2
    valid_passwords = []
    for x in range(start, end):
        seed = str(x)
        if is_valid_v2(seed):
            valid_passwords.append(seed)
    print(len(valid_passwords))


if __name__ == '__main__':
    assert is_valid('111111')
    assert not is_valid('223450')
    assert not is_valid('123789')

    solve()
