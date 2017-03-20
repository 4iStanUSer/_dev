import logging
import time

from iap.common.repository.models_managers.warehouse import Warehouse
from iap.data_loading.loading_lib.iwarehouse import Storage

logging.basicConfig(level=logging.DEBUG)


class Project(Storage):
    """
    Project allows to get information from database,
    any external dataframe serialise it in objects,
    save it to database.
    Also Provide all neccessary methods for objects hierarchy

    """
    def __init__(self, name):
        self.entities = {}
        self.project_name = name

    def get_entities(self):
        """
        Return dict of ent_path: entity
        :return:
        :rtype:
        """
        return self.entities

    def add_entity(self, entity):
        """
        Add entity
        :param entity:
        :type entity:
        :return:
        :rtype:
        """
        self.entities[entity.path] = entity

    def get_entity_by_path(self, ent_path):
        """
        Return Entity by path
        :param ent_path:
        :type ent_path:
        :return:
        :rtype:
        """
        if ent_path in self.entities.keys():
            return self.entities[ent_path]
        else:
            return None

    def delete_entities(self, entity_path):
        """
        Delete entitie with entity_path
        :param entity_path:
        :type entity_path:
        :return:
        :rtype:
        """
        if entity_path in self.entities.keys():
            del self.entities[entity_path]

    def read(self, df=None):
        """
        Read dataframe and  transform it into objective hierarchy
        Project-Entity-Variable-TimeSerie
        :return:
        :rtype: None
        """

        storage = Storage()
        storage.read_from_df(df)
        ents = storage.process_data_frame(self.project_name)
        self.entities = ents

    def save_sql(self, config):
        """
        Data Loader save to sql
        Args:
            config

        :param db_config:
        :type db_config:
        :param warehouse:
        :type warehouse:
        :return:
        :rtype:
        """
        db_config = config['General']['db_config']

        warehouse = Warehouse(db_config)
        warehouse.add_project(self.project_name)
        self.dataframe = self.save()
        self.dataframe['variable_id'] = None
        for ent_path, ent in self.entities.items():
            ent_path = ent.path
            node = warehouse.add_IEntity(ent, project_name=self.project_name)
            for var_name, variable in ent.vars.items():
                var = warehouse.add_IVariable(ent=node, var_name=var_name)

                self.dataframe.loc[
                    (self.dataframe.Project == self.project_name) &
                    (self.dataframe.Entity == ent_path[0]) &
                    (self.dataframe.Variable == var_name), 'variable_id'] = var._id

        warehouse.commit()


        variables = self.dataframe[
                    ['TimePoint', 'TimeSeries', 'Value', 'variable_id']]
        variables = variables.rename(columns={'TimeSeries':'_name',
                                         'TimePoint':'_time_stamp',
                                         'Value':'_value'})

        warehouse.add_ITimeSerie(variables.to_dict(orient='records'))
        warehouse.commit()

    def save(self):
        """
        Serialise object hierarchy to dataframe

        :return:
        :rtype:
        """
        storage = Storage()
        for ent_path, ent in self.entities.items():
            logging.info('Entity Save To DataFrame {0}'.format(ent_path))
            ent._save(storage, project_name=self.project_name)
        return storage.dataframe

    def collect_df_from_db(self, config):
        """
        Collect all data from datavae that correspond for project_name
        and transform it into dataframe
        :param config:
        :type config:
        :return:
        :rtype:
        """

        db_config = config['General']['db_config']
        warehouse = Warehouse(db_config)
        project = warehouse.get_project_data(self.project_name)
        return project


class Entity(Project):

    def __init__(self, path=["root"], meta=[(None, None)]):
        self.name = path[-1]
        self.path = path
        self.meta = meta
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
                          ent_path=self.name)
        else:
            logging.info('Entity Saved To LocalStorage {0}'.format(self.path))
            storage._save_data_frame(project_name=project_name,
                                     entity_path=self.name)


