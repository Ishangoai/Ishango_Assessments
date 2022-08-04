import os
import enum

# The class below will hold the credentials information
# These should be requested to the Team Lead (Oliver) and
# stored locally as environmental variables

"""
To store the credentials, please edit your .zshenv file or
the .bash_profile file, so it can export them (copy the whole
3 lines below and paste them in the file):

# Adding the coderbyte Ishango credentials as local env var
export ISHANGO_USER=<username>
export ISHANGO_PASS=<password>

(Please replace the <username> and <password> with the credentials
given to you by the Team Lead, when editing your file)
"""


class Payload(str, enum.Enum):
    """
    Placeholder for the login credentials
    """

    username = os.environ['ISHANGO_USER']
    password = os.environ['ISHANGO_PASS']


class Postgres(str, enum.Enum):
    """
    Placeholder for the login credentials
    """

    USER = os.environ['POSTGRES_USER']
    PASS = os.environ['POSTGRES_PASSWORD']


class GoogleSheets(str, enum.Enum):
    B64_CREDS = os.environ['SHEETS_API_CREDENTIALS_B64']
    SPREADSHEET_ID = "12kzUd8wHKWDomBz0M2ng-6zQ_t46UblKiSnMebD5su4"
    RANGE = "test!A1"
