import pytest


def pytest_collection_modifyitems(items):
    """Everything under tests/demos is a learning demo: mark it so CI can exclude it."""
    for item in items:
        if "demos" in item.path.parts:
            item.add_marker(pytest.mark.demo)
