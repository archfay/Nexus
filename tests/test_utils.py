import pytest
from nexus import utils


def test_escape_html():
    assert utils.escape_html("<test>") == "&lt;test&gt;"
    assert utils.escape_html("normal") == "normal"


def test_get_args_raw():
    class MockMessage:
        text = ".cmd arg1 arg2"
    
    # Basic test structure
    assert True  # Placeholder
