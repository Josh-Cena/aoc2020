from typing import Union


def neighbors2d(
    r: int, c: int, grid: list[list[str]], allowed: Union[list[str], None]
) -> list[tuple[int, int]]:
    res: list[tuple[int, int]] = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            d = 1
            nr = r + dr * d
            nc = c + dc * d
            while 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                if not allowed or grid[nr][nc] in allowed:
                    if grid[nr][nc] != ".":
                        res.append((nr, nc))
                    break
                d += 1
                nr = r + dr * d
                nc = c + dc * d
    return res


def evolve(grid: list[list[str]], allowed: Union[list[str], None], empty_thresh: int):
    h = len(grid)
    w = len(grid[0])
    points = [(r, c) for r in range(h) for c in range(w) if grid[r][c] != "."]
    point_neighbors = {(r, c): neighbors2d(r, c, grid, allowed) for (r, c) in points}
    has_changed = True
    while has_changed:
        has_changed = False
        new_grid = [row.copy() for row in grid]
        for r, c in points:
            neighbors = [grid[nr][nc] for (nr, nc) in point_neighbors[(r, c)]]
            if "#" not in neighbors and grid[r][c] == "L":
                new_grid[r][c] = "#"
                has_changed = True
            elif neighbors.count("#") >= empty_thresh and grid[r][c] == "#":
                new_grid[r][c] = "L"
                has_changed = True
        grid = new_grid
    return grid


def solve1(data: list[str]):
    grid = [list(line) for line in data]
    grid = evolve(grid, None, 4)
    print(sum(row.count("#") for row in grid))


def solve2(data: list[str]):
    grid = [list(line) for line in data]
    grid = evolve(grid, ["L", "#"], 5)
    print(sum(row.count("#") for row in grid))
