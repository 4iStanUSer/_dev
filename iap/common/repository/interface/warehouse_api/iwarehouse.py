import pandas as pd
import numpy as np
from . import warehouse_api
import sqlalchemy
import logging
logging.getLogger(__name__)


class Storage():

    def __init__(self):
        self.dataframe = pd.DataFrame(data=dict(Project=[None], Entity=[None], Variable=[None],
                                       TimeSeries=[None], TimePoint=[None], Value=[None]),
                             columns=['Project', 'Entity', 'Variable', 'TimeSeries', 'TimePoint', 'Value']
                             )

        self.config = dict(in_path=None, out_path=None)

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

    def save_to_local_storage(self, db_config=None, table_name=None):

        logging.info("DataFrame Saved To Local Storage {0}".format(self.dataframe))

        self.dataframe = self.dataframe.dropna(how='all')
        engine = sqlalchemy.create_engine(db_config)
        self.dataframe.to_sql(con=engine, name=table_name,
                              if_exists='append')

    def read_from_df(self, df=None):
        """
        Read dataframe from local file

        :param project_name:
        :type project_name: str
        :return:
        :rtype: None
        """
        if df is not None:
            self.dataframe = self.dataframe.append(df)
            self.dataframe = self.dataframe.dropna(how='all')

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
            if var_name is not np.nan:
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
            if time_serie_name is not np.nan:
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
            point = i.TimePoint
            value = i.Value
            logging.info("Get timepoint {0}".format(i))
            time_serie.timeserie.append(dict(index=int(point), value=value, stamp=None))
        logging.info("Get timepoint {0}".format(time_serie_name))








