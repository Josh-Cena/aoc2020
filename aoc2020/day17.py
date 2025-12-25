import itertools
from typing import Callable, Generator, Any


def neighbors3d(point: tuple[int, int, int], include_self: bool):
    x, y, z = point
    for dx, dy, dz in itertools.product(range(-1, 2), repeat=3):
        if dx == 0 and dy == 0 and dz == 0 and not include_self:
            continue
        yield (x + dx, y + dy, z + dz)


def neighbors4d(point: tuple[int, int, int, int], include_self: bool):
    x, y, z, w = point
    for dx, dy, dz, dw in itertools.product(range(-1, 2), repeat=4):
        if dx == 0 and dy == 0 and dz == 0 and dw == 0 and not include_self:
            continue
        yield (x + dx, y + dy, z + dz, w + dw)


def solve(
    points: set[tuple[int, int, int]],
    n: int,
    neighbors: Callable[[tuple[int, ...]], Generator[tuple[int, ...], Any, None]],
):
    alive = set(points)
    for _ in range(n):
        new_alive = set()
        for p in itertools.chain.from_iterable(
            neighbors(p, include_self=True) for p in alive
        ):
            alive_neighbors = sum(
                np in alive for np in neighbors(p, include_self=False)
            )
            if p in alive and alive_neighbors == 2 or alive_neighbors == 3:
                new_alive.add(p)
        alive = new_alive
    print(len(alive))


def solve1(data: list[str]):
    points = set()
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == "#":
                points.add((i, j, 0))
    solve(points, 6, neighbors3d)


def solve2(data: list[str]):
    points = set()
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == "#":
                points.add((i, j, 0, 0))
    solve(points, 6, neighbors4d)
