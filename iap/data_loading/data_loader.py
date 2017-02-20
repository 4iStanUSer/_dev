import os
import io
import xlrd
import configparser
import re
import csv
import pandas as pd

from .config import config as c
from ..data_loading import loading_lib


class Loader:
    def __init__(self, warehouse, config):

        self._warehouse = warehouse
        self._source = config['path.data_lake']

        #TODO set path from configuration
        #self._source = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        #                            'data_storage', 'data_lake')

    def run_processing(self, proj_name):
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
                raise Exception
            if file_config.getboolean('ignore', fallback=False):
                continue

            # Loading function.
            loader = getattr(loading_lib, file_config['loader_function'])

            # Open file and run loading function.
            try:
                print(file_config)
                file_name = file_config['file_name']
                abs_path = file_config['abs_path']
            except KeyError:
                raise Exception#TODO change on no data set
            else:
                self._load_data_set(abs_path=abs_path, file_name=file_name,
                                    loader=loader, file_config=file_config, proj_path=proj_path)
            #TODO change on path to dataset

        # Run post loading function if it is defined
        postloader_name = config.get('DEFAULT', 'postloading_function',
                                     fallback=None)
        if postloader_name  is not None:
            postloader = getattr(loading_lib, postloader_name)
            postloader(config['DEFAULT'], self._warehouse)
        # Commit changes
        self._warehouse.commit()


    def _get_proj_info(self, proj_name):
        # Read main config
        main_config_path = os.path.join(self._source, 'config.ini')
        main_config = configparser.ConfigParser()
        main_config.read(main_config_path)
        proj_folder = main_config.get(section=proj_name, option='path',
                                      fallback=None)

        if proj_folder is None:
            raise Exception
        # Read project config
        proj_config_path = os.path.join(self._source, proj_folder,
                                        proj_name + '_config.ini')
        proj_config = configparser.ConfigParser()
        proj_config.read(proj_config_path)
        return proj_folder, proj_config

    def _load_data_set(self, abs_path, file_name, loader, file_config, proj_path=None):
        print(abs_path)
        if abs_path == "/":
            file_path = os.path.join(proj_path, file_name)
        else:
            file_path = os.path.join(abs_path, file_name)

        if os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            base_name, extension = os.path.splitext(file_name)
            with open(file_path, 'rb') as file:
                data = self._read_file(extension, file)
                loader(data, file_config, self._warehouse)

        else:
            print("file path", file_path)
            raise Exception
            #TODO change on corrupted data

        return data

    def _post_load_function(self, ):
        pass

    @staticmethod
    def _read_file(extension, file):
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


class InsDictReader(csv.DictReader):
    @property
    def fieldnames(self):
        return [field.strip().lower() for field in super(InsDictReader, self)
                .fieldnames]