import os, io, xlrd, datetime
from csv import DictReader

from .config import config
from ..data_processing import data_loading

class Loader:
    def __init__(self, warehouse, data_load_command='jj'):
        self.warehouse = warehouse
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        self.lake_src = os.path.join(BASE_DIR, 'repository', 'data_lake')
        self.files_map = ('.xlsx', '.csv')

    def load(self):
        for file_name in os.listdir(self.lake_src):
            base_name, extension = os.path.splitext(file_name)
            if extension in self.files_map:
                file_path = os.path.join(self.lake_src, file_name)
                self.__process_file(base_name, extension, file_path)

    def __process_file(self, file_name, extension, file_path):
        if file_name in config:
            options_list = config[file_name]
            run_method = getattr(data_loading, options_list['func'])
            options_list['date_func'] = getattr(data_loading, options_list['date_func'])
            with open(file_path, 'rb') as file:
                read_obj = read_file(extension, file)
                # Run method
                try:
                    run_method(self.warehouse, read_obj, options_list)
                    self.warehouse.commit()
                except Exception as err:
                    print(err.args)


def read_file(extension, file):
    if extension == '.csv':
        reader = InsDictReader(io.TextIOWrapper(file))
        return reader
    if extension == '.xlsx':
        wb = xlrd.open_workbook(file_contents=file.read())
        return wb
    return None


class InsDictReader(DictReader):

    @property
    def fieldnames(self):
        return [field.strip().lower() for field in super(InsDictReader, self)
                .fieldnames]