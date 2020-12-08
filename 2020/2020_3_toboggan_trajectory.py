def parse(data):
    slope = []
    for line in data.splitlines():
        row = [1 if x == "#" else 0 for x in line.strip()]
        slope.append(row)

    height = len(slope)
    width = len(slope[0])

    slopes = [
        {'x':1, 'y':1},
        {'x':3, 'y':1},
        {'x':5, 'y':1},
        {'x':7, 'y':1},
        {'x':1, 'y':2}
    ]

    tree_product = 1

    for s in slopes:
        x = 0
        y = 0
        trees = 0

        while True:
            x += s['x']
            y += s['y']
            if y >= height:
                break
            if slope[y][x % width]:
                trees += 1

        tree_product *= trees

    return tree_product

data = """....#...##......##..#..#.#...#.
..######...#......#....#..#.##.
..#.#...##......#.#..#..#....#.
..#.....#..#.#........#.#..#..#
#......##..###...#.#..#.....#..
#.......##...###...#....#......
.....##...#......##.#.#..#.##..
.........#......#.....#......#.
..#.#..#....#....#......##.#.##
.#...#..#.............#.#..#.#.
....#..#.#.##.#....#..#..#....#
...#..#.....#.......#...#..#..#
.....#.....#.......#..#...#....
.##.......#...#..#........#...#
...#.......#.#.#...#.#.#......#
#....#..#.....#......##....#..#
###.#......#.#.#.#..#....#....#
......##......#.#...#...#..#...
.....#......#.#.#......#.#.....
...##...#..#........#..#.##....
..##.#.#..#...###..........#.#.
.#..#..#.....#.........#.###.#.
....##.....#...#...##..#.##...#
....#.##....#.....##......#....
........#.#.........#.#.......#
#....##.#....#..#...#..........
#..###......#....##..........##
....##.#.....#..#.##......#....
#..#......#......#.............
...##.....##.......#.......#...
#...#.#.....#..........#...###.
#.....#..#.#.###...#......###..
...##.#......#........#..#.....
......#.....###.#...##........#
.#......##......##....#....#...
..#.#..#.....##....#....#..#...
..#.#.....#.##.#.....#.....#...
....#.......#...#.........##...
.#....#..#.......##.......#....
..#..##.....#...##.##.#.#......
.##.#....#............#.......#
.......#...#..#.#.##.....##..##
..###....#..#.##........##.#...
....#.#..#.....#..#.#.....#....
..#..#.#..............#..#.....
.......#.#.#.........#......#..
...##..#.#...#......##.#.......
#....#.#.........#...#....#..##
.#..#.#...#.......#.#.#....#.##
.#..###.#..#.#.....#..#........
#.#..##.###.....##.........#..#
#...##...#..##..#..#..........#
.#...#..#......................
...##..###...........#.#...##..
..........#.#....#.#...........
..#....#....#..#....#.#.#......
.#..#.....###......#...#...#...
#.##..#..#.........#..#....#...
........#......#...#.........#.
..#.....#.#..##...#.#.#...##...
..#...........#.##..#.#..#.##..
..............##...#.#......#..
#.#..#....#...##.###........#..
.#...#..#........#........##..#
.....##..#...#.....#.#.........
.#...#...#....###...#.#.#..##..
....#.........#....###..##....#
.#....#...####...##....####.#..
..#..#.......#..#......#.#.#...
....#....#.......##..#.#.......
..#....#...........##.#.##.....
#..#..#...##.##....#.#.#.###.##
...#...#....#.#...##...#....###
......##........#.........#.#..
....#####..#..##.......#.#....#
....##..#...###....#..#.....#..
..#........#..#.#.....#....#...
..#....#......#..#...#......#..
...#.....##...#.#..##.....#..#.
...#..#.......####.##...#......
.....#..#..#.##..##....#..#.#..
..#..#..##.#.#.##..#..#...#....
...#..........#.........#....##
.##.....###...............#.##.
...##...........#.#.#......#..#
.#...#.#.##....#....#..#.......
.#...###.#....#..#..#..#......#
#..#........###...........#..#.
..#...#......#.#.#......####.#.
...#.#....##.#.....#.....##....
...###..#.#.#...#.....#.###..#.
.#.#..#...##......#..........#.
##.....#.......#.#..###...#.#..
##.###....#.....#.....###.#....
#...#..##....#.#...#...#......#
.....##.#........#.###.........
.#..#..#.#......##.#...#.#.....
#..#.#........##...........##.#
#...###..#..####..#.#..........
..#...#....#...##.#....#....##.
......#.#........#.....#..#....
#.........#...#.....#...#..##..
#....#.........#...#.##..###.#.
#...###...#.##.#.#.............
#.#....#....#......#....#.#...#
##...#.##......#..#.#....#.....
....#...#.##....#..............
.........##..........#..##..#..
......##....#.#......#.........
..#.#..............#......#..##
...........##.......#.#.#......
##...#........##.......#.#.....
....#...#...#....#.#......##...
...#..#.#.#.........#..#.#....#
.##.#...#.#.........#.....##.#.
#.#.....#.#.....#..............
..#.#..#....#..........#..##...
...#..#....................#..#
...........#...........#...#..#
............#...#............##
..#....##......##...........#..
..#..#..#....#....##......##.##
##..........#..##.##.#...#.....
............#..#........###.#..
###...##.#.#....#....#.#....#..
...#......##...#.......####....
.......#..#..#.#.....#.........
........##.......##.....#......
#.#...#.###....#..#...##.......
...#.#....#..#####.#..##.#.....
..#.#..##.......###...#.....#..
..#.......#..#...#...#..#.##...
......#..#.......#.....#....#..
.......#........#.#.......##..#
.#.#.....#.......#.......##..#.
..#.#....#.#.#####.....#...#...
#..#............###.......#..#.
........##.........#..#...###..
.#............##...#.....#.....
.#..##..#....#....#.......#....
....##..........##.............
.##..........#..#..#....#...#..
...#..#..#............####.....
.............#..#.##..#.#.##...
.....#........#....#.#.......#.
###.#..#.#...#....##...........
....#......#...#....##.......#.
.......#.#...#.#...#........##.
..........#........#..#.##.....
##..#.#.....##.#...............
.....#....#................#...
...##....#........##.#....#....
.....##...###....#.#..#.......#
.....#.#.........##....###.....
.#.....##......#..##..##...##.#
.#..............#.....#.#......
.##......#..#..#......##.......
.......#..................#....
...#.#...##......####.........#
#....#####.#.#..#..#..#...#...#
##.#...#.......#....#...#...###
...#........#.....#...#.##.....
..##....#.......#....#.......##
#......#..##...#..##.#.....#.#.
..###........#.#..#........#.#.
...#.###..........#.....#.#.#..
#.###.....#...#...#..##..###...
#....#.#.....#.#........#......
........#.......##.......#.....
...........#...#......##.......
............#...#....#..#.....#
#.#.#.#....#.....#.#..........#
#.##...#...#..#....##.#.......#
...#..#......#..#...##..##..#..
#....#......#.#.....##.#..#....
#....#..##.#......#.#.....#..##
.#..##....##....#.#...#...#....
#.#.###....#.#............#...#
.#.#....#..#..........#....#.#.
......#..#.#...............##..
..#......###.#..........#.###..
....#.##.#..#...##..#.#...#....
..............#...##.......#.##
.#...........#....#....#.##....
#..#....#.....#...#.....##...#.
.........#...#.##.......#...#.#
.....#......#.........#.#..#...
##..........#.#..##...#.#.#....
##..##.#..#..#.....#.##....#...
........##....#.#.#....#......#
.#.##...#.###....#.........#..#
..........#....###..#.........#
#.#..#.#...#.......#..##.......
..#....#...###..............##.
#..###.....####...#..#..#...#..
......#..#...###........###....
..#.....#...#.......#....###..#
.#.........#.#.#....#.#.......#
#.#.###.#.#...........#........
......#..#.........#........#..
...........##.#........#.#...#.
.....#.#......##.......#.....##
...##...#............#..#.....#
.....#..##....##...##.#..#.#...
...#...#........#.#......##....
........#..##..#..#......##.#..
.#.#.....#.....#...........#.##
.#...#.#............#......#...
.....#...#........#....#..#.#..
...##....#..#...#..............
#....##.#.#............#.......
#..#..#.....##..#........##.#.#
##..#.#....#....##.......###..#
.#.#.#.....###.....#.#......###
.....#..#...###...#....#.#...#.
.##.....................##....#
.#.....#.........#....#.....##.
#...#....#.#...###.......#.#..#
...#.................#.#....#.#
.##...#.#......................
.##.#........#...##............
.#....#.....#.........#.##..##.
#......#...##..#.........##.##.
......#......#...####..#.##....
.###....#..##......#.##......#.
..#...#....#..#.......#.#......
#....#...#.................#.#.
....#.#.#..#...#..#.......#.#.#
#.#...##.......#.....##.#......
#.........#.....##..##..#......
....#..##..#.....#..#..#.#..#..
......#.#..#.#.#....#.#.......#
.##......#..#....##...##..#....
..#..#......#...##..#.##.....#.
..#..#.......#.#....#.....#...#
....#.#.....###...#.......#.#..
..#....##.....##.#........##...
#...............##....#.....##.
.#.........#....#...##.###.##.#
.#.##..#.............#.#.#..#..
.#.....#.................##....
..####.........#.#......#.#..#.
#.......#..........#.#........#
.#.#...##.....#.#.......#....#.
..#.##.#.......###....#....#...
.#....##.............##.#.#.#..
#.#.....#.#.#.#..#......##..#..
.............#..........#.#.#..
...#.#.............#.#...##....
.......#..#.#.......#..#.#....#
.............#.........###..#..
.#.#..#....#.....#..#.....#...#
#.....#....##..##.#..#........#
..##..###.....##....#.#..#.....
..#...##....#...#.#..........#.
...##..##.#.....#....#.........
..#...#........##.#..#........#
#.............#.###......#.##..
.#...#........#...........#...#
..##.......#.#..##.##......#...
...#.#...##....##..#...........
.#......##........#....##....#.
.........#..#....#...#..##.##..
....#..#.#...#.......#.#.##....
...#.#......#.#..#..#.#....#..#
.......#........#.........###..
#.#..#.#.........##............
##..##..#.##..###...#.#...#....
.#....#.#..#...#....#.##.....#.
.#.#.#.#........##...#..#.#.##.
.#..#.#..#...........#..#......
..#.##.#...#....#.........#...#
.....##...#.#...#...#....#.....
..#..........#.#.#.......##.#..
#.#............#..#.....#..#...
..#...........##.#.##.#....#..#
#..####.....#............#.....
.##......#####.#..#.....#....#.
...##..#.#......#.#..#..#...##.
#....................#.##...#.#
...#............#.............#
....#.##..........#.....#......
....##..##....#.#..............
...........#....##.#.....#.....
....#.....#....#....#......#...
#...##........#...#........#.#.
........#.....##..#.##.#..#.#.#
....##......##....#.....##....#
...#.#........##.......#...##..
#......##..#.#.#....##......#..
..#.......#.......##..#.##.....
.#...#...#.#.............##....
......#.#.#.........##...#..#.#
.....#..####....#.##..........#
...#...#.#....#.....#..#.....##
.........#.......#......###....
........##..##..#.#.#...###...#
.#..##.#....#...##.....#.#.#...
........##...#...##..#.........
.........#.......#.##..#...####
#......#.....#..............#.#
##..##.#.##.....##...........#.
#.............#.........#......
...####.#.##..#.#.#.##.#......#
..#.....##....#...#............
#..............#......#...###..
..#..#.#...#.##.........##.....
..#...##..#........#..#.##..##.
......###...#..#....#..#.###...
...##.##.###.....##.#.......#..
#....#..###..#.......#.#.#..#..
..##.............##..##...###.#
.#.#..#.........#..........#...
.........#.#.....##...#..#...##
....#..#....#####..#...#..#....
...#.....#.....#...#.#..#.#....
.#..#.............#.......##.#.
...##.......#.#.....##......#..
...........##..#.##..###...#.#.
...........#...........#...#..#
..#....#.##.#..#..#...........#
..#.....##...#......#...#......
...###.###.....##..........#..#
"""

print(parse(data))