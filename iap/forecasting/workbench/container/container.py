from .timelines import TimeLineManager
from .entity_data import EntityData


class Container:

    def __init__(self):
        self.timeline = TimeLineManager()
        self._root = CEntity('root', self.timeline)

    def add_entity(self, path):
        return self._root.add_node_by_path(path, 0)

    def get_entity_by_id(self, entity_id):
        try:
            return self._nodes_dict[entity_id]
        except KeyError:
            return None

    def add_time_scale(self, name, time_line):
        self.timeline.add_time_line(name, time_line)


class CEntity:

    def __init__(self, name, time_line_manager):
        self._name = name
        self._parents = []
        self._children = []
        self._data = EntityData(time_line_manager)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        for parent in self.parents:
            if name in [x.name for x in parent.children
                        if x.name != self._name]:
                raise Exception
        self._name = name

    @property
    def parents(self):
        return list(self._parents)

    @property
    def children(self):
        return list(self._children)

    def _get_root(self):
        if self.name == 'root':
            return self
        for parent in self.parents:
            return parent._get_root()
        raise Exception

    def add_parent(self, path):
        root = self._get_root()
        new_parent = root.add_node_by_path(path, 0)
        if new_parent not in self._parents:
            if self.name in [x.name for x in new_parent._children]:
                raise Exception
            self._parents.append(new_parent)
        return new_parent

    def add_node_by_path(self, path, depth):
        node = None
        for child in self._children:
            if child.name == path[depth]:
                node = child
                break
        if node is None:
            node = self.add_child(path[depth])
        if depth != len(path) - 1:
            return node.add_node_by_path(path, depth + 1)
        else:
            return node

    def add_child(self, name):
        for child in self._children:
            if child.name == name:
                return child
        new_child = CEntity(name, self._data.time_manager)
        self._children.append(new_child)
        # TODO add parenting somewhere else, following allows adding only one parent
        new_child._parents.append(self)
        return new_child

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
        if self._entity_data.does_cointain_ts(self._var_name, ts_name):
            return CTimeSeries(self._entity_data, self._var_name, ts_name)
        else:
            return None

    def force_time_series(self, ts_name, start_date, end_date):
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
