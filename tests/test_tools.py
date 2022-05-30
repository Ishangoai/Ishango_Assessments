import requests
import scraping.definitions as D
import scraping.credentials as C


def test_tools_login():
    # Testing the login process
    # Successful requests have status code between 200 and 299
    s = requests.session()
    status_code = s.get(D.Paths.URL + D.Paths.LOGIN_PAGE).status_code

    assert 199 < status_code < 300, "Connection not established"


def test_credentials_retrieval():
    # Check if the credentials stored as environmental variables
    # can be retrieved (specially in the github actions environment)
    login_user = C.Payload.username
    login_pass = C.Payload.password

    assert login_user is not None, "Username not found"
    assert login_pass is not None, "Password not found"
