import pytest


# scope="function" runs setup/teardown around every test; try "module" and compare the -s output.
# Don't name a fixture browser_name: pytest-playwright parametrizes that name and would override it.
@pytest.fixture(scope="function")
def demo_value():
    print("Fixture-Setup")
    yield "Pass"
    print("Fixture-teardown")


def test_one(demo_value):
    assert demo_value == "Pass"


@pytest.mark.skip(reason="demonstrates a skipped test")
def test_two(demo_value):
    assert demo_value == "Pass"


def test_three(demo_value):
    assert demo_value == "Pass"
