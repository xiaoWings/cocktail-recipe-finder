from collections import defaultdict

from .parsers import extract_ingredients, normalize


def build_grocery_list(selected_drinks: list[dict], pantry_items: list[str]) -> dict:
    pantry = {normalize(item) for item in pantry_items}
    grocery = defaultdict(list)

    for drink in selected_drinks:
        for item in extract_ingredients(drink):
            key = normalize(item["ingredient"])
            if key not in pantry:
                grocery[key].append(
                    {
                        "ingredient": item["ingredient"],
                        "measure": item["measure"],
                        "cocktail": drink.get("strDrink", "Unknown cocktail"),
                    }
                )

    return dict(grocery)
