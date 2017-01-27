from iap.common.repository.models.warehouse import TimeSeries

def get_time_series_names(self):
    return [x.name for x in self._time_series]


def get_time_series(self, ts_name):
    for ts in self._time_series:
        if ts.name == ts_name:
            return ts
    return None


def force_time_series(self, time_scale):
    if time_scale is None:
        raise ex.NotExistsValueError('TimeScale', 'time_scale', '',
                                     'force_time_series')
    ts_name = time_scale.name
    for ts in self._time_series:
        if ts.name == ts_name:
            return ts
    time_series = TimeSeries(_name=ts_name)
    time_series._time_scale = time_scale
    self._time_series.append(time_series)
    return time_series