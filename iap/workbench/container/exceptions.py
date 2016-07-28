''' Module contains container custom exceptions'''

class VarNotFoundError(Exception):
    '''Raised when variable name is not found.
    Attributes:
        var_name -- name of requested variable
    '''
    def __init__(self, var_name):
        self.var_name = var_name

class OutOfRangeError(Exception):
    '''Raised when requested index is out of range.
    Attributes:
        time_index -- time point index 
        var_name -- name of requested variable
    '''
    def __init__(self, time_index, var_name):
        self.time_index = time_index
        self.var_name = var_name

class WrongLenghtError(Exception):
    '''Raised when lenght of input vector and data point are not equal.
    Attributes:
        var_name -- name of requested variable
        data_len -- lenght of data vector of point
        inp_len -- lenght of input vector
    '''
    def __init__(self, time_index, var_name):
        self.var_name = var_name
        self.data_len = data_len
        self.inp_len = inp_len

class AlreadyExistsError(Exception):
    '''Raised when variable added alredy exists.
    Attributes:
        var_name -- name of variable
    '''
    def __init__(self, time_index, var_name):
        self.var_name = var_name

class DataTypeNotFoundError(Exception):
    '''Raised when wrong data type is requested.
    Attributes:
        data_type -- not founded data type
    '''
    def __init__(self, data_type):
        self.vdata_type = data_type