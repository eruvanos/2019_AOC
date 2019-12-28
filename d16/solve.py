from itertools import cycle


# pattern wiederholt sich
# pattern = fac * e for e in pattern
# skip first entry
from typing import List

from tqdm import tqdm

from utils import Timer


def pat(pattern: List[int], factor: int):
    def inner():
        for p in pattern:
            yield from factor * [p]

    gen = cycle(inner())
    next(gen) # skip one
    yield from gen


def fft(sequence: List[int], pattern):
    result = list()
    for fac in range(len(sequence)):
        gen_pattern = pat(pattern, fac + 1)
        out = sum(s * p for s, p in zip(sequence, gen_pattern))
        cut_out = abs(out) % 10
        result.append(cut_out)
    return result


def solve(file, rounds):
    with open(file) as f:
        lines = f.readlines()
    seq = tuple(map(int, lines[0]))
    # seq *= 10000

    for _ in range(rounds):#tqdm(range(rounds), total=rounds):
        seq = fft(seq, [0, 1, 0, -1])
        print(''.join(map(str, seq)))

    return seq



if __name__ == '__main__':
    # r = solve('input_test_1.txt', 4)
    # r = solve('input_test_2.txt', 100)
    r = solve('input.txt', 100)

    print(''.join(map(str, r[:8])))
    print(''.join(map(str, r)))
