import itertools
import numpy as np


def solve1(data: list[str]):
    block1, _, block3 = "\n".join(data).split("\n\n")
    rules = dict(parse_rule(line) for line in block1.split("\n"))
    joined_ranges = [*itertools.chain.from_iterable(rules.values())]
    nearby_tickets = [
        list(map(int, line.split(","))) for line in block3.split("\n")[1:]
    ]
    invalid_values: list[int] = []
    for value in itertools.chain.from_iterable(nearby_tickets):
        if all(
            value < min_val or value > max_val for min_val, max_val in joined_ranges
        ):
            invalid_values.append(value)
    print(sum(invalid_values))


def solve2(data: list[str]):
    block1, block2, block3 = "\n".join(data).split("\n\n")
    rules = dict(parse_rule(line) for line in block1.split("\n"))
    joined_ranges = [*itertools.chain.from_iterable(rules.values())]
    your_ticket = list(map(int, block2.split("\n")[1].split(",")))
    nearby_tickets = [
        list(map(int, line.split(","))) for line in block3.split("\n")[1:]
    ]
    valid_tickets = [
        ticket
        for ticket in nearby_tickets
        if all(
            any(min_val <= value <= max_val for min_val, max_val in joined_ranges)
            for value in ticket
        )
    ]
    candidate_fields = {i: set(rules.keys()) for i in range(len(valid_tickets[0]))}
    for ticket in valid_tickets:
        for i, value in enumerate(ticket):
            impossible_fields = set(
                field
                for field in candidate_fields[i]
                if all(
                    value < min_val or value > max_val
                    for min_val, max_val in rules[field]
                )
            )
            candidate_fields[i] -= impossible_fields
    figured_out = set[str]()
    for i, s in sorted(candidate_fields.items(), key=lambda x: len(x[1])):
        s.difference_update(figured_out)
        assert len(s) == 1
        figured_out = s.union(figured_out)
    fields: list[str] = []
    for s in candidate_fields.values():
        fields.append(s.pop())
    departures = list(
        val for field, val in zip(fields, your_ticket) if field.startswith("departure")
    )
    print(np.product(departures))


def parse_rule(line: str) -> tuple[str, list[tuple[int, int]]]:
    part1, part2 = line.split(": ")
    ranges = [tuple(map(int, x.split("-"))) for x in part2.split(" or ")]
    return part1, ranges
