import re
import itertools


def solve1(data: list[str]):
    mem = {}
    mask_1 = 0  # 0 bit => unchanged; 1 bit => force to 1
    mask_0 = -1 & 0xFFFFFFFFF  # 0 bit => force to 0; 1 bit => unchanged
    for line in data:
        if line.startswith("mask = "):
            mask = reversed(line[len("mask = ") :])
            mask_1 = 0
            mask_0 = -1 & 0xFFFFFFFFF
            for i, ch in enumerate(mask):
                if ch == "0":
                    mask_0 = mask_0 ^ (1 << i)  # set i bit to 0
                elif ch == "1":
                    mask_1 = mask_1 ^ (1 << i)  # set i bit to 1
        else:
            match = re.match(r"mem\[(\d+)\] = (\d+)", line)
            if not match:
                raise ValueError("Invalid input")
            mem[int(match.group(1))] = int(match.group(2)) & mask_0 | mask_1
    print(sum(mem.values()))


def generate_binaries(x_indices: list[int]):
    for comb in itertools.product((0, 1), repeat=len(x_indices)):
        mask_1 = 0
        mask_0 = -1 & 0xFFFFFFFFF
        for i, bit in zip(x_indices, comb):
            if bit == 0:
                mask_0 = mask_0 ^ (1 << i)
            elif bit == 1:
                mask_1 = mask_1 ^ (1 << i)
        yield (mask_0, mask_1)


def solve2(data: list[str]):
    mem = {}
    mask_1 = 0
    x_masks = []
    for line in data:
        if line.startswith("mask = "):
            mask = reversed(line[len("mask = ") :])
            mask_1 = 0
            x_indices = []
            for i, ch in enumerate(mask):
                if ch == "1":
                    mask_1 = mask_1 ^ (1 << i)
                elif ch == "X":
                    x_indices.append(i)
            x_masks = list(generate_binaries(x_indices))
        else:
            match = re.match(r"mem\[(\d+)\] = (\d+)", line)
            if not match:
                raise ValueError("Invalid input")
            base_index = int(match.group(1)) | mask_1
            val = int(match.group(2))
            for x_mask_0, x_mask_1 in x_masks:
                mem[base_index & x_mask_0 | x_mask_1] = val
    print(sum(mem.values()))
