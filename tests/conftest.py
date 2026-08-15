import pytest


@pytest.fixture
def margarita_drink():
    return {
        "idDrink": "11007",
        "strDrink": "Margarita",
        "strCategory": "Ordinary Drink",
        "strAlcoholic": "Alcoholic",
        "strGlass": "Cocktail glass",
        "strInstructions": "Rub the rim of the glass with the lime slice.",
        "strDrinkThumb": "https://example.com/margarita.jpg",
        "strIngredient1": " Tequila ",
        "strMeasure1": "1 1/2 oz ",
        "strIngredient2": "Triple sec",
        "strMeasure2": "1/2 oz",
        "strIngredient3": "Lime juice",
        "strMeasure3": "1 oz",
        "strIngredient4": "Salt",
        "strMeasure4": None,
        "strIngredient5": None,
        "strMeasure5": None,
    }
