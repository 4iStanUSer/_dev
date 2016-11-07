import copy
from .timelines import TimeLineManager
from .entity_data import EntityData, DataType
from .entities_hierarchy import Node


class Container:

    def __init__(self):
        self.timeline = TimeLineManager()
        self._root = Node('root', (None, None))
        self._nodes_dict = {}
        self._max_node_id = 0

    def load(self, backup):
        self._clean()
        self.timeline.load_backup(backup['timeline'])
        for node_info in backup['container']:
            ent = self.add_entity(node_info['path'], node_info['metas'])
            self._nodes_dict[ent.id]['data'].load_backup(node_info['data'])
            self._nodes_dict[ent.id]['insights'] = node_info['insights']
        return

    def save(self):
        backup = []
        for node_id, node_info in self._nodes_dict.items():
            path = []
            metas = []
            node_info['node'].get_path(path, metas)
            data = node_info['data'].get_backup()
            ins = node_info['insights']
            backup.append(dict(path=path, metas=metas, data=data, insights=ins))
        return dict(timeline=self.timeline.get_backup(), container=backup)

    def add_entity(self, path, metas):
        new_nodes = []
        # Add nodes.
        latest_node = self._root.add_node_by_path(path, metas, 0, new_nodes)
        # Register nodes
        for node in new_nodes:
            self._max_node_id += 1
            node.id = self._max_node_id
            self._nodes_dict[node.id] = \
                dict(node=node, data=EntityData(self.timeline), insights=[])
        # Transform node to entity
        return self.get_entity_by_id(latest_node.id)

    def get_entity_by_id(self, ent_id):
        node_info = self._nodes_dict.get(ent_id, None)
        if node_info is None:
            return None
        return Entity(self, node_info['node'],
                      node_info['data'],
                      node_info['insights'])

    def get_entity_by_path(self, path):
        if self._root is None:
            return None
        node = self._root.get_node_by_path(path)
        return self.get_entity_by_id(node.id)

    def get_entities_by_meta(self, meta_filter, top_entity):
        nodes_ids = []
        if top_entity is not None:
            node = self._nodes_dict[top_entity.id]['node']
            node.get_children_by_meta(meta_filter, nodes_ids)
        else:
            self._root.get_children_by_meta(meta_filter, nodes_ids)
        return [self.get_entity_by_id(x) for x in nodes_ids]

    def _clean(self):
        self._root = Node('root', (None, None))
        self._nodes_dict = {}
        self._max_node_id = 0


class Entity:

    def __init__(self, container, node, data_block, insights):
        self._node = node
        self._data = data_block
        self._insights = insights
        self._container = container

    # Hierarchy.
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
        return [self._container.get_entity_by_id(x.id) for x in
                self._node.parents]

    @property
    def children(self):
        return [self._container.get_entity_by_id(x.id) for x in
                self._node.children]

    @property
    def path(self):
        p = []
        self._node.get_path(p)
        return p

    @property
    def meta(self):
        return self._node.meta

    def add_child(self, name, meta):
        return self._container.add_entity(self.path.append(name),
                                          self.meta.append(meta))

    def get_parent_by_meta(self, meta_filter):
        parent_node = self._node.get_parent_by_meta(meta_filter)
        return self._container.get_entity_by_id(parent_node.id)

    # Data.
    @property
    def variables(self):
        return [Variable(self._data, x)
                for x in self._data.var_names]

    def get_variable(self, name):
        if name in self._data.var_names:
            return Variable(self._data, name)
        else:
            return None

    def add_variable(self, name):
        self._data.add_variable(name)
        return Variable(self._data, name)

    def add_insight(self, text):
        self._insights.append(text)

    @property
    def insights(self):
        return copy.copy(self._insights)


class Variable:

    def __init__(self, entity_data, var_name):
        self._data = entity_data
        self._var_name = var_name

    @property
    def name(self):
        return self._var_name

    @name.setter
    def name(self, name):
        self._data.rename_variable(self._var_name, name)
        self._var_name = name

    @property
    def properties(self):
        return self._data.get_var_properties(self._var_name)

    def get_property(self, name):
        return self._data.get_var_property(self._var_name, name)

    def set_property(self, name, value):
        self._data.set_var_property(self._var_name, name, value)

    def get_time_series(self, ts_name):
        if self._data.is_exist(self._var_name, ts_name, DataType.time_series):
            return TimeSeries(self._data, self._var_name, ts_name)
        else:
            return None

    def get_scalar(self, ts_name):
        if self._data.is_exist(self._var_name, ts_name, DataType.scalar):
            return Scalar(self._data, self._var_name, ts_name)
        else:
            return None

    def get_periods_series(self, ts_name):
        if self._data.is_exist(self._var_name, ts_name,
                               DataType.period_series):
            return PeriodSeries(self._data, self._var_name, ts_name)
        else:
            return None

    def add_time_series(self, ts_name):
        if not self._data.is_exist(self._var_name, ts_name,
                                   DataType.time_series):
            self._data.init_slot(self._var_name, ts_name, DataType.time_series)
        return TimeSeries(self._data, self._var_name, ts_name)

    def add_scalar(self, ts_name):
        if not self._data.is_exist(self._var_name, ts_name, DataType.scalar):
            self._data.init_slot(self._var_name, ts_name, DataType.scalar)
        return Scalar(self._data, self._var_name, ts_name)

    def add_periods_series(self, ts_name):
        if not self._data.is_exist(self._var_name, ts_name,
                                   DataType.period_series):
            self._data.init_slot(self._var_name, ts_name,
                                 DataType.period_series)
        return PeriodSeries(self._data, self._var_name, ts_name)


class TimeSeries:
    def __init__(self, data, var_name, ts_name):
        self._data = data
        self._var_name = var_name
        self._ts_name = ts_name

    def get_value(self, stamp):
        return self._data.get_ts_vals(self._var_name, self._ts_name,
                                      (stamp, None), 1)

    def get_values_from(self, stamp, length):
        return self._data.get_ts_vals(self._var_name, self._ts_name,
                                      (stamp, None), length)

    def get_values_for_period(self, period):
        return self._data.get_ts_vals(self._var_name, self._ts_name, period,
                                      None)

    def set_value(self, stamp, value):
        self._data.set_ts_vals(self._var_name, self._ts_name, [value], stamp)

    def set_values_from(self, values, stamp):
        self._data.set_ts_vals(self._var_name, self._ts_name, values, stamp)


class Scalar:
    def __init__(self, data, var_name, ts_name):
        self._data = data
        self._var_name = var_name
        self._ts_name = ts_name

    def get_value(self):
        return self._data.get_scalar_val(self._var_name, self._ts_name)

    def set_value(self, value):
        self._data.set_scalar_val(self._var_name, self._ts_name, value)


class PeriodSeries:
    def __init__(self, data, var_name, ts_name):
        self._data = data
        self._var_name = var_name
        self._ts_name = ts_name

    def get_periods(self):
        self._data.get_all_periods(self._var_name, self._ts_name)

    def get_value(self, period):
        return self._data.get_period_val(self._var_name, self._ts_name, period)

    def set_value(self, period, value):
        self._data.set_period_val(self._var_name, self._ts_name, period, value)