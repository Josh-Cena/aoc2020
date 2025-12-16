def solve1(data: list[str]):
    groups = "\n".join(data).split("\n\n")
    total = sum(len(set(g.replace("\n", ""))) for g in groups)
    print(total)


def solve2(data: list[str]):
    groups = "\n".join(data).split("\n\n")
    total = sum(len(set.intersection(*map(set, g.split("\n")))) for g in groups)
    print(total)
