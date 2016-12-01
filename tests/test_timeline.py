import pytest
import json

from iap.forecasting.workbench.container.timelines import TimeLineManager

#load test data
@pytest.fixture
def load_data():
    with open('json/timeline.json') as data_file:
        time_line = json.load(data_file)
    return time_line

@pytest.fixture
def load_correct_data():
    with open("json/timeline_correct.json") as f:
        correct_data = json.load(f)
    return correct_data

@pytest.fixture
def load_correct_timeseries():
    with open("json/timeline_correct.json") as f:
        correct_data = json.load(f)
    return correct_data

@pytest.fixture
def load_incorrect_data():
    with open("json/timeline_incorrect.json") as f:
        correct_data = json.load(f)
    return correct_data

def test_load_timelines(load_data, load_correct_data, load_incorrect_data):
    '''Fundamental test for timelinemanager
    Set the attributes for time line manager
    and check the result equalty with prepared correct/incorrect data

    :param ts_properties:

    :param alias:

    :param top_ts_points:

    :return:

    '''

    def load_timeline(load_data):
        #prepare timeline_manager
        ts_properties = load_data['properties']
        alias = load_data['alias']
        top_ts_points = load_data['top_ts_points']

        time_line_manager = TimeLineManager()
        time_line_manager.load_timelines(ts_properties,alias,top_ts_points)
        return time_line_manager
    #TODO check dictionary
    actual = load_timeline(load_data)._timescales
    expected = load_correct_data
    assert actual.sort() == expected.sort()

    actual = load_timeline(load_data)._timescales
    expected = load_incorrect_data
    assert actual.sort() == expected.sort()

    actual = load_timeline(load_data)._timescales
    expected = load_correct_data
    assert actual.sort() == expected.sort()

    actual = load_timeline(load_data)._timescales
    expected = load_incorrect_data
    assert actual.sort() == expected.sort()


def test_get_ts(load_data,load_correct_data,load_incorrect_data):
    '''Testing get_ts(self,name) - function for testing get_ts
    return dictionary information about time series by name

    Input: name of time series

    Output: dictionary information about time series

    :param name:

    :return:

    '''

    def get_ts(name):
    #TimeLineManager Preparation
        ts_properties = load_data['properties']
        alias = load_data['alias']
        top_ts_points = load_data['top_ts_points']

        time_line_manager = TimeLineManager()
        time_line_manager.load_timelines(ts_properties, alias, top_ts_points)
        return  time_line_manager._get_ts(name)

    expected = [i for i in load_incorrect_data if i['annual']=='annual']
    actual = get_ts('annual')
    assert expected == actual

    expected = [i for i in load_incorrect_data if i['month']=='month']
    actual = get_ts('month')
    assert expected == actual

    expected = [i for i in load_incorrect_data if i['day']=='day']
    actual = get_ts('day')
    assert expected == actual

    expected = [i for i in load_incorrect_data if i['hour']=='hour']
    actual = get_ts('hour')
    assert expected == actual

    expected = [i for i in load_correct_data if i['annual']=='annual']
    actual = get_ts('annual')
    assert expected == actual

    expected = [i for i in load_correct_data if i['month']=='month']
    actual = get_ts('month')
    assert expected == actual

    expected = [i for i in load_correct_data if i['day']=='day']
    actual = get_ts('day')
    assert expected == actual

    expected = [i for i in load_correct_data if i['hour']=='hour']
    actual = get_ts('hour')
    assert expected == actual

def test_get_growth_lag(load_data):
    '''Test for get_growth_lag

    Args:
        (string): ts_name - time series name

    :param self:
    :param ts_name:
    :return:

    '''

    def get_growth_lag(ts_name):

        ts_properties = load_data['properties']
        alias = load_data['alias']
        top_ts_points = load_data['top_ts_points']

        time_line_manager = TimeLineManager()
        time_line_manager.load_timelines(ts_properties, alias, top_ts_points)

        return time_line_manager.get_growth_lag(ts_name)

    expected = 1
    actual = get_growth_lag("annual")
    assert expected == actual

    expected = 1
    actual = get_growth_lag("month")
    assert expected == actual

    expected = 3
    actual = get_growth_lag("day")
    assert expected == actual

    expected = 3
    actual = get_growth_lag("minutes")
    assert expected == actual

def test_get_index(load_data):
    '''Test for get index method
    Get index of special point in ts by name and ts name

    :return:

    '''

    def get_index(ts_name,label):
        ts_properties = load_data['properties']
        alias = load_data['alias']
        top_ts_points = load_data['top_ts_points']

        time_line_manager = TimeLineManager()
        time_line_manager.load_timelines(ts_properties, alias, top_ts_points)

        return time_line_manager.get_index(ts_name,label)

    expected = 1
    actual = get_index("annual", "2017")
    assert expected == actual

    expected = 1
    actual = get_index("annual","2013")
    assert expected == actual

    expected = 3
    actual = get_index("month", "April")
    assert expected == actual

    expected = 1
    actual = get_index("month", "Jan")
    assert expected == actual

