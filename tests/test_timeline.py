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


def test_load_timelines(time_line_manager, load_correct_timeseries, load_incorrect_timeseries):
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
    actual = time_line_manager._timescales
    expected = load_correct_timeseries
    assert actual.sort() !=  expected.sort()

    actual = time_line_manager._timescales
    expected = load_incorrect_timeseries
    assert actual.sort() == expected.sort()



def test_get_ts(time_line_manager, load_correct_timeseries, load_incorrect_timeseries):
    '''Testing get_ts(self,name) - function for testing get_ts
    return dictionary information about time series by name

    Args:
        (string): ts_name - time series name

    Return:
        (list): time series content

    :param name:

    :return:

    '''

    expected = [i for i in load_incorrect_timeseries if i['name']=='annual']
    actual = time_line_manager._get_ts('annual')
    assert expected == actual

    expected = [i for i in load_incorrect_timeseries if i['name']=='month']
    actual =  time_line_manager._get_ts('month')
    assert expected == actual

    expected = [i for i in load_incorrect_timeseries if i['name']=='day']
    actual = time_line_manager._get_ts('day')
    assert expected == actual

    expected = [i for i in load_incorrect_timeseries if i['name']=='hour']
    actual = time_line_manager._get_ts('hour')
    print(actual)
    assert expected == actual

    expected = [i for i in load_correct_timeseries if i['name']=='annual']
    actual = time_line_manager._get_ts('annual')
    assert expected == actual[0]

    expected = [i for i in load_correct_timeseries if i['name']=='month']
    actual = time_line_manager._get_ts('month')
    assert expected == actual[0]

    expected = [i for i in load_correct_timeseries if i['name']=='day']
    actual = time_line_manager._get_ts('day')
    assert expected == actual[0]

    expected = [i for i in load_correct_timeseries if i['name']=='hour']
    actual = time_line_manager._get_ts('hour')
    assert expected == actual[0]

def test_get_growth_lag(time_line_manager):
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
    actual = time_line_manager.get_growth_lag("annual")
    assert expected == actual

    expected = 1
    actual = time_line_manager.get_growth_lag("month")
    assert expected == actual

    expected = 3
    actual = time_line_manager.get_growth_lag("day")
    assert expected == actual

    expected = 3
    actual = time_line_manager.get_growth_lag("minutes")
    assert expected == actual

def test_get_index(time_line_manager):
    '''Test for get index method
    Get index of special point in ts by name and ts name

    Args:
        (string): ts_name - time series name
        (string): label - full name of point in time series

    Return:
        (int): position in time series

    :return:

    '''

    expected = 1
    actual = time_line_manager.get_index("annual", "2017")
    assert expected == actual

    expected = 1
    actual = time_line_manager.get_index("annual","2013")
    assert expected == actual

    expected = 3
    actual = time_line_manager.get_index("month", "April")
    assert expected == actual

    expected = 1
    actual = time_line_manager.get_index("month", "Jan")
    assert expected == actual



def test_get_label(time_line_manager, load_data):
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
    actual = time_line_manager.get_label("annual", 0)
    assert actual==expected

    expected = "2013"
    actual = time_line_manager.get_label("annual", 1)
    assert actual==expected

    expected = "2014"
    actual = time_line_manager.get_label("month", 3)
    assert actual==expected

    expected = "2013"
    actual = time_line_manager.get_label("month", 1)
    assert actual==expected

    expected = "January"
    actual = time_line_manager.get_label("month", 0)
    assert actual==expected

    expected = "March"
    actual = time_line_manager.get_label("month", 2)
    assert actual==expected

    expected = "Decemebr"
    actual = time_line_manager.get_label("month", 11)
    assert actual==expected


def test_get_period_by_alias(time_line_manager, load_data):
    '''Test for get_perio_by_alias(ts_name, period_alias)

    Args:
        (string): ts_names - name of timeseries

    Return :
        (tuple): border of timeseries and index of that point

    :param time_line_manager:
    :param load_data:
    :return:

    '''

    def get_period_by_alias(ts_name, period_alias):
        ts_properties = load_data['properties']
        alias = load_data['alias']
        top_ts_points = load_data['top_ts_points']

        time_line_manager = TimeLineManager()
        time_line_manager.load_timelines(ts_properties, alias, top_ts_points)
        return time_line_manager.get_period_by_alias(ts_name, period_alias)

    expected = (("2012", "2016"), (0, 4))
    actual =  time_line_manager.get_period_by_alias('annual', "all")
    assert expected == actual

    expected = (("2014", "2016"), (2, 4))
    actual =  time_line_manager.get_period_by_alias('annual', "history")
    assert expected == actual

    expected = (("2013", "2018"), (1, 4))
    actual = time_line_manager.get_period_by_alias('annual', "all")
    assert expected == actual

    expected = (("Jan", "Dec"), (0, 11))
    actual = time_line_manager.get_period_by_alias('month', "history")
    assert expected == actual

    expected = (("January", "June"), (0, 6))
    actual = time_line_manager.get_period_by_alias('month', "all")
    assert expected == actual

    expected = (("January", "March"), (0, 2))
    actual = time_line_manager.get_period_by_alias('month', "history")
    assert expected == actual

