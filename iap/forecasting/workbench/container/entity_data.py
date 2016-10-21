import copy

from .. import exceptions as ex


class EntityData:
    def __init__(self, time_manager):
        self.time_manager = time_manager
        self._var_properties = {}
        self._coeff_properties = {}
        self._variables = {}
        self._coefficients = {}
        self._decomposition = {}

    @property
    def variables_names(self):
        return list(self._var_properties.keys())

    @property
    def variables_properties(self):
        return [{**self._var_properties[name], **dict(name=name)}
                for name in self._var_properties.keys()]

    @property
    def coefficients_names(self):
        return list(self._coeff_properties.keys())

    def add_variable(self, name, default_value):
        if name in self._var_properties:
            raise Exception
        if default_value is None:
            default_value = 0
        self._var_properties[name] = dict(def_value=default_value,
                                          metric='', mult='', type='')

    def add_coefficient(self, name):
        if name in self._coeff_properties:
            raise Exception
        self._coeff_properties[name] = dict()

    def rename_variable(self, old_name, new_name):
        raise NotImplementedError
        #if new_name in self._variables:
        #    # return Exception
        #    return ex.EdAlreadyExistentVarName(new_name)
        #self._variables[new_name] = self._get_var(old_name)
        #self._variables.pop(old_name)

    ##def get_default_value(self, var_name):
    #    raise NotImplementedError
    #    #return self._get_var(var_name)['default_value']

    def does_contain_ts(self, var_name, ts_name):
        ts = self._variables.get((var_name, ts_name), None)
        if ts is not None:
            return True
        return False

    def add_time_series(self, var_name, ts_name):
        var_props = self._var_properties.get(var_name, None)
        if var_props is None:
            raise Exception
        ts = self._variables.get((var_name, ts_name), None)
        if ts is not None:
            raise Exception
        length = self.time_manager.get_time_length(ts_name)

        ts_data = dict(var_name=var_name, ts_name=ts_name,
                       values=[var_props['def_value']]*length,
                       growth_rates=[0]*length, changes=dict())
        self._variables[(var_name, ts_name)] = ts_data

    def get_values(self, var_name, ts_name, period):
        ts = self._variables.get((var_name, ts_name), None)
        if ts is None:
            raise Exception
        return self._get_ts_segment(ts['values'], period, ts_name)

    def get_growth_rates(self, var_name, ts_name, period):
        ts = self._variables.get((var_name, ts_name), None)
        if ts is None:
            raise Exception
        return self._get_ts_segment(ts['growth_rates'], period, ts_name)

    def set_values(self, var_name, ts_name, values, start_label=None):
        ts = self._variables.get((var_name, ts_name), None)
        if ts is None:
            raise Exception
        self._set_ts_segment(ts['values'], values, ts_name, start_label)

    def set_growth_rates(self, var_name, ts_name, start_label, values):
        ts = self._variables.get((var_name, ts_name), None)
        if ts is None:
            raise Exception
        self._set_ts_segment(ts['growth_rates'], values, start_label, ts_name)

    def get_growth(self, var_name, ts_name, period):
        ts = self._variables.get((var_name, ts_name), None)
        if ts is None:
            raise Exception
        growth = ts['changes'].get(period)
        return growth

    def set_growth(self, var_name, ts_name, period, value):
        ts = self._variables.get((var_name, ts_name), None)
        if ts is None:
            raise Exception
        ts['changes'][period] = value
        return

    def get_coeff_value(self, coeff_name, ts_name):
        try:
            return self._coefficients[(coeff_name, ts_name)]['value']
        except KeyError:
            raise Exception

    def set_coeff_value(self, coeff_name, ts_name, value):
        if (coeff_name, ts_name) in self._coefficients:
            self._coefficients[(coeff_name, ts_name)]['value'] = value
        else:
            coeff_props = self._coeff_properties.get(coeff_name, None)
            if coeff_props is None:
                raise Exception
            self._coefficients[(coeff_name, ts_name)] = \
                dict(coeff_name=coeff_name, ts_name=ts_name, value=value)

    def get_decomposition(self, period):
        return None

    def get_backup(self):
        var_values = [dict(var_name=val['var_name'], ts_name=val['ts_name'],
                           values=copy.copy(val['values']))
                      for key, val in self._variables.items()]
        coeff_values = [dict(coeff_name=val['coeff_name'],
                             ts_name=val['ts_name'], value=val['value'])
                        for key, val in self._coefficients.items()]
        backup = dict(var_properties=self._var_properties,
                      coeff_properties=self._coeff_properties,
                      var_values=var_values,
                      coeff_values=coeff_values)
        return backup

    def load_backup(self, backup):
        for name, props in backup['var_properties'].items():
            self.add_variable(name, props['def_value'])
        for name, props in backup['coeff_properties'].items():
            self.add_coefficient(name)
        for item in backup['var_values']:
            self.add_time_series(item['var_name'], item['ts_name'])
            self.set_values(item['var_name'], item['ts_name'], item['values'])
        for item in backup['coeff_values']:
            self.set_coeff_value(item['coeff_name'], item['ts_name'],
                                 item['value'])
        return

    def _get_ts_segment(self, time_series, period, timescale_name):
        # Define borders.
        start_index = 0
        if period[0] is not None:
            start_index = \
                self.time_manager.get_index(timescale_name, period[0])
        end_index = len(time_series)
        if period[1] is None:
            end_index = \
                self.time_manager.get_index(timescale_name, period[1])
        # Check indexes correctness
        if start_index > end_index:
            raise Exception
        # Return requested segment.
        return time_series[start_index:end_index]

    def _set_ts_segment(self, time_series, values, timescale_name,
                        start_label):
        # Define borders.
        start_index = 0
        if start_label is not None:
            start_index = \
                self.time_manager.get_index(timescale_name, start_label)
        end_index = len(values) + start_index
        # Check index.
        if end_index > len(time_series):
            raise Exception
        # Set values.
        time_series[start_index:end_index] = values