import math
from collections import namedtuple, defaultdict
from itertools import permutations, chain
from typing import NamedTuple, List, Dict, Tuple, Iterable

Material = namedtuple('Material', 'amount kind')


class Reaction(NamedTuple):
    ins: List[Material]
    out: Material


def parse_mat(raw: str) -> Material:
    ingredient = raw.strip()
    amount, kind = ingredient.split(' ')
    return Material(int(amount), kind)


def solve(file, fuel):
    with open(file) as f:
        lines = f.readlines()

    # Read receipts
    reactions: Dict[str, Reaction] = {}
    for line in lines:
        ingredients, result = line.split('=>')

        mats = []
        for ingredient in ingredients.split(','):
            mats.append(parse_mat(ingredient))

        result = parse_mat(result)
        reactions[result.kind] = Reaction(mats, result)

    def revert(kind: str, amount: int, left_overs) -> Tuple[Tuple, Tuple]:
        left_overs = dict(left_overs)

        reaction = reactions[kind]
        times = math.ceil(amount / reaction.out.amount)

        left_overs.setdefault(kind, 0)
        left_overs[kind] += times * reaction.out.amount - amount

        # Calculate required mats
        mats = defaultdict(int)
        for mat in reaction.ins:
            # mats[mat.kind] += times * mat.amount

            mat_amount = times * mat.amount

            req_amount = max(mat_amount - left_overs.get(mat.kind, 0), 0)
            left_overs[mat.kind] = max(left_overs.get(mat.kind, 0) - times * mat.amount, 0)

            mats[mat.kind] += req_amount

        new_requirements = tuple()
        for kind, amount in mats.items():
            new_requirements += ((kind, amount),)

        return new_requirements, tuple(left_overs.items())

    def combine_reduce(a: Tuple[Tuple[str, int]], b: Iterable[Tuple[str, int]]):
        result = defaultdict(int)
        ore = 0
        for kind, amount in chain(a, b):
            if kind == 'ORE':
                ore += amount
            else:
                result[kind] += amount
        return ore, tuple(result.items())

    spacer = 0

    # resolve
    def backtrack(ore: int, requirements: Tuple[Tuple[str, int]], left_overs):
        nonlocal spacer
        print(f'{spacer * " "}backtrack {requirements}')

        for combination in permutations(requirements):
            for kind, amount in combination:
                print(f'{spacer * " "}solve {(kind, amount)}')
                new_req, new_left_overs = revert(kind, amount, left_overs)
                add_ore, new_req = combine_reduce(new_req, set(combination) - {(kind, amount)})
                print(f'{spacer * " "}=> {ore + add_ore} {new_req}')
                print(f'{spacer * " "}=> left: {new_left_overs}')

                if len(new_req) == 0:
                    print(f'{spacer * " "}return {ore + add_ore}')
                    yield ore + add_ore
                else:
                    spacer += 2
                    yield from backtrack(ore + add_ore, new_req, new_left_overs)
                    spacer -= 2

    for solution in backtrack(0, (('FUEL', fuel),), tuple()):
        print(solution)
        print(1_000_000_000_000)


if __name__ == '__main__':
    # solve('input_test_1.txt')
    # solve('input_test_2.txt')
    # solve('input_test_3.txt')
    # solve('input_test_4.txt')
    solve('input.txt', 4906796) # interval test
