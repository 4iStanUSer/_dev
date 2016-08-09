class NotExistingFileError(Exception):
    '''Raised when file for the specified path is not found.

    Attributes:
        file_path -- path to the file
    '''

    def __init__(self, file_path):
        self.file_path = file_path
