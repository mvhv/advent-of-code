import operator
from collections import defaultdict, deque
import math
from itertools import  repeat

DEBUG = True

NORTH = ( 0, -1)
SOUTH = ( 0,  1)
EAST  = ( 1,  0)
WEST  = (-1,  0)

ADJACENCY = {
    "|": [NORTH, SOUTH],
    "-": [EAST, WEST],
    "L": [NORTH, EAST],
    "J": [NORTH, WEST],
    "7": [SOUTH, WEST],
    "F": [SOUTH, EAST],
    ".": [],
    "S": [NORTH, SOUTH, EAST, WEST]
}

DISPLAY = {
    "|": "║",
    "-": "═",
    "L": "╚",
    "J": "╝",
    "7": "╗",
    "F": "╔",
    ".": "░",
    "S": "S"
}


def valid_direction_to(neighbour, direction):
    reverse_direction = tuple(-x for x in direction)
    return reverse_direction in ADJACENCY[neighbour]



def offset(point, offset):
    return tuple(map(operator.add, point, offset))



def valid_neighbours(grid, point):
    symbol = grid[point]
    neighbours = [(direction, offset(point, direction)) for direction in ADJACENCY[symbol]]
    return [neighbour for direction, neighbour in neighbours if valid_direction_to(grid.get(neighbour, "."), direction)]



def find_loop(adj_list, start):
    lifo = [start]
    path = []
    prev = None
    while lifo:
        curr = lifo.pop()
        if neighbours := [n for n in adj_list[curr] if n != prev]:
            path.append(curr)
            if start in neighbours:
                return path
            lifo.extend(neighbours)
        else:
            path.pop()
        prev = curr



def find_enclosed(height, width, loop, adj_list):
    enclosed = []
    for y in range(height):
        intersections = 0
        # windings_line = []
        for x in range(width):
            node = (x, y)
            if node in loop:
                if offset(node, SOUTH) in adj_list[node]:
                    intersections += 1
            else:
                if intersections % 2 :
                    enclosed.append((x,y))
            # windings_line.append(f"{intersections: >3}")
        # windings.append("".join(windings_line))

    return enclosed



def format_grid(grid, height, width, display_fn=lambda x,y,ch: ch):
    lines = []
    for row in range(height):
        line = []
        for col in range(width):
            line.append(display_fn(col, row, grid[(col, row)]))
        lines.append("".join(line))
    return format_box("\n".join(lines), width)



def format_box(text_block, width):
    lines = ["┍" + "".join(repeat("━", width)) + "┑"]
    lines.extend(["│" + line + "│"  for line in text_block.split("\n")])
    lines.append("┕" + "".join(repeat("━", width)) + "┙")
    return "\n".join(lines)



def side_by_side(block_a, block_b, divider=" | "):
    lines = []
    for a, b in zip(block_a.split("\n"), block_b.split("\n")):
        lines.append(f"{a}{divider}{b}")
    return "\n".join(lines)



def soln(data):
    lines = [line.strip() for line in data.readlines()]
    height = len(lines)
    width = len(lines[0])

    grid = dict()
    starting_point = None
    for y, line in enumerate(lines):
        for x, char in enumerate(ch for ch in line):
            grid[(x,y)] = char
            if char == "S":
                starting_point = (x,y)
    
    adj_list = {point: valid_neighbours(grid, point) for point in grid.keys()}
    loop = find_loop(adj_list, starting_point)
    windings = []
    enclosed = find_enclosed(height, width, loop, adj_list, windings)
    if DEBUG:
        print(
            side_by_side(
                format_grid(grid, height, width, lambda x, y, ch: DISPLAY[ch]),
                format_grid(grid, height, width, lambda x, y, ch: "█" if (x,y) in enclosed else DISPLAY[ch]),
            divider=" "
            )
        )

    return len(enclosed)


if __name__ == "__main__":
    import aoc
    aoc.Challenge(10, "test4").solve(soln)