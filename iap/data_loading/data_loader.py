import configparser
import csv
import json
import logging
import os
import re

import pandas as pd
from pyramid.threadlocal import get_current_registry

from iap.data_loading.loading_lib import warehouse_api as wh_api
from .exceptions import CorruptedDataSet
from ..data_loading import loading_lib


class Loader:
    """
    Starting point of Load

    Attr:
        configs - path to storage with configuration
        db_config - path to storage database

    """
    def __init__(self, settings=None, db_config=None):

        self.setting = {}
        try:
            iap_config = get_current_registry().settings
            self.setting['db_config'] = \
                iap_config['sqlalchemy.url']
            self.setting['path'] = \
                iap_config['path.data_lake']
        except TypeError:
            self.setting['path'] = settings
            self.setting['db_config'] = db_config

    def run_processing(self, config_name):

        """
        The main method of Loader object

        Read input name of configuration file.
        Get required configuration from config file
        Read dataset, and process it by predefined
        instruction

        Args:
            name of configuration

        """
        configs = self._get_proj_info(config_name)

        regime = configs.get("General", 'regime')
        is_chunk = configs['General']['ischunk']

        if regime == 'indy':
            if is_chunk:
                self._run_indy_processing(configs)
            else:
                self._run_indy_chunk_processing(configs)
        else:
            project_name = configs['General']['project_name']
            self._run_warehouse_processing(configs, project_name)

    def _run_warehouse_processing(self, configs, project_name):
        """
        Run warehouse processing

        :param configs:
        :type configs:
        :return:
        :rtype:
        """

        store = []
        for section_name in [i for i in configs.sections() if i != "General"]:
            # Loading function.
            loader_name = configs.get(section_name, 'pre_loader_function',
                                      fallback=None)

            for df in self.collects_data(configs[section_name]):
                if loader_name is not None:
                    loader = getattr(loading_lib, loader_name)
                    df = loader(configs[section_name], self.project)
                store.append(df)

        # Loading function.
        loader_name = configs.get('General', 'process', fallback=None)

        configs['General']['db_config'] = self.setting['db_config']

        project = wh_api.Project(project_name)
        if loader_name is not None:
            loader = getattr(loading_lib, loader_name)
            loader(configs, store, project)

    def _run_indy_processing(self, configs):

        dfs = []
        for section_name in \
                [i for i in configs.sections() if i != "General"]:

            for df in self.collects_data(configs[section_name]):
                dfs.append(df)
        try:
            processor = getattr(loading_lib,
                                configs.get('General', 'process'))
        except AttributeError:
            processor = None

        except KeyError:
            processor = None

        if processor:
            dfs = processor(config=configs, dfs=dfs)

        self.save_data(dfs, configs['General'])


    def _run_indy_chunk_processing(self, config, section_name):

        try:
            processor = getattr(loading_lib, config.get(section_name,
                                                         'process'))
        except AttributeError:
            processor = None

        except KeyError:
            processor = None

        for df in self.collects_data(config[section_name]):
            if processor:
                df = processor(config=config, df=df)
            self.save_data(df, config[section_name])


    def _get_proj_info(self, config_name):
        """
        Private function that called in run_processing
        Get config file, parse it and read it. Extract required
        sections.

        :param proj_name:
        :type proj_name:
        :return:
        :rtype:
        """

        # Read main config
        source = self.setting['path']
        main_config_path = os.path.join(source,
                                        '{0}.ini'.format(config_name))
        config = configparser.ConfigParser()
        config.read(main_config_path)
        return config


    def _load_data_set(self, abs_path, file_name, loader, file_config,
                       proj_path=None):
        """
        Function read data set.
        And call processing function.

        :param abs_path:
        :type abs_path:
        :param file_name:
        :type file_name:
        :param loader:
        :type loader:
        :param file_config:
        :type file_config:
        :param proj_path:
        :type proj_path:
        :return:
        :rtype:
        """

        if abs_path == "/":
            file_path = os.path.join(proj_path, file_name)
        else:
            file_path = os.path.join(abs_path, file_name)

        if os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            base_name, extension = os.path.splitext(file_name)
            with open(file_path, 'rb') as file:
                data = self._read_file(extension, file)
                #data=self._read_file_pd(file_path=file_path,extension=extension)
                loader(data, file_config, self._warehouse)
        else:
            raise CorruptedDataSet

        return data


    def _post_load_function(self, ):
        pass

    def collects_data(self, config):
        """"
            Collect data from external storage into DataFrame
        """
        format = config['format']
        if format in ['csv', 'txt']:
            return self.collect_data(config)
        elif format == 'xls':
            return self.collect_data_xls(config)
        elif format == 'hdf':
            self.collect_from_hdf(config)
        else:
            pass

    def collect_from_hdf(self, config):
        """
        Read from hdf storage and get Dataframe
        """
        try:
            storage_path = config['storage_path']
            table_name = config['table_name']
        except KeyError:
            logging.info("Wrong Input File")
            raise Exception
        else:
            columns = config['columns']
            chunk_size = config['chunk_size']
            format = config['format']
            where = config['where']
        if format == 'hdf':
            with pd.HDFStore(storage_path) as store:
                for chunk in store.select(table_name, columns=columns,
                                          auto_close=True, where=where,
                                          chunksize=chunk_size):
                    logging.info(
                        "Data Collected - storage_path: {0} - Table {1} - Chunk {2}".
                            format(storage_path, table_name, chunk_size))
                    yield chunk
        else:
            return None


    def preprocess(self, file, col_to_read, columns, sep):

        try:
            row = pd.read_table(file, sep=sep, nrows=1)
            if set(columns) >= set(col_to_read) and \
                            len(columns) == len(row.columns):
                return True
            else:
                return False
        except Exception:
            return False


    def collect_data(self, config):
        """"
        Collect data from external storage into DataFrame
        """

        try:
            data_path = config['data_folder']
            filename_mask = config['file_mask']
        except KeyError:
            logging.info("wrong input file")
            raise Exception

        columns = config['columns'].split(",")
        try:
            chunk_size = int(config['chunk_size'])
        except ValueError:
            chunk_size = None

        sep = config['sep']
        header = config['header']

        try:
            cols_props = config['columns_properties']
            with open(cols_props) as f:
                cols_props = json.load(f)
            col_to_read = [i['col_name'] for i in cols_props]
        except KeyError:
            index_cols = None
            col_to_read = columns
        else:
            index_cols = [ind for ind, x in enumerate(cols_props)
                          if x['col_type'] == 'index']
            if index_cols == []:
                index_cols = None
        if not os.path.isdir(data_path):
            data_path = os.path.join(self.setting['path'], data_path)

        filenames = self.scan_folder(data_path, filename_mask)

        for file in filenames:
            preprocess_result = self.preprocess(file, col_to_read=col_to_read,
                                           columns=columns, sep=sep)

            if header and preprocess_result:
                for chunk in pd.read_table(file, header=0, usecols=col_to_read,
                                           iterator=True,
                                           chunksize=chunk_size, sep=sep):
                    logging.info("Data Collected - File: {0} - Chunk {1}".
                                 format(file, chunk_size))
                    yield chunk

            elif preprocess_result and not header:
                for chunk in pd.read_table(file, header=None,
                                           usecols=col_to_read, iterator=True,
                                           names=columns, chunksize=chunk_size,
                                           sep=sep, index_col=index_cols):
                    logging.info("Data Collected - File {0} - Chunk {1}".
                                 format(file, chunk_size))
                    yield chunk
            else:
                logging.info(
                    "No valid format of input columns - {0}".format(file))
                raise Exception


    def collect_data_xls(self, config):
        """"
        Collect data from external xls storage into DataFrame
        """
        try:
            data_path = config['data_folder']
            filename_mask = config['file_mask']
        except KeyError:
            logging.info("Wrong Input File")
            raise Exception

        columns = config['columns'].split(',')
        format = config['format']
        sep = config['sep']
        filenames = self.scan_folder(data_path, filename_mask)

        for path in filenames:
            if format == 'xls':
                xls = pd.ExcelFile(path)
                df = xls.parse(header=0, sep=sep, usecols=columns)
                logging.info("Data Collected - {0}".format(path))
                yield df


    def collect_to_hdf(self, config):
        """
        Reading from .csv file and saving to hdf
        """
        try:
            table_name = config['table_name']
            storage_path = config['storage']
            mode = config['mode']
        except KeyError:
            logging.info("wrong input file-{0}-{1}".
                         format(table_name, storage_path))
            raise Exception

        cols_props = config['columns_properties']
        with open(cols_props) as f:
            cols_props = json.load(f)
        data_cols = [x['col_name'] for x in cols_props if
                     x['is_index_data_col']]

        with pd.HDFStore(storage_path, mode='a') as store:
            if mode == 'w' and table_name in store.keys():
                store.remove(table_name)
            result = self.process_types(df, cols_props)

            result.to_hdf(storage_path, table_name, append=True,
                              format='t',
                              min_itemsize=100)
            logging.info("Stored to Hdf: Storage - {0} Table - {1}"
                             .format(storage_path, table_name))
            store.create_table_index(table_name, columns=data_cols,
                                     kind='full')


    def scan_folder(self, path, mask):
        f_names = []
        compiled_mask = re.compile(mask)
        for filename in os.listdir(path):
            match_res = compiled_mask.match(filename)
            if not match_res:
                continue
            f_names.append(os.path.join(path, filename))
        return f_names


    def process_types(self, df, cols_props):
        for col_item in cols_props:
            c_name = col_item['col_name']
            if col_item['col_type'] == 'numeric':

                df[c_name] = pd.to_numeric(df[c_name], errors='coerce') \
                    .astype('float64')
            elif col_item['col_type'] == 'categorical':

                df[c_name] = df[c_name] \
                    .astype('category', categories=col_item['options'])
            elif col_item['col_type'] == 'date':

                df[c_name] = \
                    pd.to_datetime(df[c_name], format=col_item['format'],
                                   errors='coerce')
            elif col_item['col_type'] == 'object':

                df[c_name] = df[c_name].astype('object')
        return df


    def out_process_data_var_col(self, df, variables, time_stamp_column):
        """
        Process data into output format - Variable: var_1, var_ var_3
                                          TimeStamp_1: 2, 203, 13
                                          TimeStamp_2: 0, 12, 20
        """

        time_stamps = list(df[time_stamp_column].unique())
        for var in variables:
            for time_stamp in time_stamps:
                col_name = var + "_" + str(time_stamp)
                df[col_name] = None
                df[col_name][(df[time_stamp_column] == time_stamp)] = \
                    df[var][(df[time_stamp_column] == time_stamp)]. \
                        apply(lambda x: x)
            del df[var]
            df.drop_duplicates()
        return df


    def out_process_data_var_ts_col(self, df, variables, time_stamp_column):
        """
        Output processing into format Time_Stamp_1_Var: 1,1,2
                                      Time_Stamp_2_Var: 1,2,3

        Inputs:
            config
            DataFrame
        Output:
            Change format of DataFrame
        """

        time_stamps = list(df[time_stamp_column].unique())

        frames = []
        for var_name in variables:
            df["variable"] = var_name
            for time_stamp in time_stamps:
                df[time_stamp] = None
                df[time_stamp][(df['variable'] == var_name)] = \
                    df[(df[time_stamp_column] == time_stamp)][var_name]. \
                        apply(lambda x: x)

            df.drop_duplicates()
            frames.append(df)

        for var_name in vars:
            del df[var_name]
        df = pd.concat(frames)
        return df


    def save_data(self, df, config):

        try:
            format = config['output_format']
        except KeyError:
            raise Exception

        if format == "csv":
            path = config['output_path']
            sep = config['sep']
            mode = config['mode']
            df.to_csv(path + '.csv', sep=sep, mode=mode)
        elif format == 'xls':
            path = config['output_path']
            sep = config['sep']
            mode = config['mode']
            df.to_excel(path, sep=sep, mode=mode)
        elif format == "hdf":
            self.collect_to_hdf(df, config)
        else:
            pass


class InsDictReader(csv.DictReader):
    @property
    def fieldnames(self):
        return [field.strip().lower() for field in super(InsDictReader, self)
                .fieldnames]


