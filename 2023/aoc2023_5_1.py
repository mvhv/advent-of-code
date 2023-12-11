import aoc
import re

seeds_pattern = re.compile(r"\d+")
title_pattern = re.compile(r"\s*(?P<src>\w+)-to-(?P<dst>\w+)\s+map:\s*")
map_pattern = re.compile(r"\s*(?P<dst>\d+)\s+(?P<src>\d+)\s+(?P<len>\d+)\s*")


class RangeMapper:
    class RangeMap:
        def __init__(self, src_start, dst_start, length):
            self.src_start = src_start
            self.src_range = range(src_start, src_start+length)
            self.offset = dst_start - src_start

        def map(self, value):
            if value in self.src_range:
                return value + self.offset


    def __init__(self, name):
        self.mappings = []
        self.name = name
    
    def add_map(self, src_start, dst_start, length):
        self.mappings.append(RangeMapper.RangeMap(src_start, dst_start, length))

    def map(self, value):
        for mapping in self.mappings:
            if res := mapping.map(value):
                return res
        return value



with aoc.challenge_data(5) as data:
    lines = (line for line in data.readlines())

seeds = [int(m.group()) for m in seeds_pattern.finditer(next(lines).strip())]

range_mappers = []
curr_mapper = -1

for line in lines:
    if m := title_pattern.match(line.strip()):
        range_mappers.append(RangeMapper(f"{m['src']}-to-{m['dst']}"))
        curr_mapper += 1

    elif m := map_pattern.match(line.strip()):
        range_mappers[curr_mapper].add_map(int(m['src']), int(m['dst']), int(m['len']))


loc_numbers = []
for seed in seeds:
    val = seed
    for mapper in range_mappers:
        val = mapper.map(val)
    print(f"seed: {seed} -> location: {val}")
    loc_numbers.append(val)

print(f"minimum loc: {min(loc_numbers)}")