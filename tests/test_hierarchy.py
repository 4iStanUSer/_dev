from iap.forecasting.workbench.container.entities_hierarchy import Node
from iap.common.helper_lib import Meta
import pytest


import json
input_data = open('json/hierarchy.json').read()
data = json.loads(input_data)


@pytest.fixture
def description():
    '''Get description data

    :return:

    '''
    description = data['description']
    # meta information about each node
    return description


@pytest.fixture
def list_of_pathes():
    '''Get pathes data

    :return:

    '''
    l = []
    for i in data['path']:
        l.insert(i['id'], i['node'])
    return l


@pytest.fixture
def graph():
    '''Get graph data

    :return:

    '''
    return data['graph']


#encoded list of pathes
ENCODED_PATH = {}
#list of nodes
LIST_OF_NODES = {}


def setup_function(function):
    '''Fixture executed before each function start

    :param function:
    :return:

    '''
    list_of_nodes = {}
    ENCODED_PATH.clear()


def teardown_function(function):
    '''Fixture executed before each function end

    :param function:
    :return:

    '''
    LIST_OF_NODES.clear()
    ENCODED_PATH.clear()


def encode_list_of_pathes_into_node(root_node, list_of_pathes, description):
    '''Function serialise json list of pathes into Node object root_node

    :param root_node: root node
    :param list_of_pathes: list of pathes in graph
    :param description: meta data of each node
    :return:

    '''

    for path in list_of_pathes:
        new_nodes = []
        depth = 0
        metas = []
        for node_name in path:
            metas.append(Meta(description[node_name][0], description[node_name][1]))
        new_node = root_node.add_node_by_path(path, metas, depth, new_nodes)
        new_node.id = list_of_pathes.index(path)
        LIST_OF_NODES[new_node.id] = new_node
    return list_of_pathes


def encode(root_node, path):
    """Inteface for de encode_list_of_pathes_into_node

    :param root_node:
    :param path:
    :return:

    """

    LIST_OF_NODES = {}
    encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
    return LIST_OF_NODES


def decode(root_node, path):
    """Inteface for de decode_node_into_list_of_pathes

    :param root_node:
    :param path:
    :return:

    """

    ENCODED_PATH = {}
    decode_node_into_list_of_pathes(root_node, path)
    return ENCODED_PATH


def decode_node_into_list_of_pathes(root_node, path):
    '''Deserialise graph structure of root_node into list of pathes

    :param root_node: root node
    :param path: list that contain hitory of path traversing
    :return:

    '''

    for node in root_node.children:
        new_path = path[:]
        new_path.append(node.name)
        ENCODED_PATH[node.id] = new_path
        decode_node_into_list_of_pathes(node, new_path)


def decode(root_node, path):
    """Inteface for de decode_node_into_list_of_pathes

    :param root_node:
    :param path:
    :return:

    """

    ENCODED_PATH = {}
    decode_node_into_list_of_pathes(root_node, path)
    return ENCODED_PATH


def test_preparation(description, list_of_pathes):
    '''Test for encoding_ and decoding functions

     first step function serialise json in node
     next step in deserialise node struncture in list of pathes
     matcher check if input and output list_of_pathes and encoded_list equal

    :param list_of_pathes:
    :param description:
    :return:

    '''

    root_node = Node('root', (None, None))
    encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
    decode_node_into_list_of_pathes(root_node, path=[])

    assert list_of_pathes == [val for val in ENCODED_PATH.values()]


def test_add_child(list_of_pathes, description):
    '''Test for add_child(self,name,meta)

    Input cutted tree - without last element
    Output root node with added elements

    :param list_of_pathes:
    :param description:
    :return:

    '''

    def add_child(name):
        depth = len(list_of_pathes)-2
        tree = list_of_pathes[:-1]
        root_node = Node('root', (None, None))
        encode_list_of_pathes_into_node(root_node, list_of_pathes[:-1], description)
        last_node = LIST_OF_NODES[depth]
        last_node.add_child(name, Meta(description[name][0], description[name][1]))
        last_node.children[-1].id = depth+1
        return root_node

    decode_node_into_list_of_pathes(add_child("Number"), path=[])
    actual = [val for val in ENCODED_PATH.values()]
    expected = list_of_pathes
    assert actual.sort() == expected.sort()


def test_add_child_raise_exception_value_error(list_of_pathes, description):
    '''Test for add_child(self,name,meta)
    Check raising exception on wrong value of input

    Input cutted tree - without last element
    Output root node with added elements

    :param list_of_pathes:
    :param description:
    :return:

    '''

    def add_child(name):
        depth = len(list_of_pathes)-2
        tree = list_of_pathes[:-1]
        root_node = Node('root', (None, None))
        encode_list_of_pathes_into_node(root_node, list_of_pathes[:-1], description)
        last_node = LIST_OF_NODES[depth]
        last_node.add_child(name, Meta(description[name][0], description[name][1]))
        last_node.children[-1].id = depth+1
        return root_node

    with pytest.raises(Exception):
        add_child(['Kiev', 'Odessa'])


