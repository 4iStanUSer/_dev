class EntityData:
    def __init__(self):
        self._variables = {}
        #{'name': name, 'time_series': {'ts_name': {'start':'','end':'','values'=[]}}}

    def get_var_names(self):
        return list(self._variables.keys())

    def does_contain_var(self, name):
        return name in self._variables

    def add_var(self, name, default_value):
        if default_value is None:
            default_value = 0
        self._variables[name] = {'default_value': default_value, 'ts': {}}

    def rename_variable(self, old_name, new_name):
        if new_name in self._variables:
            return Exception
        try:
            self._variables[new_name] = self._variables[old_name]
            self._variables.pop(old_name)
        except KeyError:
            raise Exception

    def get_default_value(self, var_name):
        try:
            return self._variables[var_name]['default_value']
        except KeyError:
            raise Exception

    def does_contain_ts(self, ts_name):
        pass

    def add_time_series(self, ts_name):
        pass

    def get_ts_start(self, var_name, ts_name):
        pass

    def get_ts_end(self, var_name, ts_name):
        pass

    def get_values(self, _var_name, ts_name, start_label, length):
        pass