def find_seat(boarding_pass: str):
    pass_num = (
        boarding_pass.replace("F", "0")
        .replace("B", "1")
        .replace("L", "0")
        .replace("R", "1")
    )
    return int(pass_num, 2)


def solve1(data: list[str]):
    print(max([find_seat(line) for line in data]))


def solve2(data: list[str]):
    seats = sorted([find_seat(line) for line in data])
    for i in range(1, len(seats)):
        if seats[i] - seats[i - 1] == 2:
            print(seats[i] - 1)
            break
