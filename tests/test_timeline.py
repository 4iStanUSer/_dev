import pytest
import json
import unittest
from iap.forecasting.workbench.container.timelines import TimeLineManager

@pytest.fixture
def data():
    """Load test data
    :return:

    """
    with open('json/timeline_manager/timeline_manager.json') as data_file:
        time_line = json.load(data_file)
    return time_line

@pytest.fixture
def correct_timeseries():
    """Load correct timeseries

    :return:

    """
    with open("json/timeline_manager/timescale.timeline_correct.json") as f:
        correct_timeseries = json.load(f)
    return correct_timeseries

@pytest.fixture
def tree():
    '''Load correct tree

    :return:

    '''
    with open("json/timeline_manager/tree.json") as f:
        _tree = json.load(f)
    return _tree


@pytest.fixture
def backup(data, correct_timeseries):
    """Backup preparation

    :param data:
    :param correct_timeseries:
    :return:

    """
    #load data
    ts_properties = data['properties']
    alias = data['alias']
    top_ts_points = data['top_ts_points']
    backup = {}
    backup['alias'] = {}
    backup['timescales'] = []

    for period_name, ts_borders in alias.items():
        backup['alias'][period_name] = dict(ts_properties)
    for name, props in ts_properties.items():
        for timeserie in correct_timeseries:
            if name == timeserie['name']:
                timeline = timeserie['timeline']
                growth_lag = timeserie['growth_lag']
                backup['timescales'].append(dict(name=name,growth_lag = growth_lag, timeline = timeline))
    return backup


@pytest.fixture
def timeline_manager(data):
    '''Timeline manager preparation

    :param data:
    :return:

    '''
    ts_properties = data['properties']
    alias = data['alias']
    top_ts_points = data['top_ts_points']

    _time_line_manager = TimeLineManager()
    _time_line_manager.load_timelines(ts_properties, alias, top_ts_points)
    return _time_line_manager


def test_load_backup(backup, correct_timeseries):
    """Test for load backup method

    :param:
    :return:

    """

    _time_line_manager = TimeLineManager()
    _time_line_manager.load_backup(backup)

    actual = _time_line_manager.get_backup()['timescales']
    expected = backup['timescales']

    assert len(actual) == len(expected)

    assert [i['name'] for i in expected].sort() == \
           [i['name'] for i in actual].sort()

    assert sorted([(i['name'], len(i['timeline'])) for i in expected], key=lambda l: l[1]) == \
           sorted([(i['name'], len(i['timeline'])) for i in actual], key=lambda l: l[1])

    actual = _time_line_manager._timescales
    expected = correct_timeseries
    assert len(actual) == len(expected)

    assert [i['name'] for i in expected].sort() == \
           [i['name'] for i in actual].sort()

    assert sorted([(i['name'], len(i['timeline'])) for i in expected], key = lambda l: l[1]) == \
           sorted([(i['name'], len(i['timeline'])) for i in actual], key = lambda l: l[1])


def test_load_backup_raise_exception_value_error():
    """Test for load backup method
    Check exception on wrong input value
    :param:
    :return:

    """

    with pytest.raises(Exception):
        _time_line_manager = TimeLineManager()
        _time_line_manager.load_backup([{'1': '2'}])


def test_load_backup_raise_exception_type_error():
    """Test for load backup method
    Check exception on wrong input type
    :param:
    :return:

    """

    with pytest.raises(Exception):
        _time_line_manager = TimeLineManager()
        _time_line_manager.load_backup('backup')


def test_load_timelines(timeline_manager, backup, correct_timeseries):
    """Fundamental test for timelinemanager
    Set the attributes for time line manager
    and check the result equalty with prepared correct/incorrect data

    Args:
        (string): time series name

    Return:
        (list): time series content

    :param:

    :param:

    :param:

    :return:

    """

    actual = timeline_manager.get_backup()['timescales']
    expected = backup['timescales']

    assert len(actual) == len(expected)

    assert [i['name'] for i in expected].sort() == \
           [i['name'] for i in actual].sort()

    assert sorted([(i['name'], len(i['timeline'])) for i in expected], key=lambda l: l[0]) == \
           sorted([(i['name'], len(i['timeline'])) for i in actual], key=lambda l: l[0])


    actual = timeline_manager._timescales
    expected = correct_timeseries

    assert len(actual) == len(expected)

    assert [i['name'] for i in expected].sort() == \
           [i['name'] for i in actual].sort()

    assert sorted([(i['name'], len(i['timeline'])) for i in expected], key=lambda l: l[0]) == \
           sorted([(i['name'], len(i['timeline'])) for i in actual], key=lambda l: l[0])


