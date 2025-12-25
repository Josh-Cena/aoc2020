from collections import defaultdict


def solve(data: list[str]):
    allergen_possible_ingredients: dict[str, set[str]] = {}
    ingredient_counts = defaultdict(int)
    for line in data:
        part1, part2 = line.split(" (contains ")
        ingredients = part1.split(" ")
        allergens = part2[:-1].split(", ")
        for a in allergens:
            allergen_possible_ingredients.setdefault(
                a, set(ingredients)
            ).intersection_update(ingredients)
        for i in ingredients:
            ingredient_counts[i] += 1
    allergen_to_ingredient: dict[str, str] = {}
    while len(allergen_possible_ingredients) > 0:
        for allergen, ingredients in allergen_possible_ingredients.items():
            if len(ingredients) == 1:
                del allergen_possible_ingredients[allergen]
                for i in allergen_possible_ingredients.values():
                    i.difference_update(ingredients)
                allergen_to_ingredient[allergen] = ingredients.pop()
                break
        else:
            # Can't find any allergen to figure out
            raise ValueError("Arrived at an impasse")
    for i in allergen_to_ingredient.values():
        ingredient_counts.pop(i)
    return allergen_to_ingredient, ingredient_counts


def solve1(data: list[str]):
    _, ingredient_counts = solve(data)
    print(sum(ingredient_counts.values()))


def solve2(data: list[str]):
    allergen_to_ingredient, _ = solve(data)
    print(
        ",".join(
            x[1] for x in sorted(allergen_to_ingredient.items(), key=lambda x: x[0])
        )
    )
