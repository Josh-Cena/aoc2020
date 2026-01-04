shift_dir: dict[str, complex] = {
    "E": 1,
    "S": -1j,
    "W": -1,
    "N": 1j,
}


def solve1(data: list[str]):
    cur_dir = 1
    cur_pos = 0
    for line in data:
        action = line[0]
        amount = int(line[1:])
        if action == "R":
            cur_dir *= (-1j) ** (amount // 90)
        elif action == "L":
            cur_dir *= 1j ** (amount // 90)
        elif action == "F":
            cur_pos += cur_dir * amount
        else:
            cur_pos += shift_dir[action] * amount
    print(abs(int(cur_pos.imag)) + abs(int(cur_pos.real)))


def solve2(data: list[str]):
    waypoint_pos = 10 + 1j
    cur_pos = 0
    for line in data:
        action = line[0]
        amount = int(line[1:])
        if action == "R":
            waypoint_pos *= (-1j) ** (amount // 90)
        elif action == "L":
            waypoint_pos *= 1j ** (amount // 90)
        elif action == "F":
            cur_pos += waypoint_pos * amount
        else:
            waypoint_pos += shift_dir[action] * amount
    print(abs(int(cur_pos.imag)) + abs(int(cur_pos.real)))