def test_load_timelines_raise_exception_value_error():
    """Check exception on wrong input value
    :return:
    """
    with pytest.raises(Exception):
        _time_line_manager = TimeLineManager()
        _time_line_manager.load_timelines({'1': '2'}, {'1': '2'}, {'1': '2'})


def test_load_timelines_raise_exception_type_error():
    """
    Check exception on wrong input type
    :return:

    """
    with pytest.raises(Exception):
        _time_line_manager = TimeLineManager()
        _time_line_manager.load_timelines(1, 2, 3)


def test_get_ts(timeline_manager, correct_timeseries):
    """Testing get_ts(self,name) - function for testing get_ts
    return dictionary information about time series by name

    Args:
        (string): ts_name - time series name

    Return:
        (list): time series content

    :param:

    :return:

    """

    expected = [i for i in correct_timeseries if i['name'] == 'annual'][0]
    actual = timeline_manager._get_ts('annual')[0]

    assert actual['name'] == expected['name']

    assert len(actual['timeline']) == len(expected['timeline'])

    assert sorted(actual['timeline'], key=lambda l: l['name_full']) == \
           sorted(expected['timeline'], key=lambda l: l['name_full'])


    expected = [i for i in correct_timeseries if i['name'] == 'month'][0]
    actual =  timeline_manager._get_ts('month')[0]

    assert actual['name'] == expected['name']

    assert len(actual['timeline']) == len(expected['timeline'])

    assert sorted(actual['timeline'], key=lambda l: l['name_full']) == \
           sorted(expected['timeline'], key=lambda l: l['name_full'])


    expected = [i for i in correct_timeseries if i['name'] == 'day'][0]
    actual = timeline_manager._get_ts('day')[0]

    assert actual['name'] == expected['name']

    assert len(actual['timeline']) == len(expected['timeline'])

    assert sorted(actual['timeline'], key=lambda l: l['name_full']) == \
           sorted(expected['timeline'], key=lambda l: l['name_full'])


    expected = [i for i in correct_timeseries if i['name'] == 'hour'][0]
    actual = timeline_manager._get_ts('hour')[0]

    assert actual['name'] == expected['name']

    assert len(actual['timeline']) == len(expected['timeline'])

    assert sorted(actual['timeline'], key=lambda l: l['name_full']) == \
           sorted(expected['timeline'], key=lambda l: l['name_full'])


def test_get_ts_raise_exception_value_error(timeline_manager):
    """Testing get_ts(self,name) - function for testing get_ts
     return dictionary information about time series by name
    Check exception on wrong input

     Args:
         (string): ts_name - time series name

     Return:
         (list): time series content

     :param:

     :return:

     """

    with pytest.raises(Exception):
        timeline_manager._get_ts('seconds')


def test_get_ts_raise_exception_type_error(timeline_manager):
    """Testing get_ts(self,name) - function for testing get_ts
     return dictionary information about time series by name
     Check exception on wrong input


     Args:
         (string): ts_name - time series name

     Return:
         (list): time series content

     :param:

     :return:

     """

    with pytest.raises(Exception):
        timeline_manager._get_ts(['seconds',1])


def test_get_growth_lag(timeline_manager):
    """Test for get_growth_lag

    Args:
        (string): ts_name - time series name
    Return:
        (int): timeseries growth_lag

    :param:
    :param:
    :return:

    """

    expected = 1
    actual = timeline_manager.get_growth_lag("annual")
    assert expected == actual

    expected = 1
    actual = timeline_manager.get_growth_lag("month")
    assert expected == actual

    expected = 1
    actual = timeline_manager.get_growth_lag("day")
    assert expected == actual

    expected = 1
    actual = timeline_manager.get_growth_lag("hour")
    assert expected == actual


def test_get_growth_lag_raise_exception_value_error(timeline_manager):
    """Test for get_growth_lag
    Check exception on wrong input

    Args:
        (string): ts_name - time series name
    Return:
        (int): timeseries growth_lag

    :param:
    :param:
    :return:

    """

    with pytest.raises(Exception):
        timeline_manager.get_growth_lag("day")


def test_get_growth_lag_raise_exception_type_error(timeline_manager):
    """Test for get_growth_lag
    Check exception on wrong input

    Args:
        (string): ts_name - time series name
    Return:
        (int): timeseries growth_lag

    :param:
    :param:
    :return:

    """

    with pytest.raises(Exception):
        timeline_manager.get_growth_lag([1, 3, 4, 5])