def test_add_child_raise_exception_type_error(list_of_pathes, description):
    '''Test for add_child(self,name,meta)
    Check raising exception on wrong type of input

    Input cutted tree - without last element
    Output root node with added elements


    :param list_of_pathes:
    :param description:
    :return:

    '''

    def add_child(name):
        depth = len(list_of_pathes)-2
        tree = list_of_pathes[:-1]
        root_node = Node('root', (None, None))
        encode_list_of_pathes_into_node(root_node, list_of_pathes[:-1], description)
        last_node = LIST_OF_NODES[depth]
        last_node.add_child(name, Meta(description[name][0], description[name][1]))
        last_node.children[-1].id = depth+1
        return root_node

    with pytest.raises(Exception):
        add_child('Reseller')


def test_get_node_by_path(list_of_pathes, description):

    '''Test for  method get_node_by_path(self,path)

    Input: path
    Output: node's name
    Expected: names equality

    :param list_of_pathes:
    :param description:
    :return:

    '''

    def get_node_by_path(path):
        root_node = Node('root', (None, None))
        encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
        output_node = root_node.get_node_by_path(path)
        return output_node

    actual_id = get_node_by_path(['Ukraine']).id
    expected_id = 0
    assert actual_id == expected_id

    actual_id = get_node_by_path(["Ukraine", "Odessa", "Wine", "Market", "Silpo"]).id
    expected_id = 16
    assert actual_id == expected_id

    actual_id = get_node_by_path(['Ukraine', 'Kiev']).id
    expected_id = 1
    assert actual_id == expected_id

    actual_id = get_node_by_path([]).id
    expected_id = 0
    assert actual_id == expected_id


def test_get_node_by_path_raise_exception_value_error(list_of_pathes, description):
    '''Test for  method get_node_by_path(self,path)
    Check raising exception on wrong value of input

    Input: path
    Output: node's name
    Expected: names equality

    :param list_of_pathes:
    :param description:
    :return:

    '''

    def get_node_by_path(path):
        root_node = Node('root', (None, None))
        encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
        output_node = root_node.get_node_by_path(path)
        return output_node

    with pytest.raises(Exception):
        get_node_by_path(["Ukraine", "Odessa", "Wine", "Market", "Supermarket"])


def test_get_node_by_path_raise_exception_type_error(list_of_pathes, description):
    '''Test for  method get_node_by_path(self,path)
    Check raising exception on wrong type of input

    Input: path
    Output: node's name
    Expected: names equality

    :param list_of_pathes:
    :param description:
    :return:

    '''

    def get_node_by_path(path):
        root_node = Node('root', (None, None))
        encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
        output_node = root_node.get_node_by_path(path)
        return output_node

    with pytest.raises(Exception):
        get_node_by_path("Supermarket")


def test_get_children_by_meta(list_of_pathes, description):
    '''Test for method get_children_by_meta(self,meta_filter,node_ids)

    Input: meta filter
    Output: meta data of founded node by input filter
    Expected: meta data equality

    :return:

    '''

    def get_children_by_meta(meta, nodes_ids):
        root_node = Node('root', (None, None))
        encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
        node_ids = []
        meta_filter = Meta(meta[0], meta[1])
        output_node = root_node.get_children_by_meta(meta_filter, node_ids)
        return node_ids

    actual = get_children_by_meta(["Geo", "Region"], nodes_ids=[])
    expected = [1, 2, 3]
    assert actual == expected

    actual = get_children_by_meta(["Reseller", "Market"], nodes_ids=[])
    expected = [9, 10, 12]
    assert actual == expected


def test_get_children_by_meta_exception_value_error(list_of_pathes, description):
    '''Test for method get_children_by_meta(self,meta_filter,node_ids)
    Check raising exception on wrong value of input

    Input: meta filter
    Output: meta data of founded node by input filter
    Expected: meta data equality

    :return:

    '''

    def get_children_by_meta(meta, nodes_ids):
        root_node = Node('root', (None,None))
        encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
        node_ids = []
        meta_filter = Meta(meta[0], meta[1])
        output_node = root_node.get_children_by_meta(meta_filter, node_ids)
        return node_ids

    with pytest.raises(Exception):
        get_children_by_meta(["Market", "Region"], nodes_ids=[])


def test_get_children_by_meta_raise_exception_type_error(list_of_pathes, description):
    '''Test for method get_children_by_meta(self,meta_filter,node_ids)
    Check raising exception on wrong type of input

    Input: meta filter
    Output: meta data of founded node by input filter
    Expected: meta data equality

    :return:

    '''

    def get_children_by_meta(meta, nodes_ids):
        root_node = Node('root', (None,None))
        encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
        node_ids = []
        meta_filter = Meta(meta[0], meta[1])
        output_node = root_node.get_children_by_meta(meta_filter, node_ids)
        print(list_of_pathes)
        return node_ids

    with pytest.raises(Exception):
        get_children_by_meta("Market", nodes_ids=[])


