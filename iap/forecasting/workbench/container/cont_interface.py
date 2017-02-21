import copy
from .timelines import TimeLineManager
from .entity_data import EntityData
from .entities_hierarchy import Node
from ..helper import SlotType, FilterType
from ....common.helper import Meta
from ....common.exceptions import *


class Container:

    def __init__(self):
        '''Initialisation of Interface

        Args:
            (TimeLineManager):
            (Node):
            (dict)
        Dictionary save pair node, entity data

        All searching and getting operation are executed with
        node attributes - path, id, metas

        '''

        self.timeline = TimeLineManager()
        self._root = Node('root', (None, None))
        self._nodes_dict = {}
        #self._nodes_dict[node.id] = dict(node=node, data=EntityData(self.timeline), insights=[])
        self._max_node_id = 0

    def _clean(self):
        '''Clean container set _root node as None
           clean _node_dict
           set _max_node_id

        Args:

        Return:

        :return:

        '''
        self._root = Node('root', (None, None))
        self._nodes_dict = {}
        self._max_node_id = 0

    def load(self, backup):
        """Load container

        backup = {'timeline':{}, 'container':[{'path': , 'metas': ,'data': ,'insights':}]}

        Args:
            (dict): backup

        first  - run method clean
        second - fill the timeline manager using load_backup(self.backup) method
        third - fill node dictionary

        :param backup:
        :return:

        """
        self._clean()
        self.timeline.load_backup(backup['timeline'])
        for node_info in backup['container']:
            ent = self.add_entity(node_info['path'], node_info['metas'])
            self._nodes_dict[ent.id]['data'].load_backup(node_info['data'])
            self._nodes_dict[ent.id]['insights'] = node_info['insights']
        return

    def save(self):
        '''Deserialise attribute's of Container object into dictionary/
        Operation invers to load(self,backup) method

        Args:

        Return:
            (dict):backup :{'timeline':timeline ,'container':container}

        :return:

        self._node_dict = {'node_id': {'node':, 'data':, 'insights':}}


        '''

    def get_backup(self):
        backup = []
        for node_id, node_info in self._nodes_dict.items():
            path = []
            metas = []
            node_info['node'].get_path(path, metas)
            data = node_info['data'].get_backup()
            ins = node_info['insights']
            backup.append(dict(path=path, metas=metas, data=data, insights=ins))
        return dict(timeline=self.timeline.get_backup(), container=backup)

    def load_from_backup(self, backup):
        self._clean()
        self.timeline.load_backup(backup['timeline'])
        for node_info in backup['container']:
            ent = self.add_entity(node_info['path'], node_info['metas'])
            self._nodes_dict[ent.id]['data'].load_backup(node_info['data'])
            self._nodes_dict[ent.id]['insights'] = node_info['insights']
        return

    @property
    def top_entities(self):
        '''Return Entity Data that corresspond to the fist generation of Node

            Return:
             (list): list of EntityData
        :return:

        '''

        return [self.get_entity_by_id(x.id) for x in self._root.children]

    def add_entity(self, path, metas):
        '''Add node by path to the root node, add new node to the _node_dict.

        Args:
            (string): path
            (list): list of metadata

        :param path:
        :param metas:
        :return:

        '''
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
        '''Get entity by id from _node_dict

        Args:
            (int): ent_id

        Return:
            (Entity)

        :param ent_id:
        :return:

        '''

        node_info = self._nodes_dict.get(ent_id, None)
        if node_info is None:
            return None
        return Entity(self, node_info['node'],
                      node_info['data'],
                      node_info['insights'])

    def get_entity_by_path(self, path):
        """
        Get entity by path.
        Firstly get node by path, secondly get entity by id of selected node

        Args:
            (string): path of node
        Return:
            (Entity): coresponding Entity

        :param path:
        :return:

        """

        if self._root is None:
            return None
        node = self._root.get_node_by_path(path)
        if node is not None:
            return self.get_entity_by_id(node.id)
        else:
            return None

    def get_entities_by_meta(self, meta_filter, top_entity):
        """
        Get entity by meta of coresponding Node

        Args:
            (list): meta_filter
            (top-entity): Top entity

        Return:
            (list): list of Entity

        :param meta_filter:
        :param top_entity:
        :return:

        """
        nodes_ids = []
        if top_entity is not None:
            node = self._nodes_dict[top_entity.id]['node']
            node.get_children_by_meta(meta_filter, nodes_ids)
        else:
            self._root.get_children_by_meta(meta_filter, nodes_ids)
        return [self.get_entity_by_id(x) for x in nodes_ids]

    def get_entity_by_filter(self, main_ent, ent_filter):
        """Get entity by filter

        :param main_ent:
        :param ent_filter:
        :return:
        """

        meta_type = ent_filter['type']
        if meta_type == FilterType.empty:
            res_entity = main_ent
        elif meta_type == FilterType.path:
            res_entity = self.get_entity_by_path(ent_filter['path'])
        elif meta_type == FilterType.relative_path:
            res_entity = main_ent.get_child_by_relative_path(ent_filter['path'])
        elif meta_type == FilterType.meta_filter:
            res_entity = \
                main_ent.get_parent_by_meta(Meta(ent_filter['meta_filter'][0],
                                                 ent_filter['meta_filter'][1]))
        else:
            raise UnknowMetaFilterError
        if res_entity is None:
            raise EntityNotFound
        return res_entity


