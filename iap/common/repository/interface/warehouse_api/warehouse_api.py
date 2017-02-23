import pandas as pd
from .iwarehouse import IProject, IEntity, ITimeScale, ITimeSeries, IVariable, IAdmin
class IProperties:
    pass

class Properties:
    pass

class Project(IProject, IAdmin):



    def __init__(self, name):


        self.entities_ids = self._get_entities(name)
        self.project_name=name


    def get_entities(self):
        #return list of entities
        entities = []
        for ent_id in self.entities_ids:
            ent = Entity(path=ent_id)
            entities.append(ent)
            return self.entities

    def add_entities(self, entities_ids):
        #add entity to
        self.entities_ids.extend(entities_ids)

    def delete_entities(self, entity_id):
        #delete entity from project entity
        self.entities_ids.remove(entity_id)

    def save(self):
        pass

class Entity(Project, IEntity):

    def __init__(self, path):
        self.path = path
        self.vars = []
        self.childs = []
        self.parents = []

    def add_child(self, child):
        self.childs.append(child)
        return

    def get_childs(self):
        return self.childs

    def get_parents(self):
        return self.parents

    def get_var(self):
        return self.vars

    def del_var(self, var_id):


    def update_var(self):
        pass

class Variable(Entity, IVariable):



    def add_ts(self):
        pass

    def get_ts(self):
        pass

class Timescale(Variable, ITimeScale):

    def add_time_scale(self):
        pass

    def update_time_scale(self):
        pass

    def delete_update_time_scale(self):
        pass

class TimeSeries(Timescale, ITimeSeries):

    def __init__(self):
        self.name

    def get_by_stamp(self):
        pass

    def get_by_index(self):
        pass

    def set_by_stamp(self):
        pass

    def set_by_index(self):
        pass





