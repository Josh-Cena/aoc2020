from collections import defaultdict
import re
import itertools


dir_to_diff = {
    "ne": (1, 1),
    "nw": (-1, 1),
    "se": (1, -1),
    "sw": (-1, -1),
    "e": (2, 0),
    "w": (-2, 0),
}


def neighbors_hex(point: tuple[int, int], include_self: bool):
    x, y = point
    if include_self:
        yield (x, y)
    for dx, dy in dir_to_diff.values():
        yield (x + dx, y + dy)


def init_grid(data: list[str]):
    tiles_flipped: defaultdict[tuple[int, int], int] = defaultdict(int)
    for line in data:
        cur = (0, 0)
        for dir in re.findall(r"ne|nw|se|sw|e|w", line):
            diff = dir_to_diff[dir]
            cur = (cur[0] + diff[0], cur[1] + diff[1])
        tiles_flipped[cur] += 1
    return set(p[0] for p in tiles_flipped.items() if p[1] % 2 == 1)


def solve1(data: list[str]):
    print(len(init_grid(data)))


def solve2(data: list[str]):
    black = init_grid(data)
    for _ in range(100):
        new_black = set()
        for p in itertools.chain.from_iterable(
            neighbors_hex(p, include_self=True) for p in black
        ):
            black_neighbors = sum(
                np in black for np in neighbors_hex(p, include_self=False)
            )
            if p in black and black_neighbors == 1 or black_neighbors == 2:
                new_black.add(p)
        black = new_black
    print(len(black))