def test_get_timeline_by_period(time_line_manager):
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
    actual = time_line_manager.get_timeline_by_period('annual', ["2013", '2018'])
    assert excepted==actual

    excepted = ['January', 'February', 'March']
    actual = time_line_manager.get_timeline_by_period('month', ['January', 'March'])
    assert excepted == actual

    excepted = ['2012', '2014', '2015', '2016']
    actual = time_line_manager.get_timeline_by_period('annual', ["2012", '2016'])
    assert excepted==actual

    excepted = ['Monday', 'Tuesday', 'Wednesday']
    actual = time_line_manager.get_timeline_by_period('day', ['Monay', 'Wednesday'])
    assert excepted == actual

def test_get_names(time_line_manager, load_data):
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
    actual = time_line_manager.get_names('annual', 'all')
    assert expected == actual

    expected = ['January', 'April', '2015', '2016', '2017', '2018']
    actual = time_line_manager.get_names('month', 'all')
    assert expected == actual

    expected = []
    actual = time_line_manager.get_names('hour', 'all')
    assert expected == actual

    expected = []
    actual = time_line_manager.get_names('day', 'all')
    assert expected == actual

def test_get_time_length(time_line_manager, load_data):
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
    actual = time_line_manager.get_time_length("annual")
    assert  expected == actual

    expected = 12
    actual = time_line_manager.get_time_length("month")
    assert  expected == actual

    expected = 0
    actual = time_line_manager.get_time_length("day")
    assert  expected == actual

    expected = 0
    actual = time_line_manager.get_time_length("hour")
    assert  expected == actual

    expected = 8
    actual = time_line_manager.get_time_length("day")
    assert  expected == actual

    expected = 23
    actual = time_line_manager.get_time_length("hour")
    assert  expected == actual

def test_get_last_actual(time_line_manager, load_data):
    '''Check the euality between expected and output
    values of name and intex of last point in
    history period of timeseries

    Args:
        (string): ts_names - name of timeseries

    Return :
        (tuple): border of timeseries and index of that point


    :return:

    '''

    expected = ("2016", 5)
    actual = time_line_manager.get_last_actual("annual")
    assert  expected == actual

    expected = ("2018", 5)
    actual = time_line_manager.get_last_actual("annual")
    assert  expected == actual

    expected = ("June", 5)
    actual = time_line_manager.get_last_actual("month")
    assert  expected == actual

    expected = ("31", "30")
    actual = time_line_manager.get_last_actual("day")
    assert  expected == actual

def test_get_growth_period(time_line_manager):
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
    actual = time_line_manager.get_growth_periods("annual", ["2012", "2013"])
    assert  expected == actual

    expected = [("2012", "2013")]
    actual = time_line_manager.get_growth_periods("annual", None)
    assert  expected == actual

    expected = [("January", "February"),("February", "March")]
    actual = time_line_manager.get_growth_periods("month", ["January", "March"])
    assert  expected == actual

    expected = [("January", "February"),("February", "March")]
    actual = time_line_manager.get_growth_periods("annual", ["2014","2016"])
    assert  expected == actual

    [("2012", "2013"),("2012", "2013"),("2012", "2013"),("2013", "2014"),("2014", "2015"),("2015", "2016"),
     ("2016", "2017"),("2017","2018")]
    expected = 5
    actual = time_line_manager.get_growth_periods("annual", None)
    assert  expected == actual

    expected = [("January", "February"),("February", "March")]
    actual = time_line_manager.get_growth_periods("month", None)
    assert  expected == actual

    expected =[]
    actual = time_line_manager.get_growth_periods("day", None)
    assert  expected == actual

    expected = [("January", "February"), ("February", "March"),  ("March", "April")]
    actual = time_line_manager.get_growth_periods("month", ["January", "April"] )
    assert  expected == actual


def test_get_timeline_tree(time_line_manager, load_tree):
    '''
    Test for get_timeline_tree(self, time_line_manager, load_tree) method

    Args:
        (string): ts_name - time series name
        (string): bottom_ts_name - time series name
        (string): period - time series name
    Return:
        (dict): {top_ts_name:period}

    :param time_line_manager:
    :param load_tree:
    :return:
    '''
    excepted = load_tree
    actual = time_line_manager.get_timeline_tree("annual", "month", ["2012","2013"])
    assert  actual == excepted

    excepted = load_tree
    actual = time_line_manager.get_timeline_tree("annual", "day", ["2012","2018"])
    assert  actual == excepted

    excepted = load_tree
    actual = time_line_manager.get_timeline_tree("hour", "month", ["2012","2013"])
    assert  actual == excepted

#TO DO compare tree comapring  and dict comparing
