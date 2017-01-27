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
from iap.common.repository.models.warehouse import Entity, Variable, TimeSeries, TimeScale, TimePoint
import enum
from ....helper import Meta
from ...db.meta import Base

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

    def get_root(self):
        return self._root

    def add_entity(self, path, meta):
        entity = self._root
        return self._add_node_by_path(entity, path, meta, 0)

    def get_entity(self, path):
        entity = self._root
        return _find_node_by_path(entity, path, 0)

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
            return _find_node_by_path(node, path, depth + 1)
        else:
            return node


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

    def commit(self):
        self._ssn.commit()

    def rollback(self):
        self._ssn.rollback()