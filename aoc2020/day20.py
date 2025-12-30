import numpy as np
from collections import defaultdict
from typing import Literal, Union


EdgeDirection = Literal["T", "T'", "B", "B'", "L", "L'", "R", "R'"]
EdgeAlignment = dict[int, dict[int, list[tuple[EdgeDirection, EdgeDirection]]]]


def align(grids: dict[int, np.ndarray]) -> EdgeAlignment:
    edge_profiles: defaultdict[str, list[tuple[int, EdgeDirection]]] = defaultdict(list)
    for id, grid in grids.items():
        edge_profiles["".join(grid[0])].append((id, "T"))
        edge_profiles["".join(reversed(grid[0]))].append((id, "T'"))
        edge_profiles["".join(grid[-1])].append((id, "B"))
        edge_profiles["".join(reversed(grid[-1]))].append((id, "B'"))
        edge_profiles["".join(l[0] for l in grid)].append((id, "L"))
        edge_profiles["".join(reversed(list(l[0] for l in grid)))].append((id, "L'"))
        edge_profiles["".join(l[-1] for l in grid)].append((id, "R"))
        edge_profiles["".join(reversed(list(l[-1] for l in grid)))].append((id, "R'"))
    alignment: defaultdict[
        int, defaultdict[int, list[tuple[EdgeDirection, EdgeDirection]]]
    ] = defaultdict(lambda: defaultdict(list))
    for group in edge_profiles.values():
        assert 1 <= len(group) <= 2
        if len(group) == 2:
            # Note that for each two neighbors this creates two alignments:
            # L/R and L'/R'. They will be deduplicated after rotation
            alignment[group[0][0]][group[1][0]].append((group[0][1], group[1][1]))
            alignment[group[1][0]][group[0][0]].append((group[1][1], group[0][1]))
    return {i: dict(v) for i, v in alignment.items()}


def solve1(data: list[str]):
    chunks = [c.split("\n") for c in "\n".join(data).split("\n\n")]
    grids = {
        int(lines[0][5:-1]): np.array(list(map(list, lines[1:]))) for lines in chunks
    }
    edge_alignment = align(grids)
    corners = [i for i, n in edge_alignment.items() if len(n) == 2]
    assert len(corners) == 4
    print(np.product(corners))


def solve2(data: list[str]):
    chunks = [c.split("\n") for c in "\n".join(data).split("\n\n")]
    grids = {
        int(lines[0][5:-1]): np.array(list(map(list, lines[1:]))) for lines in chunks
    }
    edge_alignment = align(grids)
    corners = [i for i, n in edge_alignment.items() if len(n) == 2]
    last_row = []
    next_grid = corners[0]
    aligned_grids: list[list[int]] = []
    while next_grid is not None:
        i = 0
        left_nbr = None
        aligned_grids.append([])
        while next_grid is not None:
            aligned_grids[-1].append(next_grid)
            if i == len(last_row):
                top_nbr = None
                last_row.append(next_grid)
            else:
                top_nbr = last_row[i]
                last_row[i] = next_grid
            next_grid, left_nbr = (
                rotate_grid(next_grid, left_nbr, top_nbr, grids, edge_alignment),
                next_grid,
            )
            i += 1
        next_grid = None
        for nbr, edges in edge_alignment[last_row[0]].items():
            if edges[0][0].startswith("B"):
                next_grid = nbr
                break
    joined_grid = np.concatenate(
        list(
            map(
                lambda row: np.concatenate(
                    list(map(lambda id: grids[id][1:-1, 1:-1], row)), axis=1
                ),
                aligned_grids,
            )
        ),
        axis=0,
    )
    for r in range(joined_grid.shape[0]):
        for c in range(joined_grid.shape[1]):
            monster = search_monster(joined_grid, r, c)
            if monster is not None:
                for mr in range(monster.shape[0]):
                    for mc in range(monster.shape[1]):
                        if monster[mr, mc] == "#":
                            joined_grid[r + mr, c + mc] = "O"
    print(np.sum(joined_grid == "#"))


def get_edge_neighboring(
    grid_id: int,
    neighbor_id: int,
    direction: EdgeDirection,
    edge_alignment: EdgeAlignment,
):
    """
    Get the edge of grid_id that neighbors neighbor_id in the given direction
    neighbor_id is expected to be already aligned
    The direction is the direction from neighbor_id to grid_id
    """
    edges = edge_alignment[grid_id][neighbor_id]
    assert len(edges) == 1
    edge = edges[0]
    assert edge[1] == direction
    return edge[0]


