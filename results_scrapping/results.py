'''
This script logs into the coderbyte website, scrapes coding results, and saves them to a .csv file.
Because the coderbyte API costs $200/month, this script can save Ishango costs.
'''

import requests
import re
import json
import pandas as pd
import functools

URL = 'https://coderbyte.com/'
LOGIN_PAGE = 'sl'
BACKEND_LOGIN_PAGE = 'backend/requests/sl/login.php'
ASSESSMENT_PAGES = [
    'dashboard/ishangoai-nx1aa:data-science-as-ypd9gqutaz',
    'dashboard/ishangoai-nx1aa:data-science-as-zddhq9gim6',
    'dashboard/ishangoai-nx1aa:data-science-as-ms3m246vv3'
]

with requests.session() as s:
        
    initial_soup = s.get(URL + LOGIN_PAGE).text

    # regex explanation: 
    # search for all occurances that match pattern within re.search
    # (.*?) will match any content. It is still unclear how "?" helps
    pageToken = re.search(r'window\.__pageToken = "(.*?)";', initial_soup).group(1)

    login_payload = {
        'username': 'oliver@ishango.ai',
        'password': 'oliver0424',
        'pageToken': pageToken
    }

    login_req = s.post(URL + BACKEND_LOGIN_PAGE,
                        data=login_payload
                        )

    # fetch coding results
    dfs = []
    for page in ASSESSMENT_PAGES:
        response = s.get(URL + page).text
        results = re.search(r"window\.__org_candidates = (.*?);", response).group(1)
        results  = json.loads(results)
        df = pd.json_normalize(results)
        dfs.append(df)

df_final = functools.reduce(lambda top,bottom: pd.concat([top,bottom]), dfs)
df_final.to_csv('df_final.csv', index=False)

