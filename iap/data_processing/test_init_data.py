import os
from iap.data_processing.data_proc_manager import DataUploadManager
from iap.data_processing.processors import jj_aoc, jj_extract, jj_oc_data_proc
from iap.data_processing.processors.jj_aggr_map import DataAggregate
from iap.data_processing.processors.common import date_year_month, date_year
import collections


def test_jj_oc_data():
    func_list = {'jj_oc_input_sales_data':
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
                 }
    data_proc_path = os.path.dirname(os.path.abspath(__file__))
    upload_manager = DataUploadManager()
    # file_path = os.path.join(data_proc_path, 'test_inputs',
    #                          'jj_oc_input_sales_data.xlsx')
    file_path = os.path.join(data_proc_path, 'test_inputs',
                             'jj_oc_input_trends.xlsx')
    upload_manager.jj_oc_process_files(file_path, func_list)


def test_processing_data():
    func_list = {'MyReport (Benadryl SI Other Accaunts)': 
                        {'func': jj_aoc,
                         'meta_cols': ['Category', 'Segment', 'SubSegment',
                                       'Brand', 'SubBrand'],
                         'data_cols': 'N/A',
                         'dates_cols': {'N/A': 'N/A'}},
                 'JNJ_SALES_EXTRACT_FOR_4I_201603':  
                        {'func': jj_extract, 
                         'meta_cols': {3: 'LVL1', 5: 'LVL2', 6: ''},
                         'data_cols': {8: 'A', 10: 'B', 11: 'C', 12: 'D'},
                         'dates_cols': {0: 'campaign'}}
                 }
    # Rules for rows sum
    sum_rules_file1 = [{'Name':'%ACV', 'TimeScale': 'average', 'FactScale': 'sum'},
                       {'Name':'TDP', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'$', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'Base $', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'Units', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'Base Units', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'Price Decr $', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'Price Decr Base $', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'Disp w/o Feat $', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'Disp w/o Feat Base $', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'Feat w/o Disp $', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Feat w/o Disp Base $', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Feat & Disp $', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Feat & Disp Base $', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Disp w/o Feat Units', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Disp w/o Feat Base Units', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Feat w/o Disp Units', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Feat w/o Disp Base Units', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Feat & Disp Units', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Feat & Disp Base Units', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Price Decr Units', 'TimeScale': 'average', 'FactScale': 'average'},
                       {'Name':'Price Decr Base Units', 'TimeScale': 'average', 'FactScale': 'average'}]
    sum_rules_file2 = [{'Name':'A', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'B', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'C', 'TimeScale': 'sum', 'FactScale': 'sum'},
                       {'Name':'D', 'TimeScale': 'sum', 'FactScale': 'sum'}]
    sum_rules=[]
    sum_rules.append(sum_rules_file1)
    sum_rules.append(sum_rules_file2)

    map_rules = []
    map_rules1 = []
    map_sub_rule_1_1 = {'in': {'SubBrand': 'BENADRYL SI'},
                    'out': {'Category': 'TestCategory1'}}
    map_rules1.append(map_sub_rule_1_1)
    map_sub_rule_1_2 = {'in': {'Brand': 'BENADRYL',
                               'SubBrand': 'BENADRYL SI'},
                    'out': {'Brand': 'TestBrand1',
                            'Segment': 'TestSegment1'}}
    map_rules1.append(map_sub_rule_1_2)
    map_rules2 = []
    map_sub_rule_2_1 = {'in': {'LVL1': 'DRUG CHANNEL',
                               'LVL2': 'RITE AID'},
                        'out': {'LVL1': 'Ecomm'}}
    map_rules2.append(map_sub_rule_2_1)
    map_rules.append(map_rules1)
    map_rules.append(map_rules2)

    data_proc_path = os.path.dirname(os.path.abspath(__file__))
    paths = []
    paths.append(os.path.join(data_proc_path, 'test_inputs', 
                              'MyReport (Benadryl SI Other Accaunts).xlsx'))
    paths.append(os.path.join(data_proc_path, 'test_inputs', 
                              'JNJ_SALES_EXTRACT_FOR_4I_201603.xlsx'))
    upload_manager = DataUploadManager()
    for idx, val in enumerate(paths):
        output = upload_manager.process_files(val, func_list)
        data_aggr = DataAggregate(output, sum_rules[idx], map_rules[idx], 
                                  dates_source='weekly', dates_target='monthly')
        new_output = data_aggr.meta_map_by_rules()
        new_output = data_aggr.sum_by_meta()
        print(output[0])
        print(new_output[0])