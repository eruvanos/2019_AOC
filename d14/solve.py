import math
from collections import namedtuple, defaultdict
from math import ceil
from queue import Queue
from typing import Dict, NamedTuple, List

Material = namedtuple('Material', 'amount kind')


class Reaction(NamedTuple):
    ins: List[Material]
    out: Material


def parse_mat(raw: str) -> Material:
    ingredient = raw.strip()
    amount, kind = ingredient.split(' ')
    return Material(int(amount), kind)


def solve():
    # file = 'input.txt'
    file = 'input_test_1.txt'
    with open(file) as f:
        lines = f.readlines()

    # Build tree
    reactions: Dict[str, Reaction] = {}
    for line in lines:
        ingredients, result = line.split('=>')

        mats = []
        for ingredient in ingredients.split(','):
            mats.append(parse_mat(ingredient))

        result = parse_mat(result)
        reactions[result.kind] = Reaction(mats, result)

    # resolve
    tasks = Queue()
    tasks.put(Material(1, 'FUEL'))
    ore = 0

    while not tasks.empty():
        # get reaction to rollback

        amount, kind = tasks.get()
        reaction = reactions[kind]
        times = math.ceil(amount / reaction.out.amount)

        # Calculate required mats
        mats = defaultdict(int)
        for mat in reaction.ins:
            mats[mat.kind] += times * mat.amount

        # start new tasks
        for kind, amount in mats.items():
            if kind == 'ORE':
                ore += amount
            else:
                tasks.put(Material(amount, kind))

    print(ore)


if __name__ == '__main__':
    solve()
