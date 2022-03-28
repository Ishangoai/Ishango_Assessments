import requests
from bs4 import BeautifulSoup as bs

URL = 'https://coderbyte.com/'
LOGIN_ROUTE = 'sl'

RESULTS_PATH = 'dashboard/ishangoai-nx1aa'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
            'origin': 'https://coderbyte.com',
            'referer': 'https://coderbyte.com/sl'}

s = requests.session()
test_cookies = s.get(URL + LOGIN_ROUTE).cookies

csrf_token = {'CoderbyteSessionKey': 'nFWZPgGKivrJnifqBPy8'}

login_payload = {
    'username': 'oliver@ishango.ai',
    'password': 'oliver0424',
    'pageToken': 'a33a31beb913663277787b546e273d9305ebd735'
}

login_req = s.post(URL + LOGIN_ROUTE,
                    headers=HEADERS,
                    data=login_payload
                    )

print(login_req)

cookies = login_req.cookies

soup = bs(s.get(URL + RESULTS_PATH).text, 'html.parser')

print(soup)
