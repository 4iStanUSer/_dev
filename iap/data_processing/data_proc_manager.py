import os
import io
import xlrd
from csv import DictReader
from datetime import datetime


class DataUploadManager():
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


class InsDictReader(DictReader):

    @property
    def fieldnames(self):
        return [field.strip().lower() for field in super(InsDictReader, self)
                .fieldnames]