import pytest
import json
import unittest
from iap.forecasting.workbench.container.timelines import TimeLineManager


#load test data
@pytest.fixture
def load_data():
    with open('json/timeline.json') as data_file:
        time_line = json.load(data_file)
    return time_line

#load correct timeseries
@pytest.fixture
def load_correct_timeseries():
    with open("json/timeline_correct.json") as f:
        correct_data = json.load(f)
    return correct_data

#load incorrect timeseries
@pytest.fixture
def load_incorrect_timeseries():
    with open("json/timeline_incorrect.json") as f:
        correct_data = json.load(f)
    return correct_data

#load correct tree
@pytest.fixture
def load_tree():
    with open("json/tree.json") as f:
        correct_data = json.load(f)
    return correct_data

#backup preparation
@pytest.fixture
def backup(load_data, load_correct_timeseries):
    #load data
    ts_properties = load_data['properties']
    alias = load_data['alias']
    top_ts_points = load_data['top_ts_points']
    backup = {}
    backup['alias'] = {}
    backup['timescales'] = []

    for period_name, ts_borders in alias.items():
        backup['alias'][period_name] = dict(ts_properties)

    for name, props in ts_properties.items():
        for timeserie in load_correct_timeseries:
            if name == timeserie['name']:
                timeline = timeserie
    return backup

#timeline manager preparation
@pytest.fixture
def timeline_manager(load_data):
    ts_properties = load_data['properties']
    alias = load_data['alias']
    top_ts_points = load_data['top_ts_points']
    _time_line_manager = TimeLineManager()
    _time_line_manager.load_timelines(ts_properties, alias, top_ts_points)
    return _time_line_manager

def test_load_backup(load_data, backup, load_correct_timeseries, load_incorrect_timeseries):
    '''Test for load backup method

    :param load_data:
    :param backup:
    :param load_correct_timeseries:
    :param load_incorrect_timeseries:
    :return:

    '''
    _time_line_manager = TimeLineManager()
    _time_line_manager.load_backup(backup)

    assert _time_line_manager.get_backup() == backup
    assert _time_line_manager._timescales == load_correct_timeseries
    # Failed test case
    assert _time_line_manager._timescales == load_incorrect_timeseries

def test_load_timelines(timeline_manager, backup, load_correct_timeseries, load_incorrect_timeseries):
    '''Fundamental test for timelinemanager
    Set the attributes for time line manager
    and check the result equalty with prepared correct/incorrect data

    Args:
        (string): time series name

    Return:
        (list): time series content

    :param ts_properties:

    :param alias:

    :param top_ts_points:

    :return:

    '''

    actual = timeline_manager.get_backup()
    expected = backup
    assert actual.keys() == expected.keys()
    assert json.dumps(actual) == json.dumps(expected)

def test_load_timelines_1(timeline_manager, load_correct_timeseries):

    actual = timeline_manager._time_scales
    expected = load_correct_timeseries
    assert len(actual) == len(expected)
    assert json.dumps(actual) == json.dumps(expected)

def test_load_timelines_2(timeline_manager, load_incorrect_timeseries):
    # Failed test case

    actual = timeline_manager._time_scales
    expected = load_incorrect_timeseries
    assert json.dumps(actual) == json.dumps(expected)


def test_get_ts(timeline_manager, load_data, load_correct_timeseries, load_incorrect_timeseries):
    '''Testing get_ts(self,name) - function for testing get_ts
    return dictionary information about time series by name

    Args:
        (string): ts_name - time series name

    Return:
        (list): time series content

    :param name:

    :return:

    '''

    # Failed test case

    expected = [i for i in load_incorrect_timeseries if i['name']=='annual'][0]
    actual = timeline_manager._get_ts('annual')[0]
    assert actual.keys() == expected.keys()
    assert json.dumps(actual) == json.dumps(expected)

def test_get_ts_1(timeline_manager, load_data, load_correct_timeseries, load_incorrect_timeseries):
    # Failed test case

    expected = [i for i in load_incorrect_timeseries if i['name']=='month'][0]
    actual =  timeline_manager._get_ts('month')[0]
    assert actual.keys() == expected.keys()
    assert json.dumps(actual) == json.dumps(expected)

def test_get_ts_2(timeline_manager, load_data, load_correct_timeseries, load_incorrect_timeseries):
    # Failed test case

    expected = [i for i in load_incorrect_timeseries if i['name']=='day'][0]
    actual = timeline_manager._get_ts('day')[0]
    assert actual.keys() == expected.keys()
    assert json.dumps(actual) == json.dumps(expected)

