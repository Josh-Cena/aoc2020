import numpy as np


shift_dir = {
    "E": np.array([1, 0]),
    "S": np.array([0, -1]),
    "W": np.array([-1, 0]),
    "N": np.array([0, 1]),
}

dir_order = ["E", "S", "W", "N"]


def solve1(data: list[str]):
    cur_dir = 0
    cur_pos = np.array([0, 0])
    for line in data:
        action = line[0]
        amount = int(line[1:])
        if action == "R":
            cur_dir = (cur_dir + amount // 90) % 4
        elif action == "L":
            cur_dir = (cur_dir - amount // 90 + 4) % 4
        elif action == "F":
            cur_pos += shift_dir[dir_order[cur_dir]] * amount
        else:
            cur_pos += shift_dir[action] * amount
    print(np.sum(np.abs(cur_pos)))


rot = {
    90: np.array([[0, -1], [1, 0]]),
    180: np.array([[-1, 0], [0, -1]]),
    270: np.array([[0, 1], [-1, 0]]),
}


def solve2(data: list[str]):
    cur_pos = np.array([0, 0])
    waypoint_pos = np.array([10, 1])
    for line in data:
        action = line[0]
        amount = int(line[1:])
        if action == "R" or action == "L":
            if action == "R":
                amount = 360 - amount
            waypoint_pos = rot[amount] @ waypoint_pos
        elif action == "F":
            cur_pos += waypoint_pos * amount
        else:
            waypoint_pos += shift_dir[action] * amount
    print(np.sum(np.abs(cur_pos)))
