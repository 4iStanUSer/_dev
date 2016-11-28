import pytest
#load modules
from iap.forecasting.workbench.container.entities_hierarchy import Node
from iap.common.helper_lib import Meta,is_equal_meta

path = []

#fixture executed before each function start
def setup_function(function):
    path=[]

#fixture executed before each function end
def teardown_function(function):
    path.clear()


#Load data from json
import json
input_data = open('json/hierarchy_data.json').read()
data = json.loads(input_data)


#get_graph_data
@pytest.fixture
def description():
    description = data['description']
    # meta information about each node
    return description

#get description data
@pytest.fixture
def graph():
    return data['graph']


def encode_json_into_node(graph, description, root_node):
    '''

    Function encode tree structure of json file or dictionary into Node object

    :param graph:
    :param description:
    :param root_node:
    :return:

    '''

    if root_node.name in path:
        pass
    else:
        path.append(root_node.name)
        for child in graph[root_node.name]:
            node = Node(child,description[child])
            root_node.children.append(node)
            encode_json_into_node(graph, description,node)

def decode_node_into_json(data_graph, data_description, root_node):
    '''
    Function decode tree structure of Node object into the json or dict

    :param data_graph:
    :param data_desciprion:
    :param root_node:
    :return:

    '''

    data_graph[root_node.name] = []
    if root_node.children == []:
        pass
    else:
        for child in root_node.children:
            data_graph[root_node.name].append(child.name)
            decode_node_into_json(data_graph, data_description, child)




def test_preparation(graph, description):
    '''
    Test for encoding_ and decoding functions


    :param graph:
    :param description:
    :return:

    '''
    root_node = Node('Ukraine', description['Ukraine'])
    #encoding json object into root_node

    encode_json_into_node(graph, description, root_node)

    data_graph = {}
    data_description = {}

    decode_node_into_json(data_graph, data_description, root_node)


    #print("input: {0}, output: {1}, expected {2}".format(graph, data_graph,"Dictionary equal !!!")
    assert data_graph == graph

#!!!      Tests for Node methods   !!!

def test_add_child(graph, description):
    '''
    Test for add_child(self,name,meta)



    :param graph:
    :param description:
    :return:
    '''

    print("input: , output: , expected: {0}".format("Kiev"))

    def add_child(input_name):
        parent = Node('Ukraine', description['Ukraine'])
        child = parent.add_child(input_name, Meta(description[input_name][0], description[input_name][1]))
        return child.name

    assert add_child("Kiev") == "Kiev"
    #print("input: {0}, output: {1}, expected {2}".format('Kiev', add_child("Kiev"), " Kiev")

    assert add_child("Ukraine") == "Kiev"
    #print("input: {0}, output: {1}, expected {2}".format('Ukraine', add_child("Ukraine"), "Kiev")

    assert add_child("Kiev") == "Odessa"
    #print("input: {0}, output: {1}, expected {2}".format('Kiev', add_child("Kiev"), "Odessa")



def test_add_node_by_path(graph, description):
    '''
    Test for method add_node_by_path(self,path, metas, depth, new_nodes)


    :param graph:
    :param description:
    :return:
    '''
    def add_by_path(path,meta_list):
        parent = Node('Ukraine', description['Ukraine'])
        metas = [Meta(meta[0], meta[1]) for meta in meta_list]
        new_nodes = []
        depth =0
        new_node = parent.add_node_by_path(path, metas, depth, new_nodes)
        return new_node.name

    assert add_by_path(['Kiev'], [description['Kiev']])=='Kiev'
    #print("input: {0}, output: {1}, expected {2}".format('Kiev',add_by_path(['Kiev'], [description['Kiev']]), "Kiev")

    assert add_by_path(['Kiev', 'Candy'], [description['Kiev'], description['Candy']]) == 'Kiev'
    #print("input: {0}, output: {1}, expected {2}".format(['Kiev', 'Candy'], add_by_path(['Kiev', 'Candy'], [description['Kiev'], description['Candy']]), " Kiev")

