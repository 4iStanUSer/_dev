import copy
from enum import IntEnum, unique
import pytest
import json
from iap.forecasting.workbench.container.timelines import TimeLineManager
from iap.forecasting.workbench.container.entity_data import *

@pytest.fixture
def backup():
    from obj_entity_data import backup
    print(backup)
    return backup

#load test data
@pytest.fixture
def load_data():
    with open('json/timeline.json') as data_file:
        i = data_file
        time_line = json.load(data_file)
    return time_line

#prepare timeline manager
@pytest.fixture
def time_line_manager(load_data):
    '''
    Fixture that prepare timeline manager

    :param load_data:
    :return:

    '''
    ts_properties = load_data['properties']
    alias = load_data['alias']
    top_ts_points = load_data['top_ts_points']

    _time_line_manager = TimeLineManager()
    _time_line_manager.load_timelines(ts_properties, alias, top_ts_points)
    return _time_line_manager

@pytest.fixture
def entity_data(time_line_manager):
    _entity_data = EntityData(time_line_manager)
    return _entity_data

def test_init_slot(entity_data):
    '''
      Args:
          (string): var_name
          (string): ts_name
          (int): data_type

      if DataType is time_series:
          get_var_property
          get length of timeline
          init empty slot for specific variable with
          example

      :return:

      '''
    entity_data.init_slot('Sales','annual', DataType.time_series)
    expected = {('Sales', 'annual'): []}
    actual = entity_data._time_series
    assert actual == expected

    entity_data.init_slot('Sales', 'month', DataType.time_series)
    expected =  {('Sales', 'annual'): [], ('Sales', 'month'): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}

    assert actual == expected


    entity_data.init_slot('Sales', 'day', DataType.time_series)
    print(entity_data._time_series)
    assert actual == expected

def test_get_backup(entity_data, backup):
    '''
    Test for get_backup method

    :param entity_data:
    :param backup:
    :return:

    '''
    entity_data.load_backup(backup)
    assert entity_data.get_backup() == backup

def test_get_ts_vals(entity_data, backup):
    '''

    Args:
        (string): var_name - name of variable
        (string):ts_name - timeseries name
        (tuple): period in timeseries
        (int): length of time series
    Return:
        (list): slice of time series by specific period

    :return:

    '''

    entity_data.load_backup(backup)
    expected =""
    actual = entity_data.get_ts_vals("Sales", "annual", ("2012","2013"), 3)
    assert expected == actual

def test_set_ts_vals(entity_data, backup):
    '''
    Args:
        (string): var_name - variable name
        (string): ts_name - timeseries name
        (list): values -list of values
        (None): stamp - initial points
    Return:

    :return:

    '''
    entity_data.load_backup(backup)

    print(entity_data.set_ts_vals("Sales", "annual", ("2012","2013"), "2012"))
    print(entity_data.set_ts_vals("Income", "annual", ("2014","2016"), "2014"))
    print(entity_data.set_ts_vals("Costs", "annual", ("2016","2017"), "2016"))

def test_get_period_vals(entity_data, backup):
    '''Test for get_period_vals(entity_data, backup)

    Args:
        (string): var_name - variable name
        (tuple): period - star_period, end_period
        (int): value - value of variable
    :return:

    '''
    entity_data.load_backup(backup)
    print(entity_data.get_period_val("Sales", "annual", ("2012","2013")))
    print(entity_data.get_period_val("Income", "annual", ("2012","2013")))
    print(entity_data.get_period_val("Costs", "annual", ("2012","2013")))



def test_set_period_vals(entity_data, backup):
    '''Test for set_period_vals(entity_data, backup)

    Args:
        (string): var_name - variable name
        (tuple): period - star_period, end_period
        (int): value - value of variable
    :return:

    '''
    entity_data.load_backup(backup)

    print(entity_data.set_period_val("Sales", "annual", ("2012","2013")))
    print(entity_data.set_period_val("Income", "annual", ("2012","2013")))
    print(entity_data.set_period_val("Costs", "annual", ("2012","2013")))

def test_get_all_period(entity_data, backup):
    entity_data.load_backup(backup)

    print(entity_data.get_all_periods("Sales", "annual"))
    print(entity_data.get_all_periods("Income", "annual"))
    print(entity_data.get_all_periods("SalCostses", "annual"))

def test_is_exist(entity_data, backup):
    '''Bool function check wether variable are in backup

    Args:
        (string): var_name - name of variable
        (string): ts_name - timeseries name
        (DataType): data_type - specific data type

    Return:
        (bool)

    :return:

    '''

    entity_data.load_backup(backup)
    print(entity_data.is_exist("Sales", "annual", DataType.time_series))
    print(entity_data.is_exist("Sales", "annual", DataType.time_series))
    print(entity_data.is_exist("Sales", "annual", DataType.time_series))

def test_rename_variable(entity_data, backup):
    '''Method that rename variable

    Args:
        (string): old_name - old name of variable
        (string): new_name - new name of variable

    Return:

    :param old_name:
    :param new_name:
    :return:

    '''
    entity_data.load_backup(backup)

    print(entity_data.rename("Sales", "Pre-sales"))
    print(entity_data.rename("Costs", "Pre-sales"))
    print(entity_data.rename("Sales", "Pre-sales"))

def test_set_var_property(entity_data, backup):
    '''Set specific value for variable propery
    Args:
        (string): var_name -variable name
        (string): prop_name - property name
        (obj): value

    Return:

    :return:

    '''

    entity_data.load_backup(backup)

    entity_data.set_var_property("Sales", 'total', 10)
    entity_data.set_var_property("Costs", 'tota;', 100)
    entity_data.set_var_property("Income", 'untotal', 500)
    entity_data.set_var_property("Pre-Sales", 'untotal', 10)
    entity_data.set_var_property("Pre-Costs", 'untotal;', 100)
    entity_data.set_var_property("Income", 'total', 500)
    entity_data.set_var_property("Pre-Sales", 'untotal', 10)
    entity_data.set_var_property("Pre-Costs", 'untotal;', 100)
    entity_data.set_var_property("Income", 'total', 500)

def test_get_var_property(entity_data, backup):
    '''Return value of variable property
    Args:
        (string): var_name - variable name
        (string): prop_name -  property name
    Return:
        value
    :return:

    '''

    entity_data.load_backup(backup)

    print(entity_data.get_var_property("Sales","total"))
    print(entity_data.get_var_property("Sales", "total"))
    print(entity_data.get_var_property("Sales", "total"))
    print(entity_data.get_var_property("Sales", "total"))

def test_get_var_properties(entity_data, backup):
    '''Return all properties of specific variable
    Args:
        (string): var_name - variable name
    Return:
        value
    '''

    entity_data.load_backup(backup)

    print(entity_data.get_var_properties("Sales"))
    print(entity_data.get_var_properties("Income"))
    print(entity_data.get_var_properties("Costs"))


def test_var_names(entity_data, backup):
    '''Return value of variable property
    Args:
        (string): var_name - variable name
        (string): prop_name -  property name
    Return:
        value
    '''

    entity_data.load_backup(backup)

    print(entity_data.var_names())
    print(entity_data.var_names())
    print(entity_data.var_names())

def add_variable(entity_data, backup):
    '''Add new variable to backup

    Args:
        (string): var_name
    Return:

    :return:

    '''
    entity_data.load_backup(backup)

    print(entity_data.add_variable("New Sales"))
    print(entity_data.add_variable("New Deposit"))
    print(entity_data.add_variable("New Variable"))
