## Setup


Clone the repo to download it from GitHub. Perhaps onto the Desktop.

Navigate to the repo using the command line.

```sh
cd ~/Desktop/software-dev-exercise
```

Create a virtual environment:

```sh
conda create -n software-dev-env python=3.11
```

Activate the virtual environment:

```sh
conda activate software-dev-env
```

Install package dependencies:

```sh
pip install -r requirements.txt
```

## Configuration

The stocks functionality requires an AlphaVantage API key. Obtain a premium AlphaVantage API Key (using the [form](https://www.alphavantage.co/support/#api-key) or shared by the prof).

Create a local ".env" file and store your environment variable in there:

```sh
# this is the ".env" file...

ALPHAVANTAGE_API_KEY="______________"

# also tell flask where our web app is defined:
FLASK_APP=web_app
```

## Usage

Run RPS game:

```sh
python -m app.rps
```

Run stocks dashboard:

```sh
python -m app.stocks
```

## Testing

Run tests:

```sh
pytest
```
