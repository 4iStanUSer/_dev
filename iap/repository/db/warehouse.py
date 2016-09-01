from sqlalchemy import (
    Table,
    ForeignKey,
    Column,
    Integer,
    String,
    Float,
    DateTime
)
from sqlalchemy.orm import relationship, object_session
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
import enum


from .meta import Base

from operator import attrgetter


class DataType(enum.IntEnum):
    float = 0
    int = 1
    string = 2


def get_default_value(type_index):
    if type_index == DataType.float:
        return 0.0
    if type_index == DataType.int:
        return 0
    if type_index == DataType.string:
        return ''


def cast_value(type_index, value):
    if type_index == DataType.float:
        return float(value)
    if type_index == DataType.int:
        return int(value)
    if type_index == DataType.string:
        return str(value)


class Warehouse:

    def __init__(self, ssn_factory):
        self._ssn = ssn_factory()
        self._root = self._ssn.query(Entity)\
            .filter(Entity.name == 'root').one_or_none()

    def add_entity(self, path):
        return self._root._add_node_by_path(path, 0)

    def get_entity_by_id(self, entity_id):
        return self._ssn.query(Entity).get(entity_id)  # .one_or_none()

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
            max_new_stamp = next(reversed(time_line.values()))
            # Check values on Exception
            if max_new_stamp < min_old_stamp:
                delta = min_old_stamp - max_new_stamp
                if delta.days > 31:
                    raise Exception
            if min_new_stamp is None:
                raise Exception
            if min_new_stamp > max_old_stamp:
                delta = min_new_stamp - max_old_stamp
                if delta.days > 31:
                    raise Exception
            # Add new TimePoints
            for period_name, period_stamp in time_line.items():
                if period_stamp < min_old_stamp\
                        or period_stamp > max_old_stamp:
                    tp = TimePoint(name=period_name, timestamp=period_stamp)
                    time_scale.timeline.append(tp)
        return time_scale

    def commit(self):
        self._ssn.commit()

    def rollback(self):
        self._ssn.rollback()


class TimeScale(Base):
    __tablename__ = 'time_scales'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    timeline = relationship('TimePoint', back_populates='time_scale')

    def get_stamp_by_label(self, label):
        try:
            timestamp = next(x.timestamp for x in self.timeline
                             if x.name == label)
            return timestamp
        except StopIteration:
            raise Exception

    def get_stamps_by_start_label(self, start_label, length):
        start_timestamp = self.get_stamp_by_label(start_label)
        timestamps = sorted([x.timestamp for x in self.timeline
                             if x.timestamp >= start_timestamp])
        if len(timestamps) < length:
            raise Exception
        return timestamps[:length]

    def get_stamps_for_range(self, start_point, end_point):
        timestamps = sorted([x.timestamp for x in self.timeline
                             if start_point <= x.timestamp <= end_point])
        if timestamps[0] != start_point or timestamps[-1] != end_point:
            raise Exception
        return timestamps


class TimePoint(Base):
    __tablename__ = 'time_lines'
    id = Column(Integer, primary_key=True)
    time_scale_id = Column(Integer, ForeignKey('time_scales.id'))
    name = Column(String(length=255))
    timestamp = Column(DateTime)
    time_scale = relationship('TimeScale', back_populates='timeline')


entities_edge = Table(
    'entities_edge',
    Base.metadata,
    Column('parent_id', Integer, ForeignKey('entities._id'), primary_key=True),
    Column('child_id', Integer, ForeignKey('entities._id'), primary_key=True)
)


