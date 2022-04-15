import re
import requests
import pandas as pd
import json
import functools

from typing import List

import credentials as C
import definitions as D

"""
This file holds any main and accessory functions
"""

def login() -> requests.session:
    """
    Connects to the main site and retrieves the pageToken,
    necessary to login into the test result pages.
    The payload is then posted using requests.

    The variable window\.__pageToken is the JS variables that holds
    the pageToken and that are used in the regex search.

    Returns:
        s (requests.session): requests session that does the
        cookie and token automated management.
    """

    # Using a requests session to keep the connection alive; it also
    # does the cookies management (post to payload, etc.) automatically

    with requests.session() as session:
        
        # Connect to the main site
        main_site = session.get(D.Paths.URL + D.Paths.LOGIN_PAGE).text

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
        session.post(D.Paths.URL + D.Paths.BACKEND_LOGIN_PAGE,
                data=login_payload
                )

        return session

def retrive_and_model_results(assessments: List[str], session: requests.session) -> pd.DataFrame:
    """
    Once logged in, the student information and the results of a
    list of tests/challenges must be retrieved and stored into a list
    of dataframes (one per each assessment).

    These dataframes are then concatenated and returned.

    The variable window\.__org_candidates is the JS variable that
    holds the assessment results, and that is used in the regex search.

    Args:
        assessments (List[str]): list with the URLs pointing to each
        assessment for with a set of results must be retrieved

        session (request.session): requests session containing does
        the cookie management and keeps the connection alive

    Returns:
        results_union (pd.DataFrame): union of multiple dataframes,
        each contained the students' information and results.
    """
    
    # Fetch assessments results
    results_list = []
    for page in assessments:
        response = session.get(D.Paths.URL + page).text
        results = re.search(r"window\.__org_candidates = (.*?);", response).group(1)
        results = json.loads(results)
        results = pd.json_normalize(results)
        results_list.append(results)

    # Union the results of all assessments
    results_union = functools.reduce(lambda top,bottom: pd.concat([top,bottom]),
                                results_list)
    
    return results_union

def save_results(dataframe: pd.DataFrame, path: str) -> None:
    """
    Takes the concatenated dataframe with the results of all assessments
    and saves it into the path location

    Args:
        dataframe (pd.DataFrame): Concatenated dataframe to be saved
        path (str): local path to export the .csv file into
    """

    dataframe.to_csv(path, index=False)

