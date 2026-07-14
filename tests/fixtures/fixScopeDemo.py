# import pytest
#
# @pytest.fixture(scope="function")
# def browser_name():
#     print("Fixture-Setup")
#     return "Pass"
#     #print("Fixture-teardown")
#
# @pytest.mark.smoke
# def test_one(browser_name):
#     print(f"test_one")
#     assert browser_name == "Pass"
#
# @pytest.mark.skip
# def test_two(browser_name):
#     print(f"test_two")
#     print(browser_name)
#     assert browser_name == "Pass"
#
# @pytest.mark.smoke
# def test_three(browser_name):
#     print(f"test_three")
#     print(browser_name)
#     assert browser_name == "Pass"