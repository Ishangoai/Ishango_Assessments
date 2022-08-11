import base64
import re
import requests
import numpy as np
import pandas as pd
import json
import functools
import sqlalchemy
import googleapiclient.discovery
import google.oauth2.service_account
from typing import Iterable, Any

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
        pagetoken = search.group(1)

        login_payload = {
            "username": D.Payload.username,
            "password": D.Payload.password,
            "pageToken": pagetoken,
        }

        # Post payload to login, retrieve status code
        session.post(D.Paths.URL + D.Paths.BACKEND_LOGIN_PAGE, data=login_payload)

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
        as_id = ":" + assessment.split(":")[1]
        results["report_url"] = D.Paths.URL + D.Paths.REPORT + results["username"] + as_id

        results_list.append(results)

    # Union the results of all assessments
    results_union = functools.reduce(lambda top, bottom: pd.concat([top, bottom]), results_list)

    return results_union


def pre_process_results(dataframe: pd.DataFrame) -> pd.DataFrame:
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
    dataframe.replace(["N/A"], np.nan, regex=True, inplace=True)
    
    #dataframe["mc_answers"] = dataframe["mc_answers"].str.strip("[]").astype(object)

    # automatically convert datetimes to datetime64. https://stackoverflow.com/a/41230801/5392289
    dataframe = dataframe.apply(lambda col: pd.to_datetime(col, errors='ignore') if col.dtypes == object else col, axis=0)

    # transform columns into final dtypes
    # dataframe = dataframe.astype(dtype=col_types)

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

    def __init__(self, table_name: str, dataframe: pd.DataFrame = None) -> None:
        self.__db_path: str = D.DatabaseConnection.DB_PATH
        self.__host: str = D.DatabaseConnection.HOST
        self.__user: str = D.DatabaseConnection.USER
        self.__password: str = D.DatabaseConnection.PASS
        self.__port: str = D.DatabaseConnection.PORT
        self.__db_name: str = D.DatabaseConnection.DB_NAME
        self.__db_type: str = D.DatabaseTypes.POSTGRES
        self._table_name: str = table_name
        self.__dataframe: pd.DataFrame = dataframe
        self._db_engine: sqlalchemy.engine.base.Engine = None

    def save_results_to_db(self) -> None:
        """
        Calls two auxiliary methods to connect and then convert the pandas
        dataframe to SQL

        Args:
        db_type (str): type of database to create the engine for, with
        the SQLalchemy library. Defaults to SQLite and will save a
        local .db file.
        """

        # Create a connection engine
        self._db_connect()

        # Save the dataframe into the database
        self.__dataframe_to_db()

    def _db_connect(self) -> None:

        """
        Connects to a database using the parameters provided and
        according to the DB type, stores the connection engine
        (sqlalchemy.engine.base.Engine) as a property.
        """

        if self.__db_type == D.DatabaseTypes.SQLITE:
            self._db_engine = sqlalchemy.create_engine(f"{self.__db_type}:///" + self.__db_path)

        elif self.__db_type == D.DatabaseTypes.POSTGRES:
            self._db_engine = sqlalchemy.create_engine(
                "{}://{}:{}@{}:{}/{}".format(
                    self.__db_type,
                    self.__user,
                    self.__password,
                    self.__host,
                    self.__port,
                    self.__db_name,
                )
            )

    def __dataframe_to_db(self) -> None:
        """
        Takes the concatenated dataframe with the results of all assessments
        and saves it into a local database using the Pandas .to_sql method,
        passing in table_name and db_engine
        """

        self.__dataframe.to_sql(name=self._table_name, con=self._db_engine, if_exists="replace", index=False)


class GoogleSheets(DataBaseInteraction):
    """
    Object reads from SQL (using inherited method db_connect);
    processes data in a format compatible with Google Sheets;
    and writes to Google Sheets.
    """

    @staticmethod
    def __base64_to_json(b64: str) -> dict[str, str]:
        """
        Decodes base64 string into JSON credentials dictionary

        Args:
        b64 (str]: base64 encoded string of credentials
        originally in JSON format. encoding is done in
        order to be able to store in Github Secrets (JSON does
        not pass as an environment variable in Github Actions).

        Returns:
        dictionary of credentials in JSON format
        """
        trim_string = slice(1, -1)
        decodedbytes: bytes = base64.b64decode(b64[trim_string])
        decodedstr: str = decodedbytes.decode("ascii")
        json_dict: dict[str, str] = json.loads(decodedstr)
        return json_dict

    def __read_from_sql(self) -> None:
        """
        reads table from SQL and stores as dataframe in object state
        """
        super()._db_connect()
        self.__coderbyte_df: pd.DataFrame = pd.read_sql(self._table_name, con=self._db_engine)

    def __process_data(self):
        """
        convert non-string values (datetime64[ns], np.NaN) into
        string format inorder to be compatible with Google Sheets

        """
        self.__coderbyte_df["date_joined"] = self.__coderbyte_df["date_joined"].dt.strftime("%Y-%m-%d")
        self.__coderbyte_df["date_link_sent"] = self.__coderbyte_df["date_link_sent"].dt.strftime("%Y-%m-%d")
        self.__coderbyte_df.replace(np.nan, "N/A", inplace=True)

        # convert dataframe into list of lists, with first list being column names
        self.__coderbyte_list: list[list[Any]] = self.__coderbyte_df.to_numpy().tolist()
        column_names: list[str] = self.__coderbyte_df.columns.tolist()
        self.__coderbyte_list.insert(0, column_names)

    def sqltosheets(self) -> dict[str, Any]:
        """
        public method to read, process, and write to Google Sheets.
        """
        self.__read_from_sql()
        self.__process_data()

        SCOPES: list[str] = ["https://www.googleapis.com/auth/spreadsheets"]
        json_dict: dict[str, str] = self.__base64_to_json(D.GoogleSheets.B64_CREDS)

        # create service account credentials object
        creds = google.oauth2.service_account.Credentials.from_service_account_info(json_dict, scopes=SCOPES)

        # Construct a Resource for interacting with an API
        service = googleapiclient.discovery.build("sheets", "v4", credentials=creds)

        # instantiate class to interact with a resource
        sheet = service.spreadsheets()

        # write to google sheets
        update_instructions = sheet.values().update(
            spreadsheetId=D.GoogleSheets.SPREADSHEET_ID.value,
            range=D.GoogleSheets.RANGE.value,
            valueInputOption="USER_ENTERED",
            body={"values": self.__coderbyte_list},
        )
        result: dict[str, Any] = update_instructions.execute()

        return result
