import re
from collections import defaultdict
from itertools import product


num_pattern = re.compile(r"[0-9]+")
sym_pattern = re.compile(r"[^\.0-9]")


class Bbox:
    """inclusive exclusive bounding box for collision detection"""
    def __init__(self, top_left, bottom_right):
        self.x1, self.y1 = top_left
        self.x2, self.y2 = bottom_right
        assert(self.x1 <= self.x2 and self.y1 <= self.y2)

    def x_range(self):
        return range(self.x1, self.x2)
    
    def y_range(self):
        return range(self.y1, self.y2)

    def contains(self, point):
        px, py = point
        return px in self.x_range() and py in self.y_range()



class PartNumber:
    def __init__(self, value, start_x, start_y, length):
        self.value = value
        self.bbox = Bbox((start_x, start_y), (start_x + length, start_y + 1))

    def __members(self):
        return (self.value, self.bbox.x1, self.bbox.y1)

    def __hash__(self):
        return hash(self.__members())

    def __eq__(self, other):
        return self.__members() == other.__members()



class Engine:
    def __init__(self):
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
                    self.numbers_hit.add(part_num)

    def part_sum(self):
        return sum(num.value for num in self.numbers_hit)



def neighbourhood(point, n=1):
    def centered_range(c):
        return range(c-n, c+n+1)

    px, py = point
    return product(centered_range(px), centered_range(py))



def solution(data, debug=False):
    lines = [line.strip() for line in data.readlines()]
    
    engine = Engine()
    part_symbols = []
    
    for row, line in enumerate(lines):
        for num in num_pattern.finditer(line):
            engine.add_part_number(num.group(), row, num.start())
        for sym in sym_pattern.finditer(line):
            part_symbols.append((sym.start(), row))
    
    for symbol in part_symbols:
        for neighbour in neighbourhood(symbol):
            engine.collide(neighbour)

    return engine.part_sum()