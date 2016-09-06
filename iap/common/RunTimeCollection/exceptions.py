class InstanceAlreadyExistsError(Exception):
    """Raised when instance for current user is already in the RunTimeCollection.

    Attributes:
        user_id -- user ID
    """

    def __init__(self, user_id):
        self.user_id = user_id


class BackupNotFound(Exception):
    """Raised when backup for current user and specified tool not found in backups storage directory

    Attributes:
        user_id -- user ID
        tool_name -- tool name
    """

    def __init__(self, user_id, tool_name):
        self.user_id = user_id
        self.tool_name = tool_name


class InstanceCanNotBeCreated(Exception):
    """Raised when tool name passed doesn't have corresponding class instance to be created

    Attributes:
        tool_name -- tool name
    """

    def __init__(self, tool_name):
        self.tool_name = tool_name
