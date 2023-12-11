import aoc
import re
import itertools

id_pattern = re.compile(r"[A-Z]{3}")

INSTRUCTION_MAP = {"L": 0, "R": 1}

def parse_instruction_line(line):
    return [INSTRUCTION_MAP[i] for i in line.strip()]

def parse_map_line(line):
    [n, l, r] = id_pattern.findall(line)
    return n, (l, r)

def solution(data, debug=False):
    lines = data.readlines()

    instructions = itertools.cycle(parse_instruction_line(lines[0]))
    graph = dict(map(parse_map_line, lines[2:]))

    node = "AAA"
    n = 0
    while node != "ZZZ":
        node = graph[node][next(instructions)]
        n += 1

    return n