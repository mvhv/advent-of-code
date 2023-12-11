import string
import re
import operator

RAW_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
DIGIT_MAP = {RAW_WORDS[n]: digit for (n, digit) in enumerate(string.digits)} | {d: d for d in string.digits}  # mapping to itself just to simplfy later logic
digit_matcher = re.compile(f"(?=({"|".join(DIGIT_MAP.keys())}))")
ends = operator.itemgetter(0, -1)

def parse_digits(line):
    return [DIGIT_MAP[d] for d in digit_matcher.findall(line)]

def process_line(line):
    return int(''.join(ends(parse_digits(line))))

def solution(data, debug=False):
    return sum(process_line(line) for line in data.readlines())