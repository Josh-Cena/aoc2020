def solve1(data: list[str]):
    num1 = int(data[0])
    num2 = int(data[1])
    loop_size = 1
    while True:
        if pow(7, loop_size, 20201227) == num1:
            print(pow(num2, loop_size, 20201227))
            return
        loop_size += 1


def solve2(_: list[str]):
    print("No such thing, yay")
