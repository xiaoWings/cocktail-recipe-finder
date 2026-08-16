import streamlit as st
from src.cocktail_finder.api_client import CocktailDBClient, CocktailDBError
from src.cocktail_finder.grocery import build_grocery_list
from src.cocktail_finder.parsers import extract_ingredients
from src.cocktail_finder.services import find_by_pantry, hydrate_filter_results

st.set_page_config(
    page_title="Cocktail Recipe Finder",
    page_icon="🍹",
    layout="wide",
)


@st.cache_resource
def get_client() -> CocktailDBClient:
    return CocktailDBClient()


@st.cache_data(ttl=3600, show_spinner=False)
def cached_list_values(filter_type: str) -> list[str]:
    client = get_client()
    return client.list_filter_values(filter_type)


def init_state() -> None:
    """
    Initialize every session_state key before anything reads it.

    This prevents:
    KeyError / AttributeError:
    st.session_state has no key "selected_drinks"
    """
    st.session_state.setdefault("selected_drinks", [])
    st.session_state.setdefault("pantry_items", [])

    # Persist results so recipe cards survive Streamlit reruns.
    st.session_state.setdefault("name_results", [])
    st.session_state.setdefault("ingredient_results", [])
    st.session_state.setdefault("pantry_results", [])
    st.session_state.setdefault("filter_results", [])
    st.session_state.setdefault("random_result", None)

    # Optional user feedback.
    st.session_state.setdefault("last_added", None)


def selected_drinks() -> list[dict]:
    """
    Defensive getter. Use this instead of reading
    st.session_state.selected_drinks before initialization.
    """
    init_state()
    return st.session_state.get("selected_drinks", [])


def is_drink_selected(drink_id: str | None) -> bool:
    init_state()

    if not drink_id:
        return False

    return any(
        drink.get("idDrink") == drink_id for drink in st.session_state.get("selected_drinks", [])
    )


def add_drink_to_grocery(drink: dict) -> None:
    """
    Callback for the Add to grocery list button.
    """
    init_state()

    drink_id = drink.get("idDrink")

    if not is_drink_selected(drink_id):
        st.session_state.selected_drinks.append(drink)
        st.session_state.last_added = drink.get("strDrink", "Cocktail")


def remove_selected_drink(drink_id: str | None) -> None:
    init_state()

    st.session_state.selected_drinks = [
        drink
        for drink in st.session_state.get("selected_drinks", [])
        if drink.get("idDrink") != drink_id
    ]


def clear_selected_drinks() -> None:
    init_state()

    st.session_state.selected_drinks = []
    st.session_state.last_added = None


def update_pantry_from_text(pantry_text: str) -> None:
    init_state()

    st.session_state.pantry_items = [
        item.strip() for item in pantry_text.split(",") if item.strip()
    ]


def render_recipe_card(drink: dict, show_add_button: bool = True) -> None:
    """
    Render one cocktail recipe card.
    """
    drink_name = drink.get("strDrink", "Unnamed drink")
    drink_id = drink.get("idDrink") or drink_name.replace(" ", "_").lower()

    st.subheader(drink_name)

    cols = st.columns([1, 2])

    with cols[0]:
        if drink.get("strDrinkThumb"):
            st.image(drink["strDrinkThumb"], use_container_width=True)

    with cols[1]:
        st.write(f"**Category:** {drink.get('strCategory') or 'Unknown'}")
        st.write(f"**Alcoholic status:** {drink.get('strAlcoholic') or 'Unknown'}")
        st.write(f"**Glass:** {drink.get('strGlass') or 'Unknown'}")

        st.write("**Ingredients**")
        ingredients = extract_ingredients(drink)

        if ingredients:
            for item in ingredients:
                text = f"{item['measure']} {item['ingredient']}".strip()
                st.write(f"- {text}")
        else:
            st.write("_No ingredient details found for this result._")

        st.write("**Instructions**")
        st.write(drink.get("strInstructions") or "No instructions found.")

        if show_add_button:
            already_added = is_drink_selected(drink.get("idDrink"))

            st.button(
                "Already added" if already_added else "Add to grocery list",
                key=f"add_{drink_id}",
                on_click=add_drink_to_grocery,
                args=(drink,),
                disabled=already_added,
            )

    st.divider()


def render_grocery_list_page() -> None:
    init_state()

    selected = st.session_state.get("selected_drinks", [])

    st.subheader(f"Selected cocktails ({len(selected)})")

    if not selected:
        st.info(
            "No cocktails selected yet. Go to a search page, find a recipe, "
            "and click **Add to grocery list**."
        )
        return

    st.write("These cocktails are currently selected:")

    for drink in selected:
        drink_id = drink.get("idDrink")
        cols = st.columns([4, 1])

        with cols[0]:
            st.write(f"🍹 **{drink.get('strDrink', 'Unnamed cocktail')}**")

        with cols[1]:
            st.button(
                "Remove",
                key=f"remove_{drink_id}",
                on_click=remove_selected_drink,
                args=(drink_id,),
            )

    st.button(
        "Clear all selected cocktails",
        key="clear_selected_drinks",
        on_click=clear_selected_drinks,
    )

    st.divider()

    st.subheader("Pantry items you already have")

    pantry_default = ", ".join(st.session_state.get("pantry_items", []))
    pantry_text = st.text_area(
        "Enter ingredients you already have, separated by commas",
        value=pantry_default,
        key="grocery_pantry_text",
    )

    if st.button("Update pantry for grocery list", key="update_grocery_pantry"):
        update_pantry_from_text(pantry_text)
        st.success("Pantry updated.")

    st.caption("The grocery list below only shows ingredients missing from your pantry.")

    grocery = build_grocery_list(
        st.session_state.get("selected_drinks", []),
        st.session_state.get("pantry_items", []),
    )

    st.subheader("Missing ingredients to buy")

    if not grocery:
        st.success(
            "No missing ingredients found. Either your pantry covers the selected "
            "cocktail(s), or the selected recipe has no ingredient details."
        )
    else:
        for entries in grocery.values():
            st.write(f"**{entries[0]['ingredient']}**")

            for entry in entries:
                measure = entry.get("measure") or "measure not specified"
                cocktail = entry.get("cocktail") or "Unknown cocktail"
                st.write(f"- {measure} for {cocktail}")


