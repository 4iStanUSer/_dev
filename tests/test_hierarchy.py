import unittest
import sys

sys.path.append("C:/Users/Alex/Desktop/dev/iap/iap/forecasting/workbench/container")
sys.path.append("C:/Users/Alex/Desktop/dev/iap/iap/common")
from entities_hierarchy import Node
from helper_lib import Meta, is_equal_meta

class Test_Node(unittest.TestCase):

    def setUp(self):
        #prepared case for Node class testing
        #graph structure
        self.graph = {'Ukraine':['Kiev','Odessa','Lviv'],'Odessa':['Cars','Wine'],'Kiev':['Candy']}

        #meta infodrmation about each node
        self.description = {'Ukraine':['Geo','Country'],
                            'Kiev':['Geo','Region'],
                            'Lviv': ['Geo', 'Region'],
                            'Odessa':['Geo','Region'],
                            'Candy':['Food','Delicios'],
                            'Wine': ['Product', 'Drink'],
                            'Cars': ['Product', 'Transport'], }
        #root
        self.parent = Node('Ukraine',['Geo','Country'])

    def tearDown(self):
        self.parent = None

    def test_initisation(self):
        #testing initialisation
        meta = Meta(self.description['Ukraine'][0],self.description['Ukraine'][1])
        self.assertEqual(self.parent.name,'Ukraine',msg = "Initialisation error")



    #test for add_child method

    def test_add_child(self):
        #prepare test - add some child node from dict
        for i in self.graph['Ukraine']:
            self.parent.add_child(i,Meta(self.description[0],self.description[1]))

        #check names equality of child node to the names from dict
        self.assertEqual([child.name for child in self.parent.children],[name for i in self.graph['Ukraine']],"Success expected")
        self.assertEqual([child.name for child in self.parent.children], [name for i in self.description.keys()],
                         "Error adding child")

#Testing adding/getting node by path
    def test_add_node_by_path(self):

        path = ['Kiev','Candy']
        metas = [Meta(self.description[i][0],self.description[i][1]) for i in path]
        depth =1
        new_nodes =[]
        assert self.parent.add_node_by_path(path,metas,depth,new_nodes), "Add node by path don't work"


    def test_get_node_by_path(self):
        #prepare test_case
        for i in self.graph['Ukraine']:
            self.parent.add_child(i,Meta(self.description[i][0],self.description[i][1]))

        #run tests
        assert self.parent.get_node_by_path(['Kiev']).name == "Kiev", "Error with get node by path right answer"
        assert self.parent.get_node_by_path(['Ukraine','Odessa']).name == "Kiev","Error expected"
        assert self.parent.get_node_by_path(['Ukraine','Odessa','Kiev']).name == "Odessa","Error expected"

    def test_get_node_by_path_2(self):
        # prepare test_case
        for i in self.graph['Ukraine']:
            region = self.parent.add_child(i, Meta(self.description[i][0], self.description[i][1]))
            if i in self.graph.keys():
                for j in self.graph[i]:
                    region.add_child(j, Meta(self.description[j][0], self.description[j][1]))
        # run tests
        assert self.parent.get_node_by_path([]), "Error expected"
        assert self.parent.get_node_by_path(["text error"]), "Error with get node by path "
        assert self.parent.get_node_by_path(['Kiev']), "Error with get node by path "
        assert self.parent.get_node_by_path(['Kiev','Candy']),"Error with get node by path "
        assert self.parent.get_node_by_path(['Ukraine', 'Candy', 'Kiev']),"Error with get node by path "




#testing getting children - parent by meta

    def get_children_by_meta(self, meta_filter, nodes_ids):
        #test preparation - add some child to parent node

        for i in self.graph.keys():
            self.parent.add_child(i,Meta(self.description[i][0],self.description[i][1]))
        #trivial case
        list_of_meta = [Meta(self.description[name][0],self.description[name][1]) for name in self.graph.keys()]
        node_ids =[]
        for meta in  list_of_meta:
            assert self.parent.get_children_by_meta(meta,node_ids),"Error getting children by meta"

        assert self.parent.get_children_by_meta(Meta('Ukraine','Candy')),"Error expected"
        assert self.parent.get_children_by_meta(Meta('Geo', 'City')),"Success expected"

#!!! Method get_child_by_meta don't return list of children_id, now mechanism for id indexation. Better to use list_names


    def test_get_parent_by_meta(self):
        for i in self.graph.keys():
            self.parent.add_child(i,Meta(self.description[i][0],self.description[i][1]))
        # trivial case
        list_of_meta = [Meta(self.description[name][0], self.description[name][1]) for name in self.graph.keys()]

        child = self.parent.children[-1] #Odessa

        assert child.get_parent_by_meta(Meta('Product', 'Region')), "Error expected"
        assert child.get_parent_by_meta(Meta('Ukraine', 'Candy')), "Error expected"
        assert child.get_parent_by_meta(Meta('Geo', 'Country')), "Success expected"


    def test_rename(self):
        self.parent.rename("USA")
        self.assertEqual(self.parent.name,"USA",msg = "Error expected")

#rename method not realised


    #get child by meta vs get parent by meta
    #get node by path vs add node by path
if __name__ =="__main__":
    unittest.main()