from pathlib import Path
import string

RAW_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
DIGIT_MAP = {RAW_WORDS[n]: digit for (n, digit) in enumerate(string.digits)} | {d:d for d in string.digits}  # mapping to itself just to simplfy later logic

def process_line(line):
    found_digits = set()
    for raw, normalised in DIGIT_MAP.items():
        if (pos := line.find(raw)) >= 0:
            found_digits.add((pos, normalised))
        if (pos := line.rfind(raw)) >= 0:
            found_digits.add((pos, normalised))
    sorted_digits = sorted(found_digits)
    print(line, sorted_digits)
    return int(sorted_digits[0][1] + sorted_digits[-1][1])


input_path = Path(r"C:\Users\Jesse Wyatt\Desktop\aoc\aoc2023_1_input.txt")
with input_path.open("r") as input_file:
    print(sum(process_line(line.strip()) for line in input_file.readlines()))