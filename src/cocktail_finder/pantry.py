from .parsers import normalize


def compare_to_pantry(recipe_items: list[dict], pantry_items: list[str]) -> dict:
    pantry = {normalize(item) for item in pantry_items if normalize(item)}
    available: list[dict] = []
    missing: list[dict] = []

    for item in recipe_items:
        if normalize(item["ingredient"]) in pantry:
            available.append(item)
        else:
            missing.append(item)

    return {
        "available": available,
        "missing": missing,
        "available_count": len(available),
        "missing_count": len(missing),
    }


def rank_by_pantry(full_drinks: list[dict], pantry_items: list[str], extract_func) -> list[dict]:
    ranked = []
    for drink in full_drinks:
        comparison = compare_to_pantry(extract_func(drink), pantry_items)
        ranked.append({"drink": drink, **comparison})
    return sorted(ranked, key=lambda row: (row["missing_count"], -row["available_count"]))
