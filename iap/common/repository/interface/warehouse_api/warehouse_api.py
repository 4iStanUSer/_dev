import pandas as pd
from .iwarehouse import IProject, IEntity, ITimeScale, ITimeSeries, IVariable, IAdmin

class IProperties:
    pass


class Properties:
    pass


class Project(IProject, IAdmin):


    def __init__(self, name):

        self.entities = {}
        self.project_name=name


    def get_entities(self):
        #return list of entities
        return self.entities

    def add_entity(self, entity):
        #add entity to
        self.entities[entity.path] = entity

    def get_entity_by_path(self, ent_path):
        if ent_path in self.entities.keys():
            return self.entities[ent_path]
        else:
            return None

    def delete_entities(self, entity_path):
        #delete entity from project entity
        if entity_path in self.entities.keys():
            del self.entities[entity_path]


    def save(self):
        pass


class Entity(Project, IEntity):

    def __init__(self, path):

        self.path = path
        self.childs = []
        self.parents = []
        self.vars = {}

        self._fill_attributes()

    def _fill_attributes(self):

        for child_path in self._get_childs(ent_path=self.path):
            ent = Entity(child_path)
            self.childs.append(ent)

        for parent_path in self._get_parents(ent_path=self.path):
            ent = Entity(parent_path)
            self.parents.append(ent)

        for var_id in self._get_variables(ent_path=self.path):
            var = Variable(var_id)
            self.vars[var_id] = var

    def add_child(self, child):
        if child.path not in self.childs.append(child):
            self.childs.append(child.path)
        return

    def get_childs(self):
        return self.childs

    def get_parents(self):
        return self.parents

    def get_vars(self):
        return self.vars

    def get_var_by_name(self, var_name):
        if var_name in self.vars.keys():
            return self.vars[var_name]
        else:
            return None

    def del_var(self, var_name):
        if var_name in self.vars.keys():
            del self.vars[var_name]


    def update_var(self):
        pass


class Variable(Entity, IVariable):

    def __init__(self, var_name):
        self.var_name = var_name
        self.time_scale = {}

    def add_time_scale(self, time_scale):
        self.time_scale[time_scale.name] = time_scale
        return

    def get_time_scales(self):
        return self.time_scales

    def get_time_scale_by_name(self, ts_name):
        _ts = None
        if ts_name in  self.get_time_scales().keys():
            _ts = self[ts_name]
        return _ts

    def delete_time_scale(self, time_scale_name):
        if time_scale_name in self.get_time_scales().keys():
            del self[time_scale_name]
        return

class Timescale(Variable, ITimeScale):

    def __init__(self, time_scale_name):
        self.time_scale_name = time_scale_name
        self.timeseries = {}

    def get_time_series(self, ts_name):
        _ts = None
        if ts_name in self.timeseries.keys():
            _ts = self.timeseries[ts_name]
        return _ts

    def add_time_serie(self, timeserie):
        self.timeseries[timeserie.name] = timeserie

    def update_time_serie(self):
        pass

    def delete_update_time_serie(self, ts_name):
        if ts_name in self.timeseries.keys():
            del self.timeseries[ts_name]


class TimeSeries(Timescale, ITimeSeries):

    def __init__(self, name):
        self.name
        self.values = []
        self.time_points = []

    @property
    def timeserie(self):
        return self.timeserie

    def get_time_period(self):

        return list(self.timeserie.keys())

    def get_time_period_values(self):

        return list(self.timeserie.keys())

    def get_by_stamp(self, start_stamp=None, end_stamp=None, len=None, values=None):
        if start_stamp and end_stamp:


    def get_by_index(self, start_index=None, end_index=None, len=None, values=None):
        pass

    def set_by_stamp(self, start_stamp=None, end_stamp=None, len=None, values=None):
        pass

    def set_by_index(self, start_index=None, end_index=None, len=None, values=None):
        pass





