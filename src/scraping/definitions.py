import os
import enum
from typing import Dict, List

# Constants and strings should be stored in this file


class Paths(str, enum.Enum):
    """
    Placeholder for the web links/paths to be accessed,
    filenames and the path to read/store any files
    """

    URL = 'https://coderbyte.com/'
    LOGIN_PAGE = 'sl'
    BACKEND_LOGIN_PAGE = 'backend/requests/sl/login.php'
    REPORT = 'report/'

    # path where the file will be saved (if other than the
    # current folder)
    destination_folder = ''

    # Individual programs filename and paths
    ghana_2022_export_file = '2022_ghana_assessment_results.csv'
    ghana_2022_export_path = ''.join([destination_folder, ghana_2022_export_file])


class Assessments(List, enum.Enum):
    """
    Placeholder for the assessment links
    """

    ghana_2022_assessments = [
        'dashboard/ishangoai-nx1aa:data-science-as-ypd9gqutaz',
        'dashboard/ishangoai-nx1aa:data-science-as-zddhq9gim6',
        'dashboard/ishangoai-nx1aa:data-science-as-ms3m246vv3'
    ]


class PandasSchemas(Dict, enum.Enum):
    """
    Placeholder for the Pandas dataframe schemas
    """

    ghana_2022_schema = {
        'username':                 'object',
        'email':                    'object',
        'name':                     'object',
        'challenges_completed':     'Int64',
        'mc_score':                 'Int64',
        'code_score':               'Int64',
        'final_score':              'Int64',
        'mc_answers':               'object',
        'total_points':             'Int64',
        'final_grade':              'object',
        'time_taken':               'Int64',
        'cheated':                  'object',
        'status':                   'object',
        'action':                   'object',
        'compensation':             'object',
        'video_response_uploaded':  'bool',
        'date_joined':              'datetime64[ns]',
        'date_link_sent':           'datetime64[ns]',
        'report_url':               'object',
    }


class DatabaseConnection(str, enum.Enum):
    """
    Placeholder for the database connection details
    """

    # SQLite Database connection
    DB_PATH = 'general_docs/Ishango_Coderbyte_DB.db'

    # Docker Postgres Database connection
    LOCALHOST = 'localhost'
    HOST = os.getenv('POSTGRES_HOST')
    PORT = "5432"
    DB_NAME = "ishango"


class DatabaseTypes(str, enum.Enum):
    """
    Placeholder for the possible database types
    """

    # Possible database types:
    SQLITE = 'sqlite'
    POSTGRES = 'postgresql+psycopg2'


class DatabaseTables(str, enum.Enum):
    """
    Placeholder for the database tables details
    """

    # Table(s) to be accessed/created
    TABLE_ghana_2022 = 'ghana2022'
