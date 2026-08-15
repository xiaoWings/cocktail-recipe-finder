from pathlib import Path
import sys

import streamlit as st

# Make the src-layout package importable when running `streamlit run app.py`.
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from cocktail_finder.api_client import CocktailDBClient, CocktailDBError  # noqa: E402
from cocktail_finder.grocery import build_grocery_list  # noqa: E402
from cocktail_finder.parsers import extract_ingredients, parse_pantry_text  # noqa: E402
from cocktail_finder.services import find_by_pantry, hydrate_filter_results  # noqa: E402

st.set_page_config(page_title="Cocktail Recipe Finder", page_icon="🍹", layout="wide")


@st.cache_resource
def get_client() -> CocktailDBClient:
    return CocktailDBClient()


@st.cache_data(ttl=3600, show_spinner=False)
def cached_list_values(filter_type: str) -> list[str]:
    return get_client().list_filter_values(filter_type)


def init_state() -> None:
    st.session_state.setdefault("selected_drinks", [])
    st.session_state.setdefault("pantry_items", [])


def render_recipe_card(drink: dict, show_add_button: bool = True) -> None:
    st.subheader(drink.get("strDrink", "Unnamed drink"))
    cols = st.columns([1, 2])
    with cols[0]:
        if drink.get("strDrinkThumb"):
            st.image(drink["strDrinkThumb"], use_container_width=True)
    with cols[1]:
        st.write(f"**Category:** {drink.get('strCategory') or 'Unknown'}")
        st.write(f"**Alcoholic status:** {drink.get('strAlcoholic') or 'Unknown'}")
        st.write(f"**Glass:** {drink.get('strGlass') or 'Unknown'}")
        st.write("**Ingredients**")
        for item in extract_ingredients(drink):
            text = f"{item['measure']} {item['ingredient']}".strip()
            st.write(f"- {text}")
        st.write("**Instructions**")
        st.write(drink.get("strInstructions") or "No instructions found.")
        if show_add_button and st.button("Add to grocery list", key=f"add_{drink.get('idDrink')}"):
            if drink not in st.session_state.selected_drinks:
                st.session_state.selected_drinks.append(drink)
                st.success("Added to grocery list selections.")


def main() -> None:
    init_state()
    client = get_client()

    st.title("🍹 Cocktail Recipe Finder + Pantry Matcher")
    st.caption("Recipe data and imagery: TheCocktailDB (https://www.thecocktaildb.com/)")

    with st.sidebar:
        st.header("Search controls")
        mode = st.radio(
            "Mode",
            [
                "Search by cocktail name",
                "Search by ingredient/liquor",
                "Pantry matcher",
                "Ingredient metadata",
                "Filters",
                "Random cocktail",
                "Grocery list",
            ],
        )

    try:
        if mode == "Search by cocktail name":
            name = st.text_input("Cocktail name", "margarita")
            if st.button("Search"):
                results = client.search_drinks_by_name(name)
                if not results:
                    st.warning("No cocktails found.")
                for drink in results:
                    render_recipe_card(drink)

        elif mode == "Search by ingredient/liquor":
            ingredient = st.text_input("Ingredient or liquor", "Gin")
            if st.button("Find cocktails"):
                summaries = client.filter_drinks("i", ingredient)
                drinks = hydrate_filter_results(client, summaries)
                if not drinks:
                    st.warning("No cocktails found for that ingredient.")
                for drink in drinks:
                    render_recipe_card(drink)

        elif mode == "Pantry matcher":
            pantry_text = st.text_area("Ingredients you have, comma-separated", "gin, lemon juice")
            main_ingredient = st.text_input("Main ingredient/liquor", "Gin")
            limit = st.slider("Maximum candidate recipes", min_value=3, max_value=20, value=12)
            if st.button("Match pantry"):
                pantry_items = parse_pantry_text(pantry_text)
                st.session_state.pantry_items = pantry_items
                ranked = find_by_pantry(client, main_ingredient, pantry_items, limit=limit)
                if not ranked:
                    st.warning("No pantry matches found.")
                for row in ranked:
                    st.info(
                        f"Missing {row['missing_count']} ingredient(s); "
                        f"available {row['available_count']} ingredient(s)."
                    )
                    render_recipe_card(row["drink"])

        elif mode == "Ingredient metadata":
            ingredient = st.text_input("Ingredient name", "vodka")
            if st.button("Lookup ingredient"):
                metadata = client.search_ingredient_by_name(ingredient)
                if metadata:
                    st.json(metadata)
                else:
                    st.warning("No ingredient metadata found.")

        elif mode == "Filters":
            filter_options = {
                "Category": "c",
                "Glass": "g",
                "Alcoholic": "a",
                "Ingredient": "i",
            }
            filter_label = st.selectbox("Filter type", list(filter_options.keys()))
            filter_type = filter_options[filter_label]
            values = cached_list_values(filter_type)
            value = st.selectbox("Filter value", values)
            if st.button("Apply filter"):
                drinks = hydrate_filter_results(client, client.filter_drinks(filter_type, value))
                if not drinks:
                    st.warning("No cocktails found for that filter.")
                for drink in drinks:
                    render_recipe_card(drink)

        elif mode == "Random cocktail":
            if st.button("Surprise me"):
                drink = client.random_drink()
                if drink:
                    render_recipe_card(drink)
                else:
                    st.warning("No random cocktail returned.")

        elif mode == "Grocery list":
            st.write(f"Selected cocktails: {len(st.session_state.selected_drinks)}")
            grocery = build_grocery_list(st.session_state.selected_drinks, st.session_state.pantry_items)
            if not grocery:
                st.write("No missing ingredients yet. Add recipes from other modes first.")
            for entries in grocery.values():
                st.write(f"**{entries[0]['ingredient']}**")
                for entry in entries:
                    detail = f"{entry['measure']} for {entry['cocktail']}".strip()
                    st.write(f"- {detail}")
            if st.button("Clear selected cocktails"):
                st.session_state.selected_drinks = []
                st.session_state.pantry_items = []
                st.success("Grocery list cleared.")

    except CocktailDBError as exc:
        st.error(str(exc))


if __name__ == "__main__":
    main()
