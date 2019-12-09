from collections import defaultdict
from typing import List


def solve():
    with open('input.txt') as f:
        lines: List = f.readlines()

    sat_center_map = dict()
    center_sat_map = defaultdict(list)

    # convert input to map
    for line in lines:
        center, satalite = line.strip().split(')')
        sat_center_map[satalite] = center
        center_sat_map[center].append(satalite)

    # part 1
    # print('PART 1')
    # counter = 0
    # for obj in sat_center_map.keys():
    #     print(obj, '> ', end='')
    #     while obj := sat_center_map.get(obj):
    #         counter += 1
    #         print(obj, end=',')
    #     print()
    # print(counter)

    # part 2
    print('PART 2')
    def trace(obj):
        while obj := sat_center_map.get(obj):
            yield obj

    you = list(trace('YOU'))
    san = list(trace('SAN'))
    print(you)
    print(san)

    for x in reversed(you):
        if x in san:
            san.remove(x)
            you.remove(x)
            last = x
    else:
        san.append(last)
        you.append(last)

    print()
    print(you)
    print(san)

    print(len(san) + len(you) - 2)




    # build graph
    # orbit_map = defaultdict(list)
    # tasks = ['COM']
    # while tasks:
    #     cur = tasks.pop(0)
    #     for sat in center_sat_map[cur]:
    #         tasks.append(sat)
    #
    #         orbit_map[sat].append(cur)
    #         orbit_map[sat].extend(orbit_map[sat])
    #
    # for k, v in orbit_map.items():
    #     print(k, v)


if __name__ == '__main__':
    solve()
