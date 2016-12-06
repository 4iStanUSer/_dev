import pytest
import json

from conf_test import interface_backup as backup

from iap.forecasting.workbench.container.interface import Container,Entity
from iap.forecasting.workbench.container.timelines import TimeLineManager
from iap.forecasting.workbench.container.entity_data import EntityData
from iap.forecasting.workbench.container.entities_hierarchy import Node
from iap.common.helper_lib import Meta,is_equal_meta

@pytest.fixture
def container():
    _container = Container()
    _container.load(backup)
    return _container



#####Entity
@pytest.fixture
def entity(container):
    entity = container.get_entity_by_id(4)
    return entity

def test_property(entity):

    assert entity._node.id == 4
    assert entity._node.name == "Candy"
    assert entity._node.parents
    assert entity._node.children
    assert entity._node.path
    assert entity._node.meta

def test_setter():
    pass

def test_add_child(entity):

    name = "Test"
    meta = Meta("Test","Test")
    entity.add_child(name, meta)

    assert name in [child.name for child in entity.children]
    assert [meta['dimension'],meta['level']] in [[child.meta['dimension'], child.meta['level']]
                                               for child in entity.children]

def test_get_parent_by_meta(entity):
    expected = ['Ukraine']
    actual = entity.get_parent_by_meta()


def variables(entity):
    print(entity.variables)
    expected = []
    actual = entity.variables
    assert expected == actual

def get_variable(entity):
    pass

def add_variable(entity):
    pass

def add_insights(entity):
    pass

#######Variable

def test_variable():
    pass

def test_variable_properies():
    pass

def test_get_periods_series():
    pass

def test_add_time_series():
    pass

def test_add_periods_series():
    pass

######TimeSeries

def test_timeseries_init():
    pass

def test_timeseries_get_value():
    pass

def test_timeseries_get_value_from():
    pass

def test_get_values_for_period():
    pass

def test_set_value():
    pass

def test_set_value_from():
    pass

#####Scalar

def test_scalar_init():
    pass

def test_scalar_get_value():
    pass

def test_scalar_set_value():
    pass

######PeriodSeries

def period_series():
    pass

def test_period_series_init():
    #initialise and chekc attributes
    pass

def test_period_series_get_periods():
    #check method corespondence
    pass

def test_period_series_get_value():
    #check value corespondence
    pass

def test_period_series_set_value():
    #check set_value input and output corespondence
    pass

######Variable

def test_variable_init():
    pass

def test_variable_set_property():
    pass

def test_variable_get_time_series():
    pass

def test_vatiable_get_scalars():
    pass

def test_variable_get_periods_series():
    pass

def test_add_time_series():
    pass

def add_scalar():
    pass

def add_period_series():
    pass
