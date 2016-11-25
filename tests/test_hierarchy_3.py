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

graph = data['graph']
description = data['description']

def test_entity_hierarchy():
    path = []
    root_node = Node('Ukraine', description['Ukraine'])
    path.append('Ukraine')

    def DFC(graph, node, root_node):

        if node not in path:
            path.append(node)
            parent = Node(node, description[node])
        elif len(path) == 1:
            parent = root_node
        for adj_node in graph[node]:
            if adj_node not in path:
                parent.add_child(adj_node, Meta(description[adj_node][0], description[adj_node][1]))
                print node, adj_node
                DFC(graph, adj_node, root_node)

    DFC(graph, 'Ukraine', root_node)
    for i in root_node.children:
        assert [j.name for j in i.children] == graph[i.name]