def test_parent_by_meta(list_of_pathes, description):
    '''Test for method get_parent_by_meta(self,meta_filter)

    Input: meta data filters, node id
    Output: list of meta data of getted parent node

    :return:

    '''

    def get_parent_by_meta(meta_filter, id):
        meta_filter = Meta(meta_filter[0], meta_filter[1])
        root_node = Node('root', (None, None))
        encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
        default_node = LIST_OF_NODES[id]
        output_node = default_node.get_parent_by_meta(meta_filter)
        return output_node

    actual = get_parent_by_meta(["Geo", "Country"], 2).id
    expected = 0
    assert actual == expected

    actual = get_parent_by_meta(["Geo", "Region"], 15).id
    expected = 2
    assert actual == expected


def test_parent_by_meta_raise_exception_value_error(list_of_pathes, description):
    '''Test for method get_parent_by_meta(self,meta_filter)
    Check raising exception on wrong value of input

    Input: meta data filters, node id
    Output: list of meta data of getted parent node

    :return:

    '''

    def get_parent_by_meta(meta_filter, id):
        meta_filter = Meta(meta_filter[0], meta_filter[1])
        root_node = Node('root', (None, None))
        encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
        default_node = LIST_OF_NODES[id]
        output_node = default_node.get_parent_by_meta(meta_filter)
        return output_node

    with pytest.raises(Exception):
        get_parent_by_meta(["Product", "Drink"], 7)


def test_parent_by_meta_raise_exception_type_error(list_of_pathes, description):
    '''Test for method get_parent_by_meta(self,meta_filter)
    Check raising exception on wrong type of input

    Input: meta data filters, node id
    Output: list of meta data of getted parent node

    :return:

    '''

    def get_parent_by_meta(meta_filter, id):
        meta_filter = Meta(meta_filter[0], meta_filter[1])
        root_node = Node('root', (None, None))
        encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
        default_node = LIST_OF_NODES[id]
        output_node = default_node.get_parent_by_meta(meta_filter)
        return output_node

    with pytest.raises(Exception):
        get_parent_by_meta("Product", 7)


def test_rename():
    '''Test for rename(self,new_name) method

    Input: new_name
    Output: node's new name
    Expected: name equality

    :return:

    '''

    def rename(new_name):
        root_node = Node('root', (None, None))
        root_node.rename(new_name)
        return root_node.name

    assert rename('USA') == 'USA'

    assert rename('Ukraine') == 'Ukraine'


def test_rename_raise_exception_value_error():
    '''Test for rename(self,new_name) method

    Input: new_name
    Output: node's new name
    Expected: name equality

    :return:

    '''

    def rename(new_name):
        root_node = Node('root', (None, None))
        root_node.rename(new_name)
        return root_node.name

    with pytest.raises(Exception):
        rename("Product", ['Kiev', 'Product'])


def test_get_path(list_of_pathes, description):
    '''Test for get_path(self,node) method

    Input node id
    Output path of node
    Expected path equality

    :return:

    '''

    def get_path(id):
        root_node = Node('root', (None, None))
        path = []
        metas = []
        encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
        default_node = LIST_OF_NODES[id]
        default_node.get_path(path, metas)
        return path

    actual = get_path(1)
    expected = ["Ukraine", "Kiev"]
    assert actual == expected

    actual = get_path(0)
    expected = ["Ukraine"]
    assert actual == expected

    actual = get_path(13)
    expected = ["Ukraine", "Odessa", "Cars", "Market", "Silpo"]
    assert actual == expected

    actual = get_path(2)
    expected = ["Ukraine", "Odessa"]
    assert actual == expected


def test_get_path_raise_exception_value_error(list_of_pathes, description):
    '''Test for get_path(self,node) method

    Input node id
    Output path of node
    Expected path equality

    :return:

    '''

    def get_path(id):
        root_node = Node('root', (None, None))
        path = []
        metas = []
        encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
        default_node = LIST_OF_NODES[id]
        default_node.get_path(path, metas)
        return path

    with pytest.raises(Exception):
        get_path(150)


def test_get_path_raise_exception_type_error(list_of_pathes, description):
    '''Test for get_path(self,node) method

    Input node id
    Output path of node
    Expected path equality

    :return:
    '''

    def get_path(id):
        root_node = Node('root', (None, None))
        path = []
        metas = []
        encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
        default_node = LIST_OF_NODES[id]
        default_node.get_path(path, metas)
        return path

    with pytest.raises(Exception):
        get_path("Test")



