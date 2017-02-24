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

    dataframe = pd.DataFrame(project = None, entity=None, variable = None, time_scale = None,
                             time_series = None, value = None)

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

    def _get_entity(self, project_name):
        #provide operation around dataframe
        pass

    def _add_entity(self, project_name):
        #provide operation around dataframe
        pass

    def _update_entity(self, project_name):
        #provide operation around dataframe
        pass

    def _delete_entity(self, projetc_name):
        #provide operation around dataframe
        pass

class IEntity(Storage):

    def _get_variable(self, ent_path, var_name):
        #provide operation around dataframe
        return var_name

    def _get_variables(self, ent_path):
        pass

    def _get_childs(self, ent_path):
        pass

    def _get_parents(self, ent_path):
        pass

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

    def _add_time_series(self, time_series, time_scale_name, variable_name, entity_path):

        self.data_frame.
        self.data_frame.update()
        #connect toddf


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







