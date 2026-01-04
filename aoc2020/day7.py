from collections import defaultdict


def parse_line(line: str):
    parent, children = line.split(" contain ")
    parent = parent.split(" bag")[0]
    children = children[:-1].split(", ")
    if children[0] == "no other bags":
        children = []
    else:
        children = [
            (int(child.split(" ")[0]), " ".join(child.split(" ")[1:-1]))
            for child in children
        ]
    return parent, children


def solve1(data: list[str]):
    graph = {parent: children for parent, children in map(parse_line, data)}
    rev_graph: defaultdict[str, list[str]] = defaultdict(list)
    for parent, children in graph.items():
        for _, child in children:
            rev_graph[child].append(parent)

    seen = set[str]()
    stack = ["shiny gold"]
    while stack:
        node = stack.pop()
        for neighbor in rev_graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    print(len(seen))


def solve2(data: list[str]):
    graph = {parent: children for parent, children in map(parse_line, data)}

    def dfs(node: str) -> int:
        return sum(count * (1 + dfs(child)) for count, child in graph[node])

    print(dfs("shiny gold"))
