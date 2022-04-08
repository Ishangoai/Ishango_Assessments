'''
This script logs into the coderbyte website, scrapes coding results, and saves them to a .csv file.
Because the coderbyte API costs $200/month, this script can save Ishango costs.
'''

import requests
import re
import json
import pandas as pd

URL = 'https://coderbyte.com/'
LOGIN_ROUTE = 'sl'
REQUEST_URL = 'backend/requests/sl/login.php'
RESULTS_PATH = 'dashboard/ishangoai-nx1aa:data-science-as-ypd9gqutaz'

with requests.session() as s:
        
    initial_soup = s.get(URL + LOGIN_ROUTE).text

    # regex explanation: 
    # search for all occurances that match pattern within re.search
    # (.*?) will match any content. It is still unclear how "?" helps
    pageToken = re.search(r'window\.__pageToken = "(.*?)";', initial_soup).group(1)

    login_payload = {
        'username': 'oliver@ishango.ai',
        'password': 'oliver0424',
        'pageToken': pageToken
    }

    login_req = s.post(URL + REQUEST_URL,
                        data=login_payload
                        )

    page = s.get(URL + RESULTS_PATH).text


# fetch the display name
assessment_details = re.search(r"window\.__org_assessmentDetails = (.*?);", page).group(1)
display_name = json.loads(assessment_details)['display_name']
display_name = display_name.replace(' ', '_').lower()

# fetch coding results
data = re.search(r"window\.__org_candidates = (.*?);", page).group(1)
data  = json.loads(data)
df = pd.json_normalize(data)
df.to_csv(display_name + '.csv', index=False)

