#Warehouse manager
from iap.common.repository import exceptions as ex
from sqlalchemy.orm.exc import NoResultFound
from iap.common.repository.models.warehouse import TimeScale


def get_label_by_stamp(request, id, stamp):
    try:
        timescale = request.TimeScale.filter(TimeScale.id == id).one()
        for x in timescale.timeline:
            if x.timestamp == stamp:
                return x.name
        return None
        # label = next(x.name for x in self.timeline
        #                 if x.timestamp == stamp)
        # return label
    except NoResultFound:
        raise ex.NotFoundError('TimeStamp', 'stamp', stamp,
                                       'No label was found by timestamp',
                                       'get_label_by_stamp')
    except StopIteration:
        raise ex.NotFoundError('TimeStamp', 'stamp', stamp,
                               'No label was found by timestamp',
                               'get_label_by_stamp')


def get_stamp_by_label(request, id, label):
    try:
        timescale = request.TimeScale.filter(TimeScale.id == id).one()
        for x in timescale.timeline:
            if x.name == str(label):
                return x.timestamp
        return None

        # timestamp = next(x.timestamp for x in self.timeline
        #                 if x.name == label)
        return timestamp

    except NoResultFound:
        raise ex.NotFoundError('TimeStamp', 'label', label,
                               'No timestamp was found by label',
                               'get_stamp_by_label')
    except StopIteration:
        raise ex.NotFoundError('TimeStamp', 'label', label,
                               'No timestamp was found by label',
                               'get_stamp_by_label')


def get_stamps_by_start_label(request, id, start_label, length):

    try:
        timescale = request.TimeScale.filter(TimeScale.id == id).one()

        start_timestamp = get_stamp_by_label(request, id, start_label)

        timestamps = sorted([x.timestamp for x in timescale.timeline
                         if x.timestamp >= start_timestamp])
        if len(timestamps) < length:
            raise ex.WrongValueError(len(timestamps),'length >= ' + str(length),
                                                     'Wrong timestamps length',
                                                     'get_stamps_by_start_label')
        return timestamps[:length]

    except NoResultFound:
        raise ex.NotFoundError('TimeStamp', 'id', id,
                               'No timestamp was found by id',
                               'get_stamps_by_start_label')


def get_stamps_for_range(request, id, start_point, end_point):

    try:
        timescale = request.TimeScale.filter(TimeScale.id == id).one()

        timestamps = sorted([x.timestamp for x in timescale.timeline
                             if start_point <= x.timestamp <= end_point])
        if timestamps[0] != start_point or timestamps[-1] != end_point:
            raise ex.WrongValueError(
                str(timestamps[0]) + ' or ' + str(timestamps[-1]),
                str(start_point) + ' or ' + str(end_point),
                'Query result not equals to the filter',
                'get_stamps_for_range')
        return timestamps

    except NoResultFound:
        raise ex.NotFoundError('TimeScale', 'id', id,
                               'No timestamp was found by id',
                               'get_stamps_for_range')