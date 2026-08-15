# Starter Repository for Software Development Exercise

Student instructions (feel free to remove this section later, as desired):

> FYI - there are some important things missing from this repo. Follow along in class to implement testing and continuous integration, and secure environment variables using a ".env" and ".gitignore" file, etc. We may also extend the functionality to build a web interface. For full solutions, see https://github.com/s2t2/my-first-repo-fall-2025 (including that repository's [commit history](https://github.com/s2t2/my-first-repo-fall-2025/commits/main/) for step-by-step walkthrough).
>
> FYI - students please use a "premium" AlphaVantage API Key shared by the prof (see "Configuration" section below).


Students: first visit https://github.com/prof-rossetti/software-dev-exercise and click "Use this template" green button to make a copy of the repo under your own control.


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
