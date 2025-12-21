import numpy as np


def solve1(data: list[str]):
    adapters = sorted(map(int, data))
    adapters = [0] + adapters + [adapters[-1] + 3]
    diffs = np.diff(adapters)
    ones = np.sum(diffs == 1)
    threes = np.sum(diffs == 3)
    print(ones * threes)


def solve2(data: list[str]):
    adapters = sorted(map(int, data))
    adapters = [0] + adapters + [adapters[-1] + 3]
    ways = {adapters[0]: 1}
    for adapter in adapters[1:]:
        # For each adapter, the number of ways to reach it is equal to how many
        # ways to reach each adapter that can connect to it
        ways[adapter] = (
            ways.get(adapter - 1, 0)
            + ways.get(adapter - 2, 0)
            + ways.get(adapter - 3, 0)
        )
    print(ways[adapters[-1]])
