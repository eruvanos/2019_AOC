# 10 ORE => 10 A
# 1 ORE => 1 B
# 7 A, 1 B => 1 C
# 7 A, 1 C => 1 D
# 7 A, 1 D => 1 E
# 7 A, 1 E => 1 FUEL


# ORE  A   B   C   D   E
#      7               1
#     14           1
#     21       1
#     28   1



# 9 ORE => 2 A
# 8 ORE => 3 B
# 7 ORE => 5 C
# 3 A, 4 B => 1 AB
# 5 B, 7 C => 1 BC
# 4 C, 1 A => 1 CA
# 2 AB, 3 BC, 4 CA => 1 FUEL


# ORE   A   B   C  AB   BC  CA
#                   2    3   4
#       4      16   2    3
#       4  15  37   2
#      10  23  37
#  45
#  64
#  56
# 165


from typing import Tuple

file = 'input_test_1.txt'
with open(file) as f:
    lines = f.readlines()


def react(*ins) -> Tuple[int, str]:
    return 0, 'X'