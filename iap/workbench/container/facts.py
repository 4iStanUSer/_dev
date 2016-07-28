import abc
import numpy as np
from ..container import exceptions as ex


class Point:
    def __init__(self, coords, config):
        # Parse config.
        try:
            _time_len = config['time_len']
            _var_names = config['var_names']
        except KeyError:
            raise Exception
        # Init.
        self.coordinates = coords
        self.vars = {}
        for name in _var_names:
            self.vars[name] = np.zeros(_time_len, dtype=np.float32)

    def get_data_for_save(self):
        return self.vars

    def load_saved_data(self, value):
        self.vars = value

    def set_var_data(self, name, value):
        try:
            var = self.vars[name]
        except KeyError:
            raise ex.VarNotFoundError(name)
        if len(value) != len(var):
            raise ex.WrongLenghtError(name, len(var), len(value))
        np.copyto(var, np.array(value, dtype=np.float32)) 

    def get_data_for_view(self):
        return self.vars
