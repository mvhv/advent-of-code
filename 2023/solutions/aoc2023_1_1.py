import string

def parse_line(line):
    digits = [ch for ch in line if ch in string.digits]
    return int(digits[0] + digits[-1])

def solution(data, debug=False):
    return sum(parse_line(line) for line in data.readlines())