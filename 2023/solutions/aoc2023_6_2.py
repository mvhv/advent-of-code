import aoc
import re

num_pattern = re.compile(r"\s(\d+)")

def solution(data, debug=False):
    times = [int(''.join([n.group(1) for n in num_pattern.finditer(next(data))]))]
    distances = [int(''.join([n.group(1) for n in num_pattern.finditer(next(data))]))]

    total_score = 1
    for time_limit, record in zip(times, distances):
        winning_holds = 0
        for hold_time in range(1, time_limit):
            speed = hold_time
            travel_time = time_limit - hold_time
            game_score = speed * travel_time
            if game_score > record:
                winning_holds += 1
        total_score *= winning_holds

    return total_score