class Entity:

    def __init__(self, container, node, data_block, insights):
        """
        Attr:
            (Container): _container
            (Node): node
            (data_block):
            (list): _insights

        :param container:
        :param node:
        :param data_block:
        :param insights:

        """
        self._node = node
        self._data = data_block
        self._insights = insights
        self._container = container

    # Hierarchy.
    @property
    def id(self):
        '''
        (int): id
        Return:
            node id
        :return:
        '''
        return self._node.id

    @property
    def name(self):
        '''
        (string): name
        Return node name
        :return:
        '''
        return self._node.name

    @name.setter
    def name(self, name):
        '''Set new name for node

        :param name:
        :return:

        '''

        self._node.rename(name)

    @property
    def parents(self):
        '''Return all Entity data from parent's nodes

        Return:
            (list): list of EntityData

        :return:

        '''

        return [self._container.get_entity_by_id(x.id) for x in
                self._node.parents]

    @property
    def children(self):
        '''Return all EntityData from children node's

        Return:
            (list): list of EntityData

        :return:

        '''

        return [self._container.get_entity_by_id(x.id) for x in
                self._node.children]

    @property
    def path(self):
        '''Get path of node

        Return:
            (list): Path of Node

        :return:

        '''
        p = []
        m = []
        self._node.get_path(p, m)
        return p

    @property
    def meta(self):
        '''Get meta of node

        Return:
            (Meta): meta of node

        :return:

        '''
        return self._node.meta

    def add_child(self, name, meta):
        '''

        :param name:
        :param meta:
        :return:

        '''
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
    """
    Class realise variable from entity data

    """
    def __init__(self, entity_data, var_name):
        """Initialise Variable

        Args:
            (EntityData): entity_data
            (string): var_name

        :param entity_data:
        :param var_name:

        """

        self._data = entity_data
        self._var_name = var_name

    @property
    def name(self):
        """
        Property save name of variable

        Return:
            (string): variable name

        :return:

        """

        return self._var_name

    @name.setter
    def name(self, name):
        """
        Set new name of variable,
        using EntityData method

        Args:
            (string): name - new variable name

        :param name:
        :return:

        """
        self._data.rename_variable(self._var_name, name)
        self._var_name = name

    @property
    def properties(self):
        """
        Return properties of variable
        Return:
            (list): [{'prop': 'property_name', 'value': 'property_value'}]

        :return:

        """
        return self._data.get_var_properties(self._var_name)

    def get_property(self, name):
        """Return property value

        Args:
            (string): name - name of property
        Return:
            (obj): value - value of property

        :param name:

        :return:

        """

        return self._data.get_var_property(self._var_name, name)

    def set_property(self, name, value):
        """Set value for mentioned value
        Args:
            (string) - name of property
            (obj) - property value

        :param name:
        :param value:
        :return:

        """

        self._data.set_var_property(self._var_name, name, value)

    def get_time_series(self, ts_name):
        if self._data.is_exist(self._var_name, ts_name, SlotType.time_series):
            return TimeSeries(self._data, self._var_name, ts_name)
        else:
            return None

    def get_scalar(self, ts_name):

        if self._data.is_exist(self._var_name, ts_name, SlotType.scalar):
            return Scalar(self._data, self._var_name, ts_name)
        else:
            return None

    def get_periods_series(self, ts_name):

        if self._data.is_exist(self._var_name, ts_name,
                               SlotType.period_series):
            return PeriodSeries(self._data, self._var_name, ts_name)
        else:
            return None

    def add_time_series(self, ts_name):
        """

        :param ts_name:
        :type ts_name: str
        :return:
        :rtype: iap.forecasting.workbench.container.cont_interface.TimeSeries
        """
        if not self._data.is_exist(self._var_name, ts_name,
                                   SlotType.time_series):
            self._data.init_slot(self._var_name, ts_name, SlotType.time_series)
        return TimeSeries(self._data, self._var_name, ts_name)

    def add_scalar(self, ts_name):

        if not self._data.is_exist(self._var_name, ts_name, SlotType.scalar):
            self._data.init_slot(self._var_name, ts_name, SlotType.scalar)

        if not self._data.is_exist(self._var_name, ts_name, SlotType.scalar):
            self._data.init_slot(self._var_name, ts_name, SlotType.scalar)
        return Scalar(self._data, self._var_name, ts_name)

    def add_periods_series(self, ts_name):

        if not self._data.is_exist(self._var_name, ts_name,
                                   SlotType.period_series):
            self._data.init_slot(self._var_name, ts_name,
                                 SlotType.period_series)
        return PeriodSeries(self._data, self._var_name, ts_name)


