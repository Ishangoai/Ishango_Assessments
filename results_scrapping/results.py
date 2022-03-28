import requests
from bs4 import BeautifulSoup as bs

URL = 'https://coderbyte.com/'
LOGIN_ROUTE = 'sl'
REQUEST_URL = 'backend/requests/sl/login.php'

RESULTS_PATH = 'dashboard/ishangoai-nx1aa'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
            'origin': 'https://coderbyte.com',
            'referer': 'https://coderbyte.com/sl'}

s = requests.session()
initial_soup = s.get(URL + REQUEST_URL).content
print(initial_soup)


csrf_token = {'CoderbyteSessionKey': 'nFWZPgGKivrJnifqBPy8'}

login_payload = {
    'username': 'oliver@ishango.ai',
    'password': 'oliver0424'
}

login_req = s.post(URL + REQUEST_URL,
                    headers=HEADERS,
                    data=login_payload
                    )

print(login_req.content)

middle_soup = login_req.headers
#print(middle_soup)
cookies = login_req.cookies

soup = bs(s.get(URL + RESULTS_PATH).text, 'html.parser')

