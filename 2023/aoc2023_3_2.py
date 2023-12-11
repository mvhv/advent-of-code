import re
from collections import defaultdict
from itertools import product


num_pattern = re.compile(r"[0-9]+")
sym_pattern = re.compile(r"\*")


class Bbox:
    """inclusive exclusive bounding box for collision detection"""
    def __init__(self, top_left, bottom_right):
        self.tl = top_left
        self.br = bottom_right
        self.x1, self.y1 = self.tl
        self.x2, self.y2 = self.br
        self.width = self.x2 - self.x1
        self.height = self.y2 - self.y1
        assert(self.x1 <= self.x2 and self.y1 <= self.y2)


    def contains(self, point):
        px, py = point
        return px in range(self.x1, self.x2) and py in range(self.y1, self.y2)


    def __repr__(self):
        return f"Bbox {{tl: {self.tl}, br: {self.br}}}"



class PartNumber:
    def __init__(self, value, start_x, start_y, length):
        self.value = value
        self.bbox = Bbox((start_x, start_y), (start_x + length, start_y + 1))


    def __members(self):
        return (self.value, self.bbox.tl, self.bbox.br)


    def __hash__(self):
        return hash(self.__members())


    def __eq__(self, other):
        return self.__members() == other.__members()


    def __repr__(self):
        return f"PartNumber {{value: {self.value}, bbox: {self.bbox}}}"



class Engine:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = defaultdict(list)
        self.numbers_hit = set()


    def add_part_number(self, number_string, row, col):
        length = len(number_string.strip())
        value = int(number_string)
        self.rows[row].append(PartNumber(value, col, row, length))


    def collide(self, point):
        _, py = point
        if py in self.rows:
            for part_num in self.rows[py]:
                if part_num.bbox.contains(point):
                    return part_num


    def part_sum(self):
        return sum(num.value for num in self.numbers_hit)


    def __repr__(self):
        return "\n".join(f"{n}: {row}" for n, row in self.rows.items())



def adj_range(n):
    return range(n-1, n+2)


def neighbours(x, y):
    return product(adj_range(x), adj_range(y))


def soln(data):
    lines = [line.strip() for line in data.readlines()]

    height = len(lines)
    width = len(lines[0])

    engine = Engine(height, width)
    
    for row, line in enumerate(lines):
        for num_res in num_pattern.finditer(line):
            engine.add_part_number(num_res.group(), row, num_res.start())
    
    part_symbols = []
    for row, line in enumerate(lines):
        for sym_res in sym_pattern.finditer(line):
            part_symbols.append((sym_res.start(), row))

    gears = []
    for x, y in part_symbols:
        adj_nums = set(part_num for point in neighbours(x, y) if (part_num := engine.collide(point)))
        if len(adj_nums) == 2:
            gears.append(adj_nums.pop().value * adj_nums.pop().value)
            assert(len(adj_nums) == 0)

    print(gears)
    return sum(gears)