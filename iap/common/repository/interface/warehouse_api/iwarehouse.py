import pandas as pd
import numpy as np
from . import warehouse_api
import logging
logging.getLogger(__name__)

class IProperties:
    pass

class Properties:
    pass

#@singleton
class IStorage:
    #there must be path for storing
    pass

class Storage(IStorage):

    def __init__(self):
        self.dataframe = pd.DataFrame(data=dict(Project=[None], Entity=[None], Variable=[None],
                                       TimeSeries=[None], TimePoint=[None], Value=[None]),
                             columns=['Project', 'Entity', 'Variable', 'TimeSeries', 'TimePoint', 'Value']
                             )

    def _save_data_frame(self, project_name=None, entity_path=None, var_name=None,
                         time_series=None, time_point=None, values=None):

        serie = pd.DataFrame(data=dict(Project=[project_name], Entity=[entity_path], Variable=[var_name],
                                       TimeSeries=[time_series], TimePoint=[time_point], Value=[values]),
                             columns=['Project', 'Entity', 'Variable', 'TimeSeries', 'TimePoint', 'Value']
                             )

        serie.reset_index(drop=True, inplace=True)
        self.dataframe.reset_index(drop=True, inplace=True)

        frames = [serie, self.dataframe]
        self.dataframe = pd.concat(frames)

    def save_to_local_storage(self, project_name):
        logging.info("DataFrame {0}".format(self.dataframe))
        self.dataframe.to_csv("C:/Users/Alex/Desktop/parser/{0}.csv".format(project_name), index=False)

    def read_from_local_storage(self, project_name):
        """
        Read dataframe from local file

        :param project_name:
        :type project_name: str
        :return:
        :rtype: None
        """
        self.dataframe = pd.read_csv("C:/Users/Alex/Desktop/parser/{0}.csv".format(project_name))
        self.dataframe.replace('-', self.dataframe.replace(['-'], [None]))

    def process_data_frame(self, project_name):
        """
        Process data frame

        :param project_name:
        :type project_name:
        :return:
        :rtype:
        """

        self.dataframe.loc(lambda df: (df.Project == project_name))
        ent_list = self.process_entity(project_name=project_name)
        return ent_list

    def process_entity(self, project_name):
        ent_info = {}
        ent_names = self.dataframe[self.dataframe.Project == project_name].Entity.unique()
        for entity_path in ent_names:
            logging.info("Get entities {0}".format(entity_path))
            entity = warehouse_api.Entity(path=entity_path)
            ent_info[entity_path] = entity
            self.process_variable(project_name, entity, entity_path)
        return ent_info

    def process_variable(self, project_name, entity, entity_path):
        variables = self.dataframe[(self.dataframe.Project == project_name)&
                                   (self.dataframe.Entity == entity_path)].Variable.unique()
        for var_name in variables:
            logging.info("Get variable {0}".format(var_name))
            var = warehouse_api.Variable(name=var_name)
            entity.add_var(var)
            self.process_time_series(project_name, entity_path, var_name, var)
        pass

    def process_time_series(self, project_name, entity_path, var_name, var):
        time_series = self.dataframe[
                                     (self.dataframe.Project == project_name) &
                                     (self.dataframe.Entity == entity_path) &
                                     (self.dataframe.Variable == var_name)
                                    ].TimeSeries.unique()
        for time_serie_name in time_series:
            logging.info("Get timeseries {0}".format(time_serie_name))
            time_serie = warehouse_api.TimeSeries(name=time_serie_name)
            var.add_time_serie(time_serie)
            self.process_time_point(project_name, entity_path, var_name, time_serie_name, time_serie)

    def process_time_point(self, project_name, entity_path, var_name, time_serie_name, time_serie):

        time_points = self.dataframe[
                                     (self.dataframe.Project == project_name) &
                                     (self.dataframe.Entity == entity_path) &
                                     (self.dataframe.Variable == var_name) &
                                     (self.dataframe.TimeSeries == time_serie_name)
                                    ]

        for i in time_points.itertuples():
            print(i)
            point = i.TimePoint
            value = i.Value
            logging.info("Get timepoint {0}".format(i))
            time_serie.set_by_index(start_index=int(point), len=1, values=[value])
        logging.info("Get timepoint {0}".format(time_serie_name))


class IProject(Storage):

    def _get_entities(self, project_name):
        #provide operation around dataframe
        # provide operation around dataframe
        project_info = self.data_frame.loc(lambda df: (df.Project == project_name))
        return project_info

    def _update_project(self, project_name):
        #provide operation around dataframe
        project_info = self.data_frame.loc(lambda df: (df.Project == project_name))
        #TODO provide updating of module
        return project_info

    def _delete_project(self, project_name):
        #provide operation around dataframe
        project_info = self.data_frame.loc(lambda df: (df.Project == project_name))

        return project_info