class Entity(Base):
    __tablename__ = 'entities'
    _id = Column(Integer, primary_key=True)
    _name = Column(String(length=255))
    _layer = Column(String(length=255))
    _dimension_name = Column(String(length=255))
    children = relationship('Entity',
                            secondary=entities_edge,
                            primaryjoin=_id == entities_edge.c.parent_id,
                            secondaryjoin=_id == entities_edge.c.child_id,
                            backref='parents')
    _variables = relationship('Variable', back_populates='_entity')

    @property
    def id(self):
        return self._id

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        for parent in self.parents:
            if name in [x.name for x in parent.children if x.id != self.id]:
                raise Exception
        self._name = name

    @hybrid_property
    def dimension(self):
        return self._dimension_name

    @dimension.setter
    def dimension(self, dimension_name):
        for parent in self.parents:
            if dimension_name in [x.dimension for x in parent.children if x.id
                    != self.id]:
                raise Exception
        self._dimension_name = dimension_name

    @hybrid_property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, layer):
        for parent in self.parents:
            if layer in [x.layer for x in parent.children if x.id
                    != self.id]:
                raise Exception
        self._layer = layer

    def add_parent(self, path):
        root = self._get_root()
        new_parent = root._add_node_by_path(path, 0)
        if new_parent not in self.parents:
            if self.name in [x.name for x in new_parent.children]:
                raise Exception
            self.parents.append(new_parent)
        return new_parent

    def add_child(self, item):
        name = 'Name'
        layer = 'Layer'
        dimension = 'Dimension_name'
        for child in self.children:
            if child.name == item[name] \
                    and child.dimension == item[dimension]\
                    and child.layer == item[layer]:
                return child
        new_child = Entity(_name=item[name], _dimension_name=item[dimension],
                           _layer=item[layer])
        self.children.append(new_child)
        return new_child

    def _add_node_by_path(self, path, depth):
        node = None
        for child in self.children:
            if child.dimension == path[depth]['Dimension_name']\
                    and child.name == path[depth]['Name']\
                    and child.layer == path[depth]['Layer']:
                node = child
                break
        if node is None:
            node = self.add_child(path[depth])
        if depth != len(path) - 1:
            return node._add_node_by_path(path, depth + 1)
        else:
            return node

    def _get_root(self):
        if self.name == 'root':
            return self
        for parent in self.parents:
            return parent._get_root()
        raise Exception

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
        # Check if data type is valid.
        try:
            type_enum = DataType[data_type]
        except KeyError:
            raise Exception
        # Validate default value.
        if default_value is not None:
            try:
                cast_value(type_enum, default_value)
            except ValueError:
                raise Exception
        else:
            default_value = get_default_value(type_enum)
        # Create new variable.
        new_var = Variable(_name=name, _data_type=type_enum.value,
                           _default_value=default_value)
        self._variables.append(new_var)
        return new_var


class Variable(Base):
    __tablename__ = 'variables'
    _id = Column(Integer, primary_key=True)
    _entity_id = Column(Integer, ForeignKey('entities._id'))
    _name = Column(String(length=255))
    _data_type = Column(Integer)
    _entity = relationship('Entity', back_populates='_variables')
    _time_series = relationship('TimeSeries', back_populates='_variable')
    _default_value = Column(String(length=255), default=None)

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
    def data_type(self):
        return self._data_type

    @property
    def default_value(self):
        return self._default_value

    def get_time_series(self, ts_name):
        for ts in self._time_series:
            if ts.name == ts_name:
                return ts
        return None

    def force_time_series(self, time_scale):
        if time_scale is None:
            raise Exception
        ts_name = time_scale.name
        for ts in self._time_series:
            if ts.name == ts_name:
                return ts
        time_series = TimeSeries(_name=ts_name)
        time_series._time_scale = time_scale
        self._time_series.append(time_series)
        return time_series


class TimeSeries(Base):
    __tablename__ = 'time_series'
    _id = Column(Integer, primary_key=True)
    _variable_id = Column(Integer, ForeignKey('variables._id'))
    _time_scale_id = Column(Integer, ForeignKey('time_scales.id'))
    _name = Column(String(length=255))
    _time_scale = relationship('TimeScale')
    _values = relationship('Value')
    _variable = relationship('Variable', back_populates='_time_series')
    _start = Column(DateTime, default=None)
    _end = Column(DateTime, default=None)

    @property
    def name(self):
        return self._name

    @property
    def start_point(self):
        return self._start

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
        # Get existing points from range defined in inputs.
        existing_points = \
            sorted([x for x in self._values
                    if new_stamps[0] <= x.timestamp <= new_stamps[-1]])
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
        if start_label is None:
            # Get all points
            return [x.get() for x in
                    sorted(self._values, key=lambda y: y.timestamp)]
        else:
            # Get timestamp from start label.
            start = self._time_scale.get_stamp_by_label(start_label)
            # Get all points from start.
            points = sorted([x for x in self._values if x.timestamp >= start])
            # Limit length, if length is less than expected throw exception.
            if length is not None:
                if len(points) < length:
                    raise Exception
                points = points[:length]
            return [x.get() for x in points]

    def get_value(self, time_label):
        timestamp = self._time_scale.get_stamp_by_label(time_label)
        try:
            return next(x.get() for x in self._values
                        if x.timestamp == timestamp)
        except StopIteration:
            return None


class Value(Base):
    __tablename__ = 'values'
    id = Column(Integer, primary_key=True)
    time_series_id = Column(Integer, ForeignKey('time_series._id'))
    timestamp = Column(DateTime)
    modified_date = Column(DateTime)
    data_type = Column(Integer)
    float_value = Column(Float(precision=53), server_default=None)
    int_value = Column(Integer, server_default=None)
    text_value = Column(String(length=255), server_default=None)

    def get(self):
        if self.data_type == 0:
            return self.float_value
        if self.data_type == 1:
            return self.int_value
        if self.data_type == 2:
            return self.text_value

    def set(self, value):
        self.modified_date = datetime.now()
        if self.data_type == 0:
            self.float_value = value
        if self.data_type == 1:
            self.int_value = value
        if self.data_type == 2:
            self.text_value = value





