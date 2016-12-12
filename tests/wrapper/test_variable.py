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
def variable(entity_data):
    entity_data.load_backup(entity_data_backup)
    _variable = Variable(entity_data, "Sales")
    return _variable


@pytest.fixture
def timeseries(entity_data):
    """Fixture for Timeseries class object

    :param entity_data:
    :return:

    """
    entity_data.load_backup(entity_data_backup)
    _timeseries = TimeSeries(entity_data, 'Sales', 'annual')
    return _timeseries


@pytest.fixture
def scalar(entity_data):
    """Fixture for Scalar class object

    :param entity_data:
    :return:

    """

    entity_data.load_backup(entity_data_backup)
    _scalar = Scalar(entity_data, 'Loan', 'annual')
    return _scalar



def test_variable_get_property(variable):
    """Test for method get_property

    :param variable:
    :return:
    """
    expected = '1000'
    actual = variable.get_property('total')
    assert expected == actual


def test_variable_get_property_raise_exception(variable):
    """Test for method get_property

    :param variable:
    :return:
    """
    expected = None
    actual = variable.get_property('untotal')
    assert expected == actual

def test_variable_set_property(variable):
    """Test for method get_property

    :param variable:
    :return:
    """
    variable.set_property('total', 1000)
    actual = variable.get_property('total')
    expected = 1000
    assert expected == actual


def test_variable_get_time_series(variable, timeseries):

    expected = timeseries
    actual = variable.get_time_series("annual")
    assert expected._ts_name == actual._ts_name


def test_variable_get_time_series_raise_exception(variable):

    expected = variable.get_time_series('seconds')
    actual = None
    assert expected == actual


def test_variable_get_scalar(variable, scalar):

    actual = variable.get_scalar('annual')
    expected = scalar
    assert actual._ts_name == expected._ts_name


def test_variable_get_scalar_raise_exception(variable):

    expected = None
    actual =  variable.get_time_series('seconds')
    assert expected == actual


def test_variable_get_periods_series(variable, period_series):

    expected = period_series
    actual = variable.get_periods_series('annual')
    assert actual._ts_name == expected._ts_name


def test_variable_get_periods_series_raise_exception(variable):

    expected = None
    actual = variable.get_periods_series('seconds')
    assert expected == actual


def test_variable_add_time_series(variable, timeseries):

    variable.add_time_series('month')
    actual = variable.get_time_series('month')
    expected = "month"
    assert actual._ts_name == expected


def test_add_scalar(variable):

    variable.add_scalar('month')
    actual = variable.get_scalar('month')
    expected = "month"
    assert actual._ts_name == expected


def test_add_period_series(variable):

    variable.add_periods_series('month')
    actual = variable.get_periods_series('month')
    expected = "month"
    assert actual._ts_name == expected