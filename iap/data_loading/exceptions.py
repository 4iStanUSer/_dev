class NonExistedDataSet(Exception):
    '''Raised in TimeLineManager when time scale name is not found (is empty)

    Attributes:
        ts_name -- time scale name
    '''

    def __init__(self, dataset_name):
        self.dataset_name = dataset_name


class NonExistedConfig(Exception):
    '''Raised in TimeLineManager when time scale name is not found (is empty)

    Attributes:
        ts_name -- time scale name
    '''

    def __init__(self, project_name):
        self.project_name = project_name


class CorruptedDataSet(Exception):
    '''Raised in TimeLineManager when time scale name is not found (is empty)

    Attributes:
        ts_name -- time scale name
    '''

    def __init__(self, dataset_name):
        self.dataset_name = dataset_name

