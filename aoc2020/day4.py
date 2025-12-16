import re

required = {
    "byr": lambda x: 1920 <= int(x) <= 2002,
    "iyr": lambda x: 2010 <= int(x) <= 2020,
    "eyr": lambda x: 2020 <= int(x) <= 2030,
    "hgt": lambda x: (x.endswith("cm") and 150 <= int(x[:-2]) <= 193)
    or (x.endswith("in") and 59 <= int(x[:-2]) <= 76),
    "hcl": lambda x: re.match(r"^#[0-9a-f]{6}$", x) is not None,
    "ecl": lambda x: x in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
    "pid": lambda x: re.match(r"^[0-9]{9}$", x) is not None,
}


def solve1(data: list[str]):
    entries = "\n".join(data).split("\n\n")
    count = 0
    for entry in entries:
        parts = entry.replace("\n", " ").split()
        fields = {}
        for part in parts:
            subparts = part.split(":", 1)
            fields[subparts[0]] = subparts[1]
        if all(k in fields for k in required.keys()):
            count += 1
    print(count)


def solve2(data: list[str]):
    entries = "\n".join(data).split("\n\n")
    count = 0
    for entry in entries:
        parts = entry.replace("\n", " ").split()
        fields = {}
        for part in parts:
            subparts = part.split(":", 1)
            if subparts[0] in fields:
                break
            fields[subparts[0]] = subparts[1]
        else:
            if all(k in fields and required[k](fields[k]) for k in required.keys()):
                count += 1
    print(count)
