class ProjectNotFoundError(Exception):
    pass

class UserNotFoundError(Exception):

    def __init__(self, user_id):
        self.user_id = user_id


class UnknownToolError(Exception):
    """Raised when tool name passed doesn't have corresponding class instance to be created

    Attributes:
        tool_name -- tool name
    """

    def __init__(self, tool_id):
        self.tool_id = tool_id


class InvalidStateError(Exception):

    def __init__(self, invalid_state):
        self.invalid_state = invalid_state



class BackupNotFoundError(Exception):
    """Raised when backup for current user and specified tool not found in backups storage directory

    Attributes:
        user_id -- user ID
        tool_name -- tool name
    """

    def __init__(self, user_id, tool_id, project_id):
        self.user_id = user_id
        self.tool_name = tool_id
        self.project_id = project_id

class WrongToolError(Exception):

    def __init__(self, user_id, requested_tool_id, loaded_tool_id):
        self.user_id = user_id
        self.requested_tool_id = requested_tool_id
        self.loaded_tool_id = loaded_tool_id

class NotExistingFileError(Exception):
    '''Raised when file for the specified path is not found.

    Attributes:
        file_path -- path to the file
    '''

    def __init__(self, file_path):
        self.file_path = file_path

class InvalidRequestParametersError(Exception):
    pass


class VariableNotFoundError(Exception):
    """
    Raised when specific varibale not found or not exist
    """
    pass

class ScalarNotFoundError(Exception):
    """
    Raised when specific scalar not found or not exist
    """
    pass

class PeriodSeiresNotFoundError(Exception):
    """
    Raised when specific period series not found or not exist
    """
    pass


class VariableAlreadyExistdError(Exception):
    """
    Raised when specific variable already exist
    """
    pass


class SlotNotFoundError(Exception):
    """
    Raised when specific slot not found
    """
    pass


class UnknowSlotTypeError(Exception):
    """
    Raised when type of slot does't exist
    """
    pass

class CorruptedBackupError(Exception):
    """
    Raised when structure of backup is corrupted
    """
    pass


class NameDublicateError(Exception):
    """
    Raised when name of node already exist
    """
    pass


class MultiParentError(Exception):
    """
    Raised when node has more than one parent
    """
    pass


class WrongCargsPeriodError(Exception):
    """
    Raised when carg's period has wrong time ordering
    """
    pass

class TimeSeriesNotFoundError(Exception):
    """
    Raised when timeseries not found
    """
    pass

class PeriodOutOfRangeError(Exception):
    """
    Raised when periodseries is out of range
    """
    pass

class TimeSeriesOutOfRangeError(Exception):
    """
    Raised when periodseries is out of range
    """
    pass

class EntityNotFound(Exception):
    """
    Raised when specifc entity not found
    """
    pass

class UnknowMetaFilterError(Exception):
    """
    Raised when specifc meta filted does't exist
    """
    pass



