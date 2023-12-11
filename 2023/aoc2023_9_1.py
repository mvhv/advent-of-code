import aoc
import itertools


def diff(series):
    return [b - a for a, b in itertools.pairwise(series)]


def predict_next(series):
    if not any(series):
        return 0
    return series[-1] + predict_next(diff(series))


with aoc.Challenge(9).data() as data:
    params = [list(map(int, line.strip().split())) for line in data.readlines()]


print(sum(predict_next(param) for param in params))
