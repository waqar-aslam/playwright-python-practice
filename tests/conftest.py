import json

import pytest
from playwright.sync_api import Playwright

from Utils.APIUtils import APIUtils

@pytest.fixture(scope="session")
def api_utils(playwright: Playwright):
    """Fixture to provide APIUtils instance with playwright"""
    return APIUtils(playwright)

#@pytest.fixture
#def user_credentials(request):
#        return user_credentials
        #return credentials