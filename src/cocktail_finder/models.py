from typing import TypedDict


class IngredientItem(TypedDict):
    ingredient: str
    measure: str


class PantryComparison(TypedDict):
    available: list[IngredientItem]
    missing: list[IngredientItem]
    available_count: int
    missing_count: int
