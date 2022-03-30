import requests
from bs4 import BeautifulSoup as bs

URL = 'https://coderbyte.com/'
LOGIN_ROUTE = 'sl'
REQUEST_URL = 'backend/requests/sl/login.php'

RESULTS_PATH = 'dashboard/ishangoai-nx1aa'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
            'origin': 'https://coderbyte.com',
            'referer': 'https://coderbyte.com/sl'}

with requests.session() as s:
        
    initial_soup = s.get(URL + LOGIN_ROUTE).content
    pageToken = str(initial_soup,'utf-8').split(r'window.__pageToken = "')[1].split(r'";')[0]

    #soup = bs(initial_soup.text, 'html.parser')
    #script = soup.find_all('script')

    login_payload = {
        'username': 'oliver@ishango.ai',
        'password': 'oliver0424',
        'pageToken': pageToken
    }

    login_req = s.post(URL + REQUEST_URL,
                        data=login_payload
                        )

    print(login_req.content)

    middle_soup = login_req.headers
    #print(middle_soup)
    cookies = login_req.cookies
    print(cookies)

    soup = bs(s.get(URL + RESULTS_PATH).text, 'html.parser')

    #print(soup)
