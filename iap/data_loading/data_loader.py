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
    def __init__(self, warehouse, config):

        self._warehouse = warehouse
        self._source = config['path.data_lake']

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

        main_config_path = os.path.join(self._source, 'config.ini')
        main_config = configparser.ConfigParser()
        main_config.read(main_config_path)
        try:
            proj_folder = main_config.get(section=proj_name, option='path',
                                      fallback=None)
        except Exception:
            raise NonExistedProject
        # Read project config
        else:
            proj_config_path = os.path.join(self._source, proj_folder,
                                        proj_name + '_config.ini')
            proj_config = configparser.ConfigParser()
            proj_config.read(proj_config_path)
            return proj_folder, proj_config

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


class InsDictReader(csv.DictReader):
    @property
    def fieldnames(self):
        return [field.strip().lower() for field in super(InsDictReader, self)
                .fieldnames]