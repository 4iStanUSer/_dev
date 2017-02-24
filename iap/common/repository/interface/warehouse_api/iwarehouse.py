import pandas as pd

class IProperties:
    pass

class Properties:
    pass

#@singleton
class IStorage:
    #there must be path for storing
    pass

class Storage(IStorage):

    dataframe = pd.DataFrame(data = dict(Project = None, Entity=None, Variable = None, TimeScale = None,
                             TimeSeries = None, Value = None))

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True

    @property
    def data_frame(self):
        return self.data_frame


    def _save_data_frame(self, project_name):
        try:
            entities = self.data_frame[['Entity','Project']].unique
        except KeyError:
            pass
        except AttributeError:
            pass
        else:
            return entities

    def _get_data_frame(self, entity_name):
        pass


class IProject(Storage):

    def _get_entities(self, project_name):
        #provide operation around dataframe
        # provide operation around dataframe
        project_info = self.data_frame.loc(lambda df: (df.Project == project_name))
        return project_info

    def _update_project(self, project_name):
        #provide operation around dataframe
        project_info = self.data_frame.loc(lambda df: (df.Project == project_name))
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







