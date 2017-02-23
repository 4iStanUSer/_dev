import pandas as pd
from .iwarehouse import IProject, IEntity, ITimeScale, ITimeSeries, IVariable, IAdmin

class IProperties:
    pass


class Properties:
    pass


class Project(IProject, IAdmin):


    def __init__(self, name):

        self.entities_ids = []
        self.project_name=name


    def get_entities(self):
        #return list of entities

        self.entities_ids = self._get_entities(self.project_name)
        ents = []
        for entity_id in self.entities_ids:
            ent = Entity(entity_id)
            ents.append(ent)
        return ents

    def add_entity(self, entity):
        #add entity to
        pass


    def delete_entities(self, entity_id):
        #delete entity from project entity
        self.entities_ids.remove(entity_id)

    def save(self):
        pass


class Entity(Project, IEntity):

    def __init__(self, path):

        self.path = path
        self._fill_attributes()

    def _fill_attributes(self):

        self.childs = self._get_childs(ent_path=self.path)
        self.parents = self._get_parents(ent_path=self.path)
        self.vars = self._get_variables(ent_path=self.path)


    def add_child(self, child):
        if child.path not in self.childs.append(child):
            self.childs.append(child.path)
        return

    def get_childs(self):

        ent_child = []
        for child in self.childs:
            ent_child.append(Entity(child))
        return ent_child

    def get_parents(self):

        ent_parent = []
        for child in self.childs:
            ent_parent.append(Entity(child))
        return ent_parent

    def get_vars(self):

        vars = []
        for var in self.vars:
            vars.append(Variable(var))
        return vars


    def get_var(self):
        return self.vars

    def del_var(self, var_id):
        pass

    def update_var(self):
        pass


class Variable(Entity, IVariable):

    def __init__(self, var_name):
        self.var_name = var_name
        self.ts = []

    def add_time_scale(self):
        pass

    def get_time_scale(self):
        return self.ts

    def get_time_scale_by_name(self, ts_name):
        _ts = None
        for ts in self.ts:
            if ts.name == ts_name:
                _ts = ts
            return _ts


class Timescale(Variable, ITimeScale):

    def __init__(self, time_scale_name):
        self.time_scale_name = time_scale_name
        self.timeseries = []

    def get_time_series(self):
        return

    def add_time_serie(self):
        pass

    def update_time_serie(self):
        pass

    def delete_update_time_serie(self):
        pass


class TimeSeries(Timescale, ITimeSeries):

    def __init__(self, name):
        self.name
        self.timeserie = {}

    def add_timeserie(self):
        pass

    @property
    def timeserie(self):
        return self.timeserie

    def get_time_period(self):

        return list(self.timeserie.keys())

    def get_time_period_values(self):

        return list(self.timeserie.keys())

    def get_by_stamp(self, start_stamp=None, end_stamp=None, len=None, values=None):
        pass

    def get_by_index(self, start_index=None, end_index=None, len=None, values=None):
        pass

    def set_by_stamp(self, start_stamp=None, end_stamp=None, len=None, values=None):
        pass

    def set_by_index(self, start_index=None, end_index=None, len=None, values=None):
        pass





