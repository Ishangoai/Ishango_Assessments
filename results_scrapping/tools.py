import re
import requests
import pandas as pd
import json
import functools

from typing import List

import credentials as C
import definitions as D

"""
This file holds any accessory functions
"""

def return_results(assessments: List[str]) -> List[pd.DataFrame]:
    """
    Connects to the main site and retrieves the pageToken,
    necessary to login into the test result pages.
    The payload is then posted using requests

    Once logged in, the student information and the results of a
    list of tests/challenges are retrieved and store into a list
    of dataframes (one per each assessment)

    Args:
        assessments (List[str]): list with the URLs pointing to each
        assessment for with a set of results must be retrieved

    Returns:
        assessments_results (List[pd.DataFrame]): list with multiple
        dataframes, each containing the students' information and
        results on the assessment
    """

    # Using a requests session to keep the connection alive; it also
    # does the cookies management (post to payload, etc.) automatically

    with requests.session() as s:
        
        # Connect to the main site
        main_site = s.get(D.Paths.URL + D.Paths.LOGIN_PAGE).text

        # Retrieve necessary token - regex explanation: 
        # search for all occurrences that match pattern within re.search
        # (.*?) will match any content. It is still unclear how "?" helps
        pageToken = re.search(r'window\.__pageToken = "(.*?)";', main_site).group(1)

        login_payload = {
            'username': C.Payload.username,
            'password': C.Payload.password,
            'pageToken': pageToken
        }

        # Post payload to login
        s.post(D.Paths.URL + D.Paths.BACKEND_LOGIN_PAGE,
                data=login_payload
                )

        # Fetch assessments results
        results_list = []
        for page in assessments:
            response = s.get(D.Paths.URL + page).text
            results = re.search(r"window\.__org_candidates = (.*?);", response).group(1)
            results  = json.loads(results)
            results = pd.json_normalize(results)
            results_list.append(results)

        # Union the results of all assessments
        results_union = functools.reduce(lambda top,bottom: pd.concat([top,bottom]),
                                    results_list)
        
        return results_union