def test_get_label(load_data):
    '''Test for get index of point in timeseries

    Args:
        (string): ts_name - time series name
        (index): point position in timeseries

    :param load_data:
    :return:

    '''

    def get_label(ts_name, index):
        ts_properties = load_data['properties']
        alias = load_data['alias']
        top_ts_points = load_data['top_ts_points']

        time_line_manager = TimeLineManager()
        time_line_manager.load_timelines(ts_properties, alias, top_ts_points)

        return time_line_manager.get_label(ts_name, index)

    expected = "2012"
    actual = get_label("annual", 0)
    assert actual==expected

    expected = "2013"
    actual = get_label("annual", 1)
    assert actual==expected

    expected = "2014"
    actual = get_label("month", 3)
    assert actual==expected

    expected = "2013"
    actual = get_label("month", 1)
    assert actual==expected

    expected = "January"
    actual = get_label("month", 0)
    assert actual==expected

    expected = "March"
    actual = get_label("month", 2)
    assert actual==expected

    expected = "Decemebr"
    actual = get_label("month", 11)
    assert actual==expected


def test_get_period_by_alias(load_data):


    def get_period_by_alias(ts_name, period_alias):
        ts_properties = load_data['properties']
        alias = load_data['alias']
        top_ts_points = load_data['top_ts_points']

        time_line_manager = TimeLineManager()
        time_line_manager.load_timelines(ts_properties, alias, top_ts_points)
        return time_line_manager.get_period_by_alias(ts_name, period_alias)

    expected = (("2012", "2016"), (0, 4))
    actual = get_period_by_alias('annual', "all")
    assert expected == actual

    expected = (("2014", "2016"), (2, 4))
    actual = get_period_by_alias('annual', "history")
    assert expected == actual

    expected = (("2013", "2018"), (1, 4))
    actual = get_period_by_alias('annual', "all")
    assert expected == actual

    expected = (("Jan", "Dec"), (0, 11))
    actual = get_period_by_alias('month', "history")
    assert expected == actual

    expected = (("January", "June"), (0, 6))
    actual = get_period_by_alias('month', "all")
    assert expected == actual

    expected = (("January", "March"), (0, 2))
    actual = get_period_by_alias('month', "history")
    assert expected == actual

def test_get_timeline_by_period(load_data):
    '''Test for get timeline_by_period
    Check wether output list of point equal to
    expected.

    Args:
        (string): ts_name - time series name
        (string): period

    :param load_data:
    :return:

    '''

    def get_timeline_by_period(ts_name,period):

        ts_properties = load_data['properties']
        alias = load_data['alias']
        top_ts_points = load_data['top_ts_points']

        time_line_manager = TimeLineManager()
        time_line_manager.load_timelines(ts_properties, alias, top_ts_points)

        return time_line_manager.get_timeline_by_period(ts_name,period)

    excepted = ['2013', '2014', '2015', '2016', '2017', '2018']
    actual = get_timeline_by_period('annual', ["2013", '2018'])
    print(actual)
    assert excepted==actual

    excepted = ['January', 'February', 'March']
    actual = get_timeline_by_period('month', ['January', 'March'])
    print(actual)
    assert excepted == actual

    excepted = ['2012', '2014', '2015', '2016']
    actual = get_timeline_by_period('annual', ["2012", '2016'])
    assert excepted==actual

    excepted = ['Monday', 'Tuesday', 'Wednesday']
    actual = get_timeline_by_period('day', ['Monay', 'Wednesday'])
    assert excepted == actual

def test_get_names(load_data):
    '''Test for get_names(self, ts_names, ts_period)

    Return list of time point's names in timeseries

    :return:

    '''

    def get_ts_names(ts_name, ts_period):
        time_line_manager = TimeLineManager()

        ts_properties = load_data['properties']
        alias = load_data['alias']
        top_ts_points = load_data['top_ts_points']

        time_line_manager = TimeLineManager()
        time_line_manager.load_timelines(ts_properties, alias, top_ts_points)

        return time_line_manager.get_names(ts_name,ts_period)

    expected = ['2013', '2014', '2015', '2016', '2017', '2018']
    actual = get_ts_names('annual', 'all')
    assert expected == actual

    expected = ['January', 'April', '2015', '2016', '2017', '2018']
    actual = get_ts_names('month', 'all')
    assert expected == actual

    expected = []
    actual = get_ts_names('hour', 'all')
    assert expected == actual

    expected = []
    actual = get_ts_names('day', 'all')
    assert expected == actual

