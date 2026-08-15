from cocktail_finder.grocery import build_grocery_list


def test_build_grocery_list_groups_missing_ingredients(margarita_drink):
    grocery = build_grocery_list([margarita_drink], ["tequila", "lime juice"])
    assert "triple sec" in grocery
    assert "salt" in grocery
    assert grocery["triple sec"][0]["cocktail"] == "Margarita"
    assert grocery["triple sec"][0]["measure"] == "1/2 oz"