def test_get_index(timeline_manager):
    """Test for get index method
    Get index of special point in ts by name and ts name

    Args:
        (string): ts_name - time series name
        (string): label - full name of point in time series

    Return:
        (int): position in time series

    :return:

    """

    expected = 5
    actual = timeline_manager.get_index("annual", "2017")
    assert expected == actual

    expected = 1
    actual = timeline_manager.get_index("annual","2013")
    assert expected == actual

    expected = 1
    actual = timeline_manager.get_index("month", "Jan")
    assert expected == actual


def test_get_index_raise_exception_value_error(timeline_manager):
    """Test for get index method
    Check exception on wrong input


    Args:
        (string): ts_name - time series name
        (string): label - full name of point in time series

    Return:
        (int): position in time series

    :return:

    """

    with pytest.raises(Exception):
        timeline_manager.get_index("seconds", "Jan")


def test_get_index_raise_exception_type_error(timeline_manager):
    """Test for get index method
    Check exception on wrong input


    Args:
        (string): ts_name - time series name
        (string): label - full name of point in time series

    Return:
        (int): position in time series

    :return:

    """

    with pytest.raises(Exception):
        timeline_manager.get_index(["month", "Jan"],5)


def test_get_label(timeline_manager):
    """Test for get index of point in timeseries

    Args:
        (string): ts_name -  name of time series
        (int ):  label - position of point in time series

    Return:
        (string): name of point in time series

    :param:
    :return:

    """

    expected = "2012"
    actual = timeline_manager.get_label("annual", 0)
    assert actual == expected

    expected = "2013"
    actual = timeline_manager.get_label("annual", 1)
    assert actual == expected

    expected = "Fabruary"
    actual = timeline_manager.get_label("month", 1)
    assert actual == expected

    expected = "January"
    actual = timeline_manager.get_label("month", 0)
    assert actual == expected


def test_get_label_exception_value_error(timeline_manager):
    """Test for get index of point in timeseries
    Check exception on wrong input

    Args:
        (string): ts_name -  name of time series
        (int ):  label - position of point in time series

    Return:
        (string): name of point in time series

    :param:
    :return:

    """

    with pytest.raises(Exception):
        timeline_manager.get_label("seconds", 0)


def test_get_label_exception_type_error(timeline_manager):
    """Test for get index of point in timeseries
    Check exception on wrong input

    Args:
        (string): ts_name -  name of time series
        (int ):  label - position of point in time series

    Return:
        (string): name of point in time series

    :param:
    :return:

    """

    with pytest.raises(Exception):
        timeline_manager.get_label(100, "annual")


def test_get_period_by_alias(timeline_manager):
    """"Test for get_period_by_alias(ts_name, period_alias)

    Args:
        (string): ts_names - name of timeseries

    Return :
        (tuple): border of timeseries and index of that point

    :param timeline_manager:
    :param:
    :return:

    """

    expected = (("2012", "2016"), (0, 4))
    actual = timeline_manager.get_period_by_alias('annual', "all")
    assert expected == actual

    expected = (("2014", "2016"), (2, 4))
    actual = timeline_manager.get_period_by_alias('annual', "history")
    assert expected == actual

    expected = (("Jan", "Dec"), (0, 11))
    actual = timeline_manager.get_period_by_alias('month', "history")
    assert expected == actual

    expected = (("January", "June"), (0, 6))
    actual = timeline_manager.get_period_by_alias('month', "all")
    assert expected == actual

    expected = (("January", "March"), (0, 2))
    actual = timeline_manager.get_period_by_alias('month', "history")
    assert expected == actual


def test_get_period_by_alias_exception_value_error(timeline_manager):
    """"Test for get_period_by_alias(ts_name, period_alias)
    Check exception on wrong input

    Args:
        (string): ts_names - name of timeseries

    Return :
        (tuple): border of timeseries and index of that point

    :param timeline_manager:
    :param:
    :return:

    """
    with pytest.raises(Exception):
        timeline_manager.get_period_by_alias('seconds', "first")


def test_get_period_by_alias_exception_type_error(timeline_manager):
    """"Test for get_period_by_alias(ts_name, period_alias)
    Check exception on wrong input

    Args:
        (string): ts_names - name of timeseries

    Return :
        (tuple): border of timeseries and index of that point

    :param timeline_manager:
    :param:
    :return:

    """
    with pytest.raises(Exception):
        timeline_manager.get_period_by_alias(['seconds'], ['history'])


