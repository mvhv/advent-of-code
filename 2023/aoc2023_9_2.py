import aoc
import itertools

def diff(series):
    return [b - a for a, b in itertools.pairwise(series)]


def predict_next(series):
    if not any(series):
        return 0
    return series[-1] + predict_next(diff(series))


def predict_prev(series):
    if not any(series):
        return 0
    return series[0] - predict_prev(diff(series))


def soln(data):
    params = [list(map(int, line.strip().split())) for line in data.readlines()]
    return sum(predict_prev(param) for param in params)


if __name__ == "__main__":
    aoc.Challenge(9).solve(soln)