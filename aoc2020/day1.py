def solve1(data: list[str]):
    seen: set[int] = set()
    for line in data:
        num = int(line)
        if 2020 - num in seen:
            print((2020 - num) * num)
            return
        seen.add(num)


def solve2(data: list[str]):
    seen: set[int] = set()
    for line in data:
        num = int(line)
        for e in seen:
            if 2020 - num - e in seen:
                print((2020 - num - e) * num * e)
                return
        seen.add(num)