class Variable(Entity):

    def __init__(self, name):
        """
        Create Var by name
        :param name:
        :type name:
        """
        self.name = name
        self.time_series = {}

    def add_time_serie(self, time_serie):
        """
        Add time serie for variable
        :param time_serie:
        :type time_serie:
        :return:
        :rtype:
        """
        self.time_series[time_serie.name] = time_serie
        return

    def get_time_scales(self):
        """
        Return dictionary of timeseries
        :return:
        :rtype:
        """
        return self.time_series

    def get_time_scale_by_name(self, ts_name):
        """
        Return timeseries by name
        :param ts_name:
        :type ts_name:
        :return:
        :rtype:
        """
        _ts = None
        if ts_name in  self.get_time_scales().keys():
            _ts = self[ts_name]
        return _ts

    def delete_time_scale(self, time_scale_name):
        """
        Delete timeseries by name
        :param time_scale_name:
        :type time_scale_name:
        :return:
        :rtype:
        """
        if time_scale_name in self.get_time_scales().keys():
            del self[time_scale_name]
        return

    def _save(self, storage, project_name, ent_path):
        """
        Serialise Variable object into dataframe
        and initialise serialising all TimeSerie
        :param storage:
        :type storage:
        :param project_name:
        :type project_name:
        :param ent_path:
        :type ent_path:
        :return:
        :rtype:
        """
        if self.time_series!=dict():
            for time_series_name, time_series in self.time_series.items():
                logging.info('Time Serie Saved To DataFrame {0}'
                             .format(time_series_name))
                time_series._save(storage,
                                  project_name=project_name,
                                  ent_path=ent_path, var_name=self.name)
        else:
            logging.info('Entity To DataFrame {0}'.format(ent_path))
            storage._save_data_frame(project_name=project_name,
                                     entity_path=ent_path,
                                     var_name=self.name)


class TimeSeries(Variable):

    def __init__(self, name):
        """
        Initialise TimeSerie Object
        :param name:
        :type name:
        """
        self.name = name
        self.timeserie = []

    def get_time_period(self):
        """

        Return
        :return:
        :rtype:
        """
        return [i['stamp'] for i in self.timeserie]

    def get_time_period_values(self):

        return [i['value'] for i in self.timeserie]

    def get_by_stamp(self, start_stamp=None, end_stamp=None,
                     len=None, values=None):
        """
        Get by stamp TimeSerie Values
        :param start_stamp:
        :type start_stamp:
        :param end_stamp:
        :type end_stamp:
        :param len:
        :type len:
        :param values:
        :type values:
        :return:
        :rtype:
        """
        if start_stamp and end_stamp:
            pass

    def get_by_index(self, start_index=None, end_index=None,
                     len=None):
        """
        Get by index TimeSerie Values
        :param start_index:
        :type start_index:
        :param end_index:
        :type end_index:
        :param len:
        :type len:
        :param values:
        :type values:
        :return:
        :rtype:
        """
        if len:
            return sorted(self.timeserie,
                          key=lambda x: x['index'])[start_index:len-start_index]


    def set_by_stamp(self, start_stamp=None, end_stamp=None, len=None):
        """
        Set TimeSerie Values by stamp
        :param start_stamp:
        :type start_stamp:
        :param end_stamp:
        :type end_stamp:
        :param len:
        :type len:
        :param values:
        :type values:
        :return:
        :rtype:
        """
        pass

    def set_by_index(self, start_index=None,
                     end_index=None, len=None, values=None):
        """
        Set TimeSerie by index
        :param start_index:
        :type start_index:
        :param end_index:
        :type end_index:
        :param len:
        :type len:
        :param values:
        :type values:
        :return:
        :rtype:
        """
        for i in range(start_index, start_index+len):
            self.timeserie.append(dict(index=start_index+i,
                                       value=values[i], stamp=None))

    def _save(self, storage, project_name, ent_path, var_name):
        if self.timeserie != []:
            for timepoint in self.timeserie:

                storage._save_data_frame(project_name=project_name,
                                         entity_path=ent_path,
                                         var_name=var_name,
                                         time_series=self.name,
                                         time_point=timepoint['index'],
                                         values=timepoint['value'])
                logging.info('TimePoint Saved To DataFrame')
        else:
            logging.info('Entity To DataFrame {0}'.format(ent_path))
            storage._save_data_frame(project_name=project_name,
                                     entity_path=ent_path,
                                     var_name=self.name,
                                     time_series=self.name)
