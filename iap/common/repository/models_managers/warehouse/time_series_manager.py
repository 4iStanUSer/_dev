def get_timeline(self):
    return self._time_scale.timeline


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
                                 data_type=self._variable.data_type)
            self._values.append(point_to_set)
            point_to_set.set(values[ind])


def get_values(self, period=None):
    if period is None:
        # Get all points
        return [x.get() for x in
                sorted(self._values, key=lambda y: y.timestamp)]
    else:
        # Get timestamp from start label.
        start = self._time_scale.get_stamp_by_label(period[0])
        end = self._time_scale.get_stamp_by_label(period[1])
        # Get all points in range start end.
        points = sorted([x for x in self._values
                         if start <= x.timestamp <= end],
                        key=lambda x: x.timestamp)

        return [x.get() for x in points]


def get_value(self, time_label):
    timestamp = self._time_scale.get_stamp_by_label(time_label)
    try:
        return next(x.get() for x in self._values
                    if x.timestamp == timestamp)
    except StopIteration:
        return None