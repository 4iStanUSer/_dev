class TlmNonExistentName(Exception):
    '''Raised in TimeLineManager when time scale name is not found (is empty)

    Attributes:
        ts_name -- time scale name
    '''

    def __init__(self, ts_name):
        self.ts_name = ts_name


class TlmNonExistentLabel(Exception):
    '''Raised in TimeLineManager when label for time scale name is not found

    Attributes:
        ts_name -- time scale name
        label -- label
    '''

    def __init__(self, ts_name, label):
        self.ts_name = ts_name
        self.label = label


class TlmNonExistentLabelIndex(Exception):
    '''Raised in TimeLineManager when index for label for time scale name is not found

    Attributes:
        ts_name -- time scale name
        index -- index
    '''

    def __init__(self, ts_name, index):
        self.ts_name = ts_name
        self.index = index


class EdNonExistentVarName(Exception):
    '''Raised in EntityData when variable name is not found

    Attributes:
        var_name -- variable name
    '''

    def __init__(self, var_name):
        self.var_name = var_name


class EdNonExistentTsName(Exception):
    '''Raised in EntityData when time scale name for variable name is not found

    Attributes:
        var_name -- variable name
        ts_name -- time scale name
    '''

    def __init__(self, var_name, ts_name):
        self.var_name = var_name
        self.ts_name = ts_name


class EdAlreadyExistentVarName(Exception):
    '''Raised in EntityData when variable name already exists

    Attributes:
        new_name -- new variable name
    '''

    def __init__(self, new_name):
        self.new_name = new_name


class ContAlreadyExistentCEntityName(Exception):
    '''Raised in Container when CEntity name already exists on the same level
        (one parent cannot have children with the same name)

    Attributes:
        name -- new CEntity name
    '''

    def __init__(self, name):
        self.name = name


class ContRootNotFound(Exception):
    '''Raised in Container when root cannot be found for the passed CEntity obg name already exists on theject.
        CEntity name is returned

    Attributes:
        name -- CEntity name
    '''

    def __init__(self, name):
        self.name = name
