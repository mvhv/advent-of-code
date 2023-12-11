import re

COLOUR_LIMITS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

def process_game_line(game_line):
    [game_header, *hands] = re.split(r"\s*:\s*|\s*;\s*", game_line)
    for hand in hands:
        cubes = hand.split(",")
        for cube in cubes:
            [num, colour] = cube.strip().split()
            if int(num) > COLOUR_LIMITS[colour]:
                return 0
    print(game_header)
    [_, game_id] = game_header.strip().split()
    return int(game_id)


def solution(data, debug=False):
    return sum(process_game_line(line) for line in data.readlines())
