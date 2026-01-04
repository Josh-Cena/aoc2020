import itertools
import numpy as np
from typing import Union
from collections import Counter


def find_invalid(nums: list[int], preamble_len: int) -> Union[int, None]:
    sums = Counter[int]()
    for pair in itertools.combinations(nums[:preamble_len], 2):
        sums[sum(pair)] += 1
    for i in range(preamble_len, len(nums)):
        if nums[i] not in sums:
            return nums[i]
        for j in range(i - preamble_len + 1, i):
            pair_sum = nums[i - preamble_len] + nums[j]
            sums[pair_sum] -= 1
            pair_sum = nums[i] + nums[j]
            sums[pair_sum] += 1
    return None


def solve1(data: list[str]):
    nums = list(map(int, data))
    print(find_invalid(nums, 25))


def solve2(data: list[str]):
    nums = list(map(int, data))
    invalid = find_invalid(nums, 25)
    if invalid is None:
        raise ValueError("No invalid number found")
    running_sum = np.cumsum(nums)
    # A contiguous range sum from i to j is running_sum[j] - running_sum[i-1]
    # So we just search for running_sum[i-1] for each running_sum[j] - invalid
    # This set should contain two sums: one corresponding to i-1..j, the other
    # corresponding to the invalid number itself
    sum_i_p_1 = min(set(running_sum - invalid).intersection(set(running_sum)))
    i = np.where(running_sum == sum_i_p_1)[0][0] + 1
    j = np.where(running_sum == sum_i_p_1 + invalid)[0][0]
    num_range = nums[i : j + 1]
    print(min(num_range) + max(num_range))
