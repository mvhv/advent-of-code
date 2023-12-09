from pathlib import Path
from contextlib import contextmanager


class Challenge:
    def __init__(self, number):
        self.number = number
    
    def data_path(self, suffix="input"):
        return Path.cwd() / "data" / f"aoc2023_{num}_{suffix}.txt"

    def ans_path(self, suffix="input"):
        return Path.cwd() / "data" / f"aoc2023"

    @contextmanager
    def data(self):
        with self.data_path().open("r") as fp:
            yield fp

    def validate(self, validate):
        with

@contextmanager
def challenge_data(num, suffix="input"):
    file_path = Path.cwd() / "data" / f"aoc2023_{num}_{suffix}.txt"
    with file_path.open("r") as input_file:
        yield input_file