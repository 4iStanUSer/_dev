class EntityData:
    def __init__(self, time_manager):
        self._variables = {}
        self.time_manager = time_manager

    def _get_var(self, var_name):
        try:
            return self._variables[var_name]
        except KeyError:
            raise Exception

    def _get_ts(self, var_name, ts_name):
        try:
            var = self._variables[var_name]
        except KeyError:
            raise Exception
        try:
            return var['time_series'][ts_name]
        except KeyError:
            raise Exception

    def get_var_names(self):
        return list(self._variables.keys())

    def does_contain_var(self, name):
        return name in self._variables

    def add_var(self, name, default_value):
        if default_value is None:
            default_value = 0
        self._variables[name] = {'default_value': default_value,
                                 'time_series': {}
                                 }

    def rename_variable(self, old_name, new_name):
        if new_name in self._variables:
            return Exception
        self._variables[new_name] = self._get_var(old_name)
        self._variables.pop(old_name)

    def get_default_value(self, var_name):
        return self._get_var(var_name)['default_value']

    def does_contain_ts(self, var_name, ts_name):
        return ts_name in self._get_var(var_name)['time_series']

    # TODO review passing start and end dates
    def add_time_series(self, var_name, ts_name, start_date, end_date):
    # def add_time_series(self, var_name, ts_name):
        var = self._get_var(var_name)
        length = self.time_manager.get_time_length(ts_name)
        def_value = var['default_value']
        var['time_series'][ts_name] = {'start': start_date,
                                       'end': end_date,
                                       'values': [def_value]*length
                                       }
        # var['time_series'][ts_name] = {'start': None,
        #                                'end': None,
        #                                'values': [def_value]*length
        #                                }

    def get_ts_start(self, var_name, ts_name):
        return self._get_ts(var_name, ts_name)['start']

    def get_ts_end(self, var_name, ts_name):
        return self._get_ts(var_name, ts_name)['end']

    def get_values(self, var_name, ts_name, start_label, length):
        time_series = self._get_ts(var_name, ts_name)
        if start_label is None:
            return time_series['values']
        else:
            start_index = \
                self.time_manager.get_index_by_label(ts_name, start_label)
            if length is None:
                return time_series['values'][start_index:]
            else:
                return time_series['values'][start_index:start_index+length]

    def set_values(self, var_name, ts_name, start_label, values):
        time_series = self._get_ts(var_name, ts_name)
        start_index = \
            self.time_manager.get_index_by_label(ts_name, start_label)
        for ind, item in enumerate(values):
            adj_index = start_index + ind
            time_series['values'][adj_index] = item





