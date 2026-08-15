import pytest

streamlit_testing = pytest.importorskip("streamlit.testing.v1")
AppTest = streamlit_testing.AppTest


def test_app_loads_without_initial_network_call():
    at = AppTest.from_file("app.py").run(timeout=10)
    assert not at.exception