def test_get_timeline_by_period(timeline_manager):
    """Test for get timeline_by_period
    Check whether output list of point equal to
    expected.

    Args:
        (string): ts_name - time series name
        (string): period

    Return:
        (list): list of points name

    :param:
    :return:

    """

    excepted = ['2013', '2014', '2015', '2016', '2017', '2018']
    actual = timeline_manager.get_timeline_by_period('annual', ["2013", '2018'])
    assert excepted == actual

    excepted = ['January', 'February', 'March']
    actual = timeline_manager.get_timeline_by_period('month', ['January', 'March'])
    assert excepted == actual

    excepted = ['2012', '2014', '2015', '2016']
    actual = timeline_manager.get_timeline_by_period('annual', ["2012", '2016'])
    assert excepted == actual


def test_get_timeline_by_period_exception_value_error(timeline_manager):
    """Test for get timeline_by_period
    Check exception on wrong input


    Args:
        (string): ts_name - time series name
        (string): period

    Return:
        (list): list of points name

    :param:
    :return:

    """

    with pytest.raises(Exception):
        timeline_manager.get_timeline_by_period('seconds', ["0", '60'])


def test_get_timeline_by_period_exception_type_error(timeline_manager):
    """Test for get timeline_by_period
    Check exception on wrong input

    Args:
        (string): ts_name - time series name
        (string): period

    Return:
        (list): list of points name

    :param:
    :return:

    """

    with pytest.raises(Exception):
        timeline_manager.get_timeline_by_period('seconds', [2012, 2016])


def test_get_names(timeline_manager):
    """Test for get_names(self, ts_names, ts_period)
    Return list of time point's names in timeseries

    Args:
        (string): ts_name - time series name
        (string): ts_period

    Return:
        (list): names of point in timeseries

    :return:

    """

    expected = ['2013', '2014', '2015', '2016', '2017', '2018']
    actual = timeline_manager.get_names('annual', 'all')
    assert expected == actual

    expected = ['January', 'February', 'March']
    actual = timeline_manager.get_names('month', 'all')
    assert expected == actual

    expected = []
    actual = timeline_manager.get_names('hour', 'all')
    assert expected == actual

    expected = []
    actual = timeline_manager.get_names('day', 'all')
    assert expected == actual


def test_get_names_exception_value_error(timeline_manager):
    """Test for get_names(self, ts_names, ts_period)
    Return list of time point's names in timeseries

    Args:
        (string): ts_name - time series name
        (string): ts_period

    Return:
        (list): names of point in timeseries

    :return:

    """

    with pytest.raises(Exception):
        timeline_manager.get_names('seconds', 'all')


def test_get_names_exception_type_error(timeline_manager):
    """Test for get_names(self, ts_names, ts_period)
    Return list of time point's names in timeseries

    Args:
        (string): ts_name - time series name
        (string): ts_period

    Return:
        (list): names of point in timeseries

    :return:

    """

    with pytest.raises(Exception):
        timeline_manager.get_names(['day'], ['all'])


def test_get_time_length(timeline_manager):
    """Test for get_time_length(self, ts_name)
    Check wether expected and output length of
    timeseries the same.

    Args:
        ts_name (string): time series name

    Returns:
        int: number of points in time series


    :param:
    :return:

    """

    expected = 7
    actual = timeline_manager.get_time_length("annual")
    assert expected == actual

    expected = 12
    actual = timeline_manager.get_time_length("month")
    assert expected == actual

    expected = 0
    actual = timeline_manager.get_time_length("day")
    assert expected == actual

    expected = 0
    actual = timeline_manager.get_time_length("hour")
    assert expected == actual


def  test_get_time_length_raise_exception_value_error(timeline_manager):
    """Test for get_time_length(self, ts_name)
    Check exception on wrong input

    Args:
        ts_name (string): time series name

    Returns:
        int: number of points in time series


    :param:
    :return:

    """

    with pytest.raises(Exception):
        timeline_manager.get_time_length('seconds')


def  test_get_time_length_raise_exception_type_error(timeline_manager):
    """Test for get_time_length(self, ts_name)
    Check exception on wrong input


    Args:
        ts_name (string): time series name

    Returns:
        int: number of points in time series


    :param:
    :return:

    """

    with pytest.raises(Exception):
        timeline_manager.get_time_length(10)


