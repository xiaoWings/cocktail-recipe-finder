from cocktail_finder.pantry import compare_to_pantry, rank_by_pantry
from cocktail_finder.parsers import extract_ingredients


def test_compare_to_pantry_marks_missing_items():
    recipe = [
        {"ingredient": "Gin", "measure": "2 oz"},
        {"ingredient": "Lime Juice", "measure": "1 oz"},
    ]
    result = compare_to_pantry(recipe, ["gin"])
    assert result["available_count"] == 1
    assert result["missing_count"] == 1
    assert result["missing"][0]["ingredient"] == "Lime Juice"


def test_rank_by_pantry_sorts_by_fewest_missing(margarita_drink):
    drink2 = dict(margarita_drink)
    drink2["idDrink"] = "2"
    drink2["strDrink"] = "Simple Tequila"
    drink2["strIngredient2"] = None
    drink2["strIngredient3"] = None
    drink2["strIngredient4"] = None

    ranked = rank_by_pantry([margarita_drink, drink2], ["tequila"], extract_ingredients)
    assert ranked[0]["drink"]["strDrink"] == "Simple Tequila"