def render_sidebar_debug() -> None:
    """
    Debug output must be inside main(), after init_state().
    Never place this at module scope.
    """
    with st.expander("Debug session state"):
        current_selected = st.session_state.get("selected_drinks", [])

        st.write("Selected drinks count:", len(current_selected))
        st.write(
            "Selected drink names:",
            [drink.get("strDrink") for drink in current_selected],
        )
        st.write("Pantry items:", st.session_state.get("pantry_items", []))


def main() -> None:
    init_state()
    client = get_client()

    st.title("Cocktail Recipe Finder + Pantry Matcher")
    st.caption("Recipe data and imagery: TheCocktailDB")

    if st.session_state.get("last_added"):
        st.success(f"Added {st.session_state.last_added} to your grocery list.")

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

        render_sidebar_debug()

    try:
        if mode == "Search by cocktail name":
            name = st.text_input("Cocktail name", "margarita")

            if st.button("Search", key="search_by_name_btn"):
                st.session_state.name_results = client.search_drinks_by_name(name)

            if st.session_state.get("name_results"):
                st.caption(f"{len(st.session_state.name_results)} cocktail(s) found.")

                for drink in st.session_state.name_results:
                    render_recipe_card(drink)
            else:
                st.info("Search for a cocktail to see recipe cards.")

        elif mode == "Search by ingredient/liquor":
            ingredient = st.text_input("Ingredient or liquor", "Gin")

            if st.button("Find cocktails", key="ingredient_search_btn"):
                summaries = client.filter_drinks("i", ingredient)
                st.session_state.ingredient_results = hydrate_filter_results(
                    client,
                    summaries,
                )

            if st.session_state.get("ingredient_results"):
                st.caption(f"{len(st.session_state.ingredient_results)} cocktail(s) found.")

                for drink in st.session_state.ingredient_results:
                    render_recipe_card(drink)
            else:
                st.info("Search by ingredient or liquor to see recipe cards.")

        elif mode == "Pantry matcher":
            pantry_text = st.text_area(
                "Ingredients you have, comma-separated",
                "gin, lemon juice",
            )

            main_ingredient = st.text_input("Main ingredient/liquor", "Gin")

            if st.button("Match pantry", key="pantry_match_btn"):
                pantry_items = [item.strip() for item in pantry_text.split(",") if item.strip()]

                st.session_state.pantry_items = pantry_items
                st.session_state.pantry_results = find_by_pantry(
                    client,
                    main_ingredient,
                    pantry_items,
                )

            if st.session_state.get("pantry_results"):
                for row in st.session_state.pantry_results:
                    st.info(
                        f"Missing {row['missing_count']} ingredient(s); "
                        f"available {row['available_count']}."
                    )
                    render_recipe_card(row["drink"])
            else:
                st.info("Enter pantry ingredients and click **Match pantry**.")

        elif mode == "Ingredient metadata":
            ingredient = st.text_input("Ingredient name", "vodka")

            if st.button("Lookup ingredient", key="ingredient_metadata_btn"):
                results = client.search_ingredient_by_name(ingredient)

                if results:
                    st.json(results)
                else:
                    st.warning("No ingredient metadata found.")

        elif mode == "Filters":
            filter_options = {
                "Ingredient": "i",
                "Category": "c",
                "Glass": "g",
                "Alcoholic": "a",
            }

            filter_label = st.selectbox(
                "Filter type",
                list(filter_options.keys()),
            )

            filter_type = filter_options[filter_label]
            values = cached_list_values(filter_type)

            if values:
                value = st.selectbox("Filter value", values)

                if st.button("Apply filter", key="apply_filter_btn"):
                    summaries = client.filter_drinks(filter_type, value)
                    st.session_state.filter_results = hydrate_filter_results(
                        client,
                        summaries,
                    )

                if st.session_state.get("filter_results"):
                    for drink in st.session_state.filter_results:
                        render_recipe_card(drink)
                else:
                    st.info("Choose a filter and click **Apply filter**.")
            else:
                st.warning("No values found for this filter.")

        elif mode == "Random cocktail":
            if st.button("Surprise me", key="random_btn"):
                st.session_state.random_result = client.random_drink()

            if st.session_state.get("random_result"):
                render_recipe_card(st.session_state.random_result)
            else:
                st.info("Click **Surprise me** to load a random cocktail.")

        elif mode == "Grocery list":
            render_grocery_list_page()

    except CocktailDBError as exc:
        st.error(str(exc))


if __name__ == "__main__":
    main()
