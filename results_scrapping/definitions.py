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

    # path where the file will be saved if other than the
    # current folder
    destination_folder = ''

    export_file = '2022_ghana_assessment_results.csv'


class Assessments(List, enum.Enum):
    """
    Placeholder for the assessment links
    """

    GHANA_2022_ASSESSMENT_PAGES = [
    'dashboard/ishangoai-nx1aa:data-science-as-ypd9gqutaz',
    'dashboard/ishangoai-nx1aa:data-science-as-zddhq9gim6',
    'dashboard/ishangoai-nx1aa:data-science-as-ms3m246vv3'
    ]

