import pytest
import json

from conf_test import interface_backup
from conf_test import backup as entity_data_backup
from tests.test_data import backup, data, time_line_manager, entity_data
from iap.forecasting.workbench.container.cont_interface import *
from iap.common.helper import Meta

@pytest.fixture
def container():
    """Fixture for Container class object

    Return:
        (Container)

    :return:
    """
    _container = Container()
    _container.load(interface_backup)
    return _container


@pytest.fixture
def entity(container):
    """Fixture for Entity class object

    Return:
        (Container)

    :return:
    """
    entity = container.get_entity_by_id(4)
    return entity


@pytest.fixture
def period_series(entity_data):
    """Fixture for PeriodSeries class object

    Return:
        (Container)

    :return:
    """
    entity_data.load_backup(entity_data_backup)
    _period_series = PeriodSeries(entity_data, 'Sales', 'annual')
    return _period_series


@pytest.fixture
def timeseries(entity_data):
    """Fixture for timeseries

    :param entity_data:
    :return:

    """
    entity_data.load_backup(entity_data_backup)
    _timeseries = TimeSeries(entity_data, 'Sales', 'annual')
    return _timeseries


@pytest.fixture
def scalar(entity_data):
    """Fixture for scalar

    :param entity_data:
    :return:

    """

    entity_data.load_backup(entity_data_backup)
    _scalar = Scalar(entity_data, 'Loan', 'annual')
    return _scalar


def test_period_series_get_periods(period_series):
    """Test for method get_periods method
    Check whether expected and output value equal

    :param period_series:
    :return:

    """

    expected = [('2012', '2013'), ('2013', '2014'), ('2014', '2015'), ('2015', '2016'), ('2016', '2017'), ('2017', '2018')]
    actual = period_series.get_periods()
    assert sorted(expected, key=lambda el: el[0]) == sorted(actual, key=lambda el: el[0])


def test_period_series_get_value(period_series):
    """Test for method get_period_value
    Check whether expected and output value equal
    change

    :param period_series

    """

    expected = 2
    actual = period_series.get_value(('2014', '2015'))
    assert expected == actual

    expected = 3
    actual = period_series.get_value(('2015', '2016'))
    assert expected == actual

    expected = 0
    actual = period_series.get_value(('2012', '2013'))
    assert  expected == actual


def test_period_series_set_value(period_series):
    """Test for method set_period_value
    Check whether get method return tha same value as set have been
    change

    """

    period_series.set_value(('2012', '2013'),100)
    actual = period_series.get_value(('2012', '2013'))
    expected = 100
    assert expected == actual

    period_series.set_value(('2014', '2015'), 10)
    actual = period_series.get_value(('2014', '2015'))
    expected = 10
    assert expected == actual

    period_series.set_value(('2016', '2017'), 100)
    actual = period_series.get_value(('2016', '2017'))
    expected = 100
    assert expected == actual
