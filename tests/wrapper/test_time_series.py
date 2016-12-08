import pytest
import json

from conf_test import interface_backup
from conf_test import backup as entity_data_backup
from test_data import backup, data, time_line_manager, entity_data
from iap.forecasting.workbench.container.cont_interface import *
from iap.common.helper import Meta

@pytest.fixture
def container():
    _container = Container()
    _container.load(interface_backup)
    return _container


@pytest.fixture
def entity(container):
    entity = container.get_entity_by_id(4)
    return entity


@pytest.fixture
def period_series(entity_data):
    entity_data.load_backup(entity_data_backup)
    _period_series = PeriodSeries(entity_data, 'Sales', 'annual')
    return _period_series


@pytest.fixture
def timeseries(entity_data):
    """Fixture for Timeseries class object

    :param entity_data:
    :return:

    """
    entity_data.load_backup(entity_data_backup)
    _timeseries = TimeSeries(entity_data, 'Sales', 'annual')
    return _timeseries


def test_timeseries_get_value(timeseries):
    """Test for method get value

    Args:
        (string): timestamp in timeseries

    Return:
        (obj): list of value for timestamp

    :param _timeseries:
    :return:

    """

    expected = [0, 1]
    actual = timeseries.get_value('2012')
    assert expected == actual

    expected = [3, 4]
    actual = timeseries.get_value('2015')
    assert expected == actual

    expected = [4, 5]
    actual = timeseries.get_value('2016')
    assert expected == actual

    expected = [5, 0]
    actual = timeseries.get_value('2017')
    assert expected == actual

    expected = [0]
    actual = timeseries.get_value('2018')
    assert expected == actual


def test_timeseries_get_value_raise_exception(timeseries):
    with pytest.raises(Exception):
        timeseries.get_value('0000')


def test_timeseries_get_values_from(timeseries):
    """Test for method get value from

    Args:
        (string): timestamp in timeseries
        (int): length of inderval in timeseries

    Return:
        (list): list of value for specific time period

    :param timeseries:
    :return:

    """
    expected = [0, 1]
    actual = timeseries.get_values_from('2012', 1)
    assert expected == actual

    expected = [3, 4, 5]
    actual = timeseries.get_values_from('2015', 2)
    assert expected == actual

    expected = [2, 3, 4]
    actual = timeseries.get_values_from('2014',2)
    assert expected == actual


def test_timeseries_get_values_from_raise_exception(timeseries):
    with pytest.raises(Exception):
        timeseries.get_values_from('111111',2)


def test_timeseries_get_values_for_period(timeseries):
    """Test for get_value_from

    :param _timeseries:
    :return:

    """
    expected = [0,1]
    actual = timeseries.get_values_for_period(('2012', '2013'))
    assert expected == actual

    expected = [3, 4]
    actual = timeseries.get_values_for_period([('2015', '2016'), ('2016', '2017')])
    assert expected == actual

    expected = [3, 4, 5]
    actual = timeseries.get_values_for_period([('2015', '2016'), ('2016', '2017'),
                                        ('2017','2018')])
    assert expected == actual


def test_timeseries_get_values_for_period_raise_exception(timeseries):
    with pytest.raises(Exception):
        timeseries.get_values_for_period(('Monday', 'Friday'))


def test_timeseries_set_value(timeseries):
    """Test for get_value_from

    :param _timeseries:
    :return:

    """
    expected = [0]
    actual = timeseries.set_value(('2012', '2013'),1)
    assert expected == actual

    expected = [3, 4]
    actual = timeseries.set_value(('2015', '2016'), 4)
    assert expected == actual

    expected = [3, 4, 5]
    actual = timeseries.set_value(('2016', '2017'), 10)
    assert expected == actual


def test_timeseries_set_value_raise_exception(timeseries):
    with pytest.raises(Exception):
        timeseries.set_value(('Monday', 'Friday'),110)


def test_timeseries_set_value_from(timeseries):
    """Test for get_value_from

    :param _timeseries:
    :return:

    """
    expected = [1]
    timeseries.set_values_from([1], ('2012', '2013'))
    actual = timeseries.get_values_for_period(('2012', '2013'))
    assert expected == actual

    expected = [3, 4]
    timeseries.get_values_from([3, 4], ('2016', '2017'))
    actual = timeseries.get_values_for_period(('2016', '2017'))
    assert expected == actual

    expected = [5, 6]
    timeseries.get_values_from([5,6],('2017', '2018'))
    actual = timeseries.get_values_for_period(('2017', '2018'))
    assert expected == actual


def test_timeseries_set_value_raise_exception(timeseries):
    with pytest.raises(Exception):
        timeseries.get_values_for_period(('Monday', 'Friday'))
