import pytest
import requests
import results_scrapping.definitions as D


def test_tools_login():
    # Testing the login process
    # Successful requests have status code between 200 and 299
    s = requests.session()
    status_code = s.get(D.Paths.URL + D.Paths.LOGIN_PAGE).status_code

    assert 199 < status_code < 300, "Connection not established"
