import copy
from enum import IntEnum, unique
import pytest
import json
from iap.forecasting.workbench.container.timelines import TimeLineManager
from iap.forecasting.workbench.container.entity_data import *

@pytest.fixture
def backup():
    from conf_test import backup
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

def test_get_backup(entity_data, backup):
    '''
    Test for get_backup method

    :param entity_data:
    :param backup:
    :return:

    '''

    entity_data.load_backup(backup)
    expected = json.dumps(backup)
    actual = json.dumps(entity_data.get_backup())
    assert actual == expected


def test_get_backup_1(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup['periods_series'])
    expected = json.dumps(backup)
    actual = json.dumps(entity_data.get_backup())
    assert actual == expected

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
    expected = [0]
    actual = entity_data.get_ts_vals("Sales", "annual", ("2012","2013"), 3)
    assert expected == actual

def test_get_ts_vals_1(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = [0,1,2,3]
    actual = entity_data.get_ts_vals("Sales", "annual", ("2012","2016"), 3)
    assert expected == actual

def test_get_ts_vals_2(entity_data, backup):

    entity_data.load_backup(backup)
    expected = [0,1,2,3, 4, 5]
    actual = entity_data.get_ts_vals("Costs", "annual", ("2012","2018"), 3)
    assert expected == actual

def test_get_ts_vals_3(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = [0,1,2,3]
    actual = entity_data.get_ts_vals("Income", "annual", ("2012","2020"), 3)
    assert expected == actual


def test_get_ts_vals_4(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = [0]
    actual = entity_data.get_ts_vals("Oucomes", "annual", ("2012","2013"), 3)
    assert expected == actual

def test_get_ts_vals_5(entity_data, backup):

    entity_data.load_backup(backup)
    expected = [0,1,2,3]
    actual = entity_data.get_ts_vals("Sales", "day", ("2012","2016"), 3)
    assert expected == actual

def test_get_ts_vals_6(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = [0,1,2,3]
    actual = entity_data.get_ts_vals("Income", "annual", ("2018","2002"), 3)
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
    entity_data.set_ts_vals("Sales", "annual", ("2012","2013"), [1, 2])
    expected = [1,2,2,4,6]
    actual = entity_data._time_series[('Sales','annual')]
    assert actual==expected


def test_set_ts_vals_1(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    entity_data.set_ts_vals("Income", "annual", ("2014","2016"), [0, 1, 3])
    expected = [2,2,0,4,6]
    actual = entity_data._time_series[('Sales','annual')]
    assert actual==expected


def test_set_ts_vals_2(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    entity_data.set_ts_vals("Costs", "month", ("2016","2017"), [1, 10, 20, 30])
    expected = [1,2,3,0,6]
    actual = entity_data._time_series[('Sales','annual')]
    assert actual==expected

def test_get_period_vals(entity_data, backup):
    '''Test for get_period_vals(entity_data, backup)

    Args:
        (string): var_name - variable name
        (tuple): period - star_period, end_period
        (int): value - value of variable
    :return:

    '''
    entity_data.load_backup(backup)
    expected = 0
    actual = entity_data.get_period_val("Sales", "annual", ("2012", "2013"))
    assert expected == actual


def test_get_period_vals_1(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = 1
    actual = entity_data.get_period_val("Income", "annual", ("2012", "2013"))
    assert expected == actual

def test_get_period_vals_2(entity_data, backup):

    entity_data.load_backup(backup)
    expected = 101
    actual = entity_data.get_period_val("Costs", "annual", ("2012", "2013"))
    assert expected == actual

def test_get_period_vals_3(entity_data, backup):

    entity_data.load_backup(backup)
    expected = 0
    actual = entity_data.get_period_val("Sales", "day", ("2012", "2013"))
    assert expected == actual

def test_get_period_vals_4(entity_data, backup):

    entity_data.load_backup(backup)
    expected = 1
    actual = entity_data.get_period_val("Outcome", "month", ("2012", "2013"))
    assert expected == actual

def test_get_period_vals_5(entity_data, backup):

    entity_data.load_backup(backup)
    expected = 101
    actual = entity_data.get_period_val("Costs", "annual", ("2018", "2013"))
    assert expected == actual

def test_set_period_vals(entity_data, backup):
    '''Test for set_period_vals(entity_data, backup)

    Args:
        (string): var_name - variable name
        (tuple): period - star_period, end_period
        (int): value - value of variable
    :return:

    '''
    entity_data.load_backup(backup)
    expected = 10
    entity_data.set_period_val("Sales", "annual", ("2012","2013"),10)
    actual = entity_data._periods_series[("Sales", "annual")][("2012","2013")]
    assert actual == expected


def test_set_period_vals_1(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = 15
    entity_data.set_period_val("Sales", "annual", ("2012","2013"),10)
    actual = entity_data._periods_series[("Sales", "annual")][("2012","2013")]
    assert actual == expected

def test_set_period_vals_2(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = 100
    entity_data.set_period_val("Sales", "annual", ("2012","2017"),100)
    actual = entity_data._periods_series[("Sales", "annual")][("2012","2017")]
    assert actual == expected

def test_get_all_period(entity_data, backup):
    '''Test for method get all periods

    :param entity_data:
    :param backup:
    :return:

    '''
    entity_data.load_backup(backup)

    expected = [('2015', '2016'), ('2016', '2017'), ('2014', '2015'), ('2012', '2013'), ('2013', '2014'), ('2017', '2018')]
    actual = entity_data.get_all_periods("Sales", "annual")


def test_get_all_period_1(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = [('2015', '2016'), ('2016', '2017'), ('2014', '2015'), ('2012', '2013'), ('2013', '2014'), ('2017', '2018')]
    actual = entity_data.get_all_periods("Sales", "month")


def test_get_all_period_2(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = [('2015', '2016'), ('2016', '2017'), ('2014', '2015'), ('2012', '2013'), ('2013', '2014'), ('2017', '2018')]
    actual = entity_data.get_all_periods("Sales", "day")

def test_get_all_period_3(entity_data, backup):

    entity_data.load_backup(backup)
    expected = []
    actual = entity_data.get_all_periods("Costs", "annual")

def test_get_all_period_4(entity_data, backup):

    entity_data.load_backup(backup)
    expected = [('2015', '2016'), ('2016', '2017'), ('2014', '2015'), ('2012', '2013'), ('2013', '2014'), ('2017', '2018')]
    actual = entity_data.get_all_periods("Income", "annual")


def test_get_all_period_5(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = [('2015', '2016'), ('2016', '2017'), ('2014', '2015'), ('2012', '2013'), ('2013', '2014'), ('2017', '2018')]
    actual = entity_data.get_all_periods("Outcome", "annual")


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
    expected = True
    actual = entity_data.is_exist("Sales", "annual", DataType.time_series)
    assert expected == actual


def test_is_exist_1(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = True
    actual = entity_data.is_exist("Sales", "annual", DataType.scalar)
    assert expected == actual


def test_is_exist_2(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = True
    actual = entity_data.is_exist("Cloth", "annual", DataType.time_series)
    assert expected == actual

def test_is_exist_3(entity_data, backup):

    entity_data.load_backup(backup)
    expected = True
    actual = entity_data.is_exist("Loan", "annual", DataType.scalar)
    assert expected == actual

def test_is_exist_4(entity_data, backup):

    entity_data.load_backup(backup)
    expected = True
    actual = entity_data.is_exist("Income", "annual", DataType.period_series)
    assert expected == actual

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
    entity_data.rename_variable("Sales", "Pre-sales")
    assert "Pre-sales" in entity_data._variables.keys()
    assert "Sales" in entity_data._variables.keys()

def test_rename_variable_1(entity_data, backup):

    entity_data.load_backup(backup)
    entity_data.rename_variable("Costs", "Pre-sales")
    assert "Pre-sales" in entity_data._variables.keys()
    assert "Costs" in entity_data._variables.keys()

def test_rename_variable_2(entity_data, backup):

    entity_data.load_backup(backup)
    entity_data.rename_variable("Income", "Pre-sales")
    assert "Pre-sales" in entity_data._variables.keys()
    assert "Income" in entity_data._variables.keys()

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
    assert entity_data._variables['Sales'] == {'total': 10}

def test_set_var_property_1(entity_data, backup):

    entity_data.load_backup(backup)
    entity_data.set_var_property("Costs", 'total', 100)
    assert entity_data._variables['Costs'] == {'total': 100}


def test_set_var_property_2(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    entity_data.set_var_property("Income", 'untotal', 500)
    assert entity_data._variables['Income'] == {'untotal': 500}


def test_set_var_property_3(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    entity_data.set_var_property("Pre-Sales", 'untotal', 10)
    assert entity_data._variables['Pre-Sales'] == {'untotal': 10}


def test_set_var_property_4(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    entity_data.set_var_property("Pre-Costs", 'untotal', 100)
    assert entity_data._variables['Pre-Costs'] == {'untotal': 100}

def test_set_var_property_5(entity_data, backup):

    entity_data.load_backup(backup)
    entity_data.set_var_property("Income", 'total', 500)
    assert entity_data._variables['Income'] == {'total': 500}


def test_set_var_property_6(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    entity_data.set_var_property("Pre-Sales", 'untotal', 10)
    assert entity_data._variables["Pre-Sales"] == {'untotal': 10}


def test_set_var_property_7(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    entity_data.set_var_property("Pre-Costs", 'untotal', 100)
    assert entity_data._variables['Pre-Costs'] == {'untotal': 100}

def test_set_var_property_8(entity_data, backup):

    entity_data.load_backup(backup)
    entity_data.set_var_property("Income", 'total', 500)
    assert entity_data._variables['Income'] == {'total': 500}


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
    expected = "10"
    actual = entity_data.get_var_property("Sales","total")
    assert actual == expected


def test_get_var_property_1(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = "5000"
    actual = entity_data.get_var_property("Outcome","total")
    assert actual == expected


def test_get_var_property_2(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = "1000"
    actual = entity_data.get_var_property("Costs","all")
    assert actual == expected


def test_get_var_property_3(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = "11200"
    actual = entity_data.get_var_property("Tax","year")
    assert actual == expected


def test_get_var_property_4(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = "1000"
    actual = entity_data.get_var_property("Outcome","total")
    assert actual == expected

def test_get_var_properties(entity_data, backup):
    '''Return all properties of specific variable
    Args:
        (string): var_name - variable name
    Return:
        value
    '''

    entity_data.load_backup(backup)
    expected = {"total":"1000"}
    actual = entity_data.get_var_properties("Sales")
    assert actual == expected

def test_get_var_properties_1(entity_data, backup):

    entity_data.load_backup(backup)
    expected = {"total": "1000"}
    actual = entity_data.get_var_properties("Income")
    assert actual == expected

def test_get_var_properties_2(entity_data, backup):

    entity_data.load_backup(backup)
    expected = {"total": "1000"}
    actual = entity_data.get_var_properties("Costs")
    assert actual == expected

def test_get_var_properties_3(entity_data, backup):

    entity_data.load_backup(backup)
    expected = {"total": "1000"}
    actual = entity_data.get_var_properties("Sales")
    assert actual == expected

def test_get_var_properties_4(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = {"total": "1000"}
    actual = entity_data.get_var_properties("Outcome")
    assert actual == expected


def test_get_var_properties_5(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    expected = {"total": "1000"}
    actual = entity_data.get_var_properties("Uncosts")
    assert actual == expected

def test_var_names(entity_data, backup):
    '''Return value of variable property
    Args:
        (string): var_name - variable name
        (string): prop_name -  property name
    Return:
        value
    '''

    entity_data.load_backup(backup)
    actual = entity_data.var_names
    expected = ['Sales', 'Income', 'Costs']
    assert list(actual) == expected


def test_var_names_1(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    actual = entity_data.var_names
    expected = ['Sales', 'Costs']
    assert list(actual)  == expected

def test_var_names_2(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    actual = entity_data.var_names
    expected = ['Sales', 'Outcome', 'Costs']
    assert list(actual)  == expected


def test_var_names_3(entity_data, backup):
    # Failed test

    entity_data.load_backup(backup)
    actual = entity_data.var_names
    expected = []
    assert list(actual)  == expected


def test_add_variable(entity_data, backup):
    '''Add new variable to backup

    Args:
        (string): var_name
    Return:

    :return:

    '''

    entity_data.load_backup(backup)
    entity_data.add_variable("New Sales")
    actual = entity_data._variables.keys()
    assert "New Sales" in actual
    assert list(actual).count("New Sales") == 1

def test_add_variable_1(entity_data, backup):

    entity_data.load_backup(backup)
    entity_data.add_variable("Sales")
    actual = entity_data._variables.keys()
    assert "Sales" in actual
    assert list(actual).count("Sales")==1

def test_add_variable_2(entity_data, backup):

    entity_data.load_backup(backup)
    entity_data.add_variable(5)
    actual = entity_data._variables.keys()
    assert 5 in actual
    assert list(actual).count(5)==1