def rotate_grid(
    grid_id: int,
    left_nbr: Union[int, None],
    top_nbr: Union[int, None],
    grids: dict[int, np.ndarray],
    edge_alignment: EdgeAlignment,
):
    """
    Each grid is rotated based on its left neighbor and top neighbor.
    We need to eventually create edge alignment (left_nbr, "R"): (grid_id, "L")
    and (top_nbr, "B"): (grid_id, "T").
    It is guaranteed that (left_nbr, "R"): (grid_id, \\<something>) and
    (top_nbr, "B"): (grid_id, \\<something>) exists.
    After rotation, grid_id does not use any X' edges. Because left_nbr and
    top_nbr are already rotated, they also do not use R' or B'.
    Returns the right neighbor grid id if exists, else None.
    """
    if top_nbr:
        top_edge = get_edge_neighboring(grid_id, top_nbr, "B", edge_alignment)
    else:
        missing_edges: set[EdgeDirection] = {"T", "B", "L", "R"} - {
            # Only consider non-flipped edges
            x[0][0][0]
            for x in edge_alignment[grid_id].values()
        }
        assert 1 <= len(missing_edges) <= 2
        assert missing_edges != {"T", "B"} and missing_edges != {"L", "R"}
        # If left_nbr and top_nbr are both missing (which can only happen for
        # the first cell), either order of the missing edges is fine.
        # Otherwise, we have to respect left_nbr, because top_edge cannot be
        # the opposite of left_edge.
        if len(missing_edges) == 2:
            if left_nbr is not None:
                left_edge = get_edge_neighboring(grid_id, left_nbr, "R", edge_alignment)
                if left_edge.startswith("R") or left_edge.startswith("L"):
                    missing_edges = missing_edges - {"L", "R"}
                else:
                    missing_edges = missing_edges - {"T", "B"}
            else:
                # Prefer T/B so there's a chance to not rotate
                missing_edges = missing_edges - {"L", "R"}
        assert len(missing_edges) == 1
        top_edge = missing_edges.pop()
    # Rotate such that top_edge becomes "T"
    if top_edge.startswith("B"):
        grids[grid_id] = np.rot90(grids[grid_id], k=2)
        realign(
            grid_id,
            edge_alignment,
            {"T": "B'", "B": "T'", "L": "R'", "R": "L'"},
        )
    elif top_edge.startswith("L"):
        grids[grid_id] = np.rot90(grids[grid_id], k=-1)
        realign(
            grid_id,
            edge_alignment,
            {"T": "R", "R": "B'", "B": "L", "L": "T'"},
        )
    elif top_edge.startswith("R"):
        grids[grid_id] = np.rot90(grids[grid_id], k=1)
        realign(
            grid_id,
            edge_alignment,
            {"T": "L'", "L": "B", "B": "R'", "R": "T"},
        )
    else:
        assert top_edge.startswith("T")
    if left_nbr:
        left_edge = get_edge_neighboring(grid_id, left_nbr, "R", edge_alignment)
    else:
        missing_edges: set[EdgeDirection] = {"L", "R"} - {
            x[0][0][0] for x in edge_alignment[grid_id].values()
        }
        left_edge = missing_edges.pop()
    # Now flip such that left_edge becomes "L"
    if left_edge.startswith("R"):
        grids[grid_id] = np.fliplr(grids[grid_id])
        realign(
            grid_id,
            edge_alignment,
            {"L": "R", "R": "L", "T": "T'", "B": "B'"},
        )
    else:
        assert left_edge.startswith("L")
    for nbr in edge_alignment[grid_id]:
        if len(edge_alignment[grid_id][nbr]) == 1 and edge_alignment[grid_id][nbr][0][
            0
        ].endswith("'"):
            raise ValueError("Failed to align grid without flipped edges")
        edge_alignment[grid_id][nbr] = [
            (a, b) for a, b in edge_alignment[grid_id][nbr] if not a.endswith("'")
        ]
        edge_alignment[nbr][grid_id] = [
            (a, b) for a, b in edge_alignment[nbr][grid_id] if not b.endswith("'")
        ]
    for nbr, edges in edge_alignment[grid_id].items():
        if edges[0][0].startswith("R"):
            return nbr
    return None


def realign(
    grid_id: int,
    edge_alignment: EdgeAlignment,
    replacements: dict[EdgeDirection, EdgeDirection],
):
    def replace_edge(old_edge: EdgeDirection):
        if old_edge.endswith("'"):
            new_edge = replacements[old_edge[0]]
            if new_edge.endswith("'"):
                return new_edge[0]
            else:
                return new_edge + "'"
        else:
            return replacements[old_edge]

    for nbr in edge_alignment[grid_id]:
        edge_alignment[grid_id][nbr] = [
            (replace_edge(edge_pair[0]), edge_pair[1])
            for edge_pair in edge_alignment[grid_id][nbr]
        ]
        edge_alignment[nbr][grid_id] = [(b, a) for a, b in edge_alignment[grid_id][nbr]]


monster = np.array(
    [
        list("                  # "),
        list("#    ##    ##    ###"),
        list(" #  #  #  #  #  #   "),
    ]
)

monsters = [
    monster,
    np.rot90(monster, k=1),
    np.rot90(monster, k=2),
    np.rot90(monster, k=3),
    np.fliplr(monster),
    np.rot90(np.fliplr(monster), k=1),
    np.rot90(np.fliplr(monster), k=2),
    np.rot90(np.fliplr(monster), k=3),
]


def search_monster(grid: np.ndarray, r: int, c: int) -> bool:
    for monster in monsters:
        if r + monster.shape[0] > grid.shape[0] or c + monster.shape[1] > grid.shape[1]:
            continue
        for mr in range(monster.shape[0]):
            for mc in range(monster.shape[1]):
                if monster[mr, mc] == "#" and grid[r + mr, c + mc] != "#":
                    break
            else:
                continue
            break
        else:
            return monster
    return None
