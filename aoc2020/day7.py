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

    def dfs(node: str) -> bool:
        if node == "shiny gold":
            return True
        return any(dfs(child) for _, child in graph[node])

    print(sum(dfs(parent) for parent in graph if parent != "shiny gold"))


def solve2(data: list[str]):
    graph = {parent: children for parent, children in map(parse_line, data)}

    def dfs(node: str) -> int:
        if not graph[node]:
            return 0
        return sum(count + count * dfs(child) for count, child in graph[node])

    print(dfs("shiny gold"))
