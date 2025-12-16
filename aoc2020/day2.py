def solve1(data: list[str]):
    total = 0
    for line in data:
        count, char, password = line.split(" ")
        char = char[0]
        count = list(map(int, count.split("-")))
        if count[0] <= password.count(char) <= count[1]:
            total += 1
    print(total)


def solve2(data: list[str]):
    total = 0
    for line in data:
        ind_range, char, password = line.split(" ")
        char = char[0]
        ind_range = list(map(int, ind_range.split("-")))
        if (password[ind_range[0] - 1] == char) != (password[ind_range[1] - 1] == char):
            total += 1
    print(total)
