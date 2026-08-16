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

## Local setup in github desktop, visual studio desktop and git bash for windows user

1. Open the folder in github desktop and vs desktop: **File > Open Folder...** and choose this project folder.
2. Navigate to the repo using the command line.
cd ~/OneDrive\ -\ Prime/Desktop/cocktail-recipe-finder (For Xiaoying specifically)

Otherwise: cd ~/you file path for the repository on your local machine
3. Create a virtual environment:

conda create -n cocktail-recipe-finder python=3.11
4. Activate the virtual environment:

conda activate cocktail-recipe-finder
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m pip install --upgrade pip
   python -m pip install -r requirements-dev.txt
   ```
5. Copy `.env.example` to `.env` if you want local environment variables:
   ```bash
   cp .env.example .env
   ```

## Quick Troubleshoot on Streamlit
1. Run the app using: python -m streamlit run app.py
2. Verify Streamlit is Installed: python -m pip show streamlit
If installed, you'll see version information.
3. If not installed, Install streamlit: pip install streamlit
or you can install with: conda install streamlit

## Configuration 
Create a local ".env" file and store your environment variable in there, copy folloiwng code:

this is the ".env" file...
THECOCKTAILDB_API_KEY=1

## Usage
 Run the app:
   ```bash
   python -m streamlit run app.py
   ```
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

## Security and Privacy
This app uses TheCocktailDB's development API key for educational use.
Do not commit .env, API keys, passwords, or private credentials.
Local environment variables can be stored in .env, based on .env.example.
This app does not store user accounts, passwords, or personal data.
Pantry ingredients entered in the app are stored only in the current Streamlit session.
