from cocktail_finder.parsers import extract_ingredients, normalize, parse_pantry_text


def test_extract_ingredients_pairs_measure_and_ingredient(margarita_drink):
    assert extract_ingredients(margarita_drink) == [
        {"ingredient": "Tequila", "measure": "1 1/2 oz"},
        {"ingredient": "Triple sec", "measure": "1/2 oz"},
        {"ingredient": "Lime juice", "measure": "1 oz"},
        {"ingredient": "Salt", "measure": ""},
    ]


def test_normalize_collapses_case_and_spaces():
    assert normalize("  Lime   Juice ") == "lime juice"


def test_parse_pantry_text_ignores_blanks():
    assert parse_pantry_text("gin, , lemon juice, sugar ") == ["gin", "lemon juice", "sugar"]
