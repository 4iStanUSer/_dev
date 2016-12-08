import pytest
import json

from conf_test import interface_backup
from conf_test import backup as entity_data_backup
from test_data import backup, data, time_line_manager, entity_data
from iap.forecasting.workbench.container.interface import *
from iap.common.helper_lib import Meta

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

######PeriodSeries
def test_period_series_get_periods(period_series):
    #check method corespondence
    expected = []
    actual = period_series.get_periods()
    assert  expected == actual


def test_period_series_get_value(period_series):
    #check method corespondence
    expected = []
    actual = period_series.get_value(('2014', '2015'))
    assert  expected == actual

    expected = []
    actual = period_series.get_value(('2014', '2015'))
    assert  expected == actual

    expected = []
    actual = period_series.get_value(('2014', '2015'))
    assert  expected == actual


def test_period_series_set_value(period_series):
    expected = []
    actual = period_series.set_value(('2012,2013'),100)
    assert  expected == actual


@pytest.fixture
def scalar(entity_data):
    """Fixture for scalar

    :param entity_data:
    :return:

    """

    entity_data.load_backup(entity_data_backup)
    _scalar = Scalar(entity_data, 'Loan', 'annual')
    return _scalar


def test_scalar_get_value(scalar):
    """Test scalar method get value

    :return:

    """
    expected = 10
    actual = scalar.get_value()
    assert expected == actual


def test_scalar_set_value(scalar):
    """Test for scalar method set value

    :return:

    """

    expected = 10
    scalar.set_value(10)
    actual = scalar.get_value()
    assert expected == actual


def test_scalar_set_value_raise_exception(scalar):
    """Test scalar method get value
    Check exception on wrong input

    :return:

    """
    with pytest.raises(Exception):
        scalar.set_value({"value":"value"})

@pytest.fixture
def timeseries(entity_data):
    """Fixture for timeseries

    :param entity_data:
    :return:

    """
    entity_data.load_backup(entity_data_backup)
    _timeseries = TimeSeries(entity_data, 'Sales', 'annual')
    return _timeseries


def test_timeseries_get_value(timeseries):
    """Test for method get value

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
    actual = timeseries.get_value('2017')
    assert expected == actual


def test_timeseries_get_values_from(timeseries):
    """Test for get_value_from

    :param _timeseries:
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


def test_timeseries_get_values_for_period(timeseries):
    """Test for get_value_from

    :param _timeseries:
    :return:

    """
    expected = [0]
    actual = timeseries.get_values_for_period(('2012', '2013'))
    assert expected == actual

    expected = [3, 4]
    actual = timeseries.get_values_for_period(('2015', '2016'), ('2016', '2017'))
    assert expected == actual

    expected = [3, 4, 5]
    actual = timeseries.get_values_for_period(('2015', '2016'), ('2016', '2017'),
                                        ('2017','2018'))
    assert expected == actual


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


def test_timeseries_set_value_from(timeseries):
    """Test for get_value_from

    :param _timeseries:
    :return:

    """
    expected = [0]
    actual = timeseries.set_values_from([1], ('2012', '2013'))
    assert expected == actual

    expected = [3, 4]
    actual = timeseries.get_values_from([3, 4], ('2016', '2017'))
    assert expected == actual

    expected = [3, 4, 5]
    actual = timeseries.get_values_from([5,6],('2017','2018'))
    assert expected == actual


#Test for Variable

@pytest.fixture
def variable(entity_data):
    entity_data.load_backup(entity_data_backup)
    _variable = Variable(entity_data, "Sales")
    return _variable


def test_variable_get_property(variable):

    expected = {'total':1000}
    actual = variable.get_property('total')
    assert expected == actual


def test_variable_get_property_raise_exception(variable):

    expected = {'total': 100}
    actual = variable.get_property('untotal')
    assert  expected == actual


def test_variable_set_property(variable):

    expected = {'total':1000}
    actual = variable.set_property('total', 100)
    assert expected == actual


def test_variable_set_property_raise_exception(variable):

    expected = {'total': 100}
    actual = variable.set_property('untotal', 10)
    assert  expected == actual


def test_variable_get_time_series(variable):
    #TODO
    expected = []
    actual = variable.get_time_series("annual")
    assert expected == actual


def test_variable_get_time_series_raise_exception(variable):
    #TODO
    expected = []
    actual = variable.get_time_series("month")
    assert expected == actual


def test_variable_get_scalar(variable):

    scalar =  variable.get_scalar("annual")
    actual = [scalar.name, scalar.propertie]
    expected = ['Sales', {'total':1000}]

    assert actual == expected


def test_variable_get_periods_series(variable):
    #TODO - compare data
    period_series = variable.get_periods_series('annual')
    actual = [period_series._var_name, period_series._ts_name]
    expected = ['Sales', 'annua;']
    assert actual == expected


def test_variable_add_time_series(variable):
    pass


def test_add_scalar(variable):
    pass

def test_add_perio_series(variable):
    pass