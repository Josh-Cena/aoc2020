from typing import Literal
import itertools


def solve1(data: list[str]):
    part1, part2 = "\n".join(data).split("\n\n")
    rules = dict(parse_rule(l) for l in part1.split("\n"))
    total = sum((len(s) in matches_rule(s, 0, 0, rules)) for s in part2.split("\n"))
    print(total)


def solve2(data: list[str]):
    part1, part2 = "\n".join(data).split("\n\n")
    rules = dict(parse_rule(l) for l in part1.split("\n"))
    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]
    total = sum((len(s) in matches_rule(s, 0, 0, rules)) for s in part2.split("\n"))
    print(total)


def parse_rule(line: str):
    id, content = line.split(": ")
    if content == '"a"' or content == '"b"':
        return int(id), content
    return int(id), [list(map(int, a.split(" "))) for a in content.split(" | ")]


def matches_rule(
    inp: str,
    ind: int,
    id: int,
    rules: dict[int, list[list[int]] | Literal['"a"', '"b"']],
) -> list[int]:
    if ind >= len(inp):
        return []
    rule = rules[id]
    if rule == '"a"':
        return [ind + 1] if inp[ind] == "a" else []
    if rule == '"b"':
        return [ind + 1] if inp[ind] == "b" else []
    end_inds = []
    for alternative in rule:
        possible_inds = [ind]
        for part in alternative:
            possible_inds = list(
                itertools.chain.from_iterable(
                    matches_rule(inp, i, part, rules) for i in possible_inds
                )
            )
        end_inds.extend(possible_inds)
    return end_inds
