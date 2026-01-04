from collections import Counter


def parse_input(data: list[str]):
    res: list[tuple[set[str], set[str]]] = []
    for line in data:
        part1, part2 = line.split(" (contains ")
        ingredients = set(part1.split(" "))
        allergens = set(part2[:-1].split(", "))
        res.append((ingredients, allergens))
    return res


def get_possible_ingredients(data: list[tuple[set[str], set[str]]]):
    res: dict[str, set[str]] = {}
    for ingredients, allergens in data:
        for a in allergens:
            res.setdefault(a, set(ingredients)).intersection_update(ingredients)
    return res


def solve1(data: list[str]):
    input_data = parse_input(data)
    possible_ingredients = get_possible_ingredients(input_data)
    ingredient_counts = Counter[str]()
    for ingredients, _ in input_data:
        ingredient_counts.update(ingredients)
    for ingredients in possible_ingredients.values():
        for i in ingredients:
            del ingredient_counts[i]
    print(sum(ingredient_counts.values()))


def solve2(data: list[str]):
    input_data = parse_input(data)
    possible_ingredients = get_possible_ingredients(input_data)
    allergen_to_ingredient: dict[str, str] = {}
    while len(possible_ingredients) > 0:
        for allergen, ingredients in possible_ingredients.items():
            if len(ingredients) == 1:
                del possible_ingredients[allergen]
                for i in possible_ingredients.values():
                    i.difference_update(ingredients)
                allergen_to_ingredient[allergen] = ingredients.pop()
                break
        else:
            # Can't find any allergen to figure out
            raise ValueError("Arrived at an impasse")
    print(
        ",".join(
            x[1] for x in sorted(allergen_to_ingredient.items(), key=lambda x: x[0])
        )
    )