def test_get_last_actual(timeline_manager):
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
    actual = timeline_manager.get_last_actual("annual")
    assert expected == actual

    expected = ("June", 5)
    actual = timeline_manager.get_last_actual("month")
    assert expected == actual

    expected = ("31", "30")
    actual = timeline_manager.get_last_actual("day")
    assert expected == actual


def test_get_last_actual_raise_exception_value_error(timeline_manager):
    '''Check exception on wrong input

    Args:
        (string): ts_names - name of timeseries

    Return :
        (tuple): border of timeseries and index of that point


    :return:

    '''

    with pytest.raises(Exception):
        timeline_manager.get_last_actual("second")


def test_get_last_actual_raise_exception_type_error(timeline_manager):
    '''Check exception on wrong input

    Args:
        (string): ts_names - name of timeseries

    Return :
        (tuple): border of timeseries and index of that point


    :return:

    '''

    with pytest.raises(Exception):
        timeline_manager.get_last_actual(10)


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

    expected = [("2012", "2013")]
    actual = timeline_manager.get_growth_periods("annual", ["2012", "2013"])
    assert expected == actual

    expected = [("2012", "2013")]
    actual = timeline_manager.get_growth_periods("annual", None)
    assert expected == actual

    expected = [("January", "February"), ("February", "March")]
    actual = timeline_manager.get_growth_periods("month", ["January", "March"])
    assert expected == actual

    expected =[]
    actual = timeline_manager.get_growth_periods("day", None)
    assert expected == actual



def test_get_growth_period_raise_exception_value_error(timeline_manager):
    '''Test for get_growth)period(self,ts_name,period)
    Check exception on wrong input

    Args:
        (string): ts_names - name of
        (list): period - start and end of period

    Return :
        (list): list of tuples (start_interva,end_interval)


    :return:

    '''

    with pytest.raises(Exception):
        timeline_manager.get_growth_periods("hour", ["2019", "2012"])


def test_get_growth_period_raise_exception_type_error(timeline_manager):
    '''Test for get_growth)period(self,ts_name,period)
    Check exception on wrong input


    Args:
        (string): ts_names - name of
        (list): period - start and end of period

    Return :
        (list): list of tuples (start_interva,end_interval)


    :return:

    '''

    with pytest.raises(Exception):
        timeline_manager.get_growth_periods(["annual"], "2013")


def test_get_timeline_tree(timeline_manager, tree):

    """Test for get_timeline_tree(self, timeline_manager, tree) method

    Args:
        (string): ts_name - time series name
        (string): bottom_ts_name - time series name
        (string): period - time series name
    Return:
        (dict): {top_ts_name:period}

    :param timeline_manager:
    :param tree:
    :return:
    """

    excepted = tree
    print(tree)
    actual = timeline_manager.get_timeline_tree("annual", "month", ["2012", "2013"])
    assert len(actual) == len(excepted)
    assert sorted([[el['timescale'], el['full_name'], el['parent_index']]
                   for el in actual], key=lambda l: l['full_name']) == \
           sorted([[el['timescale'], el['full_name'], el['parent_index']]
                   for el in excepted], key=lambda l: l['full_name'])

    excepted = tree
    actual = timeline_manager.get_timeline_tree("annual", "day", ["2012", "2018"])
    assert len(actual) == len(excepted)
    assert sorted([[el['timescale'], el['full_name'], el['parent_index']]
                   for el in actual], key=lambda l: l['full_name']) == \
           sorted([[el['timescale'], el['full_name'], el['parent_index']]
                   for el in excepted], key=lambda l: l['full_name'])


def test_get_timeline_tree_raise_exception_value_error(timeline_manager):
    """Test for get_timeline_tree(self, timeline_manager, tree) method
    Check exception on wrong input


    Args:
        (string): ts_name - time series name
        (string): bottom_ts_name - time series name
        (string): period - time series name
    Return:
        (dict): {top_ts_name:period}

    :param timeline_manager:
    :param tree:
    :return:
    """

    with pytest.raises(Exception):
        timeline_manager.get_timeline_tree("hour", "month", ["2012", "2013"])


def test_get_timeline_tree_raise_exception_type_error(timeline_manager):
    """Test for get_timeline_tree(self, timeline_manager, tree) method
    Check exception on wrong input


    Args:
        (string): ts_name - time series name
        (string): bottom_ts_name - time series name
        (string): period - time series name
    Return:
        (dict): {top_ts_name:period}

    :param timeline_manager:
    :param tree:
    :return:
    """

    with pytest.raises(Exception):
        timeline_manager.get_timeline_tree(["hour"], ["month"], [1, 2, 3, 4])