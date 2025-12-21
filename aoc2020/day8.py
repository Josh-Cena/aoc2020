def exec_until_loop(data: list[str]):
    line_num = 0
    seen: set[int] = set()
    acc = 0
    while line_num not in seen and line_num < len(data):
        seen.add(line_num)
        line = data[line_num]
        instr, value = line.split(" ")
        value = int(value)
        if instr == "acc":
            acc += value
            line_num += 1
        elif instr == "jmp":
            line_num += value
        elif instr == "nop":
            line_num += 1
    if line_num == len(data):
        return acc, True
    return acc, False


def solve1(data: list[str]):
    acc, _ = exec_until_loop(data)
    print(acc)


def solve2(data: list[str]):
    for i in range(len(data)):
        line = data[i]
        instr, value = line.split(" ")
        if instr == "jmp":
            data[i] = f"nop {value}"
        elif instr == "nop":
            data[i] = f"jmp {value}"
        else:
            continue

        res, terminated = exec_until_loop(data)
        if terminated:
            print(res)
            return
        data[i] = line
