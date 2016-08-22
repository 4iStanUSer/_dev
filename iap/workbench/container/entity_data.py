from functools import wraps


class EntityData:
    def __init__(self, time_manager):
        self._variables = {}
        #{'name': name, 'time_series': {'ts_name': {'start':'','end':'','values'=[]}}}
        self._time_manager = time_manager

    def get_var_names(self):
        return list(self._variables.keys())

    def does_contain_var(self, name):
        return name in self._variables

    def add_var(self, name, default_value):
        if default_value is None:
            default_value = 0
        self._variables[name] = {'default_value': default_value, 'time_series': {}}

    @check_key
    def rename_variable(self, old_name, new_name):
        if new_name in self._variables:
            return Exception
        try:
            self._variables[new_name] = self._variables[old_name]
            self._variables.pop(old_name)
        except KeyError:
            raise Exception

    @check_key
    def get_default_value(self, var_name):
        try:
            return self._variables[var_name]['default_value']
        except KeyError:
            raise Exception

    @check_key
    def does_contain_ts(self, var_name, ts_name):
        return ts_name in self._variables[var_name]['time_series']

    @check_key
    def add_time_series(self, var_name, ts_name):
        var = self._variables[var_name]
        length = self._time_manager.get_time_len(ts_name)
        def_value = var['default_value']
        var['time_series'][ts_name] = {'start': None,
                                       'end': None,
                                       'values': [def_value]*length}

    @check_key
    def get_ts_start(self, var_name, ts_name):
        pass

    @check_key
    def get_ts_end(self, var_name, ts_name):
        pass

    @check_key
    def get_values(self, _var_name, ts_name, start_label, length):
        pass


def check_key(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return Exception
    return func_wrapper
