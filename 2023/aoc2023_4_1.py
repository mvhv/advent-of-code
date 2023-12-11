import aoc
import re

game_line_pattern = re.compile(r"Card\s+\d+:\s+(?P<winning>[\d\s]*)\s+\|\s+(?P<ours>[\d\s]*)")

def score_game(line):
    if results := game_line_pattern.match(line):
        winning = set(int(n) for n in results["winning"].split() if n)
        ours = set(int(n) for n in results["ours"].split() if n)
        matches = winning & ours
        if matches:
            return pow(2, len(matches)-1)
    return 0

with aoc.challenge_data(4) as data:
    print(sum(score_game(line.strip()) for line in data.readlines()))