def test_get_time_length(load_data):
    '''Test for get_time_length(self, ts_name)
    Check wether expected and output lenth of
    timeseries the same.
    Args:
        (string): ts_names - name of time series
    :param load_data:
    :return:

    '''

    def get_time_length(ts_name):
        time_line_manager = TimeLineManager()

        ts_properties = load_data['properties']
        alias = load_data['alias']
        top_ts_points = load_data['top_ts_points']

        time_line_manager = TimeLineManager()
        time_line_manager.load_timelines(ts_properties, alias, top_ts_points)

        return time_line_manager.get_time_length(ts_name)

    expected = 7
    actual = get_time_length("annual")
    assert  expected == actual

    expected = 12
    actual = get_time_length("month")
    assert  expected == actual

    expected = 0
    actual = get_time_length("day")
    assert  expected == actual

    expected = 0
    actual = get_time_length("hour")
    assert  expected == actual

    expected = 8
    actual = get_time_length("day")
    assert  expected == actual

    expected = 23
    actual = get_time_length("hour")
    assert  expected == actual

def test_get_last_actual(load_data):
    '''Check the euality between expected and output
    values of name and intex of last point in
    history period of timeseries
     Args:
        (string): ts_names - name of timeseries
    :return:

    '''
    def get_last_actual(ts_names):
        time_line_manager = TimeLineManager()

        ts_properties = load_data['properties']
        alias = load_data['alias']
        top_ts_points = load_data['top_ts_points']

        time_line_manager = TimeLineManager()
        time_line_manager.load_timelines(ts_properties, alias, top_ts_points)

        return time_line_manager.get_last_actual(ts_names)

    expected = ("2016",5)
    actual = get_last_actual("annual")
    print(actual)
    assert  expected == actual

    expected = ("2018",5)
    actual = get_last_actual("annual")
    print(actual)
    assert  expected == actual

    expected = ("June",5)
    actual = get_last_actual("month")
    print(actual)
    assert  expected == actual

    expected = ("31","30")
    actual = get_last_actual("day")
    print(actual)
    assert  expected == actual

def test_get_growth_period():
    '''Test for get_growth)period(self,ts_name,period)
    Check equality expected and output list of intervals
     Args:
        (string): ts_names - name of timeseries
        (list): period - start and end of period
    :return:

    '''
    def get_growth_period(ts_names,period):
        time_line_manager = TimeLineManager()

        ts_properties = load_data['properties']
        alias = load_data['alias']
        top_ts_points = load_data['top_ts_points']

        time_line_manager = TimeLineManager()
        time_line_manager.load_timelines(ts_properties, alias, top_ts_points)

        return time_line_manager.get_growth_period(ts_names, period)

    expected = [("2012","2013")]
    actual = get_growth_period("annual", ["2012", "2013"])
    assert  expected == actual

    expected = [("2012", "2013")]
    actual = get_growth_period("annual", None)
    assert  expected == actual

    expected = [("January", "February"),("February", "March")]
    actual = get_growth_period("month", ["January", "March"])
    assert  expected == actual

    expected = [("January", "February"),("February", "March")]
    actual = get_growth_period("annual", ["2014","2016"])
    assert  expected == actual

    [("2012", "2013"),("2012", "2013"),("2012", "2013"),("2013", "2014"),("2014", "2015"),("2015", "2016"),
     ("2016", "2017"),("2017","2018")]
    expected = 5
    actual = get_growth_period("annual", None)
    assert  expected == actual

    expected = [("January", "February"),("February", "March")]
    actual = get_growth_period("month", None)
    assert  expected == actual

    expected =[]
    actual = get_growth_period("day", None)
    assert  expected == actual

    expected = [("January", "February"), ("February", "March"),  ("March", "April")]
    actual = get_growth_period("month", ["January", "April"] )
    assert  expected == actual


def test_get_timeline_tree(load_data):

    def get_timeline_tree(top_ts_name, bottom_ts_name, period):
        time_line_manager = TimeLineManager()

        ts_properties = load_data['properties']
        alias = load_data['alias']
        top_ts_points = load_data['top_ts_points']

        time_line_manager = TimeLineManager()
        time_line_manager.load_timelines(ts_properties, alias, top_ts_points)
        tree =time_line_manager.get_timeline_tree(top_ts_name, bottom_ts_name, period)
        return tree
    #TODO
    excepted = " "
    actual = get_timeline_tree("annual", "month", ["2012","2013"])
    print(actual)
    assert  actual == excepted

    #TODO
    excepted = ''
    actual = get_timeline_tree("month", "annual", ["2012","2013"])
    print(actual)
    assert  actual == excepted

    #TODO
    excepted = ''
    actual = get_timeline_tree("hour", "month", ["2012","2013"])
    print(actual)
    assert  actual == excepted

