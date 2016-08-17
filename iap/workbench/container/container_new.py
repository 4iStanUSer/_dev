import numpy as np

class Container:

    def __init__(self):
        self._root = CEntity()
        self._last_id = 0
        self._nodes_dict = {'0': self._root}

    def add_entity(self, path):
        self._root.add_node_by_path(path, 0)

    def get_entity_by_id(self, entity_id):
        try:
            return self._nodes_dict[entity_id]
        except KeyError:
            return None

    def add_time_scale(self, name, time_line):
        pass


class CEntity:

    def __init__(self, name):
        self._name = name
        self._parents = None
        self._children = None
        self._variables = None

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
        self._name = name
        self._entity = entity
        self._time_series = None
        self._default_value = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if self._name == name:
            return
        if name in self._entity.get_variables_names():
            raise Exception
        self._name = name

    @property
    def default_value(self):
        return self._default_value

    def get_time_series(self, ts_name):
        for ts in self._time_series:
            if ts.name == ts_name:
                return ts
        return None

    def force_time_series(self, ts_name):
        for ts in self._time_series:
            if ts.name == ts_name:
                return ts
        #TODO add getter from timescale
        time_scale = None
        if time_scale is None:
            raise Exception
        time_series = CTimeSeries(ts_name, self)
        time_series._time_scale = time_scale
        self._time_series.append(time_series)
        return time_series


class CTimeSeries:

    def __init__(self, name, variable, length):
        self._name = name
        self._variable = variable
        self._start = None
        self._end = None
        self._values = [self._variable.default_value] * length

    @property
    def name(self):
        return self._name

    @property
    def start_point(self):
        return self._start

    @property
    def end_point(self):
        return self._end

    def set_values(self, start_label, values):




        # Get timestamps for new values.
        new_stamps = self._time_scale.get_stamps_by_start_label(start_label,
                                                                len(values))
        new_start = new_stamps[0]
        new_end = new_stamps[-1]
        # Check and adjust current borders.
        if self._start is None:
            self._start = new_start
            self._end = new_end
        else:
            # Check for gaps
            gap_timestamps = []
            # Gap to the right.
            if self._end < new_start:
                gap_timestamps = \
                    self._time_scale.get_stamps_for_range(self._end,
                                                          new_start)[1:-1]
            # Gap to the left.
            if self._start > new_end:
                gap_timestamps = \
                    self._time_scale.get_stamps_for_range(new_end,
                                                          self._start)[1:-1]
            # Shift borders according to latest data.
            if new_start < self._start:
                self._start = new_start
            if new_end > self._end:
                self._end = new_end
            # Fill gaps with default values
            for time_point in gap_timestamps:
                point = Value(timestamp=time_point,
                              data_type=self._variable.data_type)
                point.set(self._variable.default_value)
                self._values.append(point)

        # Set new values.
        ssn = object_session(self)
        # Get existing points from range defined in inputs.
        existing_points = ssn.query(Value) \
            .filter(Value.time_series_id == self._id,
                    Value.timestamp.in_(new_stamps)) \
            .order_by(Value.timestamp).all()
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
                                     data_type=self._variable.data_type)
                self._values.append(point_to_set)
                point_to_set.set(values[ind])

    def get_values(self, start_label=None, length=None):
        ssn = object_session(self)
        if start_label is None:
            # Get all points
            points = ssn.query(Value) \
                .filter(Value.time_series_id == self._id) \
                .order_by(Value.timestamp).all()
        else:
            # Get timestamp from label.
            start_point = ssn.query(TimePoint) \
                .filter(TimePoint.time_scale_id == self._id,
                        TimePoint.name == start_label).one_or_none()
            if start_point is None:
                raise Exception
            else:
                start = start_point.timestamp
            # Get all points from start.
            points = ssn.query(Value) \
                .filter(Value.time_series_id == self._id,
                        Value.timestamp >= start) \
                .order_by(Value.timestamp).all()
            # Limit length, if length is less than expected throw exception.
            if length is not None:
                if len(points) < length:
                    raise Exception
                points = points[:length]
        # Return values of points found.
        return [x.get() for x in points]

    def get_value(self, time_label):
        return self.get_values(time_label, 1)
