import re
import requests
import numpy as np
import pandas as pd
import json
import functools
import sqlalchemy

from typing import Iterable

import scraping.credentials as C
import scraping.definitions as D

"""
This file holds any main and accessory functions
"""

#################################################
#                                               #
#                SCRAPING TOOLS                 #
#                                               #
#################################################


def login() -> requests.sessions.Session:
    """
    Connects to the main site and retrieves the pageToken,
    necessary to login into the test result pages.
    The payload is then posted using requests.

    The variable window\\.__pageToken is the JS variables that holds
    the pageToken and that are used in the regex search.

    Args:

    Returns:
        s (requests.sessions.Session): requests session that does the
        cookie and token automated management.
    """

    # Using a requests session to keep the connection alive; it also
    # does the cookies management (post to payload, etc.) automatically

    with requests.sessions.Session() as session:
        # Connect to the main site
        main_site = session.get(D.Paths.URL + D.Paths.LOGIN_PAGE).text

        # Retrieve necessary token - regex explanation:
        # search for all occurrences that match pattern within re.search
        # (.*?) will match any content. It is still unclear how "?" helps
        search = re.search(r'window\.__pageToken = "(.*?)";', main_site)
        assert search is not None
        pageToken = search.group(1)

        login_payload = {
            'username': C.Payload.username,
            'password': C.Payload.password,
            'pageToken': pageToken
        }

        # Post payload to login, retrieve status code
        session.post(
            D.Paths.URL + D.Paths.BACKEND_LOGIN_PAGE, data=login_payload
        )

        # returns the requests.session object unless in debug mode,
        # where it returns the session's status code
        return session


def retrieve_and_union_results(assessments: Iterable[str], session: requests.sessions.Session) -> pd.DataFrame:
    """
    Once logged in, the student information and the results of a
    list of tests/challenges must be retrieved and stored into a list
    of dataframes (one per each assessment).

    These dataframes are then concatenated and returned.
    The variable window\\.__org_candidates is the JS variable that
    holds the assessment results, and that is used in the regex search.

    Args:
        assessments (list[str]): list with the URLs pointing to each
        assessment for with a set of results must be retrieved

        session (request.session): requests session containing does
        the cookie management and keeps the connection alive

    Returns:
        results_union (pd.DataFrame): union of multiple dataframes,
        each contained the students' information and results.
    """
    # Fetch assessments results
    results_list = []
    for assessment in assessments:
        response = session.get(D.Paths.URL + assessment).text
        search = re.search(r"window\.__org_candidates = (.*?);", response)
        assert search is not None
        results = search.group(1)
        results = json.loads(results)
        results = pd.json_normalize(results)

        # add url to coding report
        as_id = ':' + assessment.split(':')[1]
        results['report_url'] = D.Paths.URL + D.Paths.REPORT + results['username'] + as_id

        results_list.append(results)

    # Union the results of all assessments
    results_union = functools.reduce(
        lambda top, bottom: pd.concat([top, bottom]), results_list
    )

    return results_union


def pre_process_results(dataframe: pd.DataFrame, col_types: dict[str, str]) -> pd.DataFrame:
    """
    The resulting dataframe needs to be pre-processed to be inserted into a database.
    The different columns types are passed as a list, and the dataframe is
    modified accordingly.
    The datetimes are correctly parsed, and the N/A values are converted
    to numpy null values.

    Args:
        dataframe (pd.DataFrame): union of multiple dataframes, one for
        each assessment with the students' information and results.

        col_types (dict[str, str]): Key-value pair of each columns name
        and correspondent dtype. Should be revised for each set of assessment.

    Returns:
        dataframe (pd.DataFrame): pre-processed dataframe ready to be inserted into
        the database.
    """

    # Correct N/A and empty [] values
    dataframe.replace(['N/A'], np.nan, regex=True, inplace=True)
    dataframe['mc_answers'] = dataframe['mc_answers'].str.strip('[]').astype(object)

    # Convert datetimes to datetime64
    dataframe['date_joined'] = pd.to_datetime(
        dataframe['date_joined'], format='%m/%d/%y'
        )
    dataframe['date_link_sent'] = pd.to_datetime(
        dataframe['date_link_sent'], format="%m/%d/%y, %I:%M%p"
        )

    # transform columns into final dtypes
    dataframe = dataframe.astype(dtype=col_types)

    return dataframe


def save_results(dataframe: pd.DataFrame, path: str) -> None:
    """
    Takes the concatenated dataframe with the results of all assessments
    and saves it into the path location

    Args:
        dataframe (pd.DataFrame): Concatenated dataframe to be saved
        path (str): local path to export the .csv file into
    """

    dataframe.to_csv(path, index=False)


#################################################
#                                               #
#             DB INTERACTION TOOLS              #
#                                               #
#################################################

class DataBaseInteraction:
    """
    Object that will hold most connection details

    Will also hold the connection itself, and will be able to save the
    dataframe into the chosen database.

    Args:
    dataframe (pd.DataFrame): Concatenated dataframe to be saved
    table_name (str): name of the table to be created/used in the database
    """

    def __init__(self) -> None:
        self.db_path: str = D.DatabaseConnection.DB_PATH
        self.host: str = D.DatabaseConnection.HOST
        self.user: str = C.Postgres.USER
        self.password: str = C.Postgres.PASS
        self.port: str = D.DatabaseConnection.PORT
        self.db_name: str = D.DatabaseConnection.DB_NAME
        self.db_engine: sqlalchemy.engine.base.Engine = None,
        self.db_type: str = D.DatabaseTypes.POSTGRES

    def save_results_to_db(
        self,
        dataframe: pd.DataFrame,
        table_name: str
        ) -> None:
        """
        Calls two auxiliary methods to connect and then convert the pandas
        dataframe to SQL

        Args:
        db_type (str): type of database to create the engine for, with
        the SQLalchemy library. Defaults to SQLite and will save a
        local .db file.
        """

        # Create a connection engine
        self.dataframe = dataframe
        self.table_name = table_name
        self.db_connect()

        # Save the dataframe into the database
        self.dataframe_to_db()

    def db_connect(self) -> None:

        """
        Connects to a database using the parameters provided and
        according to the DB type, stores the connection engine
        (sqlalchemy.engine.base.Engine) as a property.
        """

        if self.db_type == D.DatabaseTypes.SQLITE:
            self.db_engine = sqlalchemy.create_engine(f'{self.db_type}:///' + self.db_path)

        elif self.db_type == D.DatabaseTypes.POSTGRES:
            self.db_engine = sqlalchemy.create_engine(
                 '{}://{}:{}@{}:{}/{}'
                 .format(
                     self.db_type,
                     self.user,
                     self.password,
                     self.host,
                     self.port,
                     self.db_name
                     )
                 )

    def dataframe_to_db(self) -> None:
        """
        Takes the concatenated dataframe with the results of all assessments
        and saves it into a local database using the Pandas .to_sql method,
        passing in table_name and db_engine
        """

        self.dataframe.to_sql(
                    name=self.table_name,
                    con=self.db_engine,
                    if_exists='replace',
                    index=False
                    )

class GoogleSheets(DataBaseInteraction):
    
    def __init__(self) -> None:
        super().__init__()

    def read_table(self, table_name: str):
        self.db_connect()
        self.querytable = pd.read_sql(table_name, con=self.db_engine)



        