def test_get_ts_3(timeline_manager, load_data, load_correct_timeseries, load_incorrect_timeseries):
    # Failed test case

    expected = [i for i in load_incorrect_timeseries if i['name']=='hour'][0]
    actual = timeline_manager._get_ts('hour')[0]
    assert actual.keys() == expected.keys()
    assert json.dumps(actual) == json.dumps(expected)

def test_get_ts_4(timeline_manager, load_data, load_correct_timeseries, load_incorrect_timeseries):

    expected = [i for i in load_correct_timeseries if i['name']=='annual'][0]
    actual = timeline_manager._get_ts('annual')[0]
    assert actual.keys() == expected.keys()
    assert json.dumps(actual) == json.dumps(expected)

def test_get_ts_5(timeline_manager, load_data, load_correct_timeseries, load_incorrect_timeseries):

    expected = [i for i in load_correct_timeseries if i['name']=='month'][0]
    actual = timeline_manager._get_ts('month')[0]
    assert actual.keys() == expected.keys()
    assert json.dumps(actual) == json.dumps(expected)

def test_get_ts_6(timeline_manager, load_data, load_correct_timeseries, load_incorrect_timeseries):

    expected = [i for i in load_correct_timeseries if i['name']=='day'][0]
    actual = timeline_manager._get_ts('day')[0]
    assert actual.keys() == expected.keys()
    assert json.dumps(actual) == json.dumps(expected)

def test_get_ts_7(timeline_manager, load_data, load_correct_timeseries, load_incorrect_timeseries):

    expected = [i for i in load_correct_timeseries if i['name']=='hour'][0]
    actual = timeline_manager._get_ts('hour')[0]
    assert actual.keys() == expected.keys()
    assert json.dumps(actual) == json.dumps(expected)

def test_get_growth_lag(timeline_manager):
    '''Test for get_growth_lag

    Args:
        (string): ts_name - time series name
    Return:
        (int): timeseries growth_lag

    :param self:
    :param ts_name:
    :return:

    '''

    expected = 1
    actual = timeline_manager.get_growth_lag("annual")
    assert expected == actual

def test_get_growth_lag_1(timeline_manager):

    expected = 1
    actual = timeline_manager.get_growth_lag("month")
    assert expected == actual

def test_get_growth_lag_2(timeline_manager):
    # Failed test case

    expected = 3
    actual = timeline_manager.get_growth_lag("day")
    assert expected == actual

def test_get_growth_lag_3(timeline_manager):
    # Failed test case

    expected = 3
    actual = timeline_manager.get_growth_lag("minutes")
    assert expected == actual

def test_get_index(timeline_manager):
    '''Test for get index method
    Get index of special point in ts by name and ts name

    Args:
        (string): ts_name - time series name
        (string): label - full name of point in time series

    Return:
        (int): position in time series

    :return:

    '''

    expected = 5
    actual = timeline_manager.get_index("annual", "2017")
    assert expected == actual

def test_get_index_1(timeline_manager):

    expected = 1
    actual = timeline_manager.get_index("annual","2013")
    assert expected == actual

def test_get_index_2(timeline_manager):
    # Failed test case

    expected = 3
    actual = timeline_manager.get_index("month", "April")
    assert expected == actual

def test_get_index_3(timeline_manager):
    # Failed test case

    expected = 1
    actual = timeline_manager.get_index("month", "Jan")
    assert expected == actual

def test_get_label(timeline_manager, load_data):
    '''Test for get index of point in timeseries

    Args:
        (string): ts_name -  name of time series
        (int ):  label - position of point in time series

    Return:
        (string): name of point in time series

    :param load_data:
    :return:

    '''

    expected = "2012"
    actual = timeline_manager.get_label("annual", 0)
    assert actual==expected

def test_get_label_1(timeline_manager, load_data):

    expected = "2013"
    actual = timeline_manager.get_label("annual", 1)
    assert actual==expected

def test_get_label_2(timeline_manager, load_data):
    # Failed test case

    expected = "2014"
    actual = timeline_manager.get_label("month", 3)
    assert actual==expected

def test_get_label_3(timeline_manager, load_data):
    # Failed test case

    expected = "2013"
    actual = timeline_manager.get_label("month", 1)
    assert actual==expected

def test_get_label_4(timeline_manager, load_data):

    expected = "January"
    actual = timeline_manager.get_label("month", 0)
    assert actual==expected

