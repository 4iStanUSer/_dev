from .. import exceptions as ex
from .timelines import TimeLineManager
from .entity_data import EntityData
from .entities_hierarchy import Node

class Container:

    def __init__(self):
        self.timeline = TimeLineManager()
        self._hierarchy = Node('root', (None, None))
        self._nodes_dict = {}
        self._max_node_id = 0

    def add_entity(self, path, metas):
        new_nodes = []
        # Add nodes.
        latest_node = self._hierarchy.add_node_by_path(path, metas, 0, new_nodes)
        # Register nodes
        for node in new_nodes:
            self._max_node_id += 1
            node.id = self._max_node_id
            self._nodes_dict[node.id] = \
                dict(node=node, data=EntityData(self.timeline))
        # Transform node to entity
        return self.get_entity_by_id(latest_node.id)

    def _add_node_child(self, node_id, child_name, child_meta):
        node = self._nodes_dict[node_id]['node']
        # Add new node.
        new_child = node.add_child(child_name, child_meta)
        # Register node.
        self._max_node_id += 1
        new_child.id = self._max_node_id
        self._nodes_dict[new_child.id] = \
            dict(node=new_child, data=EntityData(self.timeline))
        # Transform node to entity
        return self.get_entity_by_id(new_child.id)

    def get_entity_by_id(self, node_id):
        try:
            node_info = self._nodes_dict[node_id]
        except KeyError:
            raise Exception
        return CEntity(self, node_info['node'], node_info['data'])

    def load_timelines(self, ts_names, alias, top_ts_points):
        self.timeline.load_timelines(ts_names, alias, top_ts_points)

    def get_entity_by_path(self, path):
        if self._hierarchy is None:
            return None
        node = self._hierarchy.get_node_by_path(path)
        return self.get_entity_by_id(node.id)

    def get_entity_data(self, entity, timescale):
        #TODO Rewrite (DR)
        variables = entity.get_variables_names()
        data = {}
        if variables:
            for variable in variables:
                c_variable = entity.get_variable(variable)
                c_time_series = c_variable.get_time_series(timescale)
                data[variable] = c_time_series.get_values()
        return data

    def load(self, backup):
        pass

    def save(self):
        pass

class CEntity:

    def __init__(self, container, node, data_block):
        self._node = node
        self._data = data_block
        self._container = container

    @property
    def id(self):
        return self._node.id

    @property
    def name(self):
        return self._node.name

    @name.setter
    def name(self, name):
        self._node.rename(name)

    @property
    def parents(self):
        return [self.container.get_entity_by_id(x.id) for x in
                self._node.parents]

    @property
    def children(self):
        return [self.container.get_entity_by_id(x.id) for x in
                self._node.children]

    @property
    def path(self):
        p = []
        self._node.get_path(p)
        return p

    @property
    def meta(self):
        return self._node.meta

    def _get_root(self):
        #if self.name == 'root':
        #    return self
        #for parent in self.parents:
        #    return parent._get_root()
        ## raise Exception
        #raise ex.ContRootNotFound(self.name)
        raise NotImplementedError

    def add_parent(self, path):
        # Use function only if we really need such functionality
        # root = self._get_root()
        # new_parent = root.add_node_by_path(path, 0)
        # if new_parent not in self._parents:
        #    if self.name in [x.name for x in new_parent._children]:
        #        # raise Exception
        #        raise ex.ContAlreadyExistentCEntityName(self.name)
        #    self._parents.append(new_parent)
        # return new_parent
        raise NotImplementedError

    def add_node_by_path(self, path, meta, last_id, depth):
        #node = None
        ## Find node in children
        #for child in self._children:
        #    if child.name == path[depth]:
        #        node = child
        #        break
        # Create new node
        #if node is None:
        #    node, last_id = self.add_child(path[depth], meta[depth], last_id)
        #if depth != len(path) - 1:
        #    return node.add_node_by_path(path, meta, last_id, depth + 1)
        #else:
        #    return node, last_id
        raise NotImplementedError

    def add_child(self, name, meta):
        return self._container._add_child(self._node, name, meta)

    def get_variables_properties(self):
        return self._data.get_var_names()

    def get_variable(self, name):
        if self._data.does_contain_var(name):
            return CVariable(self._data, name)
        else:
            return None

    def force_variable(self, name, default_value=None):
        if not self._data.does_contain_var(name):
            self._data.add_var(name, default_value)
        return CVariable(self._data, name)

    def force_coefficient(self, coeff_name, ts_name):
        self._data.add_coeff(coeff_name, ts_name)

    def set_coeff_value(self, coeff_name, ts_name, value):
        self._data.set_coeff_value(coeff_name, ts_name, value)

    def load(self, entity_dict):  #, path=[]
        pass

    def save(self):
        pass

    def get_decomposition(self, timescale, period):
        pass

class CVariable:

    def __init__(self, entity_data, var_name):
        self._entity_data = entity_data
        self._var_name = var_name

    @property
    def name(self):
        return self._var_name

    @name.setter
    def name(self, name):
        self._entity_data.rename_variable(self._var_name, name)
        self._var_name = name

    @property
    def default_value(self):
        self._entity_data.get_default_value(self._var_name)

    def get_time_series(self, ts_name):
        if self._entity_data.does_contain_ts(self._var_name, ts_name):
            return CTimeSeries(self._entity_data, self._var_name, ts_name)
        else:
            return None

    def force_time_series(self, ts_name, start_date=None, end_date=None):
        if not self._entity_data.does_contain_ts(self._var_name, ts_name):
            self._entity_data.add_time_series(self._var_name, ts_name, start_date, end_date)
        return CTimeSeries(self._entity_data, self._var_name, ts_name)


class CTimeSeries:

    def __init__(self, entity_data, var_name, ts_name):
        self._entity_data = entity_data
        self._var_name = var_name
        self._ts_name = ts_name

    @property
    def name(self):

        return self._ts_name

    @property
    def start_point(self):
        return self._entity_data.get_ts_start(self._var_name, self._ts_name)

    @property
    def end_point(self):
        return self._entity_data.get_ts_end(self._var_name, self._ts_name)

    def set_values(self, start_label, values):
        return self._entity_data.set_values(self._var_name,
                                            self._ts_name,
                                            start_label,
                                            values)

    def get_values(self, start_label=None, length=None):
        return self._entity_data.get_values(self._var_name,
                                            self._ts_name,
                                            start_label,
                                            length)

    def get_value(self, time_label):
        return self._entity_data.get_values(self._var_name,
                                            self._ts_name,
                                            time_label,
                                            1)

    def get_growth_rates(self, period):
        pass

    def get_cagr(self, period):
        pass