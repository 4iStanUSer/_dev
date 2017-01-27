class EmptyInputsError(Exception):
    """Custom Exception.
    Raised when input object is none.
    
    Attributes:
        key -- name of empty object
    """
    def __init__(self, key):
        self.key = key


class AlreadyExistsError(Exception):
    """Custom Exception.
    Raised when user tries to add new object,
    but such object already exists.

    Attributes:
        par_name -- name of dublicated parameter
        par_value -- duplicated value 
    """
    def __init__(self, class_name, par_name, par_value, func_name=''):
        self.class_name = class_name
        self.par_name = par_name
        self.par_value = par_value
        self.func_name = func_name


class NotExistsError(Exception):
    """Custom Exception.
    Raised when object not exists
 
    Attributes:
        name -- object name
        property -- field that object was searched on
        property_val -- field value
    """
    def __init__(self, name, property, property_val):
        self.name = name
        self.property = property
        self.property_val = property_val


class WrongArgsError(Exception):
    """Custom Exception.
    Raised when input object is none.
    
    Attributes:
        func_name -- name of the method which has wrong args 
    """
    def __init__(self, func_name):
        self.func_name = func_name


class NoCnahgesError(Exception):
    """Custom Exception.
    Raised when input object is none.
    
    Attributes:
        class_name -- object class name
        func_name -- method name
    """
    def __init__(self, class_name, func_name):
        self.class_name = class_name
        self.func_name = func_name


class WrongArgEx(Exception):
    """Custom Exception.
    It Should raise when value of argument isn't satisfied

    Attributes:
        var_name - name of argument
        var_value - value of argument
    """
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value


class CreatingError(Exception):
    """Custom Exception.
    It Should raise when db model wasn't created as expected

    Attributes:
        name - name of model
        data - values for model
    """
    def __init__(self, name, data=None):
        self.name = name
        if data is not None:
            self.data = data


class WrongValueError(Exception):
    """Custom Exception.
    Raised when value is incorrect.

    Attributes:
        value -- value that raised exception
        expected_value -- expected value
    """
    def __init__(self, value, expected_value='', explanation='', func_name=''):
        self.value = value
        self.expected_value = expected_value
        self.explanation = explanation
        self.func_name = func_name


class NotExistsValueError(Exception):
    """Custom Exception.
    Raised when object or value not exists

    Attributes:
        obj_name -- object name or class name
        name -- variable name
    """
    def __init__(self, obj_name, name, explanation='', func_name=''):
        self.obj_name = obj_name
        self.name = name
        self.explanation = explanation
        self.func_name = func_name


class NotFoundError(Exception):
    """Custom Exception.
    Raised when object or value not exists

    Attributes:
        obj_name -- object name or class name
        name -- variable name
        by_value -- filtered value
        explanation -- text explanation
    """
    def __init__(self, obj_name, name, by_value, explanation='', func_name=''):
        self.obj_name = obj_name
        self.name = name
        self.by_value = by_value
        self.explanation = explanation
        self.func_name = func_name


class WrongFormatError(Exception):
    """Custom Exception.
    Raised when object or value not exists

    Attributes:
        obj_name -- object name or class name
        name -- variable name
        by_value -- filtered value
        explanation -- text explanation
    """
    def __init__(self, target_format, value, explanation='', func_name=''):
        self.target_format = target_format
        self.value = value
        self.explanation = explanation
        self.func_name = func_name
