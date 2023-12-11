import csv
import importlib
from pathlib import Path
from time import perf_counter_ns as timer


AOC_ROOT_DIR = Path(__file__).parent.absolute()
AOC_DATA_DIR = AOC_ROOT_DIR / "data"
AOC_DATASET_CSV = AOC_ROOT_DIR / "data" / "datasets.csv"


class Dataset:
    def __init__(self, ds):
        self.name = ds["dataset"]
        self.challenge = int(ds["challenge"])
        self.part = int(ds["part"])
        self.test_type = ds["test_type"]
        self.answer = int(ds.get("answer")) if ds["answer"] else 0

    def path(self):
        return AOC_DATA_DIR / f"{self.name}.txt"
    
    def load(self):
        return self.path().open("r")

    def matches(self, challenge, part, test_type):
        return (self.challenge, self.part, self.test_type) == (challenge, part, test_type)


class DataLoader:
    def __init__(self):
        with AOC_DATASET_CSV.open("r") as fp:
            self.datasets = [Dataset(ds) for ds in csv.DictReader(fp)]

    def iter_datasets(self, num, part, test_type=None):
        return (ds for ds in self.datasets if ds.matches(num, part, test_type))


class Challenge:
    def __init__(self, number, part):
        self.number = number
        self.part = part
        self.data_loader = DataLoader()

    @property
    def module_name(self):
        return f"solutions.aoc2023_{self.number}_{self.part}"

    def import_solution(self):
        return importlib.import_module(self.module_name).solution

    def run_test(self, dataset, debug=False):
        solution = self.import_solution()
        with dataset.load() as data:
            start = timer()
            res = solution(data, debug)
            stop = timer()
        ms = (stop - start) / 1e6
        res_string = f"{res}/{dataset.answer if dataset.answer else "?"}"
        print(f"AoC 2023 {self.number}-{self.part} [{dataset.name}]: {res_string} ({ms} ms) -- {'OK' if res == dataset.answer else 'CHECK'}")

    def datasets(self, test_type="test"):
        return self.data_loader.iter_datasets(self.number, self.part, test_type)

    def run_tests(self, test_type="test", debug=False):
        for ds in self.datasets(test_type):
            self.run_test(ds, debug)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("challenge", type=int)
    parser.add_argument("part", type=int)
    parser.add_argument("--test", action='store_true')
    parser.add_argument("--debug", action='store_true')
    args = parser.parse_args()
    test_type = "test" if args.test else "main"
    
    Challenge(args.challenge, args.part).run_tests(test_type, args.debug)