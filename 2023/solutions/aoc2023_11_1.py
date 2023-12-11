from itertools import accumulate, combinations

def get_expansion_maps(galaxies):
    occupied_rows = {y for x, y in galaxies}
    occupied_cols = {x for x, y in galaxies}
    expanded_row_map = accumulate(
        range(max(occupied_rows) + 1),
        func=lambda acc, n: acc + (1 if n in occupied_rows else 2)
    )
    expanded_col_map = accumulate(
        range(max(occupied_cols) + 1),
        func=lambda acc, n: acc + (1 if n in occupied_cols else 2)
    )
    return list(expanded_row_map), list(expanded_col_map)


def solution(data, debug=False):
    lines = [line.strip() for line in data.readlines()]

    galaxies = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                galaxies.add((x,y))

    row_map, col_map = get_expansion_maps(galaxies)
    expanded_galaxies = ((col_map[x], row_map[y]) for x, y in galaxies)
    distances = [abs(x1 - x2) + abs(y1 - y2) for (x1, y1), (x2, y2) in combinations(expanded_galaxies, 2)]

    if debug:
        print(sorted(galaxies))
        print(sorted(row_map))

    return sum(distances)