import aoc
import re
import itertools

id_pattern = re.compile(r"[A-Z0-9]{3}")

INSTRUCTION_MAP = {"L": 0, "R": 1}

def parse_instruction_line(line):
    return [INSTRUCTION_MAP[i] for i in line.strip()]

def parse_map_line(line):
    [n, l, r] = id_pattern.findall(line)
    return n, (l, r)

def ends_with_a(node):
    return "A" == node[-1]

def ends_with_z(node):
    return "Z" == node[-1]

def map_nodes(nodes, graph, instruction):
    res = {graph[node][instruction] for node in nodes}
    # print(f"{graph} [{instruction}] : {list(nodes)} -> {res}")
    return res

if __name__ == "__main__":
    with aoc.challenge_data(8) as data:
        lines = data.readlines()

    instructions = itertools.cycle(parse_instruction_line(lines[0]))
    graph = dict(map(parse_map_line, lines[2:]))

    nodes = [node for node in graph.keys() if ends_with_a(node)]
    n = 0
    while not all(map(ends_with_z, nodes)):
        instruction = next(instructions)
        
        nodes = map_nodes(nodes, graph, instruction)
        n += 1
        print(len(nodes))
        # print(n)

    print(n)