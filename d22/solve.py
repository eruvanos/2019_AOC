from itertools import count

import tqdm


def deal_into_new(stack: list) -> list:
    return list(reversed(stack))


def cut(stack: list, n: int):
    return stack[n:] + stack[:n]


def deal_with(deck: list, n: int):
    counter = map(lambda c: c % len(deck), count(step=n))
    return list(map(lambda x: x[1], sorted(zip(counter, deck))))


def deck(n) -> list:
    return list(range(n))


def solve(file: str, d: list):
    with open(file) as f:
        instructions = f.readlines()

    return shuffle(instructions, d)

def shuffle(instructions, d):
    for instruction in instructions:
        parts = instruction.split()
        if parts[0] == 'cut':
            n = int(parts[1])
            d = cut(d, n)
        elif parts[1] == 'into':
            d = deal_into_new(d)
        elif parts[1] == 'with':
            n = int(parts[3])
            d = deal_with(d, n)
        else:
            print('Unknown command', instruction)

    return d


if __name__ == '__main__':
    d = deck(10)
    assert deal_into_new(d) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert cut(d, 3) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
    assert deal_with(d, 3) == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3], deal_with(d, 3)

    assert solve('input_test_1.txt', deck(10)) == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
    assert solve('input_test_3.txt', deck(10)) == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]

    d = solve('input.txt', deck(10007))
    print('Part 1', d.index(2019))

    with open('input.txt') as f:
        instructions = f.readlines()
    d = deck(119315717514047)
    for _ in tqdm.tqdm(range(101741582076661)):
        d = shuffle(instructions, d)
    print('Part 2', d.index(2020))
