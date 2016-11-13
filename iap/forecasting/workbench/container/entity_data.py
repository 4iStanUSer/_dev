import copy
from enum import IntEnum, unique


@unique
class DataType(IntEnum):
    empty = 0
    time_series = 1
    scalar = 2
    period_series = 4


@unique
class VariableType(IntEnum):
    is_output = 1
    is_driver = 2


class EntityData:
    def __init__(self, time_manager):
        self.time_manager = time_manager
        self._variables = {}
        self._time_series = {}
        self._scalars = {}
        self._periods_series = {}

    def get_backup(self):
        # Variables.
        var_names = list(self._variables.keys())
        var_properties = []
        for var_name, props in self._variables.items():
            for prop_name, prop_value in props.items():
                var_properties.append((dict(var=var_name, prop=prop_name,
                                            value=prop_value)))

        # Time series.
        time_series = [dict(var=var_ts[0], ts=var_ts[1], line=copy.copy(line))
                       for var_ts, line in self._time_series.items()]
        # Scalars.
        scalars = [dict(var=var_ts[0], ts=var_ts[1], value=val)
                   for var_ts, val in self._scalars.items()]
        # Period series.
        period_series = []
        for var_ts, periods in self._periods_series.items():
            for period, value in periods.items():
                period_series.append(dict(var=var_ts[0], ts=var_ts[1],
                                          period=period, value=value))
        # Collect backup.
        backup = dict(var_names=var_names,
                      var_properties=var_properties,
                      time_series=time_series,
                      scalars=scalars,
                      periods_series=period_series)
        return backup

    def load_backup(self, backup):
        try:
            # Variables.
            for name in backup['var_names']:
                self.add_variable(name)
            for item in backup['var_properties']:
                self.set_var_property(item['var'], item['prop'], item['value'])
            # Time series.
            for item in backup['time_series']:
                self.init_slot(item['var'], item['ts'], DataType.time_series)
                self.set_ts_vals(item['var'], item['ts'], item['line'])
            # Scalars.
            for item in backup['scalars']:
                self.init_slot(item['var'], item['ts'], DataType.scalar)
                self.set_scalar_val(item['var'], item['ts'], item['value'])
            # Period series.
            for item in backup['periods_series']:
                if not self.is_exist(item['var'], item['ts'],
                                     DataType.period_series):
                    self.init_slot(item['var'], item['ts'],
                                   DataType.period_series)
                self.set_period_val(item['var'], item['ts'], item['period'],
                                    item['value'])
        except KeyError:
            raise Exception
        return

    @property
    def var_names(self):
        return self._variables.keys()

    def add_variable(self, var_name):
        if var_name not in self._variables:
            self._variables[var_name] = dict()

    def get_var_properties(self, var_name):
        return copy.copy(self._variables[var_name])

    def get_var_property(self, var_name, prop_name):
        var_props = self._variables.get(var_name)
        if var_props is not None:
            return var_props.get(prop_name)
        else:
            return None

    def set_var_property(self, var_name, prop_name, value):
        if var_name not in self._variables:
            raise Exception
        self._variables[var_name][prop_name] = value
        return

    def rename_variable(self, old_name, new_name):
        pass

    def is_exist(self, var_name, ts_name, data_type):
        if data_type == DataType.time_series:
            return (var_name, ts_name) in self._time_series
        elif data_type == DataType.scalar:
            return (var_name, ts_name) in self._scalars
        elif data_type == DataType.period_series:
            return (var_name, ts_name) in self._periods_series
        else:
            raise Exception

    def init_slot(self, var_name, ts_name, data_type):
        if data_type == DataType.time_series:
            def_value = self.get_var_property(var_name, 'default_value')
            if def_value is None:
                def_value = 0
            length = self.time_manager.get_time_length(ts_name)
            self._time_series[(var_name, ts_name)] = [def_value] * length
        elif data_type == DataType.scalar:
            def_value = self.get_var_property(var_name, 'default_value')
            if def_value is None:
                def_value = 0
            self._scalars[(var_name, ts_name)] = def_value
        elif data_type == DataType.period_series:
            self._periods_series[(var_name, ts_name)] = dict()
        else:
            raise Exception

    def get_ts_vals(self, var_name, ts_name, period, length):
        # Get time series.
        ts = self._time_series.get((var_name, ts_name))
        if ts is None:
            raise Exception
        # Define borders.
        start_index = 0
        if period[0] is not None:
            start_index = \
                self.time_manager.get_index(ts_name, period[0])
        end_index = len(ts)
        if period[1] is not None:
            end_index = \
                self.time_manager.get_index(ts_name, period[1])
        elif length is not None:
            end_index = start_index + length
        # Check indexes correctness
        if start_index > end_index or end_index > len(ts):
            raise Exception
        # Return requested segment.
        return ts[start_index:end_index + 1]

    def set_ts_vals(self, var_name, ts_name, values, stamp=None):
        # Get time series.
        ts = self._time_series.get((var_name, ts_name))
        if ts is None:
            raise Exception
        # Define borders.
        start_index = 0
        if stamp is not None:
            start_index = \
                self.time_manager.get_index(ts_name, stamp)
        end_index = len(values) + start_index
        # Check index.
        if end_index > len(ts):
            raise Exception
        # Set values.
        ts[start_index:end_index] = values

    def get_scalar_val(self, var_name, ts_name):
        scalar = self._scalars.get((var_name, ts_name))
        if scalar is None:
            raise Exception
        return scalar

    def set_scalar_val(self, var_name, ts_name, value):
        if (var_name, ts_name) in self._scalars:
            self._scalars[(var_name, ts_name)] = value
        else:
            raise Exception
        return

    def get_all_periods(self, var_name, ts_name):
        ps = self._periods_series.get((var_name, ts_name))
        if ps is not None:
            return ps.keys()
        else:
            return []

    def get_period_val(self, var_name, ts_name, period):
        ps = self._periods_series.get((var_name, ts_name))
        if ps is None:
            raise Exception
        return ps.get(period)

    def set_period_val(self, var_name, ts_name, period, value):
        ps = self._periods_series.get((var_name, ts_name))
        if ps is None:
            raise Exception
        ps[period] = value
        return
