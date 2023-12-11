import operator
from collections import defaultdict, deque
import math


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

def factory(value):
    return lambda: value

def valid_direction_to(neighbour, direction):
    reverse_direction = tuple(-x for x in direction)
    return reverse_direction in ADJACENCY[neighbour]

def offset(point, offset):
    return tuple(map(operator.add, point, offset))

def valid_neighbours(grid, point):
    symbol = grid[point]
    neighbours = [(direction, offset(point, direction)) for direction in ADJACENCY[symbol]]
    return [neighbour for direction, neighbour in neighbours if valid_direction_to(grid.get(neighbour, "."), direction)]

def dijkstra(adj_list, start):
    distances = defaultdict(lambda: math.inf)
    distances[start] = 0
    visited = set()
    fifo = deque()
    fifo.append(start)
    while fifo:
        curr = fifo.popleft()
        visited.add(curr)
        neighbours = [n for n in adj_list[curr] if n not in visited]
        for n in neighbours:
            distances[n] = min(distances[curr] + 1, distances[n]) 
        fifo.extend(neighbours)
    return distances


def solution(data, debug=False):
    lines = [line.strip() for line in data.readlines()]

    grid = dict()

    starting_point = None
    for y, line in enumerate(lines):
        for x, char in enumerate(ch for ch in line):
            grid[(x,y)] = char
            if char == "S":
                starting_point = (x,y)

    adj_list = {point: valid_neighbours(grid, point) for point in grid.keys()}
    
    return max(
        dijkstra(adj_list, starting_point).values()
    )

if __name__ == "__main__":
    import aoc
    aoc.Challenge(10, "test").solve(soln)