def test_get_node_by_path(graph, description):
    '''
    Test for  method get_node_by_path(self,path)

    Input: path
    Output: node's name
    Expected: names equality


    :param graph:
    :param description:
    :return:

    Input: path
    Output: node's name
    Expected: names equality


    '''
    def get_node_by_path(path):
        root_node = Node('Ukraine', description['Ukraine'])
        encode_json_into_node(graph, description, root_node)
        output_node = root_node.get_node_by_path(path)
        return output_node.name

    assert get_node_by_path([]) == 'Ukraine'
    #print("input: {0}, output: {1}, expected {2}".format('Kiev',add_by_path(['Kiev'], [description['Kiev']]), "Kiev")

    assert get_node_by_path(['Kiev']) == 'Kiev'
    #print("input: {0}, output: {1}, expected {2}".format('Kiev',add_by_path(['Kiev'], [description['Kiev']]), "Kiev")

    assert get_node_by_path(['Kiev', 'Candy']) == 'Candy'
    #print("input: {0}, output: {1}, expected {2}".format('Kiev',add_by_path(['Kiev'], [description['Kiev']]), "Kiev")


def test_get_and_add_node_by_path(graph,description):
    '''
    Test on both methods  - get_node_by_path(self,path) and add_node_by_path


    :param graph:
    :param description:
    :return:
    '''
    def get_add_node_by_path():
        root_node = Node('Ukraine', description['Ukraine'])
        encode_json_into_node(graph, description, root_node)

        added_node = root_node.add_node_by_path(path, metas, depth, new_nodes)

        getted_node = root_node.get_node_by_path(path)

        return [added_node,getted_node]

    assert get_add_node_by_path()
    #print("input: {}, output: {1}, expected {2}".format([],add_by_path(['Kiev'], [description['Kiev']]), "Kiev")


    assert get_add_node_by_path()
    #print("input: {0}, output: {1}, expected {2}".format('Kiev',add_by_path(['Kiev'], [description['Kiev']]), "Kiev")


def test_get_children_by_meta(graph,description):
    '''
    Test for method get_children_by_meta(self,meta_filter,node_ids)


    Input: meta filter
    Output: meta data of founded node by input filter
    Expected: meta data equality

    :return:

    '''


    def get_children_by_meta(meta_filter):
        root_node = Node('Ukraine', description['Ukraine'])
        encode_json_into_node(graph,description, root_node)
        node_ids = []
        output_node = root_node.get_children_by_meta(meta_filter, node_ids)
        return output_node.meta

    meta_filter = Meta(description['Kiev'][0], description['Kiev'][1])
    assert get_children_by_meta(meta_filter) == meta_filter





def test_parent_by_meta(graph,description):
    '''
    test for method get_parent_by_meta(self,meta_filter)

    Input: meta data filters
    Output: list of meta data of getted parent node
    Expected: equality between founded and search meta data

    :return:

    '''


    def get_parent_by_meta(meta_filter):
        root_node = Node('Ukraine', description['Ukraine'])
        encode_json_into_node(graph,description, root_node)
        print(len(root_node.children))
        child = root_node.children[0]
        output_node = child.get_parent_by_meta(meta_filter)
        return [output_node.meta['level'],output_node.meta['dimension']]

    meta_filter = Meta(description['Odessa'][0], description['Odessa'][1])
    assert get_parent_by_meta(meta_filter) == [meta_filter['level'],meta_filter['dimension']]



def test_rename(graph,description):
    '''
    Test for rename(self,new_name) method

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
    #print("input: {0}, output: {1}, expected {2}".format('USA',rename('USA'), "USA")

    assert rename('') == 'Ukraine'
    #print("input: {0}, output: {1}, expected {2}".format('',rename(''), "Ukraine")


def test_get_path(graph,description):

    '''
    Test for get_path(self,node) method

    Input node
    Output path

    Expected check path equality


    :return:
    '''
    print(path)
    def get_path(path,metas):
        root_node = Node('Ukraine', description['Ukraine'])
        encode_json_into_node(graph, description, root_node)
        root_node.children[-1].get_path(path,metas)
        return path
    assert get_path([],[]) == ['Ukraine']
    #print("input: {0}, output: {1}, expected {2}".format([],get_path([],[]), ['Ukraine'])


    assert get_path(['Kiev'], []) == ['Kiev']
    #print("input: {0}, output: {1}, expected {2}".format(['Kiev'],get_path([],[]), ['Kiev'])


