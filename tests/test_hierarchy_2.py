import pytest
import sys

#load modules

sys.path.append("C:/Users/Alex/Desktop/dev/iap/iap/forecasting/workbench/container")
sys.path.append("C:/Users/Alex/Desktop/dev/iap/iap/common")
from entities_hierarchy import Node
from helper_lib import Meta, is_equal_meta
import random

#load data from json

import json
input_data =  open('hierarchy_data.json').read()
data = json.loads(input_data)


#get_graph_data
@pytest.fixture
def description():
    description = data['description']
    # meta information about each node
    return description

#get_description
@pytest.fixture
def graph():
    return data['graph']

def fill_graph(graph,description):
    discovered = []
    root_node = Node("Ukraine", description()['Ukraine'])

    def DFC(i):
        # set parent
        if i in graph()['Ukraine']:
            root_node.add_child(i, Meta(description()[i][0], description()[i][1]))
        elif i in discovered or graph()[i] == []:
            pass
        else:
            parent = Node(i, description()[i])
            discovered.append(i)
            for j in graph()[i]:
                parent.add_child(j, Meta(description()[j][0], description()[j][1]))
                DFC(j)

    for vertex in graph().keys()[1:]:
        DFC(vertex)
    return root_node








#testing equality between added nodes and getted node by same path
def get_add_by_path(path,description):
    parent = Node('Ukraine', description()['Ukraine'])
    metas = [Meta(description()[i][0],description()[i][1]) for i in path]
    depth = 0
    new_nodes = []
    add_node = parent.get_node_by_path(path)
    get_node  = parent.add_node_by_path(path, metas, depth, new_nodes)
    return [get_node.name,add_node.name]


#testing that get node by path has the same path in output as in input
def get_by_path_and_path_function_testing(path,description):
    parent = Node('Ukraine', description()['Ukraine'])
    metas = [Meta(description()[i][0], description()[i][1]) for i in path]
    depth = 0
    new_nodes = []
    get_node = parent.add_node_by_path(path, metas, depth, new_nodes)
    _path = []
    _metas = []
    get_node.get_path(_path,_metas)
    return _path

#parametrized tests


def testing_add_node_by_path_by_i_o_name(path):
    parent = Node('Ukraine', description()['Ukraine'])
    depth = 0
    new_nodes = []
    metas = [Meta(description()[i][0], description()[i][1]) for i in path]
    new_node = parent.add_node_by_path(path, metas, depth, new_nodes)
    return new_node.name



@pytest.mark.parametrize('path', [['Kiev','Cars','Candy','Market'], ['Kiev'], ['Kiev','Candy','Candy','Market']])
def test_get_add_by_path_on_equality_return(path,description):
    assert get_add_by_path(path,description)[0] == get_add_by_path(path,description)[1]

@pytest.mark.parametrize('path', [['Kiev','Cars','Candy','Market'], ['Kiev'], ['Kiev','Candy','Candy','Market']])
def test_get_add_by_path_on_equality_return(path,description):
    assert get_by_path_and_path_function_testing(path,description)[0] == path

@pytest.mark.parametrize('path', [['Kiev','Cars','Candy','Market'], ['Kiev'], ['Kiev','Candy','Candy','Market']])
def test_get_add_by_path_on_equality_return(path,description):
    assert testing_add_node_by_path_by_i_o_name(path)

##Testing get children - parent by path




def test_rename(name):
    root_node = Node("Ukraine", description['Ukraine'])
    return root_node.rename(name)


@pytest.mark.parametrize('name',['USA','Russia','Ukraine'])
def test_rename(name):
    assert test_rename(name) == name





def test_get_children_parent_by_meta_check_input_output_equality(meta,type_of_node):

    discovered = []
    root_node = Node("Ukraine", description()['Ukraine'])

    def DFC(i):
        # set parent
        if i in graph()['Ukraine']:
            root_node.add_child(i, Meta(description()[i][0], description()[i][1]))
        elif i in discovered or graph()[i] == []:
            pass
        else:
            parent = Node(i, description()[i])
            discovered.append(i)
            for j in graph()[i]:
                parent.add_child(j, Meta(description()[j][0], description()[j][1]))
                DFC(j)

    for vertex in graph().keys()[1:]:
        DFC(vertex)
    if type_of_node=="children":
        nodes_ids =[]
        children = root_node.get_children_by_meta(Meta(meta[0],meta[1]),nodes_ids)

        names = [child.name for child in children]
    elif type_of_node=="parent":
        index = random.randint(0, len(root_node.children)-1)
        print(root_node.children[index].name)
        parent = root_node.children[index].get_parent_by_meta(Meta(meta[0],meta[0]))

    return parent.name







@pytest.mark.parametrize('meta',[["Geo","Country"],["Product","Transport"]])
def test_get_children_by_meta_on_return_meta_equality(meta):
    assert [name for name in description().keys() if description()[name]==meta ]==\
           test_get_children_parent_by_meta_check_input_output_equality(meta,'children')


@pytest.mark.parametrize('meta',[["Geo","Country"],["Product","Transport"]])
def test_get_parent_by_meta_on_return_meta_equality(meta):
    assert [name for name in description().keys() if description()[name]==meta ]==\
           test_get_children_parent_by_meta_check_input_output_equality(meta,'parent')

