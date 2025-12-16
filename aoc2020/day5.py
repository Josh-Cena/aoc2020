def find_seat(boarding_pass: str):
    low = 0
    high = 128
    for i in range(7):
        mid = (low + high) // 2
        if boarding_pass[i] == "F":
            high = mid
        else:
            low = mid
    row = low
    low = 0
    high = 8
    for i in range(7, 10):
        mid = (low + high) // 2
        if boarding_pass[i] == "L":
            high = mid
        else:
            low = mid
    col = low
    return row * 8 + col


def solve1(data: list[str]):
    print(max([find_seat(line) for line in data]))


def solve2(data: list[str]):
    seats = sorted([find_seat(line) for line in data])
    for i in range(1, len(seats)):
        if seats[i] - seats[i - 1] == 2:
            print(seats[i] - 1)
            break
