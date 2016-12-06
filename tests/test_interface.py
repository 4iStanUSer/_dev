import pytest
import json

from conf_test import interface_backup as backup

from iap.forecasting.workbench.container.interface import Container,Entity
from iap.forecasting.workbench.container.timelines import TimeLineManager
from iap.forecasting.workbench.container.entity_data import EntityData
from iap.forecasting.workbench.container.entities_hierarchy import Node


@pytest.fixture
def container():
    _container = Container()
    print(backup)
    _container.load(backup)
    return _container

def test_container_save(container, backup):
    '''
    Test for save method

    :param container:
    :param backup:
    :return:

    '''
    print(backup['timeline'])
    assert container.save() == backup

def test_container_clean(container):

    assert container._node_dict == {}
    assert container._root.children == []
    assert container._max_node_id ==0

def test_container_add_entity(container, backup):
    pass

def test_container_get_entity_by_id():
    pass

def test_container_get_entity_by_path(container):

    print(container.get_entity_by_path(['Ukraine']))
    print(container.get_entity_by_path(['Ukraine']))
    print(container.get_entity_by_path(['Ukraine']))
    print(container.get_entity_by_path(['Ukraine']))

def test_container_get_entity_by_meta():
    pass



##Entity

##Variable

##TimeSeries

##Scalar

##PeriodSeries

