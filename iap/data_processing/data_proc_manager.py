import os
import io
import xlrd
from csv import DictReader
import collections
from iap.data_processing.data_loading import jj_brand, jj_brand_extract, \
    jj_oc_data_proc, jj_oral_care_sku, jj_oral_care_media_spend, \
    jj_oral_care_rgm_sales, jj_brand_media_spend
from iap.data_processing.data_loading.common import date_year_month, date_year,\
    date_jj_1week, date_yyyyww, date_monthly_excel_number, date_mmddyyyy
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
                     {'Layer': 'Products', 'Dimension_name': 'Total_market',
                      'Name': ''},
                     {'Layer': 'Products', 'Dimension_name': 'Total_category',
                      'Name': ''},
                     {'Layer': 'Products', 'Dimension_name': 'Category',
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
            'JNJ_lean_media_spend':
                {'func': jj_brand_media_spend,
                 'date_func': date_monthly_excel_number,
                 'info': 'N/A',
                 'meta_cols': [
                     {'Layer': 'Products', 'Dimension_name': '',
                      'Name': '', 'Col_number': 0},
                     {'Layer': 'Products', 'Dimension_name': 'Type',
                      'Name': '', 'Col_number': 1},
                     {'Layer': 'Products', 'Dimension_name': '',
                      'Name': '', 'Col_number': 2},
                     {'Layer': 'Products', 'Dimension_name': 'Segment',
                      'Name': '', 'Col_number': 3},
                 ],
                 'name_col': 4,
                 'properties': 'N/A',
                 'dates_cols': {'scale': 'monthly',
                                'date_name_rows': 'N/A',
                                'start_column': 5,
                                'end_column': ''}},
            'JNJ_SALES_EXTRACT_FOR_4I_201603':
                {'func': jj_brand_extract,
                 'date_func': date_yyyyww,
                 'info': 'N/A',
                 'meta_cols':
                     [{'Layer': 'Products', 'Dimension_name': 'Market',
                       'Name': '', 'Col_number': 4},
                      {'Layer': 'Products', 'Dimension_name': 'Segments',
                       'Name': '', 'Col_number': 7}],
                 'name_col': 'N/A',
                 'properties': 'N/A',
                 'dates_cols': {'scale': 'weekly',
                                'date_col': 1},
                 'data_cols': {(10, 'int'): '', (11, 'float'): '',
                               (12, 'int'): '', (13, 'float'): '',
                               (14, 'int'): '', (15, 'float'): ''},
                 # 'sum_rule':
                 #     [{'Name': 'B', 'TimeScale': 'sum', 'FactScale': 'sum'},
                 #      {'Name': 'C', 'TimeScale': 'sum', 'FactScale': 'sum'},
                 #      {'Name': 'D', 'TimeScale': 'sum', 'FactScale': 'sum'}],
                 'mapping_rule':
                     [{'in': collections.OrderedDict(
                         {'Segments': 'BAND-AID BRAND ADH BDGS OTHER'}),
                       'out': collections.OrderedDict(
                           {'Segments': 'Premium'}),
                       'rule': 'rename'},
                      {'in': collections.OrderedDict(
                         {'Segments': 'BAND-AID BRAND ADHESIVE PADS'}),
                       'out': collections.OrderedDict(
                         {'Segments': 'Premium'}),
                          'rule': 'rename'},
                      {'in': collections.OrderedDict(
                         {'Segments': 'BAND-AID BRAND ANTIBIOTIC BNDGES'}),
                       'out': collections.OrderedDict(
                         {'Segments': 'Premium'}),
                          'rule': 'rename'},
                      {'in': collections.OrderedDict(
                         {'Segments': 'BAND-AID BRAND BLISTER'}),
                       'out': collections.OrderedDict(
                         {'Segments': 'Premium'}),
                          'rule': 'rename'},
                      {'in': collections.OrderedDict(
                         {'Segments': 'BAND-AID BRAND FLEXIBLE FABRIC'}),
                       'out': collections.OrderedDict(
                         {'Segments': 'Premium'}),
                          'rule': 'rename'},
                      {'in': collections.OrderedDict(
                         {'Segments': 'BAND-AID BRAND SPORT STRIP'}),
                       'out': collections.OrderedDict(
                         {'Segments': 'Premium'}),
                          'rule': 'rename'},
                      {'in': collections.OrderedDict(
                         {'Segments': 'BAND-AID BRAND TOUGH STRIP'}),
                       'out': collections.OrderedDict(
                         {'Segments': 'Premium'}),
                          'rule': 'rename'},
                      {'in': collections.OrderedDict(
                         {'Segments': 'BAND-AID BRAND VARIETY'}),
                       'out': collections.OrderedDict(
                         {'Segments': 'Premium'}),
                          'rule': 'rename'},
                      {'in': collections.OrderedDict(
                         {'Segments': 'BAND-AID BRAND WATERBLOCK'}),
                       'out': collections.OrderedDict(
                         {'Segments': 'Premium'}),
                          'rule': 'rename'},
                      {'in': collections.OrderedDict(
                         {'Segments': 'BAND-AID BRAND CLEAR'}),
                       'out': collections.OrderedDict(
                         {'Segments': 'Value'}),
                          'rule': 'rename'},
                      {'in': collections.OrderedDict(
                         {'Segments': 'BAND-AID BRAND PLASTIC'}),
                       'out': collections.OrderedDict(
                         {'Segments': 'Value'}),
                          'rule': 'rename'},
                      {'in': collections.OrderedDict(
                         {'Segments': 'BAND-AID BRAND SHEER'}),
                       'out': collections.OrderedDict(
                         {'Segments': 'Value'}),
                          'rule': 'rename'},
                      {'in': collections.OrderedDict(
                         {'Segments': 'BAND-AID BRAND DECORATED'}),
                       'out': collections.OrderedDict(
                         {'Segments': 'Deco'}),
                          'rule': 'rename'},
                      {'in': collections.OrderedDict(
                         {'Segments': 'BENADRYL BASE ADULT'}),
                       'out': collections.OrderedDict(
                         {'Segments': 'Benadryl'}),
                          'rule': 'rename'}]
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