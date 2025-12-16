import numpy as np


def test_slope(slope: tuple[int, int], grid: np.ndarray) -> int:
    cur = (0, 0)
    total = 0
    while cur[0] < len(grid):
        if grid[cur]:
            total += 1
        cur = (cur[0] + slope[0], (cur[1] + slope[1]) % len(grid[0]))
    return total


def solve1(data: list[str]):
    grid = np.array([[c == "#" for c in line] for line in data])
    total = test_slope((1, 3), grid)
    print(total)


def solve2(data: list[str]):
    grid = np.array([[c == "#" for c in line] for line in data])
    prod = 1
    for slope in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]:
        prod *= test_slope(slope, grid)
    print(prod)
