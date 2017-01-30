from ..models.warehouse import *



class Warehouse:

    def __init__(self, ssn_factory):
        self._ssn = ssn_factory()
        self._root = self._ssn.query(Entity)\
            .filter(Entity.name == 'root').one_or_none()

    #common warehouse methods

    def get_root(self):
        return self._root

    def add_entity(self, path, meta):
        entity = self._root
        return self._add_node_by_path(entity, path, meta, 0)

    def get_entity_by_id(self, entity_id):

        return self._ssn.query(Entity).get(entity_id)  # .one_or_none()

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

    def _add_node_by_path(self, entity, path, meta, depth):
        node = None
        for child in entity.children:
            if child.name == path[depth]:
                node = child
                break
        if node is None:
            node = self.add_child(entity, path[depth], meta[depth])
        if depth != len(path) - 1:
            return self._add_node_by_path(node, path, meta, depth + 1)
        else:
            return node

    def get_child(self, entity, name):
        for child in entity.children:
            if child.name == name:
                return child
        return None

    def add_child(self, entity, name, meta):
        for child in entity.children:
            if child.name == name:
                return child
        new_child = Entity(_name=name, _dimension_name=meta[0], _layer=meta[1])
        entity.children.append(new_child)
        return new_child

    def get_time_scale(self, ts_name):
        return self._ssn.query(TimeScale)\
            .filter(TimeScale.name == ts_name).one_or_none()

    def add_time_scale(self, name, time_line):
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

    #Entity methods

    def _get_ent_root(self, ent):
        if ent.name == 'root':
            return self
        for parent in self.parents:
            return self._get_ent_root(parent)
        raise ex.NotFoundError('Entity', 'root', 'root', '', '_get_root')

    def _get_ent_path(self, ent, path):
        if ent == None:
            return list()
        if ent.name == 'root':
            return
        path.insert(0, ent.name)
        if ent.parent is not None:
            self._get_ent_path(ent.parent, path)

    def _get_ent_path_meta(self, ent, path_meta):
        if ent.name == 'root':
            return
        path_meta.insert(0, self.meta)
        if ent.parent is not None:
            self._get_path_meta(ent.parent, path_meta)

    def get_ent_variables_names(self, ent):
        return [x.name for x in ent._variables]

    def get_ent_variable(self, ent, name):
        for var in ent._variables:
            if var.name == name:
                return var
        return None

    def force_ent_variable(self, ent, name, data_type, default_value=None):
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

    #Timescale methods

    def get_label_by_stamp(self, timescale, stamp):
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
        return [x.name for x in var._time_series]

    def get_var_time_series(self, var, ts_name):
        for ts in var._time_series:
            if ts.name == ts_name:
                return ts
        return None

    def force_var_time_series(self, var, time_scale):
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
        return ts._time_scale.timeline

    def set_ts_values(self, ts, start_label, values):
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

    def get_ts_value(self, ts,time_label):
        timestamp = ts._time_scale.get_stamp_by_label(time_label)
        try:
            return next(x.get() for x in ts._values
                        if x.timestamp == timestamp)
        except StopIteration:
            return None

    #Value methods
    def get_value(self, val):
        if val.data_type == 0:
            return val.float_value
        if val.data_type == 1:
            return val.int_value
        if val.data_type == 2:
            return val.text_value

    def set_value(self,val, value):

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

    #Native methods of Warehouse
    def get_var_values(self):
        pass


    def commit(self):
        self._ssn.commit()

    def rollback(self):
        self._ssn.rollback()