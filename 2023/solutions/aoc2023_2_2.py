import re
from functools import reduce
from operator import mul

delimiters = re.compile(r"\s*:\s*|\s*;\s*")

def process_line(line):
    [_, *hands] =  delimiters.split(line)
    
    cube_max = {c: 0 for c in ("red", "green", "blue")}
    for hand in hands:
        hand_cubes = hand.split(",")
        for cube in hand_cubes:
            [num, colour] = cube.strip().split()
            cube_max[colour] = max(int(num), cube_max[colour])

    return reduce(mul, cube_max.values(), 1)


def solution(data, debug=False):
    return sum(process_line(line) for line in data.readlines())
