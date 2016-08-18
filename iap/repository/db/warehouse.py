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


def add_entity(ssn, path):
    root = ssn.query(Entity).filter(Entity.name == 'root').one_or_none()
    return root._add_node_by_path(path, 0)


def get_entity_by_id(ssn, entity_id):
    return ssn.query(Entity).get(entity_id).one_or_none()


def add_time_scale(ssn, name, time_line):
    time_scale = ssn.query(TimeScale)\
        .filter(TimeScale.name == name).one_or_none()
    if time_scale is None:
        time_scale = TimeScale(name=name)
        for period_name, period_stamp in time_line.items():
            tp = TimePoint(name=period_name, timestamp=period_stamp)
            time_scale.timeline.append(tp)
        ssn.add(time_scale)


class TimeScale(Base):
    __tablename__ = 'time_scales'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    timeline = relationship('TimePoint', back_populates='timescale')

    def get_stamps_by_start_label(self, start_label, length):
        ssn = object_session(self)
        start_point = ssn.query(TimePoint)\
            .filter(TimePoint.time_scale_id == self.id,
                    TimePoint.name == start_label).one_or_none()
        if start_point is None:
            raise Exception
        points = ssn.query(TimePoint)\
            .filter(TimePoint.time_scale_id == self.id,
                    TimePoint.timestamp >= start_point.timestamp)\
            .order_by(TimePoint.timestamp).limit(length).all()
        if len(points) < length:
            raise Exception
        return [x.timestamp for x in points]

    def get_stamps_for_range(self, start_point, end_point):
        ssn = object_session(self)
        points = ssn.query(TimePoint)\
            .filter(TimePoint.time_scale_id == self.id,
                    TimePoint.timestamp >= start_point,
                    TimePoint.timestamp <= end_point)\
            .order_by(TimePoint.timestamp).all()
        if points[0].timestamp != start_point or \
                points[-1].timestamp != end_point:
            raise Exception
        return [x.timestamp for x in points]


class TimePoint(Base):
    __tablename__ = 'time_lines'
    id = Column(Integer, primary_key=True)
    time_scale_id = Column(Integer, ForeignKey('time_scales.id'))
    name = Column(String(length=255))
    timestamp = Column(DateTime)
    timescale = relationship('TimeScale', back_populates='timeline')


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

    def add_parent(self, path):
        root = self._get_root()
        new_parent = root._add_node_by_path(path, 0)
        if new_parent not in self.parents:
            if self.name in [x.name for x in new_parent.children]:
                raise Exception
            self.parents.append(new_parent)
        return new_parent

    def add_child(self, name):
        for child in self.children:
            if child.name == name:
                return child
        new_child = Entity(_name=name)
        self.children.append(new_child)
        return new_child

    def _add_node_by_path(self, path, depth):
        node = None
        for child in self.children:
            if child.name == path[depth]:
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

    def force_time_series(self, ts_name):
        for ts in self._time_series:
            if ts.name == ts_name:
                return ts
        ssn = object_session(self)
        time_scale = ssn.query(TimeScale)\
            .filter(TimeScale.name == ts_name).one_or_none()
        if time_scale is None:
            raise Exception
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
        ssn = object_session(self)
        # Get existing points from range defined in inputs.
        existing_points = ssn.query(Value)\
            .filter(Value.time_series_id == self._id,
                    Value.timestamp.in_(new_stamps))\
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
                return []
                # raise Exception
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





