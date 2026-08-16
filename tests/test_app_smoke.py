from pathlib import Path

import pytest

streamlit_testing = pytest.importorskip("streamlit.testing.v1")
AppTest = streamlit_testing.AppTest


def test_app_loads_without_initial_network_call():
    # Get the absolute path to app.py in the project root
    test_dir = Path(__file__).parent
    app_path = (test_dir.parent / "app.py").resolve()

    at = AppTest.from_file(app_path).run(timeout=10)
    assert not at.exception
