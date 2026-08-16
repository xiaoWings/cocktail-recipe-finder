import pytest
from pathlib import Path

streamlit_testing = pytest.importorskip("streamlit.testing.v1")
AppTest = streamlit_testing.AppTest


def test_app_loads_without_initial_network_call():
    # Resolve path relative to this test file
    test_dir = Path(__file__).parent
    app_path = test_dir.parent / "app.py"
    at = AppTest.from_file(str(app_path)).run(timeout=10)
    assert not at.exception