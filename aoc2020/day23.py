# from tqdm import tqdm


class Cup:
    label: int
    next: "Cup"

    def __init__(self, label: int, next: "Cup"):
        self.label = label
        self.next = next


def play(nums: list[int], rounds: int):
    n = len(nums)
    tail = Cup(nums[-1], None)
    num_to_cup = {nums[-1]: tail}
    head = tail
    for i in range(n - 2, -1, -1):
        head = Cup(nums[i], head)
        num_to_cup[nums[i]] = head
    tail.next = head
    cur_cup = head
    for _ in range(rounds):
        cur_num = cur_cup.label
        dest_num = (cur_num - 1 - 1) % n + 1
        picked_cups = [cur_cup.next, cur_cup.next.next, cur_cup.next.next.next]
        picked_nums = [c.label for c in picked_cups]
        while dest_num in picked_nums:
            dest_num = (dest_num - 1 - 1) % n + 1
        dest_cup = num_to_cup[dest_num]
        cur_cup.next = picked_cups[-1].next
        dest_next = dest_cup.next
        dest_cup.next = picked_cups[0]
        picked_cups[-1].next = dest_next
        cur_cup = cur_cup.next
    return num_to_cup


def solve1(data: list[str]):
    nums = list(map(int, data[0]))
    num_to_cup = play(nums, 100)
    cur_cup = num_to_cup[1].next
    while cur_cup.label != 1:
        print(cur_cup.label, end="")
        cur_cup = cur_cup.next
    print()


def solve2(data: list[str]):
    nums = list(map(int, data[0])) + list(range(10, 1_000_000 + 1))
    num_to_cup = play(nums, 10_000_000)
    cur_cup = num_to_cup[1].next
    print(cur_cup.label * cur_cup.next.label)