class IEntity(Storage):


    def _get_variables(self, entity_path):
        # provide operation around dataframe
        variable_info = self.data_frame.loc(lambda df: (df.Enity == entity_path))
        return variable_info

    def _get_childs(self, entity_path):
        variable_info = self.data_frame.loc(lambda df: (df.Enity == entity_path))
        return variable_info

    def _get_parents(self, entity_path):
        variable_info = self.data_frame.loc(lambda df: (df.Enity == entity_path))
        return variable_info

    def _add_entity(self, entity_path):
        #provide operation around dataframe
        variable_info = self.data_frame.loc(lambda df: (df.Enity == entity_path))
        return variable_info

    def _update_entity(self, entity_path):
        #provide operation around dataframe
        variable_info = self.data_frame.loc(lambda df: (df.Enity == entity_path))
        return variable_info

    def _delete_entity(self, entity_path):
        #provide operation around dataframe
        variable_info = self.data_frame.loc(lambda df: (df.Enity == entity_path))
        return variable_info

class IVariable(Storage):

    def _get_variable(self, var_name, entity_path):
        #provide operation around dataframe
        variable_info = self.data_frame.loc(lambda df:
                                                (df.Enity == entity_path) &
                                                (df.Variable == var_name)
                                            )

        return variable_info

    def _add_variable(self, var_name, entity_path):
        #provide operation around dataframe
        df = pd.DataFrame(data=dict(Entity=entity_path, Variable=var_name))
        self.data_frame.append(df, ignore_index=True)
        return

    def _update_variable(self, entity_path, var_name, parameter, value):
        #provide operation around dataframe
        df = pd.DataFrame(data=dict(Entity=entity_path, Variable=var_name))
        df.update(parameter, value)
        #TODO provide updating
        return

    def _delete_variable(self, entity_path, var_name):
        #provide operation around dataframe
        #provide operation around dataframe
        df = pd.DataFrame(data=dict(Entity=entity_path, Variable=var_name))
        # TODO provide deleting
        return

class ITimeScale(Storage):

    def _get_time_scale(self, time_scale_name, var_name, entity_path):
        #provide operation around dataframe
        ts_info = self.data_frame.loc(
                                        lambda df:
                                             (df.Enity == entity_path) &
                                             (df.Variable == var_name) &
                                             (df.TimeScale == time_scale_name)
                                      )

        return ts_info

    def _add_time_scale(self, time_scale_name, var_name, entity_path):
        #provide operation around dataframe
        df = pd.DataFrame(data = dict(Entity = entity_path, Variable=var_name, TimeScale =time_scale_name))
        self.data_frame.append(df, ignore_index=True)
        return

    def _update_time_scale(self, time_scale_name, var_name, entity_path, parameter, value):
        #provide operation around dataframe
        df = pd.DataFrame(data=dict(Entity=entity_path, Variable=var_name, TimeScale=time_scale_name))
        df.update(parameter, value)
        #TODO provide updating
        return

    def _delete_time_scale(self, time_scale_name, var_name, entity_path, parameter, value):
        #provide operation around dataframe
        df = pd.DataFrame(data=dict(Entity=entity_path, Variable=var_name, TimeScale=time_scale_name))
        df.update(parameter, value)
        #TODO provide deleting
        return

class ITimeSeries(Storage):
    """
    Interface for TimeSeries
    Object created to communicate with storage dataset
    For CRUD operation with TimeSeries Obj
    """

    def get_time_series(self, time_scale_name, variable_name, entity_path):
        #provide operation around dataframe

        ts_info = self.data_frame.loc(lambda df: (df.Enity == entity_path) &
                                                 (df.Variable == variable_name) &
                                                 (df.Variable == time_scale_name) &
                                                 (df.Variable == variable_name))

        return ts_info



    def get_time_serie(self, time_series, time_scale_name, variable_name, entity_path):

        ts_info = self.data_frame.loc(lambda df: (df.Enity == entity_path) &
                                       (df.Variable == variable_name) &
                                       (df.Variable == time_scale_name) &
                                       (df.Variable == variable_name))

        return ts_info

    def _save_to_data_frame(self, ):
        pass
    def _add_time_series(self, time_serie, time_scale_name, variable_name, entity_path):

        #provide operation around dataframe
        serie = pd.DataFrame(Entity = entity_path, Variable = variable_name, TimeScale = time_scale_name,
                          TimeSeries = time_serie)

        self.df.append(serie, ignore_index=True)
        return

    def _update_time_serie(self, time_serie, time_scale_name, variable_name, entity_path, property, value):

        serie = self.get_time_serie(time_serie, time_scale_name, variable_name, entity_path)
        #TODO add update series
        serie.update(property, value)
        return
        #provide operation around dataframe

    def _delete_timeseries(self, time_serie, time_scale_name, variable_name, entity_path, property, value):
        #provide operation around dataframe
        serie = self.get_time_serie(time_serie, time_scale_name, variable_name, entity_path)
        self.data_frame.drop(serie)
        #TODO add drop
        return

class IAdmin(Storage):

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        print('A')
        self._initialized = True

    def _get_project(self, project_name, wh):
        dataframe = wh.read_sql(...)

    def _set_project(self, project_name, wh):
        dataframe = wh.read_data_set(...)

    def _del_project(self, project_name):
        pass

    def _update_project(self, projetc_name):
        pass
    pass







