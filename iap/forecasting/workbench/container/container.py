from .. import exceptions as ex
from .timelines import TimeLineManager
from .entity_data import EntityData
from .entities_hierarchy import Node
from .. import helpers

class Container:

    def __init__(self):
        self._timeline = TimeLineManager()
        self._data_blocks = {}
        self._root = Node('root', (None, None))
        self._nodes_dict = {}
        self._max_node_id = 0
        #

    def add_entity(self, path, metas):
        new_nodes = []
        # Add nodes.
        latest_node = self._root.add_node_by_path(path, metas, 0, new_nodes)
        # Register nodes
        for node in new_nodes:
            self._max_node_id += 1
            node.id = self._max_node_id
            self._nodes_dict[node.id] = node
            # Define node data.
            self._data_blocks[node.id] = EntityData(self._timeline)
        # Transform node to entity
        return self.get_entity_by_id(latest_node.id)

    def _add_node_child(self, node_id, child_name, child_meta):
        node = self._nodes_dict[node_id]
        # Add new node.
        new_child = node.add_child(child_name, child_meta)
        # Register node.
        self._max_node_id += 1
        new_child.id = self._max_node_id
        self._nodes_dict[new_child.id] = new_child
        # Define node data.
        self._data_blocks[new_child.id] = EntityData(self._timeline)
        # Transform node to entity
        return self.get_entity_by_id(new_child.id)

    def get_entity_by_id(self, node_id):
        try:
            node = self._nodes_dict[node_id]
            node_data = self._data_blocks[node_id]
        except KeyError:
            raise Exception
        return CEntity(self, node, node_data)

    def add_time_scale(self, name, time_line):
        self._timeline.add_time_line(name, time_line)

    def get_entity_by_path(self, path):
        if self._root is None:
            return None
        node = self._root.get_node_by_path(path)
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
        # TODO Rewrite (DR)
        time_lines = backup['time_line'] if backup.get('time_line') else {}
        c_entities = backup.get('c_entities')

        if time_lines:
            for timescale, timeline in time_lines.items():
                self.add_time_scale(timescale, timeline)

        if c_entities is not None and isinstance(c_entities, list):
            for c_entity in c_entities:
                self._root.load(c_entity)

    def save(self):
        # TODO Rewrite (DR)
        if self._root is None:
            return False
        return {
            'c_entities': self._root.save(),
            'time_line': self.timeline.time_scales
        }

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

    def get_variables_names(self):
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

'''
class CEntity:

    def __init__(self, name, meta, time_line_manager):
        self._id = None
        self._name = name
        self._meta = meta
        self._parents = []
        self._children = []
        self._data = EntityData(time_line_manager)

    @property
    def id(self):
        return 123

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        for parent in self.parents:
            if name in [x.name for x in parent.children
                        if x.name != self._name]:
                # raise Exception
                raise ex.ContAlreadyExistentCEntityName(name)
        self._name = name

    @property
    def parents(self):
        return list(self._parents)

    @property
    def children(self):
        return list(self._children)

    @property
    def path(self):
        p = []
        self._get_path(p)
        return p

    @property
    def meta(self):
        return helpers.Meta(self._meta[0], self._meta[1])

    @property
    def parent(self):
        if len(self.parents) != 1:
            return None
        return self.parents[0]

    def _get_root(self):
        if self.name == 'root':
            return self
        for parent in self.parents:
            return parent._get_root()
        # raise Exception
        raise ex.ContRootNotFound(self.name)

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
        node = None
        # Find node in children
        for child in self._children:
            if child.name == path[depth]:
                node = child
                break
        # Create new node
        if node is None:
            node, last_id = self.add_child(path[depth], meta[depth], last_id)
        if depth != len(path) - 1:
            return node.add_node_by_path(path, meta, last_id, depth + 1)
        else:
            return node, last_id

    def add_child(self, name, meta):
        # Use function only if we really need such functionality
        ## Check if node with the same name already exists
        #for child in self._children:
        #    if child.name == name:
        #        return child, last_id
        ## Create new node
        #new_child = CEntity(name, meta, self._data.time_manager)
        #self._children.append(new_child)
        #new_child._parents.append(self)
        #return new_child
        raise NotImplementedError

    def _get_path(self, path):
        if self.name == 'root':
            return
        path.insert(0, self.name)
        if self.parent is not None:
            self.parent._get_path(path)

    def get_variables_names(self):
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
        name = entity_dict.get('name')
        data = entity_dict.get('data')
        children = entity_dict.get('children')
        if name:
            c_entity = self.add_child(name)
            if data:
                for var_name, var_dict in data.items():
                    default_val = var_dict.get('default_value')
                    time_series = var_dict.get('time_series')

                    c_variable = c_entity.force_variable(var_name, default_val)
                    if time_series:
                        for ts_name, ts_val in time_series.items():
                            start = ts_val.get('start')
                            end = ts_val.get('end')
                            values = ts_val.get('values')
                            c_ts = c_variable.force_time_series(ts_name,
                                                                start,
                                                                end)
                            # TODO Question
                            start_label = self._data.time_manager. \
                                get_label_by_index(ts_name, 0)

                            c_ts.set_values(start_label, values)

            if children:
                for child in children:
                    c_entity.load(child)
        # pass

    def save(self):
        if self._name != 'root':
            return {
                'name': self._name,
                'data': self._data.save(),
                'children': [child.save() for child in self._children]
            }
        else:
            return [child.save() for child in self._children]

    def get_node_by_path(self, path):
        # TODO Rewrite (DR)
        if len(path) == 0:
            return self
        elif self._children:
            for child in self._children:
                if child.name == path[0]:
                    res = child.get_node_by_path(path[1:])
                    if res:
                        return res
        return None
'''

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
