class EmptyInputsError(Exception):
    '''Raised when input object is none.
    
    Attributes:
        key -- name of empty object
    '''
    def __init__(self, key):
        self.key = key

class AlreadyExistsError(Exception):
    '''Raised when user tries to add new object, 
    but such object already exists.

    Attributes:
        par_name -- name of dublicated parameter
        par_value -- duplicated value 
    '''
    def __init__(self, class_name, par_name, par_value):
        self.class_name = class_name
        self.par_name = par_name
        self.par_value = par_value

class NotExistsError(Exception):
    '''Raised when object not exists
 
    Attributes:
        name -- object name
        property -- field that object was searched on
        property_val -- field value
    '''
    def __init__(self, name, property, property_val):
        self.name = name
        self.property = property
        self.property_val = property_val

class WrongArgsError(Exception):
    '''Raised when input object is none.
    
    Attributes:
        func_name -- name of the method which has wrong args 
    '''
    def __init__(self, func_name):
        self.func_name = func_name

class NoCnahgesError(Exception):
    '''Raised when input object is none.
    
    Attributes:
        class_name -- object class name
        func_name -- method name
    '''
    def __init__(self, class_name, func_name):
        self.class_name = class_name
        self.func_name = func_name