import pytest
import requests

from cocktail_finder.api_client import CocktailDBClient, CocktailDBError


class MockResponse:
    def __init__(self, payload, should_raise=False):
        self.payload = payload
        self.should_raise = should_raise

    def raise_for_status(self):
        if self.should_raise:
            raise requests.HTTPError("boom")

    def json(self):
        return self.payload


def test_search_drinks_by_name_uses_expected_endpoint(monkeypatch):
    calls = {}

    def mock_get(url, params=None, timeout=None):
        calls["url"] = url
        calls["params"] = params
        calls["timeout"] = timeout
        return MockResponse({"drinks": [{"idDrink": "11007", "strDrink": "Margarita"}]})

    monkeypatch.setattr("requests.get", mock_get)
    client = CocktailDBClient(api_key="1")
    result = client.search_drinks_by_name("margarita")

    assert result[0]["strDrink"] == "Margarita"
    assert calls["url"].endswith("/search.php")
    assert calls["params"] == {"s": "margarita"}


def test_api_error_is_wrapped(monkeypatch):
    def mock_get(url, params=None, timeout=None):
        return MockResponse({}, should_raise=True)

    monkeypatch.setattr("requests.get", mock_get)
    client = CocktailDBClient(api_key="1")

    with pytest.raises(CocktailDBError):
        client.random_drink()


def test_list_filter_values_extracts_expected_key(monkeypatch):
    def mock_get(url, params=None, timeout=None):
        return MockResponse({"drinks": [{"strCategory": "Cocktail"}, {"strCategory": "Ordinary Drink"}]})

    monkeypatch.setattr("requests.get", mock_get)
    client = CocktailDBClient(api_key="1")
    assert client.list_filter_values("c") == ["Cocktail", "Ordinary Drink"]
