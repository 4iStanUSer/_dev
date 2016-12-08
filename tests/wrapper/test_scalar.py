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
    entity_data.load_backup(entity_data_backup)
    _period_series = PeriodSeries(entity_data, 'Sales', 'annual')
    return _period_series


@pytest.fixture
def scalar(entity_data):
    """Fixture for Scalar class object

    :param entity_data:
    :return:

    """

    entity_data.load_backup(entity_data_backup)
    _scalar = Scalar(entity_data, 'Loan', 'annual')
    return _scalar


def test_scalar_get_value(scalar):
    """Test scalar method get value
    Check whether expected value equal to the output
    :return:

    """
    expected = 10
    actual = scalar.get_value()
    assert expected == actual


def test_scalar_set_value(scalar):
    """Test for scalar method set value
    Check whether expected value equal to the output
    Args:
        (object): input value of scalar

    :return:

    """
    expected = 10
    scalar.set_value(10)
    actual = scalar.get_value()
    assert expected == actual

