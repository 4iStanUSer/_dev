''' 
Module contains classes for building and storing hierarchical dimensions.
'''

import copy
from ..container import exceptions as ex


class PointCoordinates(dict):
    '''
    Contains timescale name and id of point in each dimension.
    '''
    def __init__(self, timescale):
        super(PointCoordinates, self).__init__()
        self.timescale = timescale
    
    def is_equal_with_ts(self, coordinates, full_comp_flag=False):
        # Check timescale.
        if self.timescale != coordinates.timescale:
            return False
        # Check dimensions.
        return self.is_equal(coordinates, full_comp_flag)

    def is_equal(self, coordinates, full_comp_flag=False):
        for key,value in dict.items(self):
            if not (key in coordinates):
                if full_comp_flag:
                    return False
                else:
                    continue
            if coordinates[key] != value:
                return False
        return True

class DimensionManager:
    '''
    Manages all dimensions as hierarchical structures.
    '''

    def __init__(self):
        self.__dims = {}
        self.__level_names = {}
        self.__last_id = {}
        self.__nodes_dict = {}

    def add_dimension(self, name, level_names):
        self.__level_names[name] = list(level_names)
        self.__dims[name] = DimNode(0, 'root', None)
        self.__last_id[name] = {'id': 0 }
        self.__nodes_dict[name] = {}

    def add_point_coordinates(self, timescale, text_coords):
        # Init output.
        coords = PointCoordinates(timescale)
        # Process dimensions. 
        for dim_name, dim_values in text_coords.items():
            # Check dimension name.
            try: 
                # Add new or get existing nodes according to coordinates.
                node = self.__add_node(dim_name, dim_values)
            except KeyError:
                raise Exception
            # Fill output.
            coords[dim_name] = node.id
            # Register node.
            self.__nodes_dict[dim_name][node.id] = node
        return coords
        
    def get_point_address(self, coords):
        address = {}
        for dim_name, coord_id in coords.items():
            node = self.__get_node_by_id(dim_name, coord_id)
            address[dim_name] = node.get_address()
        return address

    def get_dim_map(self, dim_name):
        dim_map = []
        self.__get_node_map(dim_name, dim_map)
        return dim_map, copy.copy(self.__level_names[dim_name])
       
    def __get_node_by_address(self, dim_name, address):
        return self.__dims[dim_name].find_child(address, 0)

    def __get_node_by_id(self, dim_name, id):
        return self.__nodes_dict[dim_name][id]
       
    def __add_node(self, dim_name, address):
        return self.__dims[dim_name].add_child(address, 0, 
                                                self.__last_id[dim_name])
    def __get_node_map(self, dim_name, dim_map):
        for child in self.__dims[dim_name].children: 
            child.get_map(parent=None, siblings=dim_map)
        return dim_map


class DimNode:
    '''
    Represents value in hierarchical dimension. 
    Stores parent and children nodes.
    '''
    
    def __init__(self, id, name, parent):
        self.id = id
        self.name = name
        self.parent = parent
        self.children = []
        self.index = None

    def add_child(self, address, curr_depth, last_id):
        found_node = None
        for node in self.children:
            if node.name == address[curr_depth]:
                found_node = node
                break
        if found_node is None:
            last_id['id'] = last_id['id'] + 1
            found_node = DimNode(last_id['id'] ,address[curr_depth], self)
            self.children.append(found_node)
        if curr_depth + 1 == len(address):
            return found_node
        else:
            return found_node.add_child(address, curr_depth + 1, last_id)

    def find_child(self, address, curr_depth):
        found_node = None
        for node in self.children:
            if node.name == address[curr_depth]:
                found_node = node
                break
        if (found_node is None):
            return None
        if curr_depth + 1 == len(address):
           return found_node
        else:
            return found_node.find_child(address, curr_depth + 1)
    
    def find_child_by_id(self, id):
        for node in self.children:
            if node.id == id:
                return node
            found_node = node.find_child_by_id(id)
            if found_node is not None:
                return found_node
        return None 

    def get_address(self):
        address = [self.name]
        node = self.parent
        while (node is not None and node.name != 'root'):
            address.insert(0, node.name)
            node = node.parent
        return address

    def get_map(self, parent, siblings):
        node_info = {'id': self.id, 
                     'name': self.name, 
                     'parent': parent, 
                     'children': []}
        siblings.append(node_info)
        for child in self.children:
            child.get_map(node_info, node_info['children'])
