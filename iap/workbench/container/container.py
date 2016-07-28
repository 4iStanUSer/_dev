''' 
Module contains classes for container.
'''
import pickle
import os

from .dimensions import DimensionManager, PointCoordinates
from .timelines import TimelinesManager
from .facts import Point
from .configuration import ConfigManager
from ..container import exceptions as ex


class Container:
    '''
    '''

    def __init__(self):
        self.config = ConfigManager()
        self.dim_manager = DimensionManager()
        self.__data = {}

    def setup(self):
        # Set up dimension manager.
        for dim_name,level_names in self.config.dimensions.items():
            self.dim_manager.add_dimension(dim_name, level_names)
        # Set up data collection.
        for ts_name in self.config.timescales:
            self.__data[ts_name] = []
        
    #region Data getters.
    def get_dimension_map(self, dimension_name):
        tree, level_names = self.dim_manager.get_dim_map(dimension_name)
        # Sorting could be inserted here.
        return tree

    def get_available_dimension_items(self, timescale, selection):
        # Parse selection.
        curr_selection = {}
        selectors_content = []
        for dim in selection:
            dim_name = dim['name']
            selected_item = dim['selected']
            if selected_item is not None:
                curr_selection[dim_name] = selected_item
            else:
                selectors_content.append({'name': dim_name, 
                                          'content': None,
                                          'selection': None})
        # Fill selector content for requested dimensions.
        curr_points = self.__data[timescale]
        for dim in selectors_content:
            dim_name = dim['name']
            curr_points = self.__select_points(curr_points, curr_selection)
            dim['content'] = set([x.coordinates[dim_name] for x in curr_points])
            def_selection = self.__get_default_selection(curr_points, dim_name)
            dim['selection'] = def_selection
            curr_selection[dim_name] = def_selection
        # 
        return selectors_content
        
    def get_data_by_selection(self, timescale, selection):
        # Find point
        found_point = None
        for point in self.__data[timescale]:
            if point.coordinates.is_equal(selection, True):
                found_point = point
                break
        else:
            return None
        # Return point data
        return point.get_data_for_view()

    def __get_default_selection(self, collection, dim_name):
        return collection[0].coordinates[dim_name]

    def __select_points(self, collection, selection):
        subset = []
        for point in collection:
            if point.coordinates.is_equal(selection):
                subset.append(point)
        return subset

    def __get_point(self, coordinates):
        for point in self.__data[coordinates.timescale]:
            if point.coordinates.is_equal_with_ts(coordinates, True):
                return point
        return None
    #endregion Data getters.

    #region Data load.
    def load_data_from_rep(self, data):
        for ts_name, ts_content in data['data tables'].items():
            for item in ts_content['points']:
                coords = self.dim_manager\
                    .add_point_coordinates(ts_name, item['coordinates'])
                point = self.__get_point(coords)
                if point is None:
                    point = self.__add_point(coords)
                for var in item['trends']:
                    point.set_var_data(var['name'], var['value'])
                #for var in item['coefficients']:
                #    point.set_var_data(var['name'], var['value'])
                for var in item['pos_data']:
                    point.set_var_data(var['name'], var['value'])

    def __add_point(self, coords):
        point_config = self.config.get_point_config(coords)
        point = Point(coords, point_config)
        self.__data[coords.timescale].append(point)
        return point
    #endregion Data load.

    #region Serialization.
    def get_data_for_save(self):
        buffer = {} 
        for ts_name, data in self.__data.items():
            buffer[ts_name] = []
            for item in data:
                address = self.dim_manager.get_point_address(item.coordinates)
                item_data = item.get_data_for_save()
                if address is None or data is None:
                    raise Exception
                buffer[ts_name].append({'coordinates': address, 
                                        'data': item_data})
        return pickle.dumps(buffer, pickle.HIGHEST_PROTOCOL)

    def load_saved_data(self, file):
        buffer = pickle.load(file)
        for ts_name, data in self.__data.items():
            if ts_name not in buffer:
                continue
            for item in buffer[ts_name]:
                text_coords = item['coordinates']
                item_data = item['data']
                coords = self.dim_manager.add_point_coordinates(ts_name, 
                                                                text_coords)
                point = self.__add_point(coords)
                point.load_saved_data(item_data)
    #endregion Serialization.

    #region Support.
    #endregion Support.