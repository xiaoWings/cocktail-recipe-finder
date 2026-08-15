import re


def normalize(text: str | None) -> str:
    """Normalize strings for case-insensitive pantry matching."""
    return re.sub(r"\s+", " ", str(text or "").strip().lower())


def parse_pantry_text(text: str) -> list[str]:
    """Convert comma-separated pantry text into a list of ingredient names."""
    return [item.strip() for item in text.split(",") if item.strip()]


def extract_ingredients(drink: dict) -> list[dict]:
    """Convert TheCocktailDB ingredient/measure fields into ordered dictionaries."""
    items: list[dict] = []
    for number in range(1, 16):
        ingredient = drink.get(f"strIngredient{number}")
        measure = drink.get(f"strMeasure{number}")
        if ingredient and str(ingredient).strip():
            items.append(
                {
                    "ingredient": str(ingredient).strip(),
                    "measure": str(measure).strip() if measure else "",
                }
            )
    return items
