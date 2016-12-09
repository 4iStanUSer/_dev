import pytest
from conf_test import interface_backup as backup
from iap.forecasting.workbench.container.cont_interface import Container
from iap.common.helper import Meta

@pytest.fixture
def container():
    _container = Container()
    _container.load(backup)
    return _container


def test_container_save(container):
    """Test for save method.
    get all attributes ad fill dictionary

    Args:

    Return:
        (dict):backup :{'timeline': ,'container':}

    :return:

    """

    actual = container.get_backup()
    expected = backup
    assert len(actual['container']) == len(expected['container'])
    assert actual.keys() == expected.keys()


def test_container_clean(container):
    """Test for method container_clean
    check if all atribute has zero state or empty

    Args:

    Return:

    :param container:
    :return:

    """

    container._clean()

    assert container._nodes_dict == {}

    assert container._root.name == 'root'

    assert container._max_node_id == 0


def test_container_get_entity_by_path(container):
    """Test for method get_entity_by_path, check whether
    output entity has the same attribute coresponding node

    Args:
        (string): path of node
    Return:
        (Entity): coresponding Entity


    """

    actual = container.get_entity_by_path(['Ukraine']).path
    expected = ['Ukraine']
    assert actual == expected

    #actual = [container.get_entity_by_path(['Ukraine']).meta['dimension'],
              #container.get_entity_by_path(['Ukraine']).meta['level']]
    #expected = ["Geo", "Country"]
    #assert actual == expected

    actual = container.get_entity_by_path(['Ukraine', 'Odessa']).path
    expected = ['Ukraine', 'Odessa']
    assert actual == expected

    #actual = [container.get_entity_by_path(['Ukraine', 'Odessa']).meta['dimension'],
              #container.get_entity_by_path(['Ukraine', 'Odessa']).meta['level']]
    #expected = ["Geo", "Region"]
    #assert actual == expected

    actual = container.get_entity_by_path(['Ukraine', 'Kiev']).path
    expected = ['Ukraine', 'Kiev']
    assert actual == expected

    #actual = [container.get_entity_by_path(['Ukraine', 'Kiev']).meta['dimension'],
              #container.get_entity_by_path(['Ukraine', 'Kiev']).meta['level']]
    #expected = ['Geo', 'Region']
    #assert actual == expected

    actual = container.get_entity_by_path(['Ukraine', 'Kiev', 'Candy']).path
    expected = ['Ukraine', 'Kiev', 'Candy']
    assert actual == expected

    #actual = [container.get_entity_by_path(['Ukraine', 'Kiev', 'Candy']).meta['dimension'],
    #         container.get_entity_by_path(['Ukraine', 'Kiev', 'Candy']).meta['level']]
    #expected = ["Food", "Delicios"]
    #assert actual == expected


def test_container_get_entity_by_path_raise_exception_wrong_value(container):
    """Test for method get_entity_by_path
    Check raising exception on wrong input

    Args:
        (string): path of node
    Return:
        (Entity): coresponding Entity


    """
    actual = None
    expected = container.get_entity_by_path(['USA'])
    assert actual == expected


def test_top_entities(container):
    """Test for get tope_entities
    """

    top_entities = container.top_entities
    expected = ["Ukraine"]
    actual = [entity.name for entity in top_entities]
    assert expected == actual


def test_container_get_entity_by_meta(container):
    """Test for method get entity by meta of coresponding Node

    Args:
        (list): meta_filter
        (top-entity): Top entity

    Return:
        (list): list of Entity

    """

    top_entity = container.top_entities[0]
    meta = Meta('Geo', 'Country')
    entities = container.get_entities_by_meta(meta, top_entity)

    expected = ['Ukraine'].sort()
    actual = [entity._node.name for entity in entities].sort()
    assert expected == actual

    top_entity = container.top_entities[0]
    meta = Meta('Geo', 'Region')
    entities = container.get_entities_by_meta(meta, top_entity)

    expected = ['Kiev','Odessa'].sort()
    actual = [entity._node.name for entity in entities].sort()
    assert expected == actual

    top_entity = container.top_entities[0]
    meta = Meta('Food', 'Delicios')
    entities = container.get_entities_by_meta(meta, top_entity)

    expected = ['Candy'].sort()
    actual = [entity._node.name for entity in entities].sort()
    assert expected == actual


def test_container_get_entity_by_meta_raise_exception_wrong_value(container):
    """Test for method get entity by meta of coresponding Node
    Check raising exception on wrong value

    Args:
        (list): meta_filter
        (top-entity): Top entity

    Return:
        (list): list of Entity

    """

    top_entity = container.top_entities[0]
    meta = Meta('Ukraine', 'Kiev')
    expected = []
    actual = container.get_entities_by_meta(meta, top_entity)


def test_container_get_entity_by_meta_raise_exception_wrong_type(container):
    """Test for method get entity by meta of coresponding Node
    Check raising exception on wrong type

    Args:
        (list): meta_filter
        (top-entity): Top entity

    Return:
        (list): list of Entity

    """

    top_entity = ['top_entity']
    meta = ['Ukraine', 'Kiev']

    with pytest.raises(Exception):
        container.get_entities_by_meta(meta, top_entity)


def test_add_entity(container):
    """Test for method add_entity:
    Add node by path to the root node,
    add new node to the _node_dict.

    Args:
        (string): path
        (list): list of metadata

    :return:

    """

    expected = ['Ukraine', 'Kiev', 'Delicios', 'Shop']
    expected_id = 6
    metas = [["Geo", "Country"], ["Geo", "Region"], ["Food", "Delicios"], ['Market', 'Small']]
    actual = container.add_entity(['Ukraine', 'Kiev', 'Delicios', 'Shop'], metas)

    assert actual.name == expected[-1]
    assert actual.id == expected_id


    expected = ['Ukraine', 'Kiev', 'Delicios', 'Supermarket']
    expected_id = 7
    metas = [["Geo", "Country"], ["Geo", "Region"], ["Food", "Delicios"],['Market', 'Small']]
    actual = container.add_entity(['Ukraine', 'Kiev', 'Delicios', 'Supermarket'], metas)

    assert actual.name == expected[-1]
    assert actual.id == expected_id


def test_add_entity_raise_exception_wrong_type(container):
    """Test for method add_entity:
    Add node by path to the root node,
    add new node to the _node_dict.

    Args:
        (string): path
        (list): list of metadata


    :return:

    """

    metas = [{"Geo":"Country"}, {"Market": "Supermarket"}, {"Geo": "Country"}, {'Market': 'Small'}]

    path  = "Ukraine, Kiev, Ukraine, Supermarket"

    with pytest.raises(Exception):
        container.add_entity(path, metas)
