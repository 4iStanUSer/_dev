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

    dataframe = None

    @property
    def data_frame(self):
        return self.data_frame



    def _get_entities(self, project_name):
        try:
            entities = self.data_frame[['Entity','Project']].unique
        except KeyError:
            pass
        except AttributeError:
            pass
        else:
            return entities

    def _set_entity(self, entity_name):
        pass

    def _del_entity(self, entity_name):


    def _get_variable(self, project_name, entity_id):
        pass

    def _get_time_scale_(self, project_name, entity_id, var_id):
        pass

    def _get_time_serie(self, project_name, entity_id, var_id):
        pass

class IProject(Storage):

    def _get_entity(self, project_name):
        #provide operation around dataframe
        return project_name

    def _add_entity(self, project_name):
        #provide operation around dataframe
        return project_name

    def _update_entity(self, project_name):
        #provide operation around dataframe
        return project_name

    def _delete_entity(self, projetc_name):
        #provide operation around dataframe
        return projetc_name


class IEntity(Storage):

    def _get_variable(self, var_name):
        #provide operation around dataframe
        return var_name

    def _add_variable(self, var_name):
        #provide operation around dataframe
        return var_name

    def _update_variable(self, var_name):
        #provide operation around dataframe
        return var_name

    def _delete_variable(self, var_name):
        #provide operation around dataframe
        return var_name

class IVariable(Storage):

    def _get_variable(self, var_name):
        #provide operation around dataframe
        return var_name

    def _add_variable(self, var_name):
        #provide operation around dataframe
        return var_name

    def _update_variable(self, var_name):
        #provide operation around dataframe
        return var_name

    def _delete_variable(self, var_name):
        #provide operation around dataframe
        return var_name

class ITimeScale(Storage):

    def _get_time_scale(self, var_name):
        #provide operation around dataframe
        return var_name

    def _add_time_scale(self, var_name):
        #provide operation around dataframe
        return var_name

    def _update_time_scale(self, var_name):
        #provide operation around dataframe
        return var_name

    def _delete_time_scale(self, var_name):
        #provide operation around dataframe
        return var_name

class ITimeSeries(Storage):

    def _get_time_serie(self, var_name):
        #provide operation around dataframe
        return var_name

    def _add_time_series(self, var_name):
        #provide operation around dataframe
        return var_name

    def _update_time_series(self, var_name):
        #provide operation around dataframe
        return var_name

    def _delete_timeseries(self, var_name):
        #provide operation around dataframe
        return var_name

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







