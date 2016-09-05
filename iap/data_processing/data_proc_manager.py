import os
import io
import xlrd
from csv import DictReader
import collections
from iap.data_processing.data_loading import jj_brand, jj_brand_extract, \
    jj_oc_data_proc, jj_oral_care_sku, jj_oral_care_media_spend, \
    jj_oral_care_rgm_sales
from iap.data_processing.data_loading.common import date_year_month, date_year,\
    date_jj_1week, date_yyyyww, date_monthly_excel_number
import datetime

class Loader:
    def __init__(self, warehouse, data_load_command='jj'):
        self.warehouse = warehouse
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
                 'meta_cols': [
                     {'Layer': 'Geography', 'Dimension_name': 'Total_market',
                      'Name': ''},
                     {'Layer': 'Time', 'Dimension_name': 'Total_category',
                      'Name': ''},
                     {'Layer': 'Geography', 'Dimension_name': 'Category',
                      'Name': ''},
                     {'Layer': 'Products', 'Dimension_name': 'Brand',
                      'Name': ''},
                     {'Layer': 'Products', 'Dimension_name': 'SubBrand',
                      'Name': ''}
                 ],
                 'name_col': 0,
                 'properties': 'N/A',
                 'dates_cols': {'scale': 'weekly',
                                'date_name_rows': 'N/A',
                                'start_column': 1,
                                'end_column': ''}},
            'MyReport (Band-aid Other Accaunts)':
                {'func': jj_brand,
                 'date_func': date_jj_1week,
                 'info': 'N/A',
                 'meta_cols': [
                     {'Layer': 'Products', 'Dimension_name': 'Total_market',
                      'Name': ''},
                     {'Layer': 'Products', 'Dimension_name': 'Total_brand',
                      'Name': ''},
                     {'Layer': 'Products', 'Dimension_name': 'Brand',
                      'Name': ''},
                     {'Layer': 'Products', 'Dimension_name': 'SubBrand',
                      'Name': ''}
                 ],
                 'name_col': 0,
                 'properties': 'N/A',
                 'dates_cols': {'scale': 'weekly',
                                'date_name_rows': 'N/A',
                                'start_column': 1,
                                'end_column': ''}},
            'JNJ_SALES_EXTRACT_FOR_4I_201603':
                {'func': jj_brand_extract,
                 'data_func': date_yyyyww,
                 'info': 'N/A',
                 'meta_cols':
                     [{'Layer': 'Products', 'Dimension_name': 'Store',
                       'Name': '', 'Col_number': 3},
                      {'Layer': 'Products', 'Dimension_name': 'Brand',
                       'Name': '', 'Col_number': 5},
                      {'Layer': 'Products', 'Dimension_name': 'SubBrand',
                       'Name': '', 'Col_number': 6}],
                 'name_col': 'N/A',
                 'properties': 'N/A',
                 'dates_cols': {'scale': 'weekly',
                                'date_col': 1},
                 'data_cols': {(10, 'int'): '', (11, 'float'): 'C',
                               (12, 'int'): 'D'},
                 'sum_rule':
                     [{'Name': 'B', 'TimeScale': 'sum', 'FactScale': 'sum'},
                      {'Name': 'C', 'TimeScale': 'sum', 'FactScale': 'sum'},
                      {'Name': 'D', 'TimeScale': 'sum', 'FactScale': 'sum'}],
                 'mapping_rule':
                     [{'in': collections.OrderedDict(
                         {'Store': 'DRUG CHANNEL', 'Brand': 'RITE AID'}),
                       'out': collections.OrderedDict({'Store': 'Ecommerce'})}]
                 },
            'jj_oral_care_sku_data':
                {'func': jj_oral_care_sku,
                 'date_func': date_monthly_excel_number,
                 'info': {'header_row': 0, 'data_row': 1},
                 'meta_cols': [
                     {'Layer': 'Geography', 'Dimension_name': 'Region',
                      'Name': '', 'Col_number': 0},
                     {'Layer': 'Products', 'Dimension_name': '',
                      'Name': '', 'Col_number': 1},
                     {'Layer': 'Products', 'Dimension_name': '',
                      'Name': '', 'Col_number': 2},
                     {'Layer': 'Products', 'Dimension_name': '',
                      'Name': '', 'Col_number': 3}
                 ],
                 'name_col': 4,
                 'map_names': {'Value Sales LC': 'Values_sales_lc'},
                 'dates_info': {'scale': 'monthly',
                                'start_column': 5,
                                'end_column': ''}
                 },
            'jj_oral_care_sku_data_media_spend':
                {'func': jj_oral_care_media_spend,
                 'date_func': date_year_month,
                 'info': {'header_row': 2, 'data_row': 3},
                 'meta_cols': [
                     {'Layer': 'Geography', 'Dimension_name': 'Country',
                      'Name': '', 'Col_number': 0},
                     {'Layer': 'Products', 'Dimension_name': '',
                      'Name': '', 'Col_number': 1},
                     {'Layer': 'Products', 'Dimension_name': '',
                      'Name': '', 'Col_number': 2},
                     {'Layer': 'Products', 'Dimension_name': '',
                      'Name': '', 'Col_number': 3},
                     {'Layer': 'Products', 'Dimension_name': '',
                      'Name': '', 'Col_number': 4}
                 ],
                 'name_col': 5,
                 'dates_info': {'scale': 'monthly',
                                'start_column': 6,
                                'end_column': '',
                                'dates_rows': [0, 2]}
                 },
            'jj_oral_care_rgm_sales':
                {'func': jj_oral_care_rgm_sales,
                 'date_func': date_year_month,
                 'info': {'header_row': 11, 'data_row': 12},
                 'meta_cols': [
                     {'Layer': 'Geography', 'Dimension_name': 'Country',
                      'Name': '', 'Col_number': 0},
                     {'Layer': 'Products', 'Dimension_name': '',
                      'Name': '', 'Col_number': 1},
                     {'Layer': 'Products', 'Dimension_name': '',
                      'Name': '', 'Col_number': 2},
                     {'Layer': 'Products', 'Dimension_name': '',
                      'Name': '', 'Col_number': 3}
                 ],
                 'name_col': 4,
                 'dates_info': {'scale': 'monthly',
                                'start_column': 5,
                                'end_column': '',
                                'dates_rows': [9, 11]}
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
        if file_name in self.func_list:
            options_list = self.func_list[file_name]
            # info = options_list['info']
            # date_func = options_list['date_func']
            # prop_cols = options_list['properties']
            run_method = options_list['func']
            # meta_cols = options_list['meta_cols']
            # name_col_num = options_list['name_col']
            # dates_cols = options_list['dates_cols']
            t1 = datetime.datetime.now()
            with open(file_path, 'rb') as file:
                read_obj = read_file(extension, file)
                t2 = datetime.datetime.now()
                delta = (t2 - t1)
                # minutes_delta_time = delta.seconds / 60.0
                # print('Read file takes minutes:' + str(minutes_delta_time))
                print('Read file takes seconds:' + str(delta.seconds))
                # Run method
                try:
                    run_method(self.warehouse, read_obj, options_list)
                    self.warehouse.commit()
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