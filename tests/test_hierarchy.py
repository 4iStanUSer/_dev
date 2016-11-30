#load modules
from iap.forecasting.workbench.container.entities_hierarchy import Node
from iap.common.helper_lib import Meta, is_equal_meta
import pytest

#Load data from json
import json
input_data = open('json/hierarchy_data.json').read()
data = json.loads(input_data)

#get description data
@pytest.fixture
def description():
    description = data['description']
    # meta information about each node
    return description
#get pathes data
@pytest.fixture
def list_of_pathes():
    l = []
    for i in data['path']:
        l.insert(i['id'], i['node'])
    return l

#get graph data
@pytest.fixture
def graph():
    return data['graph']

#encoded list of pathes
encoded_path = []
#list of nodes
list_of_nodes = []

#fixture executed before each function start
def setup_function(function):
    list_of_nodes = []
    encoded_path=[]

#fixture executed before each function end
def teardown_function(function):
    list_of_nodes.clear()
    encoded_path.clear()

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
        new_node = root_node.add_node_by_path(path, metas,depth,new_nodes)
        #create list of node's and add specific id to node
        new_node.id = list_of_pathes.index(path)
        list_of_nodes.insert(new_node.id, new_node)
    return list_of_pathes

def decode_node_into_list_of_pathes(root_node, path):
    '''Deserialise graph structure of root_node into list of pathes

    :param root_node: root node
    :param path: list that contain hitory of path traversing
    :return:

    '''

    for node in root_node.children:
        new_path = path[:]
        new_path.append(node.name)
        encoded_path.insert(node.id, new_path)
        decode_node_into_list_of_pathes(node, new_path)

def test_preparation(description, list_of_pathes):
    '''Test for encoding_ and decoding functions

     first step function serialise json in node
     next step in deserialise node struncture in list of pathes
     matcher check if input and output list_of_pathes and encoded_list equal

    :param graph:
    :param description:
    :return:

    '''

    root_node = Node('root', (None, None))
    encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
    decode_node_into_list_of_pathes(root_node, path=[])

    assert list_of_pathes.sort() == encoded_path.sort()

def test_add_child(list_of_pathes, description):
    '''Test for add_child(self,name,meta)

    Input cutted tree - without last element
    Output root node with added elements

    :param graph:
    :param description:
    :return:

    '''

    def add_child():
        #tree preparation
        tree = list_of_pathes[:-1]
        #bottom of tree
        last_child = list_of_pathes[-1]
        root_node = Node('root', (None, None))
        encode_list_of_pathes_into_node(root_node, list_of_pathes[:-1], description)
        last_node = list_of_nodes[-1]
        print(tree)
        print(last_child[-1])
        print(last_node.name)
        last_node.add_child(last_child[-1], Meta(description[last_child[-1]][0], description[last_child[-1]][1]))
        return root_node

    decode_node_into_list_of_pathes(add_child(), path=[])

    actual = encoded_path
    expected = list_of_pathes
    assert actual.sort() == expected.sort()

    actual = encoded_path
    expected = list_of_pathes[:-2]
    assert actual == expected

def test_get_node_by_path(list_of_pathes, description):
    '''Test for  method get_node_by_path(self,path)

    Input: path
    Output: node's name
    Expected: names equality

    :param graph:
    :param description:
    :return:

    '''
    def get_node_by_path(list_of_pathes, path):
        root_node = Node('root', (None, None))
        encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
        output_node = root_node.get_node_by_path(path)
        return output_node

    actual_id = get_node_by_path(list_of_pathes, ['Ukraine']).id
    expected_id = 0
    assert actual_id == expected_id

    actual_id = get_node_by_path(list_of_pathes, ["Ukraine", "Odessa", "Wine", "Market", "Silpo"]).id
    expected_id = 16
    assert actual_id == expected_id

    actual_id = get_node_by_path(list_of_pathes, ['Ukraine', 'Kiev']).id
    expected_id = 4
    assert actual_id == expected_id

    actual_id = get_node_by_path(list_of_pathes, ["Ukraine","Odessa","Wine","Market","Silpo"]).id
    expected_id = 12
    assert actual_id == expected_id

def test_get_children_by_meta(list_of_pathes, description):
    '''Test for method get_children_by_meta(self,meta_filter,node_ids)

    Input: meta filter
    Output: meta data of founded node by input filter
    Expected: meta data equality

    :return:

    '''

    def get_children_by_meta(list_of_pathes, meta, nodes_ids):
        root_node = Node('root', (None,None))
        encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
        node_ids = []
        meta_filter = Meta(meta[0], meta[1])
        output_node = root_node.get_children_by_meta(meta_filter, node_ids)
        print(list_of_pathes)
        return node_ids

    actual = get_children_by_meta(list_of_pathes, ["Geo", "Region"], nodes_ids=[])
    expected = [1,2,3]
    assert actual == expected

    actual = get_children_by_meta(list_of_pathes, ["Reseller", "Market"], nodes_ids=[])
    expected = [1,3,4,5]
    assert actual == expected

    actual = get_children_by_meta(list_of_pathes, ["Reseller", "Market"], nodes_ids=[])
    expected = [1,3,4,5]
    assert actual == expected

def test_parent_by_meta(list_of_pathes, description):
    '''Test for method get_parent_by_meta(self,meta_filter)

    Input: meta data filters, node id
    Output: list of meta data of getted parent node

    :return:

    '''

    def get_parent_by_meta(meta_filter, id):
        meta_filter = Meta(meta_filter[0], meta_filter[1])
        root_node = Node('Ukraine', description['Ukraine'])
        encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
        default_node = list_of_nodes[id]
        output_node = default_node.get_parent_by_meta(meta_filter)
        return output_node

    actual = get_parent_by_meta(["Geo", "Country"], 2).id
    expected = 0
    assert actual == expected

    actual = get_parent_by_meta(["Geo", "Region"], 15).id
    expected = 2
    assert actual == expected

    actual = get_parent_by_meta(["Product", "Drink"], 7).id
    expected = 1
    assert actual == expected

def test_rename(graph, description):
    '''Test for rename(self,new_name) method

    Input: new_name
    Output: node's new name
    Expected: name equality

    :return:

    '''

    def rename(new_name):
        root_node = Node('Ukraine', description['Ukraine'])
        root_node.rename(new_name)
        return root_node.name

    assert rename('USA') == 'USA'

    assert rename('Ukrane') == 'Ukrane'

def test_get_path(list_of_pathes, description):
    '''Test for get_path(self,node) method

    Input node id
    Output path of node
    Expected path equality

    :return:

    '''

    def get_path(id):
        root_node = Node('Ukraine', description['Ukraine'])
        path = []
        metas = []
        encode_list_of_pathes_into_node(root_node, list_of_pathes, description)
        default_node = list_of_nodes[id]
        default_node.get_path(path, metas)
        return path

    actual = get_path(0)
    expected = ["Ukraine"]
    assert actual == expected

    actual = get_path(2)
    expectd = ["Ukraine"]
    assert actual == expected

    actual = get_path(12)
    expected = ["Ukraine","Odessa","Cars","Market","Silpo"]
    assert actual == expected

    actual = get_path(2)
    expected= ["Ukraine','Kiev"]
    assert actual == expected

    actual = get_path(14)
    expected = ["Ukraine","Odessa","Wine","Bars","Good Bar"]
    assert actual == expected

