class WrongValueError(Exception):
    # Raised when value is incorrect.
    #
    # Attributes:
    #     value -- value that raised exception
    #     expected_value -- expected value
    def __init__(self, value, expected_value='', explanation='', func_name=''):
        self.value = value
        self.expected_value = expected_value
        self.explanation = explanation
        self.func_name = func_name


class NotExistsError(Exception):
    # Raised when object or value not exists
    #
    # Attributes:
    #     obj_name -- object name or class name
    #     name -- variable name
    def __init__(self, obj_name, name, explanation='', func_name=''):
        self.obj_name = obj_name
        self.name = name
        self.explanation = explanation
        self.func_name = func_name


class NotFoundError(Exception):
    # Raised when object or value not exists
    #
    # Attributes:
    #     obj_name -- object name or class name
    #     name -- variable name
    #     by_value -- filtered value
    #     explanation -- text explanation
    def __init__(self, obj_name, name, by_value, explanation='', func_name=''):
        self.obj_name = obj_name
        self.name = name
        self.by_value = by_value
        self.explanation = explanation
        self.func_name = func_name


class AlreadyExistsError(Exception):
    # Raised when user tries to add new object,
    # but such object already exists.
    #
    # Attributes:
    #     par_name -- name of dublicated parameter
    #     par_value -- duplicated value
    def __init__(self, class_name, par_name, par_value, func_name=''):
        self.class_name = class_name
        self.par_name = par_name
        self.par_value = par_value
        self.func_name = func_name
