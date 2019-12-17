import math
from collections import namedtuple, defaultdict
from email.policy import default
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


def solve(file):
    with open(file) as f:
        lines = f.readlines()

    base_products = set()

    # Build tree
    reactions: Dict[str, Reaction] = {}
    for line in lines:
        ingredients, result = line.split('=>')

        mats = []
        for ingredient in ingredients.split(','):
            mats.append(parse_mat(ingredient))

        result = parse_mat(result)
        reactions[result.kind] = Reaction(mats, result)

        if len(mats) == 1 and mats[0].kind == 'ORE':
            base_products.add(result.kind)

    # resolve
    tasks = Queue()
    tasks.put(Material(1, 'FUEL'))
    ore = 0

    left_over: Dict[str, int] = defaultdict(int)
    req_base = defaultdict(int)

    while not tasks.empty():
        # get reaction to rollback

        req_amount, req_kind = tasks.get()
        reaction = reactions[req_kind]
        times_to_execute = math.ceil(req_amount / reaction.out.amount)
        left_over[req_kind] += times_to_execute * reaction.out.amount - req_amount

        print('req:', req_amount, ' * ', req_kind)

        # Calculate required mats
        mats = defaultdict(int)
        for mat in reaction.ins:
            # TODO: check left_over
            req_source_amount = times_to_execute * mat.amount
            old_leave_over = left_over[mat.kind]

            req_amount = max(req_source_amount - left_over[mat.kind], 0)
            left_over[mat.kind] = max(left_over[mat.kind] - times_to_execute * mat.amount, 0)

            # print(f'require {req_amount} {mat.kind} of {req_source_amount} leaves {left_over[mat.kind]}/{old_leave_over} rest')

            mats[mat.kind] += req_amount

        # start new tasks
        for source_kind, source_amount in mats.items():
            if source_kind == 'ORE':
                ore += source_amount
                print('req ore!')
            elif source_kind in base_products:
                req_base[source_kind] += source_amount
            else:
                tasks.put(Material(source_amount, source_kind))

    print('base_products', base_products)
    # print(req_base)

    # process base products
    for kind, amount in req_base.items():
        reaction = reactions[kind]
        times = math.ceil(amount / reaction.out.amount)

        for mat in reaction.ins:
            ore += mat.amount * times

    print(ore)
    return ore


if __name__ == '__main__':
    # file = 'input.txt'
    file = 'input_test_1.txt'
    assert solve(file) == 31

    file = 'input_test_2.txt'
    assert solve(file) == 165

    assert solve('input_test_3.txt') == 13312
    assert solve('input_test_4.txt') == 2210736
