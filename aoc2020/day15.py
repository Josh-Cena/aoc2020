def solve(nums: list[int], round: int):
    most_recent_turn = {x: i + 1 for i, x in enumerate(nums)}
    last_num = nums[-1]
    for i in range(len(nums) + 1, round + 1):
        num = i - 1 - most_recent_turn.get(last_num, i - 1)
        most_recent_turn[last_num] = i - 1
        last_num = num
    print(last_num)


def solve1(data: list[str]):
    solve(list(map(int, data[0].split(","))), 2020)


def solve2(data: list[str]):
    solve(list(map(int, data[0].split(","))), 30_000_000)
