
from enum import IntEnum, unique

TOOL = 'forecast'



@unique
class Feature(IntEnum):
    empty = 0
    edit_values = 1
    save_scenarios = 2


@unique
class SlotType(IntEnum):
    empty = 0
    time_series = 1
    scalar = 2
    period_series = 4


@unique
class VariableType(IntEnum):
    empty = 0
    is_output = 1
    is_driver = 2


@unique
class AccessMask(IntEnum):
    empty = 0
    view = 1
    edit = 2


@unique
class FilterType(IntEnum):
    empty = 0
    path = 1
    relative_path = 2
    meta_filter = 3



