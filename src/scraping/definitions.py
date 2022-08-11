import os
import enum

# Constants and strings should be stored in this file

"""
To store the credentials (github secrets) locally,
edit your .zshenv file or .bash_profile file,
so it can export them

# Adding the coderbyte Ishango credentials as local env var
export ISHANGO_USER=<username>
export ISHANGO_PASS=<password>

(Please replace the <username> and <password> with the credentials
given to you by the Team Lead, when editing your file)
"""


class Paths(str, enum.Enum):
    """
    Placeholder for the web links/paths to be accessed,
    filenames and the path to read/store any files
    """

    URL = "https://coderbyte.com/"
    LOGIN_PAGE = "sl"
    BACKEND_LOGIN_PAGE = "backend/requests/sl/login.php"
    REPORT = "report/"

    # path where the file will be saved (if other than the
    # current folder)
    destination_folder = ""

    # Individual programs filename and paths
    ghana_2022_export_file = "2022_ghana_assessment_results.csv"
    ghana_2022_export_path = "".join([destination_folder, ghana_2022_export_file])


class Payload(str, enum.Enum):
    """
    Placeholder for the login credentials
    """

    username = os.environ["ISHANGO_USER"]
    password = os.environ["ISHANGO_PASS"]


class Assessments(tuple[str], enum.Enum):
    """
    Placeholder for the assessment links
    """
    ghana_2022_may_assessments = (
        "dashboard/ishangoai-nx1aa:data-science-as-ypd9gqutaz",
        "dashboard/ishangoai-nx1aa:data-science-as-zddhq9gim6",
        "dashboard/ishangoai-nx1aa:data-science-as-ms3m246vv3",
    )

    ghana_2022_october_assessments = (
        "dashboard/ishangoai-nx1aa:data-science-as-4r971n98zo",
    )


class DatabaseConnection(str, enum.Enum):
    """
    Placeholder for the database connection details
    """

    # SQLite Database connection
    DB_PATH = "general_docs/Ishango_Coderbyte_DB.db"

    # Docker Postgres Database connection
    LOCALHOST = "localhost"
    HOST = os.environ["POSTGRES_HOST"]
    PORT = os.environ["POSTGRES_PORT"]
    DB_NAME = os.environ["POSTGRES_DB"]
    USER = os.environ["POSTGRES_USER"]
    PASS = os.environ["POSTGRES_PASSWORD"]


class DatabaseTypes(str, enum.Enum):
    """
    Placeholder for the possible database types
    """

    # Possible database types:
    SQLITE = "sqlite"
    POSTGRES = "postgresql"


class DatabaseTables(str, enum.Enum):
    """
    Placeholder for the database tables details
    """

    # Table(s) to be accessed/created
    TABLE_ghana_2022 = "ghana2022_october"


class GoogleSheets(str, enum.Enum):
    B64_CREDS = os.environ["SHEETS_API_CREDENTIALS_B64"]
    SPREADSHEET_ID = "1hVexzlc_1xBUZhwEfPp7fP-yNq1yWvfAWE7HrYhInLc"
    RANGE = "Coderbyte_Results!A1"
