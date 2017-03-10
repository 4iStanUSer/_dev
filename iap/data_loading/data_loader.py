import os
import io
import xlrd
import configparser
import re
import csv
import pandas as pd

from .exceptions import NonExistedConfig, NonExistedDataSet, CorruptedDataSet, NonExistedProject
from ..data_loading import loading_lib


class Loader:
    """
    Starting point of Load

    Attr:
        config - path to configuration file with all
                neccessary settings

        warehouse - interface for db interaction and data structure
                    behavior
    """
    def __init__(self, config=None, warehouse=None):

        self._warehouse = warehouse
        self._source = config

        print("Source File", self._source)

    def set_config(self, **kwargs):

        pass
        #TODO set path from configuration
        #self._source = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        #                            'data_storage', 'data_lake')

    def run_processing(self, proj_name):
        """
        The main method of Loader object

        Read input name of project.
        Get required configuration from config file
        Read dataset, and process it by predefined
        instruction

        :param proj_name:
        :type proj_name:

        :return:
        :rtype:
        """
        # Get project folder and config
        folder, config = self._get_proj_info(proj_name)
        # Run pre loading function if it is defined
        preloader_name = config.get('DEFAULT', 'preloading_function',
                                    fallback=None)
        if preloader_name is not None:
            preloader = getattr(loading_lib, preloader_name)
            preloader(config['DEFAULT'], self._warehouse)

        # Search files in project folder
        proj_path = os.path.join(self._source, folder)
        for filename in os.listdir(proj_path):
            file_config = None
            for sect_name in config.sections():
                if re.fullmatch(re.compile(sect_name), filename) is not None:
                    file_config = config[sect_name]
                    break
            if file_config is None:
                raise NonExistedConfig
            if file_config.getboolean('ignore', fallback=False):
                continue

            # Loading function.
            loader = getattr(loading_lib, file_config['loader_function'])

            # Open file and run loading function.
            try:
                file_name = file_config['file_name']
                abs_path = file_config['abs_path']
            except KeyError:
                raise NonExistedDataSet
            else:
                self._load_data_set(abs_path=abs_path, file_name=file_name,
                                    loader=loader, file_config=file_config, proj_path=proj_path)

        # Run post loading function if it is defined
        postloader_name = config.get('DEFAULT', 'postloading_function',
                                     fallback=None)
        if postloader_name is not None:
            postloader = getattr(loading_lib, postloader_name)
            postloader(config['DEFAULT'], self._warehouse)
        # Commit changes
        self._warehouse.commit()


    def _get_proj_info(self, proj_name):
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
        #TODO Change self.source
        main_config_path = os.path.join(self._source, '{0}_config.ini'.format(proj_name))
        main_config = configparser.ConfigParser()
        main_config.read(main_config_path)
        proj_folder = os.path.join(self._source, main_config['Path']['path'])
        return proj_folder, main_config

    def _load_data_set(self, abs_path, file_name, loader, file_config, proj_path=None):
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

    @staticmethod
    def _read_file(extension, file):
        """
        Read file and reaturn raw data

        :param extension:
        :type extension:
        :param file:
        :type file:
        :return:
        :rtype:
        """
        if extension == '.csv':
            # reader = InsDictReader(io.TextIOWrapper(file))
            reader = csv.reader(io.TextIOWrapper(file))
            return reader
        elif extension == '.xlsx':
            wb = xlrd.open_workbook(file_contents=file.read())
            return wb
        elif extension=="json":
            pass
        return None

    @staticmethod
    def _read_file_pd(extension, file_path):
        """Read file and transform it into pandas DataFrame

        :param extension:
        :type extension:
        :param file_path:
        :type file_path:
        :return:
        :rtype:
        """
        if extension == '.csv':
            # reader = InsDictReader(io.TextIOWrapper(file))
            df = pd.read_csv(file_path)
            return df
        elif extension == '.xlsx':
            df = pd.read_excel(file_path)
            return df
        elif extension=="json":
            df = pd.read_json(file_path)
            return df
        return None

    """"
    Fucntions from new API
    """
    def collects_data(self, config):
        """"
            Collect data from external storage into DataFrame
        """

        format = config['format']
        if format in ['csv', 'txt']:
            return self.collect_data(config)
        elif format == 'excel':
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
            print("wrong input file")
            raise Exception
        else:
            format = config['format']
            columns = config['columns']
            chunk_size = config['chunk_size']
            where = config['where']

        if format == 'hdf':
            with pd.HDFStore(storage_path) as store:
                for chunk in store.select(table_name, columns=columns, auto_close=True, where=where,
                                          chunksize=chunk_size):
                    yield chunk
        else:
            return None

    def collect_data(self, config):
        """"
        Collect data from external storage into DataFrame
        """
        try:
            data_path = config['data_folder']
            filename_mask = config['file_mask']
        except KeyError:
            print("wrong input file")
            raise Exception

        columns = config['columns']
        chunk_size = config['chunk_size']
        sep = config['sep']
        header = config['header']

        try:
            cols_props = config['columns_properties']
            col_to_read = [i['col_name'] for i in cols_props]
        except KeyError:
            index_cols = None
            col_to_read = columns
        else:
            index_cols = [ind for ind, x in enumerate(cols_props) if x['col_type'] == 'index']
            if index_cols == []:
                index_cols = None

        filenames = self.scan_folder(data_path, filename_mask)

        for file in filenames:
            if header:
                for chunk in pd.read_table(file, header=0, usecols=col_to_read, chunksize=chunk_size, sep=sep):
                    yield chunk
            else:
                for chunk in pd.read_table(file, header=0, usecols=col_to_read, names=columns, chunksize=chunk_size,
                                           sep=sep, index_col=index_cols):
                    yield chunk

    def collect_data_xls(self, config):
        """"
        Collect data from external xls storage into DataFrame
        """
        try:
            data_path = config['data_folder']
            filename_mask = config['file_mask']
        except KeyError:
            print("wrong input file")
            raise Exception

        columns = config['columns']
        format = config['format']
        sep = config['sep']

        filenames = self.scan_folder(data_path, filename_mask)

        for path in filenames:
            if format == 'xls':
                xls = pd.ExcelFile(path)
                df = xls.parse(header=0, sep=sep, usecols=columns)
                yield df


    def collect_to_hdf(config, processor):
        """
        Reading from .csv file and saving to hdf
        """
        try:
            table_name = config['table_name']
            storage_path = config['storage']
            mode = config['mode']
        except KeyError:
            print("wrong input file")
            raise Exception
        cols_props = config['columns_properties']

        data_cols = [x['col_name'] for x in cols_props if x['is_index_data_col']]
        with pd.HDFStore(storage_path, mode='a') as store:
            if mode == 'w' and table_name in store.keys():
                store.remove(table_name)
            else:
                pass
            for df in collects_data(config):
                print(df.head(2))
                if processor:
                    result = processor(df)
                    result = process_types(result, cols_props)
                else:
                    result = process_types(df, cols_props)
                    print("result", result)
                store.append(table_name, result, data_columns=data_cols, min_itemsize=100)
                print('File: {0}'.format(storage_path))


    def scan_folder(path, mask):
        f_names = []
        compiled_mask = re.compile(mask)
        for filename in os.listdir(path):
            match_res = compiled_mask.match(filename)
            if not match_res:
                continue
            f_names.append(os.path.join(path, filename))
        return f_names


    def process_types(df, cols_props):
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


    def out_process_data(df, variables, time_stamp_column):
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
                df[col_name][(df[time_line] == time_stamp)] = df[var][(df[time_line] == time_stamp)].apply(lambda x: x)
            del df[var]
            df.drop_duplicates()
        return df


    def out_process_data_2(self, df, variables, time_stamp_column):
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
                    df[(df[time_stamp_column] == time_stamp)][var_name].apply(lambda x: x)

            df.drop_duplicates()
            frames.append(df)

        for var_name in vars:
            del df[var_name]
        df = pd.concat(frames)
        return df


    def write(self, df, path, format, sep=',', mode='w'):

        """
        Save to external storage Csv or XLS
        """
        if format == 'csv':
            df.to_csv(path + '.csv', sep=sep, mode=mode)
            print("File Save  %s" % path)
        elif format == 'xls':
            df.to_excel(path, sep=sep, mode=mode)
            print("File Save  %s" % path)


class InsDictReader(csv.DictReader):
    @property
    def fieldnames(self):
        return [field.strip().lower() for field in super(InsDictReader, self)
                .fieldnames]