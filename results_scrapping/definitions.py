import enum
from typing import List

# Constants and strings should be stored in this file

class Paths(str, enum.Enum):
    """
    Placeholder for the web links/paths to be accessed,
    filenames and the path to read/store any files
    """

    URL = 'https://coderbyte.com/'
    LOGIN_PAGE = 'sl'
    BACKEND_LOGIN_PAGE = 'backend/requests/sl/login.php'

    final_destination = ''

    export_file = 'df_final.csv'


class Assessments(List, enum.Enum):
    """
    Placeholder for the assessment links
    """

    ASSESSMENT_PAGES = [
    'dashboard/ishangoai-nx1aa:data-science-as-ypd9gqutaz',
    'dashboard/ishangoai-nx1aa:data-science-as-zddhq9gim6',
    'dashboard/ishangoai-nx1aa:data-science-as-ms3m246vv3'
    ]

