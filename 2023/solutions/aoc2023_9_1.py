import itertools


def diff(series):
    return [b - a for a, b in itertools.pairwise(series)]


def predict_next(series):
    if not any(series):
        return 0
    return series[-1] + predict_next(diff(series))


def solution(data, debug=False):
    params = [list(map(int, line.strip().split())) for line in data.readlines()]
    return sum(predict_next(param) for param in params)
