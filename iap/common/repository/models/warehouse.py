from iap.common.repository import exceptions as ex


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
from iap.common.helper import Meta
#from .....helper import Meta

from iap.common.repository.db.meta import Base

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




class TimeScale(Base):
    __tablename__ = 'time_scales'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    timeline = relationship('TimePoint', back_populates='time_scale')

    def get_label_by_stamp(self, stamp):
        try:
            for x in self.timeline:
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

    def get_stamp_by_label(self, label):
        try:
            for x in self.timeline:
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

    def get_stamps_by_start_label(self, start_label, length):
        start_timestamp = self.get_stamp_by_label(start_label)
        timestamps = sorted([x.timestamp for x in self.timeline
                             if x.timestamp >= start_timestamp])
        if len(timestamps) < length:
            raise ex.WrongValueError(len(timestamps),
                                     'length >= ' + str(length),
                                     'Wrong timestamps length',
                                     'get_stamps_by_start_label')
        return timestamps[:length]

    def get_stamps_for_range(self, start_point, end_point):
        timestamps = sorted([x.timestamp for x in self.timeline
                             if start_point <= x.timestamp <= end_point])
        if timestamps[0] != start_point or timestamps[-1] != end_point:
            raise ex.WrongValueError(
                str(timestamps[0]) + ' or ' + str(timestamps[-1]),
                str(start_point) + ' or ' + str(end_point),
                'Query result not equals to the filter',
                'get_stamps_for_range')
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
                raise ex.AlreadyExistsError('Entity', 'name', name, 'name')
        self._name = name

    @property
    def path(self):
        p = []
        self._get_path(p)
        return p

    @property
    def path_meta(self):
        p = []
        self._get_path_meta(p)
        return p

    @property
    def meta(self):
        return Meta(self._dimension_name, self._layer)

    @property
    def parent(self):
        if len(self.parents) != 1:
            return None
        return self.parents[0]

    @property
    def variables(self):
        return self._variables
    #@hybrid_property
    #def dimension(self):
    #    return self._dimension_name

    #@dimension.setter
    #def dimension(self, dimension_name):
    #    for parent in self.parents:
    #        if dimension_name in [x.dimension for x in parent.children if x.id
    #                != self.id]:
    #            raise ex.AlreadyExistsError(
    #                'Entity', 'dimension_name', dimension_name, 'dimension')
    #    self._dimension_name = dimension_name

    #@hybrid_property
    #def layer(self):
    #    return self._layer

    #@layer.setter
    #def layer(self, layer):
    #    for parent in self.parents:
    #        if layer in [x.layer for x in parent.children if x.id
    #                != self.id]:
    #            raise ex.AlreadyExistsError('Entity', 'layer', layer, 'layer')
    #    self._layer = layer

    #def add_parent(self, path):
    #    root = self._get_root()
    #    new_parent = root._add_node_by_path(path, 0)
    #    if new_parent not in self.parents:
    #        if self.name in [x.name for x in new_parent.children]:
    #            raise ex.AlreadyExistsError('Entity', 'name', self.name,
    #                                        'add_parent')
    #        self.parents.append(new_parent)
    #    return new_parent



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
            raise ex.AlreadyExistsError('Variable', 'name', name, 'name')
        self._name = name

    @property
    def data_type(self):
        return self._data_type

    @property
    def default_value(self):
        return self._default_value




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

    @property
    def end_point(self):
        return self._end




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


project_tool_tbl = Table("project_tool", Base.metadata,
                                Column("projects_id", String, ForeignKey("projects.id"),primary_key=True),
                                Column("tools_id", String, ForeignKey("tools.id"), primary_key=True)
                          )

class Project(Base):
    __tablename__ = "projects"
    id = Column(String , primary_key=True)
    name = Column(String(length=255))
    description = Column(String(length=255))
    pr_tools = relationship("Pr_Tool", secondary=project_tool_tbl, back_populates="projects")


class Pr_Tool(Base):
    __tablename__ = "tools"
    id = Column(String, primary_key=True)
    name = Column(String(length=255))
    description = Column(String(length=255))
    project_id = Column(Integer, ForeignKey('projects.id'))
    projects = relationship("Project", secondary=project_tool_tbl, back_populates="pr_tools")



