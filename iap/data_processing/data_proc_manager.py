import os
import io
import xlrd
from csv import DictReader
import collections
from iap.data_processing.processors import jj_brand, jj_brand_extract, \
    jj_oc_data_proc
from iap.data_processing.processors.common import date_year_month, date_year,\
    date_jj_1week


class Loader:
    def __init__(self, data_load_command='jj'):
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        self.lake_src = os.path.join(BASE_DIR, 'repository', 'data_lake')
        self.func_list = {
            'jj_oc_input_sales_data':
                {'func': jj_oc_data_proc,
                 'date_func': date_year_month,
                 'info': {'header_row': 2, 'data_row': 3},
                 'meta_cols': collections.OrderedDict(
                  {0: '', 1: '', 2: 'NewBrand', 3: ''}),
                 'name_col': 4,
                 'properties': {5: 'Metric'},
                 'dates_cols': {'scale': 'monthly',
                                'date_name_rows': [0, 2],
                                'start_column': 6,
                                'end_column': ''}},
            'jj_oc_input_trends':
                {'func': jj_oc_data_proc,
                 'date_func': date_year,
                 'info': {'header_row': 1, 'data_row': 2},
                 'meta_cols': collections.OrderedDict({0: ''}),
                 'name_col': 1,
                 'properties': {2: 'Facts', 3: '', 4: ''},
                 'dates_cols': {'scale': 'years',
                                'date_name_rows': [1],
                                'start_column': 5,
                                'end_column': ''}},
            'MyReport (Benadryl SI Other Accaunts)':
                {'func': jj_brand,
                 'date_func': date_jj_1week,
                 'info': 'N/A',
                 'meta_cols': ['Category', 'Segment', 'SubSegment', 'Brand',
                               'SubBrand'],
                 'name_col': 0,
                 'properties': 'N/A',
                 'dates_cols': {'scale': '1week',
                                'date_name_rows': 'N/A',
                                'start_column': 1,
                                'end_column': ''}},
            'JNJ_SALES_EXTRACT_FOR_4I_201603':
                {'func': jj_brand_extract,
                 'data_func': date_year_month,
                 'info': 'N/A',
                 'meta_cols': collections.OrderedDict({3: 'LVL1', 5: 'LVL2',
                                                       6: ''}),
                 'name_col': 'N/A',
                 'properties': 'N/A',
                 'dates_cols': {'scale': 'monthly',
                                'date_col': 0},
                 'data_cols': {8: 'A', 10: 'B', 11: 'C', 12: 'D'},
                 'sum_rule':
                     [{'Name': 'A', 'TimeScale': 'sum', 'FactScale': 'sum'},
                      {'Name': 'B', 'TimeScale': 'sum', 'FactScale': 'sum'},
                      {'Name': 'C', 'TimeScale': 'sum', 'FactScale': 'sum'},
                      {'Name': 'C', 'TimeScale': 'sum', 'FactScale': 'sum'}],
                 'mapping_rule': [{'in': {'LVL1': 'DRUG CHANNEL',
                                          'LVL2': 'RITE AID'},
                                   'out': {'LVL1': 'Ecommerce'}}]
                 }
        }
        self.files_map = ('.xlsx', '.csv')

    def load(self):
        for file_name in os.listdir(self.lake_src):
            base_name, extension = os.path.splitext(file_name)
            if extension in self.files_map:
                file_path = os.path.join(self.lake_src, file_name)
                self.__process_file(base_name, extension, file_path)

    def __process_file(self, file_name, extension, file_path):
        options_list = self.func_list[file_name]
        # info = options_list['info']
        # date_func = options_list['date_func']
        # prop_cols = options_list['properties']
        run_method = options_list['func']
        # meta_cols = options_list['meta_cols']
        # name_col_num = options_list['name_col']
        # dates_cols = options_list['dates_cols']
        with open(file_path, 'rb') as file:
            read_obj = read_file(extension, file)
            # Run method
            try:
                # output = run_method(read_obj, info, meta_cols, name_col_num,
                #                     dates_cols, prop_cols, date_func)
                output = run_method(read_obj, options_list)
                print(output[1])
            except Exception as err:
                print(err.args)


class DataUploadManager:
    def jj_oc_process_files(self, file_path, func_list):
        '''
        func_list is a dictionary with a:
        1) list of functions which append
        to the file path
        2) list of meta columns: ordered names and numbers (+hierarchy)
        3) list of data column: names and numbers
        4) list of dates columns: string and numbers
        '''
        temp_path, extension = os.path.splitext(file_path)
        file_name = os.path.basename(temp_path)
        # Read file
        with open(file_path, 'rb') as file:
            read_obj = self.__read_file(extension, file)
        try:
            # Define options for the file
            options_list = func_list[file_name]
            info = options_list['info']
            date_func = options_list['date_func']
            prop_cols = options_list['properties']
            run_method = options_list['func']
            meta_cols = options_list['meta_cols']
            name_col_num = options_list['name_col']
            dates_cols = options_list['dates_cols']
            # Run method
            output = run_method(read_obj, info, meta_cols, name_col_num,
                                dates_cols, prop_cols, date_func)
            return output
        except Exception as err:
            print('Exception')
            print(err.args)

    def process_files(self, file_path, func_list):
        '''
        func_list is a dictionary with a:
        1) list of functions which append
        to the file path
        2) list of meta columns: names and numbers 
        3) list of data column: names and numbers
        4) list of dates columns: string and numbers
        '''
        temp_path, extension = os.path.splitext(file_path)
        file_name = os.path.basename(temp_path)
        # Read file
        with open(file_path, 'rb') as file:
            read_obj = self.__read_file(extension, file)
        try:
            # Define options for the file
            options_list = func_list[file_name]
            run_method = options_list['func']
            meta_cols = options_list['meta_cols']
            data_cols = options_list['data_cols']
            dates_cols = options_list['dates_cols']
            # Run method
            output = run_method(read_obj, meta_cols, data_cols, dates_cols)
            return output
        except Exception as err:
            print('Exception')
            print(err.args)

    def __read_file(self, extension, file):
        if extension == '.csv':
            reader = InsDictReader(io.TextIOWrapper(file))
            return reader
        if extension == '.xlsx':
            wb = xlrd.open_workbook(file_contents=file.read())
            return wb
        return None


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