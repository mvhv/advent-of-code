import re
import functools
import operator

GAME_LINE_DELIMITERS = r":;"
GAME_LINE_SPLIT_PATTERN = "|".join([rf"\s*{d}\s*" for d in GAME_LINE_DELIMITERS])

def process_game_line(game_line):
    [_, *hands] = re.split(r"\s*:\s*|\s*;\s*", game_line)
    
    minimum_colour_cubes = {c: 0 for c in ("red", "green", "blue")}
    for hand in hands:
        hand_cubes = hand.split(",")
        for cube in hand_cubes:
            [num, colour] = cube.strip().split()
            minimum_colour_cubes[colour] = max(int(num), minimum_colour_cubes[colour])

    return functools.reduce(operator.mul, minimum_colour_cubes.values(), 1)


def soln(data):
    return sum(process_game_line(line) for line in data.readlines())