def test_get_label_5(timeline_manager, load_data):

    expected = "March"
    actual = timeline_manager.get_label("month", 2)
    assert actual==expected

def test_get_label_6(timeline_manager, load_data):
    # Failed test case

    expected = "Decemebr"
    actual = timeline_manager.get_label("month", 11)
    assert actual==expected


def test_get_period_by_alias(timeline_manager, load_data):
    '''Test for get_perio_by_alias(ts_name, period_alias)

    Args:
        (string): ts_names - name of timeseries

    Return :
        (tuple): border of timeseries and index of that point

    :param timeline_manager:
    :param load_data:
    :return:

    '''

    expected = (("2012", "2016"), (0, 4))
    actual =  timeline_manager.get_period_by_alias('annual', "all")
    assert expected == actual

def test_get_period_by_alias_1(timeline_manager, load_data):

    expected = (("2014", "2016"), (2, 4))
    actual =  timeline_manager.get_period_by_alias('annual', "history")
    assert expected == actual

def test_get_period_by_alias_2(timeline_manager, load_data):
    # Failed test case

    expected = (("2013", "2018"), (1, 4))
    actual = timeline_manager.get_period_by_alias('annual', "all")
    assert expected == actual

def test_get_period_by_alias_3(timeline_manager, load_data):

    expected = (("Jan", "Dec"), (0, 11))
    actual = timeline_manager.get_period_by_alias('month', "history")
    assert expected == actual

def test_get_period_by_alias_4(timeline_manager, load_data):

    expected = (("January", "June"), (0, 6))
    actual = timeline_manager.get_period_by_alias('month', "all")
    assert expected == actual

def test_get_period_by_alias_5(timeline_manager, load_data):

    expected = (("January", "March"), (0, 2))
    actual = timeline_manager.get_period_by_alias('month', "history")
    assert expected == actual

def test_get_timeline_by_period(timeline_manager):
    '''Test for get timeline_by_period
    Check wether output list of point equal to
    expected.

    Args:
        (string): ts_name - time series name
        (string): period

    Return:
        (list): list of points name

    :param load_data:
    :return:

    '''

    excepted = ['2013', '2014', '2015', '2016', '2017', '2018']
    actual = timeline_manager.get_timeline_by_period('annual', ["2013", '2018'])
    assert excepted==actual

def test_get_timeline_by_period_1(timeline_manager):

    excepted = ['January', 'February', 'March']
    actual = timeline_manager.get_timeline_by_period('month', ['January', 'March'])
    assert excepted == actual

def test_get_timeline_by_period_2(timeline_manager):

    excepted = ['2012', '2014', '2015', '2016']
    actual = timeline_manager.get_timeline_by_period('annual', ["2012", '2016'])
    assert excepted==actual

def test_get_timeline_by_period_3(timeline_manager):
    # Failed test case

    excepted = ['Monday', 'Tuesday', 'Wednesday']
    actual = timeline_manager.get_timeline_by_period('day', ['Monay', 'Wednesday'])
    assert excepted == actual

def test_get_names(timeline_manager, load_data):
    '''Test for get_names(self, ts_names, ts_period)
    Return list of time point's names in timeseries

    Args:
        (string): ts_name - time series name
        (string): ts_period

    Return:
        (list): names of point in timeseries

    :return:

    '''

    expected = ['2013', '2014', '2015', '2016', '2017', '2018']
    actual = timeline_manager.get_names('annual', 'all')
    assert expected == actual

def test_get_names_1(timeline_manager, load_data):
    # Failed test case

    expected = ['January', 'April', '2015', '2016', '2017', '2018']
    actual = timeline_manager.get_names('month', 'all')
    assert expected == actual

def test_get_names_2(timeline_manager, load_data):

    expected = []
    actual = timeline_manager.get_names('hour', 'all')
    assert expected == actual

def test_get_names_3(timeline_manager, load_data):

    expected = []
    actual = timeline_manager.get_names('day', 'all')
    assert expected == actual

def test_get_time_length(timeline_manager, load_data):
    '''Test for get_time_length(self, ts_name)
    Check wether expected and output lenth of
    timeseries the same.

    Args:
        ts_name (string): time series name

    Returns:
        int: number of points in time series


    :param load_data:
    :return:

    '''

    expected = 7
    actual = timeline_manager.get_time_length("annual")
    assert  expected == actual

def test_get_time_length_1(timeline_manager, load_data):

    expected = 12
    actual = timeline_manager.get_time_length("month")
    assert  expected == actual

