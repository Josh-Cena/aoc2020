def solve1(data: list[str]):
    player1, player2 = [list(map(int, x.split("\n")[1:])) for x in "\n".join(data).split("\n\n")]
    while len(player1) > 0 and len(player2) > 0:
        card1, card2 = player1.pop(0), player2.pop(0)
        assert card1 != card2
        if card1 > card2:
            player1.extend([card1, card2])
        else:
            player2.extend([card2, card1])
    player1.extend(player2)
    total = sum(a * b for a, b in zip(range(len(player1), 0, -1), player1))
    print(total)


def play_game(player1: list[int], player2: list[int]):
    seen: set[tuple[tuple[int], tuple[int]]] = {(tuple(player1), tuple(player2))}
    while len(player1) > 0 and len(player2) > 0:
        card1, card2 = player1.pop(0), player2.pop(0)
        assert card1 != card2
        if card1 > len(player1) or card2 > len(player2):
            winner = 1 if card1 > card2 else 2
        else:
            subplayer1, subplayer2 = list(player1[:card1]), list(player2[:card2])
            winner = play_game(subplayer1, subplayer2)
        if winner == 1:
            player1.extend([card1, card2])
        else:
            player2.extend([card2, card1])
        if (tuple(player1), tuple(player2)) in seen:
            return 1
        seen.add((tuple(player1), tuple(player2)))
    if len(player1) == 0:
        return 2
    else:
        return 1



def solve2(data: list[str]):
    player1, player2 = [list(map(int, x.split("\n")[1:])) for x in "\n".join(data).split("\n\n")]
    winner = play_game(player1, player2)
    winner_deck = player1 if winner == 1 else player2
    total = sum(a * b for a, b in zip(range(len(winner_deck), 0, -1), winner_deck))
    print(total)
