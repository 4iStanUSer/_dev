from ...models_managers.warehouse import Warehouse
from .iwarehouse import Storage
import logging
logging.basicConfig(level=logging.DEBUG)


class Project(Storage):

    def __init__(self, name):
        self.entities = {}
        self.project_name = name

    def get_entities(self):
        return self.entities

    def add_entity(self, entity):
        self.entities[entity.path] = entity

    def get_entity_by_path(self, ent_path):
        if ent_path in self.entities.keys():
            return self.entities[ent_path]
        else:
            return None

    def delete_entities(self, entity_path):
        if entity_path in self.entities.keys():
            del self.entities[entity_path]

    def read(self, df=None):
        """

        :return:
        :rtype: None
        """

        storage = Storage()
        storage.read_from_df(df)
        ents = storage.process_data_frame(self.project_name)
        self.entities = ents

    def save_sql(self, db_config):
        """
        Data Loader save to sql

        :param db_config:
        :type db_config:
        :param warehouse:
        :type warehouse:
        :return:
        :rtype:
        """
        warehouse = Warehouse(db_config)
        warehouse.add_project(self.project_name)
        for ent_path, ent in self.entities.items():
            warehouse.add_entity(self.project_name, entity=ent_path)
            for var in ent.variables:
                warehouse.add_variable(self.project_name,
                                     entity=ent_path, var=var)


    def save(self):
        """

        :return:
        :rtype:
        """
        storage = Storage()
        for ent_path, ent in self.entities.items():
            logging.info('Entity Save To DataFrame {0}'.format(ent_path))
            ent._save(storage, project_name=self.project_name)

        storage.save_to_local_storage()


class Entity(Project):

    def __init__(self, path):

        if type(path) is list:
            self.path = "*".join(path)
        else:
            self.path = path

        self.childs = []
        self.parents = []
        self.vars = {}

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

    def add_var(self, var):
        self.vars[var.name] = var

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


    def _save_to_sql(self, storage, project_name):
        """

        :param storage:
        :type storage: iap.common.repository.interface.warehouse_api.iwarehouse.Storage
        :param project_name:
        :type project_name: str
        :return:
        :rtype: None
        """

        if self.vars!=dict():
            for name, var in self.vars.items():

                logging.info('Process Variable {0}'.format(name))
                var._save(storage, project_name=project_name,
                          ent_path=self.path)
        else:
            logging.info('Entity Saved To LocalStorage {0}'.format(self.path))
            storage._save_data_frame(project_name=project_name,
                                     entity_path=self.path)


    def _save(self, storage, project_name):
        """

        :param storage:
        :type storage: iap.common.repository.interface.warehouse_api.iwarehouse.Storage
        :param project_name:
        :type project_name: str
        :return:
        :rtype: None
        """

        if self.vars!=dict():
            for name, var in self.vars.items():

                logging.info('Process Variable {0}'.format(name))
                var._save(storage, project_name=project_name,
                          ent_path=self.path)
        else:
            logging.info('Entity Saved To LocalStorage {0}'.format(self.path))
            storage._save_data_frame(project_name=project_name,
                                     entity_path=self.path)

class Variable(Entity):

    def __init__(self, name):
        self.name = name
        self.time_series = {}

    def add_time_serie(self, time_serie):
        self.time_series[time_serie.name] = time_serie
        return

    def get_time_scales(self):
        return self.time_series

    def get_time_scale_by_name(self, ts_name):
        _ts = None
        if ts_name in  self.get_time_scales().keys():
            _ts = self[ts_name]
        return _ts

    def delete_time_scale(self, time_scale_name):
        if time_scale_name in self.get_time_scales().keys():
            del self[time_scale_name]
        return

    def _save(self, storage, project_name, ent_path):
        if self.time_series!=dict():
            for time_series_name, time_series in self.time_series.items():
                logging.info('Time Serie Saved To DataFrame {0}'.format(time_series_name))
                time_series._save(storage, project_name=project_name, ent_path=ent_path, var_name=self.name)
        else:
            logging.info('Entity To DataFrame {0}'.format(ent_path))
            storage._save_data_frame(project_name=project_name, entity_path=ent_path,  var_name=self.name)


class TimeSeries(Variable):

    def __init__(self, name):

        self.name = name
        self.timeserie = []

    def get_time_period(self):

        return list(self.timeserie.keys())

    def get_time_period_values(self):

        return list(self.timeserie.keys())

    def get_by_stamp(self, start_stamp=None, end_stamp=None, len=None, values=None):
        if start_stamp and end_stamp:
            pass

    def get_by_index(self, start_index=None, end_index=None, len=None, values=None):
        pass

    def set_by_stamp(self, start_stamp=None, end_stamp=None, len=None, values=None):
        pass

    def set_by_index(self, start_index=None, end_index=None, len=None, values=None):
        for i in range(start_index, start_index+len):
            self.timeserie.append(dict(index=start_index+i, value=values[i], stamp=None))

    def _save(self, storage, project_name, ent_path, var_name):
        if self.timeserie != []:
            for timepoint in self.timeserie:

                storage._save_data_frame(project_name=project_name, entity_path=ent_path,
                                         var_name=var_name, time_series=self.name, time_point=timepoint['index'],
                                         values=timepoint['value'])
                logging.info('TimePoint Saved To DataFrame')
        else:
            logging.info('Entity To DataFrame {0}'.format(ent_path))
            storage._save_data_frame(project_name=project_name, entity_path=ent_path, var_name=self.name,
                                     time_series=self.name)
