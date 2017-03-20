from ..models.warehouse import *
from ..models.access import Project
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
import logging

import pandas as pd


class Warehouse:
    """
    Warehouse class designed to
    interact with data storage and provide
    link between data structure. Such as
    Entity, TimeSeries, Variable, Value etc.
    """
    def __init__(self, config):
        """
        Object initialise with session
        And query Entity Root obj

        :param ssn_factory:
        :type ssn_factory:
        """

        self.engine = create_engine(config)
        _ssn = sessionmaker(bind=self.engine)
        self._ssn = _ssn()
        self._root = self._ssn.query(Entity).filter(Entity.name == 'root').\
            one_or_none()

    """
    Common WH methods
    """

    def add_project(self, project_name):
        """
        Add Project
        """
        pr = Project(name=project_name)

    def save_project_data(self, name, df):
        """
        Save project data
        """
        df.to_sql(name, self.engine, if_exists='append')


    def get_project_data(self, name):
        """
        Get Project Data
        """

        query = "SELECT entities._name, variables._name, entities.project, " \
                "timeseries._name, timeseries._time_stamp, timeseries._value "\
                "FROM entities "\
                "JOIN variables "\
                "ON entities._id = variables._entity_id "\
                "JOIN timeseries "\
                "ON variables._id = timeseries.variable_id "\
                "WHERE entities.project = '%s' " %name


        entities = pd.read_sql_query(query, self.engine)
        return entities


    def get_root(self):
        """
        Return root Entity

        """
        return self._root

    def add_IEntity(self, ent, project_name):
        """
        Add interface Entity
        """
        ent_path = ent.path
        meta = ent.meta
        ent = self.add_entity(ent_path, meta=meta, project_name=project_name)
        return ent

    def add_IVariable(self, ent, var_name):
        """
        Add Interface Variable
        """
        var = Variable(_name=var_name)
        ent._variables.append(var)
        self.flush()
        print('Var', var._id)
        return var

    def add_ITimeSerie(self, variables):

        self._ssn.bulk_insert_mappings(
            TimeSerie, variables)
        self._ssn.commit()

    def add_entity(self, path, meta=None, project_name=None ):
        """
        Add Entity by path and meta
        Set new Entiy object as child of root

        :param path:
        :type path:
        :param meta:
        :type meta:
        :return:
        :rtype:
        """
        entity = self._root
        return self._add_node_by_path(entity, path, meta, 0, project_name)

    def get_entity_by_id(self, entity_id):
        """
        Query object from data storage by id

        :param entity_id:
        :type entity_id:
        :return Entity:
        :rtype:
        """
        return self._ssn.query(Entity).get(entity_id) #.one_or_none()

    def _find_node_by_path(self, entity, path, depth):
        node = None
        for child in entity.children:
            if child.name == path[depth]:
                node = child
                break
        if node is None:
            return None
        if depth != len(path) - 1:
            return self._find_node_by_path(node, path, depth + 1)
        else:
            return node

    def get_entity(self, path):
        entity = self._root
        return self._find_node_by_path(entity, path, 0)

    def _add_node_by_path(self, entity, path, meta, depth, project_name=None):
        """
        Private method of WH

        Add Entity to input parent node with path ans meta requirements

        :param entity:
        :type entity:
        :param path:
        :type path:
        :param meta:
        :type meta:
        :param depth:
        :type depth:
        :return:
        :rtype:
        """
        node = None
        for child in entity.children:
            if child.name == path[depth]:
                node = child
                break
        if node is None:
            node = self.add_child(entity, path[depth], meta[depth],
                                  project_name=project_name)
        if depth != len(path) - 1:
            return self._add_node_by_path(node, path, meta, depth + 1,
                                          project_name)
        else:
            return node

    def get_child(self, entity, name):
        """
        Get child by name from input entity

        :param entity:
        :type entity:
        :param name:
        :type name:
        :return Entity:
        :rtype:
        """

        for child in entity.children:
            if child.name == name:
                return child
        return None


    def add_child(self, entity, name, meta=None, project_name=None):
        """
        Add child to input entity
        with  input name and meta

        :param entity:
        :type entity:
        :param name:
        :type name:
        :param meta:
        :type meta:
        :return:
        :rtype:
        """

        for child in entity.children:
            if child.name == name:
                return child
        new_child = Entity(_name=name, _dimension_name=meta[0], _layer=meta[1],
                           project=project_name)
        entity.children.append(new_child)
        return new_child


    def get_time_scale(self, ts_name):
        """
        Query TimeScale by given timescale name

        :param ts_name:
        :type ts_name:
        :return TimeScale ORM obj:
        :rtype:
        """
        return self._ssn.query(TimeScale)\
            .filter(TimeScale.name == ts_name).one_or_none()

    def add_time_scale(self, name, time_line):
        """
        Add time scale by given name and fill
        input time_line.

        Query TimeScale from datastorage, and stamp by stamp
        create TimePoint object and link it to TimeScale

        Args:
            TimeLine: dict - {'period_name':'period_stamp'}
            Name: str

        Return TimeScale

        :param name:
        :type name:
        :param time_line:
        :type time_line:
        :return TimeScale:
        :rtype:
        """
        time_scale = self._ssn.query(TimeScale) \
            .filter(TimeScale.name == name).one_or_none()
        if time_scale is None:
            time_scale = TimeScale(name=name)
            for period_name, period_stamp in time_line.items():
                tp = TimePoint(name=period_name, timestamp=period_stamp)
                time_scale.timeline.append(tp)
            self._ssn.add(time_scale)
        else:
            # Init values
            min_old_stamp = min(time_scale.timeline,
                                key=attrgetter('timestamp')).timestamp
            max_old_stamp = max(time_scale.timeline,
                                key=attrgetter('timestamp')).timestamp
            min_new_stamp = None
            for key in time_line:
                min_new_stamp = time_line[key]
                break
            try:
                max_new_stamp = next(reversed(time_line.values()))
            except:
                ex.NotExistsValueError('TimeStamp', 'max_new_stamp',
                                       'No time_stamps in time_line',
                                       'add_time_scale')
            # Check values on Exception
            if max_new_stamp < min_old_stamp:
                delta = min_old_stamp - max_new_stamp
                if delta.days > 31:
                    raise ex.WrongValueError(
                        delta.days, 'value < 31',
                        'Less then one month length',
                        'add_time_scale')
            if min_new_stamp is None:
                raise ex.NotExistsValueError('TimeStamp', 'min_new_stamp',
                                             'No time_stamps in time_line',
                                             'add_time_scale')
            if min_new_stamp > max_old_stamp:
                delta = min_new_stamp - max_old_stamp
                if delta.days > 31:
                    raise ex.WrongValueError(
                        delta.days, 'value <= 31',
                        'Difference between timestamps limits must be not '
                        'higher then one month',
                        'add_time_scale')
            # Add new TimePoints
            for period_name, period_stamp in time_line.items():
                if period_stamp < min_old_stamp\
                        or period_stamp > max_old_stamp:
                    tp = TimePoint(name=period_name, timestamp=period_stamp)
                    time_scale.timeline.append(tp)
        return time_scale

    """
    Entity methods
    """
    def _get_ent_root(self, ent):
        if ent.name == 'root':
            return self
        for parent in ent.parents:
            return self._get_ent_root(parent)
        raise ex.NotFoundError('Entity', 'root', 'root', '', '_get_root')


    def _get_ent_path(self, ent, path):
        """
        Return entity path by given entity

        :param ent:
        :type ent:
        :param path:
        :type path:
        :return:
        :rtype:
        """
        if ent == None:
            return list()
        if ent.name == 'root':
            return
        path.insert(0, ent.name)
        if ent.parent is not None:
            self._get_ent_path(ent.parent, path)

    def _get_ent_path_meta(self, ent, path_meta):
        """
        Get path of meta of gicen entity

        :param ent:
        :type ent:
        :param path_meta:
        :type path_meta:
        :return:
        :rtype:
        """

        if ent.name == 'root':
            return
        path_meta.insert(0, self.meta)
        if ent.parent is not None:
            self._get_path_meta(ent.parent, path_meta)

    def get_ent_variables_names(self, ent):
        """
        Get ent variable name

        :param ent:
        :type ent:
        :return:
        :rtype:
        """

        return [x.name for x in ent._variables]

    def get_ent_variable(self, ent, name):
        """
        Get variable by name of given entity
        Inputs:
            entity
            name

        :param ent:
        :type ent:
        :param name:
        :type name:
        :return Variable:
        :rtype:
        """
        #TODO check if variable exist
        for var in ent._variables:
            if var.name == name:
                return var
        return None

    def add_ent_variable(self, ent, var_name):
        """
        Add entity variable
        :param ent:
        :type ent:
        :param var_name:
        :type var_name:
        :return:
        :rtype:
        """
        new_var = Variable(_name=var_name)
        ent._variables.append(new_var)


    def force_ent_variable(self, ent, name, data_type, default_value=None):
        """

        Create new variable for given entity,
        assign name and default value

        :param ent:
        :type ent:
        :param name:
        :type name:
        :param data_type:
        :type data_type:
        :param default_value:
        :type default_value:
        :return:
        :rtype:
        """
        # Check if variable with the name already exists.
        for var in ent._variables:
            if var.name == name:
                return var
        # Check if data type is valid.
        try:
            type_enum = DataType[data_type]
        except KeyError:
            raise ex.NotFoundError('DataType', 'DataType', data_type,
                                   'Not found value in dict by key',
                                   'force_variable')
        # Validate default value.
        if default_value is not None:
            try:
                cast_value(type_enum, default_value)
            except ValueError:
                raise ex.WrongValueError(default_value, type_enum,
                                         'Value not from enum',
                                         'force_variable')
        else:
            default_value = get_default_value(type_enum)
        # Create new variable.
        new_var = Variable(_name=name, _data_type=type_enum.value,
                           _default_value=default_value)
        ent._variables.append(new_var)
        return new_var

    """
    Timescale methods
    """
    def get_label_by_stamp(self, timescale, stamp):
        """
        Return label by stamp, for given timescale

        :param timescale:
        :type timescale:
        :param stamp:
        :type stamp:
        :return:
        :rtype:
        """

        try:
            for x in timescale.timeline:
                if x.timestamp == stamp:
                    return x.name
            return None
            #label = next(x.name for x in self.timeline
            #                 if x.timestamp == stamp)
            #return label
        except StopIteration:
            raise ex.NotFoundError('TimeStamp', 'stamp', stamp,
                                   'No label was found by timestamp',
                                   'get_label_by_stamp')

    def get_stamp_by_label(self, timescale, label):
        #TODO fill stamp by label
        """

        :param timescale:
        :type timescale:
        :param label:
        :type label:
        :return:
        :rtype:
        """
        try:
            for x in timescale.timeline:
                if x.name == str(label):
                    return x.timestamp
            return None

            #timestamp = next(x.timestamp for x in self.timeline
            #                 if x.name == label)
            return timestamp
        except StopIteration:
            raise ex.NotFoundError('TimeStamp', 'label', label,
                                   'No timestamp was found by label',
                                   'get_stamp_by_label')

    def get_stamps_by_start_label(self, timescale, start_label, length):
        #TODO fill stamp by start label
        """

        :param timescale:
        :type timescale:
        :param start_label:
        :type start_label:
        :param length:
        :type length:
        :return:
        :rtype:
        """
        start_timestamp = self.get_stamp_by_label(timescale, start_label)
        timestamps = sorted([x.timestamp for x in timescale.timeline
                             if x.timestamp >= start_timestamp])
        if len(timestamps) < length:
            raise ex.WrongValueError(len(timestamps),
                                     'length >= ' + str(length),
                                     'Wrong timestamps length',
                                     'get_stamps_by_start_label')
        return timestamps[:length]


    def get_stamps_for_range(self, timescale, start_point, end_point):
        #TODO get stamp for range
        """

        :param timescale:
        :type timescale:
        :param start_point:
        :type start_point:
        :param end_point:
        :type end_point:
        :return:
        :rtype:
        """
        timestamps = sorted([x.timestamp for x in timescale.timeline
                             if start_point <= x.timestamp <= end_point])
        if timestamps[0] != start_point or timestamps[-1] != end_point:
            raise ex.WrongValueError(
                str(timestamps[0]) + ' or ' + str(timestamps[-1]),
                str(start_point) + ' or ' + str(end_point),
                'Query result not equals to the filter',
                'get_stamps_for_range')
        return timestamps


    #Variable methods
    def get_var_time_series_names(self, var):
        #TODO get var time series names
        """

        :param var:
        :type var:
        :return:
        :rtype:
        """
        return [x.name for x in var._time_series]

    def get_var_time_series(self, var, ts_name):
        #TODO get var time series
        """

        :param var:
        :type var:
        :param ts_name:
        :type ts_name:
        :return:
        :rtype:
        """
        for ts in var._time_series:
            if ts.name == ts_name:
                return ts
        return None

    def force_var_time_series(self, var, time_scale):
        #TODO force var time seties
        """

        :param var:
        :type var:
        :param time_scale:
        :type time_scale:
        :return:
        :rtype:
        """
        if time_scale is None:
            raise ex.NotExistsValueError('TimeScale', 'time_scale', '',
                                         'force_time_series')
        ts_name = time_scale.name
        for ts in var._time_series:
            if ts.name == ts_name:
                return ts
        time_series = TimeSeries(_name=ts_name)
        time_series._time_scale = time_scale
        var._time_series.append(time_series)
        return time_series

    #Timeseries methods

    def get_ts_timeline(self, ts):
        """
        Get timeline from given TimeSeries

        :param ts:
        :type ts:
        :return:
        :rtype:
        """
        return ts._time_scale.timeline

    def set_ts_values(self, ts, start_label, values):
        #TODO overview get ts values
        """
        Set timeseries value for input timeserie
        with requirement to
        :param ts:
        :type ts:
        :param start_label:
        :type start_label:
        :param values:
        :type values:
        :return:
        :rtype:
        """

        # Get timestamps for new values.
        new_stamps = self.get_stamps_by_start_label(ts._time_scale, start_label,
                                                                len(values))
        new_start = new_stamps[0]
        new_end = new_stamps[-1]
        # Check and adjust current borders.
        if ts._start is None:
            ts._start = new_start
            ts._end = new_end
        else:
            # Check for gaps
            gap_timestamps = []
            # Gap to the right.
            if ts._end < new_start:
                gap_timestamps = \
                    self.get_stamps_for_range(ts._time_scale, ts._end,
                                                          new_start)[1:-1]
            # Gap to the left.
            if ts._start > new_end:
                gap_timestamps = \
                    self.get_stamps_for_range(ts._time_scale, new_end,
                                                          ts._start)[1:-1]
            # Shift borders according to latest data.
            if new_start < ts._start:
                ts._start = new_start
            if new_end > ts._end:
                ts._end = new_end
            # Fill gaps with default values
            for time_point in gap_timestamps:
                point = Value(timestamp=time_point,
                              data_type=ts._variable.data_type)
                point.set(self._variable.default_value)
                ts._values.append(point)

        # Set new values.
        # Get existing points from range defined in inputs.
        existing_points = \
            sorted([x for x in ts._values
                    if new_stamps[0] <= x.timestamp <= new_stamps[-1]],
                   key=lambda x: x.timestamp)
        # For range defined in inputs find old points or create new.
        # Set new values.
        for ind, stamp in enumerate(new_stamps):
            point_to_set = None
            for curr_point in existing_points:
                if curr_point.timestamp > stamp:
                    break
                if curr_point.timestamp == stamp:
                    point_to_set = curr_point
                    break
            if point_to_set is None:
                point_to_set = Value(timestamp=stamp,
                                     data_type=ts._variable.data_type)
                ts._values.append(point_to_set)
                self.set_value(point_to_set, values[ind])

    def get_ts_values(self, ts, period=None):
        """
        Return timeseries values from given period


        :param ts:
        :type ts:
        :param period:
        :type period:
        :return:
        :rtype:
        """

        if period is None:
            # Get all points
            return [x.get() for x in
                    sorted(ts._values, key=lambda y: y.timestamp)]
        else:
            # Get timestamp from start label.
            start = self.get_stamp_by_label(ts._time_scale, period[0])
            end = self._time_scale.get_stamp_by_label(ts._time_scale, period[1])
            # Get all points in range start end.
            points = sorted([x for x in ts._values
                             if start <= x.timestamp <= end],
                            key=lambda x: x.timestamp)

            return [x.get() for x in points]

    def get_ts_value(self, ts, time_label):
        """
        Return timelabale value from input TimeSeries

        :param ts:
        :type ts:
        :param time_label:
        :type time_label:
        :return:
        :rtype:
        """
        timestamp = ts._time_scale.get_stamp_by_label(time_label)
        try:
            return next(x.get() for x in ts._values
                        if x.timestamp == timestamp)
        except StopIteration:
            return None

    """
    Value methods
    """
    def get_value(self, val):
        """
        Get value of
        :param val:
        :type val:
        :return:
        :rtype:
        """

        if val.data_type == 0:
            return val.float_value
        if val.data_type == 1:
            return val.int_value
        if val.data_type == 2:
            return val.text_value

    def set_value(self, val, value):

        val.modified_date = datetime.now()
        if value == '':
            value = get_default_value(val.data_type)
        if val.data_type == 0:
            val.float_value = value
            return
        if val.data_type == 1:
            val.int_value = value
            return
        if val.data_type == 2:
            val.text_value = value
            return

    """
    Native methods of Warehouse
    """
    def bulk_inser_entity(self, obj_list):
        self._ssn.bulk_insert_mappings(Entity, obj_list)

    def bulk_inser_variable(self, obj_list):
        self._ssn.bulk_insert_mappings(Variable, obj_list)

    def bulk_inser_timeseries(self, obj_list):
        self._ssn.bulk_insert_mappings(TimeSeries, obj_list)

    def bulk_inser_values(self, obj_list):
        self._ssn.bulk_insert_mappings(Value, obj_list)

    def commit(self):
        self._ssn.commit()

    def rollback(self):
        self._ssn.rollback()

    def save_entity_df(self, df, schema):
        df.to_sql('entities', con=self._ssn, schema=schema, if_exists='append')

    def save__df(self, df, schema):
        df.to_sql('entities', con=self._ssn, schema=schema, if_exists='append')

    def flush(self):
        self._ssn.flush()

    def refresh(self, obj):
        self._ssn.refresh(obj)

    def expire(self, obj):
        self._ssn.expire(obj)

