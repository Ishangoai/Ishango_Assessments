import os
import enum

# The class below will hold the credentials information
# These should be requested to the Team Lead (Oliver) and
# stored locally as environmental variables


class Payload(str, enum.Enum):
    """
    Placeholder for the login credentials
    """

    username = os.getenv('ISHANGO_USER')
    password = os.getenv('ISHANGO_PASS')
