import aoc
import re
from itertools import chain, pairwise, product
import math
import operator


seeds_pattern = re.compile(r"(?P<src>\d+)\s+(?P<len>\d+)")
title_pattern = re.compile(r"\s*(?P<src>\w+)-to-(?P<dst>\w+)\s+map:\s*")
map_pattern = re.compile(r"\s*(?P<dst>\d+)\s+(?P<src>\d+)\s+(?P<len>\d+)\s*")


def range_intersect(a, b):
    if c := range(max(a.start, b.start), min(a.stop, b.stop)):
        return c 


def offset_range(r, offset):
    return range(r.start + offset, r.stop + offset)


# could make this better with 3-way cmp
def bin_search(sorted_data, value, condition=operator.eq, comp_gt=operator.gt):
    n_min = 0
    n_max = len(sorted_data)
    n = (n_min + n_max) // 2
    while not condition(sorted_data[n], value):
        if n == n_max:
            break
        elif comp_gt(sorted_data[n], value):
            n_max = n
        else:
            n_min = n
        n = (n_min + n_max) // 2
    return (n, sorted_data[n])


class RangeMap:
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        self.offset = dst.start - src.start
        assert len(src) == len(dst)

    @staticmethod
    def from_starts(src_start, dst_start, length):
        src = range(src_start, src_start + length)
        dst = range(dst_start, dst_start + length)
        return RangeMap(src, dst)

    @staticmethod
    def from_offset(src, offset):
        return RangeMap(src, offset_range(src, offset))

    def map(self, value):
        if value in self.src:
            return value + self.offset

    def contains(self, x):
        return x in self.src

    def intersect(self, other):
        if intersection := range_intersect(self.dst, other.src):
            offset = self.offset + other.offset
            return RangeMap.from_offset(intersection, offset)


class RangeMapper:
    def __init__(self, name, mappings=None):
        self.name = name
        self.mappings = mappings if mappings else []
        self.sort_mappings()
        self.upper_limit = self.mappings[-1].src.stop if self.mappings else 0  

    def sort_mappings(self):
        self.mappings.sort(key=lambda m: m.src.start)

    def add_map(self, src_start, dst_start, length):
        self.mappings.append(RangeMap.from_starts(src_start, dst_start, length))
        # only need to sort by start as rannges will not overlap

    def map_gaps(self):
        self.sort_mappings()
        spaces = []
        for m1, m2 in pairwise(self.mappings):
            if m1.src.stop != m2.src.start:
                spaces.append(RangeMap.from_offset(range(m1.src.stop, m2.src.start), 0))

        lowest_start = self.mappings[0].src.start
        if lowest_start > 0:
            spaces.append(RangeMap.from_starts(0, 0, lowest_start))

        self.mappings.extend(spaces)
        self.sort_mappings()
        self.upper_limit = self.mappings[-1].src.stop


################## TBD
### Need to handle case of input codomain going above output domain, some kind of open range would be nice, but it doesn't exist
### I guess I could write my own open range class for that?
### could just tack on a range to extend that extra big when flattening

    def map(self, value):
        if value >= self.upper_limit:
            return value
        n, m = bin_search(self.mappings, value, condition=lambda m,v: m.contains(v), comp_gt=lambda m,v: m.src.start > v)
        return m.map(value)


    def flatten(self, other):
        # this only does product of source to source
        mappings = []
        for m1, m2 in product(self.mappings, other.mappings):
            if m3 := m1.intersect(m2):
                mappings.append(m3)
        return RangeMapper(f"{self.name}+{other.name}", mappings)



with aoc.challenge_data(5) as data:
    lines = (line for line in data.readlines())

seed_tuples = [(int(m['src']), int(m['len'])) for m in seeds_pattern.finditer(next(lines).strip())]
seed_ranges = [range(start, start+length) for start, length in seed_tuples]


print(seed_tuples)
print(seed_ranges)
range_mappers = []
curr_mapper = -1

for line in lines:
    if m := title_pattern.match(line.strip()):
        range_mappers.append(RangeMapper(f"{m['src']}-to-{m['dst']}"))
        curr_mapper += 1

    elif m := map_pattern.match(line.strip()):
        range_mappers[curr_mapper].add_map(int(m['src']), int(m['dst']), int(m['len']))

for mapper in range_mappers:
    mapper.map_gaps()


ultra_mapper = None
for m in range_mappers:
    print(f"basic_mapper: {m.name}, len: {len(m.mappings)}")
    if ultra_mapper is None:
        ultra_mapper = m 
    else:
        ultra_mapper = ultra_mapper.flatten(m)

print(f"ultra_mapper: {ultra_mapper.name}, len: {len(ultra_mapper.mappings)}")
for m in ultra_mapper.mappings:
    print(m.src.start, m.src.stop)

min_loc = math.inf
count = 0
for seed in chain.from_iterable(seed_ranges):
    val = seed
    for mapper in range_mappers:
        next_val = mapper.map(val)
        # print(f"{mapper.name: <24}: {val} -> {next_val}")
        val = next_val
        
    # print(f"{'SEED-TO-LOCATION': <24}: {seed} -> {val}\n")
    min_loc = min(min_loc, val)
    count += 1
    if count % 10000 == 0:
        print(count)
        

# print(f"minimum loc: {min_loc}")