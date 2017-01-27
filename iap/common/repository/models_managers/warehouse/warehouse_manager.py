from .enity_manager import _add_node_by_path, _find_node_by_path
from iap.common.repository.models.warehouse import *

class Warehouse:

    def __init__(self, ssn_factory):
        self._ssn = ssn_factory()
        self._root = self._ssn.query(Entity)\
            .filter(Entity.name == 'root').one_or_none()

    def get_root(self):
        return self._root

    def add_entity(self, path, meta):
        session = self._ssn
        entity_id = self._root.id
        return _add_node_by_path(session, self._root, path, meta, 0)

    def get_entity(self, path):
        session = self._ssn
        entity_id = self._root.id
        return _find_node_by_path(session, entity_id, path, 0)

    def get_entity_by_id(self, entity_id):
        return self._ssn.query(Entity).get(entity_id)  # .one_or_none()

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