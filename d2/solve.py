from typing import List

from tqdm import tqdm

DEBUG = False


def log(*text):
    if DEBUG:
        print(*text)


def solve():
    # solve part 1
    def read_input(_list: list):
        return {i: int(v) for i, v in enumerate(_list)}

    def run(init_state):

        state = read_input(init_state)

        ic = 0
        while True:
            op = state[ic]

            if op == 1:
                state[state[ic + 3]] = state[state[ic + 1]] + state[state[ic + 2]]
                log(f'Execute {state[ic + 3]} = {state[ic + 1]} + {state[ic + 2]}')
            elif op == 2:
                state[state[ic + 3]] = state[state[ic + 1]] * state[state[ic + 2]]
                log(f'Execute {state[ic + 3]} = {state[ic + 1]} * {state[ic + 2]}')
            elif op == 99:
                log('Stop program')
                break
            else:
                raise Exception(f'Unknown OP code {op}')
            ic += 4

        return [state[i] for i in range(len(state))]

    assert run([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99]
    assert run([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]
    assert run([2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801]
    assert run([1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99]

    with open('input.txt') as f:
        _input: List = f.read().split(",")
    program = _input[:]

    _input[1] = 12
    _input[2] = 2

    print(run(_input))

    # solve part 2

    def calc(noun, verb):
        _input = program[:]
        _input[1] = noun
        _input[2] = verb
        return run(_input)[0]

    for noun in tqdm(range(100)):
        for verb in tqdm(range(100)):
            if calc(noun, verb) == 19690720:
                print(f'{noun=} * 100 + {verb=} = {noun * 100 + verb}')
                return


if __name__ == '__main__':
    solve()
