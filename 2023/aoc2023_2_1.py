from pathlib import Path
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


input_path = Path(r"C:\Users\Jesse Wyatt\Desktop\aoc\aoc2023_2_input.txt")
with input_path.open("r") as fp:
    print(sum(process_game_line(line) for line in fp.readlines()))