class TimeSeries:
    """
    Wrapper around timeseries of Entity Data
    """
    def __init__(self, data, var_name, ts_name):
        """
        Initialise TimeSeries
        Args:
            (EntityData):entity data
            (string): variable name
            (string): timeseries name

        :param data:
        :param var_name:
        :param ts_name:

        """

        self._data = data
        self._var_name = var_name
        self._ts_name = ts_name

    def get_value(self, stamp):
        """
        Wrapper for method get_ts_vals

        Args:
            (string): stamp - start point of period
        Return:
            (object): value of variable for specific timeseries
                        at stamp moment

        :param stamp:
        :return:

        """
        return self._data.get_ts_vals(self._var_name, self._ts_name,
                                      (stamp, None), 1)

    def get_values_from(self, stamp, length):
        """
        Wrapper for method get_ts_vals

        Args:
            (string): stamp - start point of period
            (int): duration of period
        Return:
            (list): value of variable for specific timeseries
                      during the period with starting point stamp and
                      duration length

        :param stamp:
        :return:

        """
        return self._data.get_ts_vals(self._var_name, self._ts_name,
                                      (stamp, None), length)

    def get_values_for_period(self, period):
        """
        Wrapper for method get_ts_vals

        Args:
            (period): stamp - start point of period
        Return:
            (list): value of variable for specific timeseries
                      during the period with starting point stamp and
                      duration length

        :param stamp:
        :return:

        """
        return self._data.get_ts_vals(self._var_name, self._ts_name, period,
                                      None)

    def set_value(self, stamp, value):
        """

        :param stamp:
        :param value:
        :return:

        """

        self._data.set_ts_vals(self._var_name, self._ts_name, [value], stamp)

    def set_value_by_index(self, ts_name, index, value):

        stamp = self._data.time_manager.get_label(ts_name=ts_name, index=index)
        self._data.set_ts_vals(self._var_name, self._ts_name, [value], stamp)

    def set_values_from(self, values, stamp):
        """

        :param values:
        :param stamp:
        :return:

        """

        self._data.set_ts_vals(self._var_name, self._ts_name, values, stamp)


class Scalar:
    """Wrapper around EntityData scalar

    """
    def __init__(self, data, var_name, ts_name):
        """Initalisation of Scalar object

        Args:
            (EntityData): EntityData name
            (string): var_name - variable name
            (string): ts-name - timeseries name

        :param data:
        :param var_name:
        :param ts_name:
        """

        self._data = data
        self._var_name = var_name
        self._ts_name = ts_name

    def get_value(self):
        """Get value of variable for current scalar

        :return:

        """

        return self._data.get_scalar_val(self._var_name, self._ts_name)

    def set_value(self, value):
        """Set specific value for variable for specific scalar

        :param value:
        :return:

        """

        self._data.set_scalar_val(self._var_name, self._ts_name, value)


class PeriodSeries:
    """Wrapper around entity_data.period_series attribute
    Object realise distinct period of timeseries of variable
    """
    def __init__(self, data, var_name, ts_name):
        """Initiaise period series
        Args:
            (Entity Data): data
            (string): var_name - name of variable
            (string): ts_name - name of time series

        :param data:
        :param var_name:
        :param ts_name:

        """

        self._data = data
        self._var_name = var_name
        self._ts_name = ts_name

    def get_periods(self):
        """Get all periods


        Return:
        (list): list of period with specifc value

        :return:

        """
        periods = self._data.get_all_periods(self._var_name, self._ts_name)
        return periods

    def get_value(self, period):
        """Get value for specific period
        Args:
            (list or tuple): period - start and end time point's

        :param period:
        :return:

        """

        return self._data.get_period_val(self._var_name, self._ts_name, period)

    def set_value(self, period, value):
        """Set value of variable for period

        Args:
            (list): period
            (int): value

        :param self:
        :param period:
        :param value:
        :return:

        """

        self._data.set_period_val(self._var_name, self._ts_name, period, value)