from cocktail_finder.grocery import build_grocery_list


def test_build_grocery_list_groups_missing_ingredients(margarita_drink):
    grocery = build_grocery_list([margarita_drink], ["tequila", "lime juice"])
    assert "triple sec" in grocery
    assert "salt" in grocery
    assert grocery["triple sec"][0]["cocktail"] == "Margarita"
    assert grocery["triple sec"][0]["measure"] == "1/2 oz"


def test_grocery_list_empty_pantry_includes_recipe_items():
    drink = {
        "strDrink": "Test Cocktail",
        "strIngredient1": "Gin",
        "strMeasure1": "2 oz",
        "strIngredient2": "Lime Juice",
        "strMeasure2": "1 oz",
        "strIngredient3": None,
        "strMeasure3": None,
    }

    grocery = build_grocery_list([drink], pantry_items=[])

    assert "gin" in grocery
    assert "lime juice" in grocery
    assert grocery["gin"][0]["cocktail"] == "Test Cocktail"
    assert grocery["gin"][0]["measure"] == "2 oz"


def test_grocery_list_full_pantry_is_empty():
    drink = {
        "strDrink": "Test Cocktail",
        "strIngredient1": "Gin",
        "strMeasure1": "2 oz",
        "strIngredient2": "Lime Juice",
        "strMeasure2": "1 oz",
    }

    grocery = build_grocery_list([drink], pantry_items=["gin", "lime juice"])

    assert grocery == {}