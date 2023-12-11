import aoc
import re
import itertools
import math

id_pattern = re.compile(r"[A-Z0-9]{3}")

INSTRUCTION_MAP = {"L": 0, "R": 1}

def parse_instruction_line(line):
    return [INSTRUCTION_MAP[i] for i in line.strip()]


def parse_map_line(line):
    [n, l, r] = id_pattern.findall(line)
    return n, (l, r)


def ends_with(node, ch):
    return ch == node[-1]


if __name__ == "__main__":
    with aoc.Challenge(8).data() as data:
        lines = data.readlines()

    instructions = parse_instruction_line(lines[0])
    graph = dict(map(parse_map_line, lines[2:]))

    nodes = [node for node in graph.keys() if ends_with(node, "A")]

    distances = []
    for node in nodes:
        inst = itertools.cycle(instructions)
        n = 0
        while not ends_with(node, "Z"):
            node = graph[node][next(inst)]
            n += 1
        distances.append(n)
    
    print(distances)
    print(math.lcm(*distances))
