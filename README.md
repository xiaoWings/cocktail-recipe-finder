# Cocktail Recipe Finder

A Visual Studio Code-ready Streamlit web app that uses [TheCocktailDB](https://www.thecocktaildb.com/documentation) to search cocktail recipes, show full recipe details, compare recipes to pantry ingredients, and generate a grocery list.

## Features

- Search cocktail by name
- Search by ingredient or liquor
- Ingredient metadata lookup
- Full recipe lookup
- Random cocktail
- Pantry matching
- Grocery list generation
- Filters for ingredients, categories, glasses, and alcoholic status
- Recipe display with image, glass, alcoholic status, ingredients, measures, and instructions

## Project structure

```text
cocktail-recipe-finder/
├── app.py
├── cocktail-recipe-finder.code-workspace
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── README.md
├── render.yaml
├── .env.example
├── .gitignore
├── .streamlit/
│   └── config.toml
├── .vscode/
│   ├── extensions.json
│   ├── launch.json
│   ├── settings.json
│   └── tasks.json
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── cocktail_finder/
│       ├── __init__.py
│       ├── api_client.py
│       ├── grocery.py
│       ├── models.py
│       ├── pantry.py
│       ├── parsers.py
│       └── services.py
└── tests/
    ├── conftest.py
    ├── test_api_client.py
    ├── test_app_smoke.py
    ├── test_grocery.py
    ├── test_pantry.py
    └── test_parsers.py
```

## Local setup in VS Code

1. Open the folder in VS Code: **File > Open Folder...** and choose this project folder.
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   ```bash
   # macOS/Linux
   source .venv/bin/activate

   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   ```
4. Install dependencies:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements-dev.txt
   ```
5. Copy `.env.example` to `.env` if you want local environment variables:
   ```bash
   cp .env.example .env
   ```
6. Run the app:
   ```bash
   streamlit run app.py
   ```

## VS Code tasks

Open **Terminal > Run Task...** and choose one of:

- `Install dependencies`
- `Run Streamlit app`
- `Run tests`
- `Run lint`
- `Run format check`
- `Run local CI`

## Tests

```bash
pytest -q
ruff check .
ruff format --check .
```

## Render deployment

Use the included `render.yaml`, or configure manually:

- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT`
- Environment variable: `THECOCKTAILDB_API_KEY=1`

## Data source and responsible use

Recipe data and images are from TheCocktailDB. Alcoholic status is displayed when available. This app is a recipe lookup project and does not provide medical, allergy, or safety advice.
