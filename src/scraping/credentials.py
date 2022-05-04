import enum

# The class below will hold the credentials information
# The filename will be added to git and distributed to
# the project team members separately


class Payload(str, enum.Enum):
    """
    Placeholder for the login credentials
    """

    username = 'oliver@ishango.ai'
    password = 'oliver0424'