def test_get_time_length_2(timeline_manager, load_data):

    expected = 0
    actual = timeline_manager.get_time_length("day")
    assert  expected == actual

def test_get_time_length_3(timeline_manager, load_data):

    expected = 0
    actual = timeline_manager.get_time_length("hour")
    assert  expected == actual

def test_get_time_length_4(timeline_manager, load_data):
    # Failed test case

    expected = 8
    actual = timeline_manager.get_time_length("day")
    assert  expected == actual

def test_get_time_length_6(timeline_manager, load_data):

    expected = 23
    actual = timeline_manager.get_time_length("hour")
    assert  expected == actual

def test_get_last_actual(timeline_manager, load_data):
    '''Check the euality between expected and output
    values of name and intex of last point in
    history period of timeseries

    Args:
        (string): ts_names - name of timeseries

    Return :
        (tuple): border of timeseries and index of that point


    :return:

    '''
    # Failed test case

    expected = ("2016", 5)
    actual = timeline_manager.get_last_actual("annual")
    assert  expected == actual

def test_get_last_actual_1(timeline_manager, load_data):
    # Failed test case

    expected = ("2018", 5)
    actual = timeline_manager.get_last_actual("annual")
    assert  expected == actual

def test_get_last_actual_2(timeline_manager, load_data):

    expected = ("June", 5)
    actual = timeline_manager.get_last_actual("month")
    assert  expected == actual

def test_get_last_actual_3(timeline_manager, load_data):

    expected = ("31", "30")
    actual = timeline_manager.get_last_actual("day")
    assert  expected == actual

def test_get_growth_period(timeline_manager):
    '''Test for get_growth)period(self,ts_name,period)
    Check equality expected and output list of intervals

    Args:
        (string): ts_names - name of
        (list): period - start and end of period

    Return :
        (list): list of tuples (start_interva,end_interval)


    :return:

    '''

    expected = [("2012","2013")]
    actual = timeline_manager.get_growth_periods("annual", ["2012", "2013"])
    assert  expected == actual

def test_get_growth_period_1(timeline_manager):

    expected = [("2012", "2013")]
    actual = timeline_manager.get_growth_periods("annual", None)
    assert  expected == actual

def test_get_growth_period_2(timeline_manager):

    expected = [("January", "February"),("February", "March")]
    actual = timeline_manager.get_growth_periods("month", ["January", "March"])
    assert  expected == actual

def test_get_growth_period_3(timeline_manager):
    # Failed test case

    expected = [("January", "February"),("February", "March")]
    actual = timeline_manager.get_growth_periods("annual", ["2014","2016"])
    assert  expected == actual

def test_get_growth_period_4(timeline_manager):
    # Failed test case

    expected = 5
    actual = timeline_manager.get_growth_periods("annual", None)
    assert  expected == actual

def test_get_growth_period_5(timeline_manager):
    # Failed test case

    expected = [("January", "February"),("February", "March")]
    actual = timeline_manager.get_growth_periods("month", None)
    assert  expected == actual

def test_get_growth_period_6(timeline_manager):

    expected =[]
    actual = timeline_manager.get_growth_periods("day", None)
    assert  expected == actual

def test_get_growth_period_7(timeline_manager):

    expected = [("January", "February"), ("February", "March"),  ("March", "April")]
    actual = timeline_manager.get_growth_periods("month", ["January", "April"] )
    assert  expected == actual


def test_get_timeline_tree(timeline_manager, load_tree):
    '''
    Test for get_timeline_tree(self, timeline_manager, load_tree) method

    Args:
        (string): ts_name - time series name
        (string): bottom_ts_name - time series name
        (string): period - time series name
    Return:
        (dict): {top_ts_name:period}

    :param timeline_manager:
    :param load_tree:
    :return:
    '''
    excepted = load_tree
    actual = timeline_manager.get_timeline_tree("annual", "month", ["2012","2013"])
    assert json.dumps(actual) == json.dumps(excepted)

def test_get_timeline_tree_1(timeline_manager, load_tree):
    # Failed test case

    excepted = load_tree
    actual = timeline_manager.get_timeline_tree("annual", "day", ["2012","2018"])
    assert  actual == excepted

def test_get_timeline_tree_2(timeline_manager, load_tree):
    # Failed test case

    excepted = load_tree
    actual = timeline_manager.get_timeline_tree("hour", "month", ["2012","2013"])
    assert json.dumps(actual) == json.dumps(excepted)

