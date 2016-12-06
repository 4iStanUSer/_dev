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


def test_container_save(container):
    '''
    Test for save method

    :param container:
    :param backup:
    :return:

    '''
    actual = container.save()
    expected = backup
    assert len(actual['container']) == len(expected['container'])
    assert actual.keys() == expected.keys()


def test_container_clean(container):
    '''Test for method container_clean
    check wether all atribute has zero state or empty

    :param container:
    :return:

    '''

    assert container._nodes_dict == {}

    assert container._root.children == []

    assert container._max_node_id ==0

def test_container_clean_1(container):
    assert container._nodes_dict == {}

    assert container._root.children == []

    assert container._max_node_id == 10

def test_container_get_entity_by_id(container):


    assert container.get_entity_by_id(1).id ==1

    assert container.get_entity_by_id(2).id ==2

    assert container.get_entity_by_id(3).id ==3

    assert container.get_entity_by_id(10).id == 10

#Test for container.get_entity_by_path
def test_container_get_entity_by_path(container):

    assert container.get_entity_by_path(['Ukraine']).path == ['Ukraine']
    assert container.get_entity_by_path(['Ukraine']).metas == ['Geo', 'Country']

def test_container_get_entity_by_path_1(container):

    assert container.get_entity_by_path(['Ukraine', 'Odessa']).path == ['Ukraine', 'Odessa']
    assert container.get_entity_by_path(['Ukraine', 'Odessa']).meta == ["Geo", "Region"]

def test_container_get_entity_by_path_2(container):

    assert container.get_entity_by_path(['Ukraine', 'Kiev']).path == ['Ukraine', 'Kiev']
    assert container.get_entity_by_path(['Ukraine', 'Kiev']).meta == ["Geo", "Region"]

def test_container_get_entity_by_path_3(container):

    actual = container.get_entity_by_path(['Ukraine', 'Kiev', 'Candy']).path
    expected = ['Ukraine', 'Kiev', 'Candy']
    assert  actual.path == expected

    actual =  container.get_entity_by_path(['Ukraine', 'Kiev', 'Candy']).meta
    expected = ["Food", "Delicios"]
    assert actual == expected

def test_top_entities(container):
    '''Test for get tope_entities'''
    top_entities = container.top_entities
    expected = ["Ukraine"]
    actual = [entity.name for entity in top_entities]

def test_top_entities_1(container):
    '''Test for get tope_entities'''
    top_entities = container.top_entities
    expected = ["Ukraine","Kiev"]
    actual = [entity.name for entity in top_entities]

def test_container_get_entity_by_meta(container):

    top_entity = container.top_entities[0]
    meta = Meta('Geo', 'Country')
    entities = container.get_entities_by_meta(meta, top_entity)

    expected = ['Ukraine'].sort()
    actual = [entity._node.name for entity in entities].sort()
    assert expected == actual

def test_container_get_entity_by_meta_1(container):

    top_entity = container.top_entities[0]
    meta = Meta('Geo', 'Region')
    entities = container.get_entities_by_meta(meta, top_entity)

    expected = ['Kiev','Odessa'].sort()
    actual = [entity._node.name for entity in entities].sort()
    assert expected == actual

def test_container_get_entity_by_meta_2(container):

    top_entity = container.top_entities[0]
    meta = Meta('Food', 'Delicios')
    entities = container.get_entities_by_meta(meta, top_entity)

    expected = ['Candy'].sort()
    actual = [entity._node.name for entity in entities].sort()
    assert expected == actual

def test_add_entity(container):

    expected = ['Ukraine','Kiev','Delicios','Shop']
    expected_id = 6
    metas = [["Geo", "Country"], ["Geo", "Region"], ["Food", "Delicios"],['Market','Small']]
    actual = container.add_entity(['Ukraine','Kiev','Delicios','Shop'], metas)

    assert actual.name == expected[-1]
    assert actual.id == expected_id

def test_add_entity_1(container):

    expected = ['USA','Kiev','Delicios','Supermarket']
    expected_id = 5
    metas = [["Geo", "Country"], ["Geo", "Region"], ["Food", "Delicios"],['Market','Small']]
    actual = container.add_entity(['Ukraine','Kiev','Delicios','Supermarket'], metas)

    assert actual.name == expected[-1]
    assert actual.id == expected_id