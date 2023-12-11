import aoc
import re
from collections import defaultdict

game_line_pattern = re.compile(r"Card\s+(\d)+:\s+(?P<winning>[\d\s]*)\s+\|\s+(?P<ours>[\d\s]*)")

def score_game(line):
    if results := game_line_pattern.match(line):
        winning = set(int(n) for n in results["winning"].split() if n)
        ours = set(int(n) for n in results["ours"].split() if n)
        matches = winning & ours
        return len(matches)
    print(f"unmatched line: '{line}'")
    return 0


with aoc.challenge_data(4) as data:
    game_lines = [line.strip() for line in data.readlines()]

duplicates = list(1 for _ in range(len(game_lines)))

for n, game_line in enumerate(game_lines):
    card_score = score_game(game_line)
    for dupe in range(n+1, n+1+card_score):
        duplicates[dupe] += duplicates[n]

print(sum(duplicates))