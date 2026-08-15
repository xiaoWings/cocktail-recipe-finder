import os

import requests

BASE_URL_TEMPLATE = "https://www.thecocktaildb.com/api/json/v1/{api_key}"


class CocktailDBError(RuntimeError):
    """Raised when TheCocktailDB request fails."""


class CocktailDBClient:
    """Small client wrapper for TheCocktailDB V1 API."""

    def __init__(self, api_key: str | None = None, timeout: int = 15):
        self.api_key = api_key or os.getenv("THECOCKTAILDB_API_KEY", "1")
        self.timeout = timeout
        self.base_url = BASE_URL_TEMPLATE.format(api_key=self.api_key)

    def get_json(self, endpoint: str, params: dict | None = None) -> dict:
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            raise CocktailDBError(f"API request failed: {exc}") from exc

    def search_drinks_by_name(self, name: str) -> list[dict]:
        return self.get_json("search.php", {"s": name}).get("drinks") or []

    def search_ingredient_by_name(self, name: str) -> list[dict]:
        return self.get_json("search.php", {"i": name}).get("ingredients") or []

    def lookup_drink(self, drink_id: str) -> dict | None:
        drinks = self.get_json("lookup.php", {"i": drink_id}).get("drinks") or []
        return drinks[0] if drinks else None

    def lookup_ingredient(self, ingredient_id: str) -> dict | None:
        ingredients = self.get_json("lookup.php", {"iid": ingredient_id}).get("ingredients") or []
        return ingredients[0] if ingredients else None

    def random_drink(self) -> dict | None:
        drinks = self.get_json("random.php").get("drinks") or []
        return drinks[0] if drinks else None

    def filter_drinks(self, filter_type: str, value: str) -> list[dict]:
        safe_value = value.strip().replace(" ", "_")
        return self.get_json("filter.php", {filter_type: safe_value}).get("drinks") or []

    def list_filter_values(self, filter_type: str) -> list[str]:
        drinks = self.get_json("list.php", {filter_type: "list"}).get("drinks") or []
        key_map = {
            "c": "strCategory",
            "g": "strGlass",
            "i": "strIngredient1",
            "a": "strAlcoholic",
        }
        key = key_map[filter_type]
        return sorted(row[key] for row in drinks if row.get(key))
