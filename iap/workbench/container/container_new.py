from .timelines_new import TimeLineManager

class Container:

    def __init__(self):
        self._root = CEntity()
        self._last_id = 0
        self._nodes_dict = {'0': self._root}
        self.timeline = TimeLineManager()

    def add_entity(self, path):
        self._root.add_node_by_path(path, 0)

    def get_entity_by_id(self, entity_id):
        try:
            return self._nodes_dict[entity_id]
        except KeyError:
            return None

    def add_time_scale(self, name, time_line):
        pass






class DataStorage:
    def __init__(self):
        variables = {'name': name, 'time_series': {'ts_name': []}}

    def add_variable(self, name):
        pass





class CEntity:

    def __init__(self, name):
        self._name = name
        self._parents = None
        self._children = None
        self._data_storage = DataStorage()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        pass

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

    def add_child(self, name):
        for child in self._children:
            if child.name == name:
                return child
        new_child = CEntity(name)
        self._children.append(new_child)
        return new_child

    def get_variables_names(self):
        return [x.name for x in self._variables]

    def get_variable(self, name):
        for var in self._variables:
            if var.name == name:
                return var
        return None

    def force_variable(self, name, data_type, default_value=None):
        # Check if variable with the name already exists.
        for var in self._variables:
            if var.name == name:
                return var
        # Create new variable.
        new_var = CVariable(name, self)
        self._variables.append(new_var)

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








class CVariable:

    def __init__(self, name, entity):


    @property
    def name(self):
        pass

    @name.setter
    def name(self, name):
        pass

    @property
    def default_value(self):
        pass

    def get_time_series(self, ts_name):
        pass

    def force_time_series(self, ts_name):
        pass



class CTimeSeries:

    def __init__(self, node_data, var_name, ts_name):
        self._node_data = node_data
        self._var_name = var_name
        self._ts_name = ts_name

    @property
    def name(self):

        return self._ts_name

    @property
    def start_point(self):
        return self._node_data.get_start(self._var_name, self._ts_name)

    @property
    def end_point(self):
        return self._node_data.get_end(self._var_name, self._ts_name)

    def set_values(self, start_label, values):
        return self._node_data.set_values(self._var_name,
                                          self._ts_name,
                                          start_label,
                                          values)

    def get_values(self, start_label=None, length=None):
        return self._node_data.get_values(self._var_name,
                                          self._ts_name,
                                          start_label,
                                          length)

    def get_value(self, time_label):
        return self._node_data.get_values(self._var_name,
                                          self._ts_name,
                                          time_label,
                                          1)
