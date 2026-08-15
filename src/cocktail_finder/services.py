from .pantry import rank_by_pantry
from .parsers import extract_ingredients


def hydrate_filter_results(client, summaries: list[dict], limit: int = 12) -> list[dict]:
    drinks = []
    for summary in summaries[:limit]:
        drink_id = summary.get("idDrink")
        if drink_id:
            full = client.lookup_drink(drink_id)
            if full:
                drinks.append(full)
    return drinks


def find_by_pantry(client, main_ingredient: str, pantry_items: list[str], limit: int = 12):
    summaries = client.filter_drinks("i", main_ingredient)
    full_drinks = hydrate_filter_results(client, summaries, limit=limit)
    return rank_by_pantry(full_drinks, pantry_items, extract_ingredients)
